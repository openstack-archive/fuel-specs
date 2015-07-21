..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================
Single-cluster Upgrade To New Major Release
===========================================

https://blueprints.launchpad.net/fuel/+spec/upgrade-major-openstack-environment

Upgrading OpenStack environment by creating replacement environment and moving
all nodes to it is counterintuitive, unpractical and creates unnecessary
complexity. Copying settings between clusters of different versions is
error-prone and even seems impossible in certain cases.

We propose to handle upgrade as an operation on a single cluster with versioned
settings. Upgrade of cluster settings shall be performed as a part of database
migration while upgrading the Fuel Master node to the new release.
Upgrade-specific tasks shall be added to the deployment graph.


-------------------
Problem description
-------------------

To upgrade and OpenStack environment managed by Fuel installer, we reinstall
every node in the environment with the same settings as before upgrade, but
with different versions of all software.

Reinstallation of a node requires that new version of settings is passed to the
node. Current upgrade solution creates a new version of settings in a new
instance of cluster. Afterwards, we need to manipulate 2 clusters: move nodes
from one to another, and even migrate data between the two (e.g. state DB).
However, this breaks object model of Fuel/Nailgun much and creates inconsistent
user experience for OpenStack operators who use Fuel installer.

This significantly decreases velocity of development and reliability of the
upgrade procedure itself.

It also requires modifications and translations of multiple settings of
OpenStack cluster not limited to attributes. We need to modify network groups,
templates, volume information and more. The procedure has to be adjusted to all
changes in data model for every new release.

This creates duplication of code: DB migrations for Nailgun and clone logic in
Cluster Upgrade extension contain similar code.

We also have to change deployment settings for the cluster and node via API,
which means that we depend not only on data model, but on serialization rules
as well, and they keep changing with enhancements to Fuel features.

Creation of second cluster with the same network configurations breaks
consistency of data, for example, forces us to create network groups with the
same IP address ranges, and also creates duplication of metadata.


----------------
Proposed changes
----------------

We summarize these changes into 3 user stories. As an operator performing
upgrade of an OpenStack cloud with Fuel, I need to:

* update all cluster attributes, settings and related parameters using Fuel DB
  migration scripts as a part of update of the Fuel Master node;

* redeploy a node within the cluster after it is updated to the new version;

* seamlessly upgrade and switch OpenStack control plane.

More detailed steps in the approach to upgrade of environment are as follows:

* Don't create new cluster. Rely on Nailgun DB migrations and improve them if
  necessary to provide required changes to attributes and settings of the
  cluster and other entities related to the cluster (e.g. node groups, network
  groups, extensions, plugins and so on). [1]_

* Use UpgradeSerializer to actually serialize the new deployment information
  (or facts) for Primary controller. The updated information must not contain
  any nodes in the environment, except the controller.

* Reset, provision and deploy the Primary controller in environment. It shall
  get updated settings, library and package reposs matching updated version
  of the cluster from to the cluster's upgraded metadata.

* Make sure that the Primary controller is installed in 'isolated mode' [2]_
  to prevent IP conflicts between Virtual IP addresses and ensure they don't
  change with the upgrade.

* Use Partition Preservation (PP) feature to ensure that DB partition on the
  Primary controller remains intact. Make new DB server use existing data,
  instead of dumping/uploading data from original DB server.

* RabbitMQ messages will be dropped for now, after some grace delay period.
  In future, special task shall be added in fuel-library to handle the
  leftover messages using RabbitMQ mechanisms like Shovel [3]_, or another
  methods to preserve and re-inject messages into the queue once the control
  plane is updated.

* Switch control plane in the cluster from obsolete controllers to the new
  Primary controller using special Task in Nailgun, calling certain
  deployment tasks via Astute.

* Expand control plane by upgrading remaining controller nodes.

* Reinstall compute nodes in the cluster, as well as nodes of other roles, in a
  rolling fashion or in batches, depending on the nature of services provided
  by a certain role. [4]_

* Use PP to keep all data in-place during upgrade of software components.

Web UI
======

This change does not require changing web UI. Upgrade will remain complex and
high risk operation and won't be integrated into graphical user interface.


Nailgun
=======

Data model
----------

We plan to leverage elements of the existing data model, such as
'pending_release_id' and a harness around it in Nailgun. Attributes of
clusters shall be versioned by the release id number.

Original version of attributes will allow for managing cluster without
upgrading it. Updated version of attributes will be used to deploy nodes
during the upgrade process and manage the cluster later on.

REST API
--------

We plan to update cluster attributes with standard API call (PUT
/cluster/<:id>/) with 'pending_release_id' set to the desired release.

Two additional API calls will be required:

