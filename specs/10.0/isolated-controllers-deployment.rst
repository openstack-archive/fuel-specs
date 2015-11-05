..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================================
Deploy controllers in isolation from environment's networks
===========================================================

https://blueprints.launchpad.net/fuel/+spec/isolated-controllers-deployment

Highly available reference architecture of OpenStack installed by Fuel
implies that OpenStack Controllers are tightly coupled to each other
and coordinated by clustered services that control Virtual IP addresses of
common endpoints for services in the cluster, including, but not
limited to:

* corosync

* galera

* rabbitmq

* ceph

* haproxy

* mongodb

Other clusters might present in architecture of the particular OpenStack
environment, depending on its configuration.

The upgrade scenario without creating the new environment implies that
parallel control plane is created and then the data plane is switched to the
new control plane. This requires that new instances of clustered services are
created and attached to the same VIPs.

To avoid network conflicts between 2 sets of identical Virtual IPs for
parallel control planes, we must deploy the new control plane in isolation
from the old one.

--------------------
Problem description
--------------------

A detailed description of the problem:

* Duplication of control plane services in a single environment without
  any isolation renders the environment completely unusable due to conflicts
  between duplicated Virtual IPs.

* Controller nodes that run control plane services must be connected as they
  run clustered software that has to communicate to install properly.

* The same is true for most of OpenStack services, due to their distributed
  nature and dependency on each other.

* Cutover to the upgraded control plane has to be as seamless as possible to
  minimize the service interruptions.

----------------
Proposed changes
----------------

During the procedure of upgrade of OpenStack environment [1]_, Fuel must
execute the following sequence of steps to upgrade the control plane of the
environment.

* Reinstall Controllers in special isolation mode, without connection to
  physical networks, at least ones that have VIPs assigned to them.

* Specify 'isolated' deployment mode as a flag passed in deployment call.

* Automatically identify if 'isolated' mode is required based on composition
  of nodes and configuration of cluster.

* Support **isolated deployment mode** in Nailgun by changing serializers for
  deployment facts as follows:

    - Don't add patch ports in network scheme

    - Don't include nodes with the old release version into list of nodes

* Implement deletion of network interface resources in Fuel Library's module
  ``l23network`` for the cutover from old to upgraded controllers as
  ``del-port`` action.

* Support **cutover deployment mode** in Nailgun by changing serializers for
  deployment facts as follows:

    - Serialize network scheme for upgraded controller as usual, including
      patch ports

    - Include ``del-port`` actions in the ``transformations`` section of
      network scheme for old controllers

Web UI
======

No impact.

Nailgun
=======

General changes to the architecture, tasks and encapsulated business logic
should be described here.

Data model
----------

We plan to utilize existing data model by using parameters that allow to
change the release ID of cluster and other elements of the model.

We shall add the following parameters to Node object:

* ``release_id`` is an ID number of the release which was used to deploy the
  node. This parameter will allow for selective serialization and grouping of
  nodes. Release ID will be assigned to every existing node by Nailgun DB
  migration scrips of version 10.0. Nailgun will set this parameter to any new
  node based on release ID of the cluster it is added to.
* ``pending_release_id`` is an ID number of the release which shall be
  installed on the node with the next deployment. Parameter is NULL by
  default.

REST API
--------

Proposed operation is a part of Upgrade Environment API call (``PUT
/clusters/<cluster_id>/upgrade``).

Orchestration
=============

Primary controller shall be reinstalled with no connection to existing
controllers and shall not join existing Corosync and Galera clusters. To
achieve that, we propose to exclude nodes other than the primary controller
from orchestrator serialization for reinstallation of the primary controller.

Network scheme serializers must be modified to exclude certain ports (patch
ports for OVS or physical interfaces for Linux-bridge) from ``transformations``
section of the network scheme for deployment in isolated mode.

Network scheme serializers must be extended with additional action to delete
existing patch ports for deployment in cutover mode.

RPC Protocol
------------

TBD.

Fuel Client
===========

None.

Plugins
=======

None.

Fuel Library
============

The delete of network ports from bridges must be implemented in module
``l23network`` of the Fuel Library. Specific action ``del-port`` shall be
added. It deletes an existing port by setting it to ``ensure: absent``.

The proper parameters for this action shall be set by the network scheme
serializer (implemented in module ``orchestrator.neurton_serializers``).

------------
Alternatives
------------

Currently implemented alternative to the described mechanism of isolated
deployment is isolation ensured by external script that runs in between
provisioning and deployment stages of installation of the primary controller.

