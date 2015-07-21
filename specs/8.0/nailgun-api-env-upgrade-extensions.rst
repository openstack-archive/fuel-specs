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

More detailed changes in the approach to upgrade of environment are as follows:

* Don't create new cluster. Rely on Nailgun DB migrations and improve them if
  necessary to provide required changes to attributes and settings of the
  cluster and other entities related to the cluster (e.g. node groups, network
  groups, extensions, plugins and so on).

* Use redeployment task to run provisioning and deployment on the Primary
  controller in environment. It shall get updated settings, library and
  packages matching updated version of the cluster.

* Add tasks to the deployment graph or modify existing ones so that the Primary
  controller is installed in isolation from remaining controllers.

* Add task in Nailgun to switch control plane in the cluster from obsolete
  controllers to the new Primary controller.

* Expand control plane by upgrading remaining controller nodes.

* Reinstall compute nodes in the cluster, as well as nodes of other roles, in a
  rolling fashion or in batches, depending on the nature of services provided
  by a certain role.

Web UI
======

This change does not require changing web UI. Upgrade will remain complex and
high risk operation and won't be integrated into graphical user interface.


Nailgun
=======

Data model
----------

We plan to leverage elements of the existing data model, such as
'pending_release_id' and a harness around it in Nailgun. Required extensions
and changes to the data model are described in specs for related blueprints.

REST API
--------

Exact changes to API methods are described in specs for related blueprint.

Orchestration
=============

Deployment graph shall include new tasks which will perform functions specific
for the upgrade procedure. The following tasks shall be added to the deployment
graph:

* TBD

Certain tasks shall be modified to provide functions required for the upgrade
procedure:

* TBD

RPC Protocol
------------

TBD

Fuel Client
===========

As more elements of the upgrade logic are moved to the Fuel Library and
Nailgun, more subcommands that run certain steps of the upgrade procedure will
also move to Fuel Client.

The following commands shall be added to Fuel Client:

* TBD

The following commands of the Fuel CLI client shall be modified:

* TBD

The following API calls shall be supported in the Fuel Client library:

* TBD

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

New modular tasks shall be added to the Fuel Library to provide upgrade
functions:

* TBD

The following modular tasks shall be modified to support the upgrade procedure:

* TBD

The following Puppet modules shall be modified to suppport the upgrade
procedure:

* TBD


------------
Alternatives
------------


--------------
Upgrade impact
--------------

Upgrade process for the Fuel Master node is unaffected.

Upgrade process for MOS environment under management of the Fuel installer
shall change in a way that there will be no more additional environment to
which all nodes from the original environment eventually go.

---------------
Security impact
---------------

TBD

--------------------
Notifications impact
--------------------

TBD

---------------
End user impact
---------------

TBB

------------------
Performance impact
------------------

TBD

-----------------
Deployment impact
-----------------

TBD

----------------
Developer impact
----------------

TBD

--------------------------------
Infrastructure/operations impact
--------------------------------

TBD

--------------------
Documentation impact
--------------------

TBD

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
  yorik.sar

Other contributors:
  sryabin
  smurashov
  ogelbukh

Mandatory design review:
  TBD

Work Items
==========

TBD

Dependencies
============

TBD

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

* https://bugs.launchpad.net/fuel/+bug/1473047 -- this bug prevents us from
  using different node groups for upgraded nodes, as we need to use the same
  network groups for original and upgraded nodes
*