* Upgrade cluster

  * This method sets 'upgrade' status on the environment, sets
    'pending_release_id' for all nodes to the 'pending_release_id' of the
    cluster, upgrades primary  controller, switches control plane of
    OpenStack platform to the upgraded controller and upgrades remaining
    controllers, thus extending the control plane to HA mode.

  * Method type: PUT

  * Normal HTTP response code(s): 200 OK

  * Expected error HTTP response code(s)

    * 404 Not Found
      Cluster with the given ID is not found in database.

    * 409 Conflict
      - Cluster with the given ID already in 'upgrade' status.
      - There are active tasks running in the cluster.
      - The cluster's pending_release_id parameter is not set.

  * /clusters/<cluster_id>/upgrade

  * cluster_id: an ID of the cluster picked for upgrade.

  * This call starts a DeferredTask in Nailgun. This task is broken into a
    number of subtasks that cast deployments of appropriate nodes to Astute
    via RPC

* Upgrade node

  * This method sets status of one of more nodes to 'upgrade', prepares
    the to upgrade and starts deployment with updated settings. It is only
    applicable to nodes which roles don't include 'controller'.

  * Method type: PUT

  * Normal HTTP response code(s): 200 OK

  * Expected error HTTP response code(s)

    * 404 Not Found
      Node with the given ID is not found in database.

    * 409 Conflict
      - Node with the given ID not in 'ready' status.
      - There are active tasks running on the node.
      - Node with the given ID has 'pending_release_id' attribute not set.

  * /clusters/<cluster_id>/upgrade/?node={<node_id>,}

    * cluster_id: an ID of the cluster picked for upgrade

    * node_id: an ID of the node picked for upgrade

  * This call creates DeferredTask in Nailgun. It prepares metadata of
    node(s) with parameters from the new release and starts deployment.

Orchestration
=============

RPC Protocol
------------

See specification [2]_ for the details on changes to RPC protocol.

Fuel Client
===========

Extensions shall be implemented in ``python-fuelclient`` library to support
operations provided by the proposed API. Following commands shall be added
to the CLI of ``python-fuelclient``:

* ``env upgrade``

* ``node upgrade``

Plugins
=======

Upgrading the environment with plugins requires potential modification of
settings. This shall be implemented as a hook to plugin manager that shall ask
installed plugins to update their settings for the new version of cluster's
attributes.

Details of implementation of upgrade procedure for plugins are explained in
separate specification.

Fuel Library
============

See specifications [2]_, [4]_ for details on changes required in Fuel Library.

------------
Alternatives
------------


--------------
Upgrade impact
--------------

Upgrade process for the Fuel Master node is unaffected. Database migrations
used in the upgrade must be modified according to specification [1]_

Upgrade process for MOS environment under management of the Fuel installer
shall change in a way that there will be no more additional environment to
which all nodes from the original environment eventually go.

---------------
Security impact
---------------

The upgrade process poses risk of data loss for tenants and end users of the
cloud being upgraded.

--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

None.

------------------
Performance impact
------------------

None.

-----------------
Deployment impact
-----------------

In 'upgrade' status of the cluster, all provisioning to that cluster is
prohibited. No new nodes must be deployed until upgrade is finished.

----------------
Developer impact
----------------

None.

---------------------
Infrastructure impact
---------------------

Infrastructure shall be adjusted to support testing of the aforementioned
procedure of upgrade.

--------------------
Documentation impact
--------------------

Operations Guide shall be updated with the details of how the upgrade
procedure works and how it is managed.

--------------------
Expected OSCI impact
--------------------

TBD

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  ikharin
  sabramov

Other contributors:
  sryabin
  ogelbukh

Mandatory design review:
  alex-schultz

Work Items
==========

* Remove obsolete patching feature and make it possible to reuse
  'pending_release_id' attribute of cluster.

* Add Upgrade Cluster API call to extension ``cluster_upgrade`` in Nailgun.

* Add Upgrade Cluster task in Nailgun. See details in Isolated Controllers
  Deployment specification (see References section below).

* Add Upgrade Cluster Serializers in Nailgun.

* Extend Node data model with ``release_id`` and ``pending_release_id``
  attributes.

* Add Upgrade Node task in Nailgun. See details in Upgrade Redeploy Node
  specification (see References section below).

* Add Upgrade Node Serializers in Nailgun.

* Create system test for Upgrade Cluster API call.

* Create system test for Upgrade Node API call.

* Update documentation - Operations Guide section.

Dependencies
============

None.

------------
Testing, QA
------------

TBD

Acceptance criteria
===================

TBD

----------
References
----------

.. [1] `Upgrade Cluster Metadata To 9.0 <upgrade-major-openstack-version.rst>`_

.. [2] `Isolated Controllers Deployment blueprint and specification <https://blueprints.launchpad.net/fuel/+spec/isolated-controllers-deployment>`_

.. [3] `Shovel plugin for RabbitMQ server <https://www.rabbitmq.com/shovel.html>`_

.. [4] `Upgrade Node by Re-deployment blueprint and specification <https://blueprints.launchpad.net/fuel/+spec/upgrade-redeploy-node>`_
