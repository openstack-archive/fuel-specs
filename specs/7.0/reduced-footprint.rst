=================
Reduced footprint
=================

https://blueprints.launchpad.net/fuel/+spec/reduced-footprint

Reduced footprint is about deployment on reduced number of physical nodes.
The minimal nodes count is 5 for the current implementation and HA mode
(1 master, 3 controllers, 1 compute/storage).
The requirement is a 2 node cluster should be supported with possibility to
migrate Fuel master node to VM.
Fuel master can be installed not only on dedicated server, but also on laptop
or other machine.

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
This should be possible by assigning new role named "virt" to physical server,
after that user should upload VMs properties as node attributes.

Virtual machines will be treated by Fuel as standard bare metal servers.

New "virt" role can be mixed with "compute" role.

We should also prepare possibility to move running Fuel to
virtual machine running on our bare metal.

Deployment flow:

   - Install Fuel on baremetal/virtual machine (#1)
   - Boot another bare metal (#2) server via Fuel PXE
   - Create new environment in Fuel
   - Assign "virt" role to bare metal (#2)
   - Upload virtual machines details to Fuel
   - Provision bare metal with "virt" role (#2) 
   - Assign controller roles to virtual machines (#3)
   - Deploy environment
   - Migrate Fuel server (#1) as additional virtual machine located on physical
     server (#2)

Migration of Fuel server will be done by dedicated script.

Migration script flow:

   - Determine/get from command line/configuration needed parameters
     (destination compute, admin network parameters, disk schema)
   - Use libvirt template XML to define VM on destination node
   - Stop all services (containers) on source Fuel
   - Sync data between source Fuel and destination VM (with rsync)
   - Run post-migrate script on destination VM (fix udev rules, ...)
   - Reboot destination VM to final image
   - Shutdown source Fuel

Alternatives
------------

1) Assign compute and controller role on single machine

Allow to assign compute and controller role to single machine.

   Cons:
      - No possibility to easy separate resources used by controller processes
        from compute processes

   Pros:
      - Better performance.
      - Easy implementation.

2) Single node OpenStack setup + additional VMs located on OpenStack

Prepare dedicated Glance image for 'infrastructure node'.
This image can be spawned as additional slave on OpenStack.
This image will be pre-provisioned Fuel slave (nailgun agent, mcollective),
ready to be discovered and/or deployed by Fuel.

   Flow:
      - Deploy controller and compute as single node setup
      - Upload precreated glance image
      - Spawn OpenStack VM from dedicated image
      - Add OpenStack VM to the existing Fuel environment
      - Assign roles and continue deployment as always

   Cons:
      - Very different deployment flow from what we already have
      - We need to implement possibility combination of compute and
        controller role
      - We need to prepare dedicated Glance image

   Pros:
      - All 'run VM' logic will be handled by OpenStack

Data model impact
-----------------

None

REST API impact
---------------

We should introduce new API call which will allow to run virtual machines
on given node with "virt" role assigned.
This API call will execute all needed granular tasks on "virt" node.

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

   - Upload VMs configuration as node attributes.
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

UX impact
---------

When user want to use virtual machines located on "virt", proper flow will
be:

   - User sees just one available node on Fuel UI
   - User assigns "virt" role to this node
   - User uploads VMs configuration
   - User start provisioning
   - New servers will be available in Fuel
   - User assigns roles to new nodes
   - User runs deployment of the cluster

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Bartosz Kupidura (zynzel)

Work Items
----------

   - Implement new granular tasks to create virtual machines on "virt" when
     choosen.
   - Add new action in webUI which allows to provision servers before
     deployment.
   - Add new action in webUI which allows to configure virtual servers on given
     node.
   - Create script to migrate Fuel to VM
   - Create procedure/documentation how to move installed Fuel node to virtual
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
