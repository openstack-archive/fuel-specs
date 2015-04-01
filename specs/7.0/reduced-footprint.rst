=================
Reduced footprint
=================

https://blueprints.launchpad.net/fuel/+spec/reduced-footprint

Reduced footprint is about deployment on reduced number of physical nodes.
The minimal nodes count is 5 for the current implementation and HA mode
(1 master, 3 controllers, 1 compute/storage).
The requirement is a 2 node cluster should be supported with possibility to
migrate Fuel master node to VM.

Problem description
===================

In some cases user want to deploy OpenStack with Fuel in small environment.
This will not deliver production ready setup, but allow to play and test
OpenStack and Fuel itself.
This require to support 2 baremetal server deployments.
All reduced deployments should be capable to be migrated to proper HA setup.
After deployment, user should have possibility to migrate Fuel to VM, and use
Mirantis OpenStack on single physical machine.

Proposed change
===============

Allow user to create additional virtual machines (KVM) on single physical
machine.
This should be possible by assigning compute role to physical server, after
that user should have possibility to click "create N virtual machines".

These machines will be treated by Fuel as standard bare metal servers.

We should also prepare procedure/documentation how to move running Fuel to
virtual machine running on our bare metal.

Deployment flow:
- Install Fuel on baremetal/virtual machine (#1)
- Boot another bare metal (#2) server via Fuel PXE
- Create new environment in Fuel
- Assign compute role to bare metal (#2)
- Create new virtual machines on compute (#2)
- Provision new virtual machines (#3)
- Assign controller roles to virtual machines (#3)
- Deploy environment
- Migrate Fuel server (#1) as additional virtual machine located on physical
  server (#2)

Alternatives
------------

Allow to assign compute and controller role to single machine.

   Cons:
      - No possibility to deploy environment in full HA on single node.

   Pros:
      - Better performance.
      - Easy implementation.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

None

Security impact
---------------

In this scenario controller is located in KVM on computes where tenants VMs
are running. This can lead to unknown security vulnerabilities.

Notifications impact
--------------------

None

Other end user impact
---------------------

When user want to use virtual machines as controller, he should run additional
steps before deployment:
- Create virtual machines.
- Provision environment.
- Deploy environment.

Performance Impact
------------------

Running all OpenStack components on single physical machine in KVM will lead to
bad performance.
But we should remember that solution is not production ready.
This is only testbed/playground for real workloads.

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Bartosz Kupidura (zynzel)

Work Items
----------

Implement new task in nailgun to create virtual machines on compute when
choosen.
Add new action in webUI which allows to provision servers before deployment.
Add new action in webUI which allows to add new virtual servers on given
compute node.
Create procedure/documentation how to move installed Fuel node to virtual
machine located on compute.

Dependencies
============

None

Testing
=======

??

Documentation Impact
====================

We need to prepare new section in documentation describing new feature and
proper flow of deployment.

References
==========

- https://blueprints.launchpad.net/fuel/+spec/reduced-footprint