This method will be used as a backup if the described changes won't land in
10.0 release cycle.

The alternative that we're going to pursue in future is maintaining the
control plane through the whole upgrade process. In this case, upgraded
controllers will rejoin the existing clusters. We'll need to solve problems
with compatibility between older and newer versions of clustered software
(i.e. galera, corosync and rabbitmq) and add proper orchestration of
upgrades.

--------------
Upgrade impact
--------------

This change suggests a way to upgrade software on the controller node.

---------------
Security impact
---------------

TBD.

--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

End users won't have direct access to deployment in isolated mode. There
is no separate API call that allows to specify mode of deployment.

------------------
Performance impact
------------------

None.

-----------------
Deployment impact
-----------------

Isolated deployment mode will be used to reinstall primary controller in
upgraded environment. This will provide a method to deploy new version of
OpenStack, in addition to standard path to deploy from scratch on the
clean hardware.

Cutover deployment mode will be used to switch to the upgraded control plane.
To provide cutover mode in the previous release of Fuel (9.0), package
fuel-library must be updated or manifests patched with support for ``del-port``
actions.

The cutover mode implies that the original control plane is operating in
Maintenance Mode (read-only mode with no changes to the cluster state
allowed through Public API endpoints). There is no catch up method proposed
in this specification for messaging queues, so it is possible that certain
notifications and/or telemetry metrics might be lost with the cutover.

----------------
Developer impact
----------------

None.

---------------------
Infrastructure impact
---------------------

System test and corresponding Jenkins job shall be implemented to verify
the integrity of isolated deployment.

--------------------
Documentation impact
--------------------

Modified workflow for upgrade of Control Plane shall be described in
corresponding section of Environment Upgrade chapter of Operations Guide.

--------------------
Expected OSCI impact
--------------------

None.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  gelbuhos (Oleg S. Gelbukh)

Other contributors:
  akscram (Ilya Kharin)
  yorik-sar (Yuriy Taraday)
  sryabin (Sergey Ryabin)

Mandatory design review:
  dborodaenko (Dmitriy Borodaenko)


Work Items
==========

* Define and pass deployment mode differentiator for **isolated** and
  **cutover** modes to deployment tasks and serializers.

* Implement cluster and node serialization logic as the corresponding
  classes in ``orchestrator.upgrade_serializers`` module.

* Implement network configuration serialization logic to exclude patch ports
  for isolated deployment mode in ``orchestrator.neutron_serializers`` module.

* Implement network configuration serialization logic to include ``del-port``
  actions for cutover deployment mode in ``orchestrator.neutron_serializers``
  module.

* Implement support for ``del-port`` action in module ``l23network`` in the
  Fuel Library.

Dependencies
============

TBD.

------------
Testing, QA
------------

System test should be created to verify the isolated deployment success and
integrity.

Acceptance criteria
===================

* Default deployment information is available for a node with role
  'primary-controller' when the environment is in 'upgrade' status.

* Default deployment information doesn't contain facts of other nodes in the
  environment.

* Default deployment information contains ``network_schema`` section with no
  patch ports connecting logical bridges to physical interfaces (for ovs), or
  no actions that add physical interfaces to logical bridges (for linux
  bridge).

* A node with 'primary-controller' role reinstalled in the same environment
  after the ``fuel-upgrade`` script updates the environment's attributes.

* Reinstalled 'primary-controller' node is isolated from networks that have
  Virtual IP addresses configured, and thus also from the original control
  plane services (i.e. corosync/pacemaker, galera, rabbitmq and others).

* Reinstalled 'primary-controller' node runs the same set of clustered
  services as the original control plane has.

* Reinstalled 'primary-controller' node has the same VIPs configured on it
  as the original cluster had. Due to its isolation from physical networks,
  it does not cause IP conflicts in the environment.

* Deployment information is available for the upgraded primary controller when
  the environment in 'upgrade' status.

* Deployment information is available for controllers with old release ID in
  attributes when the environment in 'upgrade' status and primary controller
  with new release ID is in 'ready' status.

* Deployment information for old controllers includes ``del-port`` actions for
  ports that connect them to physical networks.

* Other controller nodes are reinstalled as usual nodes, without using
  isolated or cutover deployment modes.

----------
References
----------

.. [1] `umbrella blueprint for upgrade feature in Fuel 10.0 <https://blueprints.launchpad.net/fuel/+spec/upgrade-major-openstack-environment>`_
