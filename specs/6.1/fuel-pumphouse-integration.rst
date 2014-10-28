..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
Integrate Pumphouse with Fuel
=============================

https://blueprints.launchpad.net/fuel/+spec/fuel-pumphouse-integration

Integrating Pumphouse with Fuel will allow OpenStack operators to upgrade
their environment to the latest OpenStack release with lower risk and reduced
downtime for their users. In order to cleanly integrate Pumphouse with Fuel,
some additional functionality will be needed from Fuel.

Problem description
===================

Upgrading an OpenStack environment to the latest release often involves
significant downtime and high risk, as rolling back an upgrade executed
in-place may not be possible.

Proposed change
===============

Using Fuel and Pumphouse, the user could evacuate some compute nodes in their
existing environment and use those nodes as the start of a new cloud. This new
cloud can be validated in order to ensure it provides the expected
functionality. Then Pumphouse can migrate the workload on a tenant-by-tenant
basis from the original cloud to the new cloud.

In order for Pumphouse to perform these actions with Fuel, Fuel will need to be
extended in the following ways:

1. Support re-allocation of compute nodes from one environment to another in
   order to provide additional capacity for the new environment.

   a) The "delete node" task in Fuel will be extended to optionally use
   Pumphouse to migrate/evacuate a workload from the specified node

   b) During migration or evacuation, the compute node must be in maintenance
   mode so that no new VMs will be scheduled on it once the operation has begun

   c) After Pumphouse notifies Fuel that a node has been successfully
   evacuated, Fuel will reassign that node to the new environment

2. Create new environment by duplicating the settings in an existing
   environment

   a) If this can not be fully automated, Fuel will at least offer defaults for
   a new environment based on the configuration of an existing environment.

3. Enable per-tenant maintenance mode via Keystone RBAC

   a) Pumphouse supports migration of a single tenant from one environment to
   another During migration, tenant actions must be limited in order to prevent
   them from making changes (like launching or destroying VMs) while migration
   is in-progress.

Alternatives
------------

1. A proposal for how to upgrade OpenStack with minimal-to-no downtime has been
   documented on the OpenStack Wiki. In summary, it describes three methods:

   a) Big Bang - Create a parallel cloud next to the existing cloud and copy
   data to the new cloud during a maintenance window

   b) In place upgrade - Upgrade each service within the environment. This
   requires downtime while the service is being upgraded

   c) Side-by-Side upgrade - Create a parallel service next to the existing
   service. Enable the new service, disable the old service and allow the
   message queue or a load balancer to hide this downtime

2. Investigating methods for upgrading an OpenStack environment in a more
   turn-key fashion are being tracked under this blueprint:
   https://blueprints.launchpad.net/fuel/+spec/upgrade-major-openstack-environment

3. An approach that is a combination of "Big Bang" and "Side-by-side" can be
   found here: https://www.mirantis.com/blog/yes-can-upgrade-openstack-heres/.
   In summary, it describes:

   a) Deploy control node with new version of OpenStack

   b) Stop services on source cloud controller, capture configuration details
   and dump source cloud database

   d) Restore database on new controller, migrate schema as needed

   e) Move IP address of source controller to new controller, then restart
   services

Data model impact
-----------------

None.

REST API impact
---------------

The cluster configuration API handler will be modified to serialize cluster
metadata in all cases. Currently it will only serialize metadata when there
are nodes ready to be deployed.

Upgrade impact
--------------

None.

Security impact
---------------

None.

Notifications impact
--------------------

* A notification will be triggered when a compute node successfully transitions
  to maintenance mode

* A notification will be triggered when a tenant has been switched to or from
  maintenance mode

* A notification will be triggered if any attempted actions fail

Other end user impact
---------------------

There will be additional options in the UI:

* Enable/disable maintenance mode on a compute node

* Initiate evacuation of a compute node

* There will probably be some other UI changes? [DETAILS NEEDED]

Performance Impact
------------------

None.

Other deployer impact
---------------------

None.

Developer impact
----------------

None. The proposed changes will not impact existing code or functionality.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Andrew Woodward <awoodward@mirantis.com>

Other contributors:
  Ryan Moe <rmoe@mirantis.com>
  Christopher Aedo <caedo@mirantis.com>

Work Items
----------

1. Install Pumphouse as a plugin to Fuel in a docker container.
   
2. Automatically retrieve source and destination cloud configuration
   settings to remove the need to manually create Pumphouse configuration
   files.

3. Connect Neutron subnets in source and destination clouds. This is TBD.
   It could be accomplished through L2 VPN or GRE tunnels.

Dependencies
============

TBD

Testing
=======

Reallocation test:

* create OpenStack environment with three compute nodes ("cloud 1")

* create OpenStack environment with one controller, no compute nodes ("cloud 2")

* use Pumphouse to initiate reallocation of a compute node from "cloud 1"
  environment to "cloud 2" environment

Expected result:

* all VMs running on a compute node on "cloud 1" environment will be moved to a
  diferent compute node, all moved VMs will be running after being moved

* "cloud 1" and "cloud 2" environments  will pass "Sanity tests" in Fuel
  OpenStack Health Check after compute node is moved from "cloud 1" to
  "cloud 2"

Environment duplication test:

* create new environment in Fuel

* create additional new environment in Fuel using "duplicate environment"
  functionality

Expected result:

* newly created environment will have similar configuation to environment being
  duplicated (same network type, same storage type, etc.)

Tenant maintenance mode test:

* use Pumphouse to enable a specific tenant to "maintenance mode" in an
  OpenStack environment

Expected result:

* tenant should be prevented from creating, deleting or suspending VMs while
  maintenance mode is enabled

* tenant should be prevented from modifying the network while maintenance mode
  is enabled

* tenant should be able to execute any read-only action (like list vms) while
  maintenance mode is enabled

* all tenant access should be restored after maintenance mode is disabled

Documentation Impact
====================

Usage of new functionality will need to be documented. This will include:

* Enable/Disable maintenance mode on compute node

* Enable/Disable tenant maintenance mode

* Initiate compute node evacuation

* Creating a new cloud based on settings from existing cloud


References
==========

* Keystone RBAC:
  http://docs.openstack.org/developer/keystone/configuration.html#keystone-api-protection-with-role-based-access-control-rbac
