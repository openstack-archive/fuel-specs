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
This will not deliver production ready setup on 1 node, but allow to play and
test OpenStack and Fuel itself. Full working HA will be possible with 3
physical nodes (each controller located on other physical server).

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
Fuel will allow only to start/deploy VMs.
User should take care about VMs maintenance.
We will deliver fire-and-forget solution.

New "virt" role can be mixed with "compute" role.

We will introduce new feature group ex. "Advanced/expert mode" and put
reduced-footprint inside.

We should also prepare possibility to move running Fuel to
virtual machine running on our bare metal.

Deployment flow:

   - Install Fuel on baremetal/virtual machine
   - Boot another bare metal server via Fuel PXE
   - Create new environment in Fuel
   - Assign "virt" role to bare metal
   - Upload virtual machines details to Fuel
   - Provision bare metal with "virt" role
   - Execute dedicated granular tasks to spawn VMs
   - Assign controller roles to virtual machines
   - Deploy environment
   - Migrate Fuel server (#1) as additional virtual machine located on physical
     server

Migration of Fuel server will be done by dedicated script.

Migration script flow:

   - Determine/get from command line/configuration needed parameters
     (destination compute, admin network parameters, disk schema)
   - Use libvirt template XML to define VM on destination node
   - Start destination node (bootstrap with PXE from source node)
   - Prepare destination node (partitioning)
   - Reboot source Fuel to runlevel with disabled all services (containers)
   - Sync data between source Fuel and destination VM (with rsync+dd)
   - Run post-migrate script on destination VM (fix udev rules, ...)
   - Reboot destination VM to final image
   - Stop network on source node and up admin interface with temporary address

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

VMs details will be stored inside node attributes. Data will be stored
as JSON list.

node:
  attributes:
    vm_configuration:
      - {'id': 0, 'cpu': 2, 'ram': 4, 'new_value': 'example'}
      - {'id': 1, 'cpu': 4, 'ram': 8, 'new_value': 'ex'}
      - {'id': 2, 'cpu': 2, 'ram': 4, 'new_value': 'example2'}


Details from nodes attributes will be used inside libvirt XML template.
Libvirt XML template will be stored as normal file inside fuel-library.

.. code-block:: xml

    <domain type='kvm'>
      <name>{id}</name>
        <memory unit='GiB'>{ram}</memory>
        <vcpu placement='static'>{cpu}</vcpu>
    </domain>

If user want to modify libvirt template, and introduce new variable it only
require to upload new libvirt xml template with new variables.

.. code-block:: xml

    <domain type='kvm'>
      <something new>{new_value}</something new>
    </domain>

In that case "new_value" from node attributes will be injected into template.

When user pass in node attribute value which is not used inside libvirt
template, nothing happend.

When user dont pass in node attribute value which is used inside libvirt
template, template will be generated with empty value.

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

Running all OpenStack components on single physical machine in KVM will lead
to bad performance. Also tenants VMs can affect reduced-footprint VMs
performance.
But we should remember that reduced-footprint will be available only for
advanced users.

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

Uploading VMs detail will be only needed when "virt" role in use.
VMs details will be only visible on nodes with "virt" role assigned.
When "virt" role will be used in environment, new button comes up in UI.
This button will call API, which will prepare/start VMs.

Both VMs details and "virt" role limitations will be created inside
openstack.yaml, as other UI parts.

vm_configuration:
  metadata:
    label: "VMs configuration"
    type: "textarea"
    value: "{'id': 0, 'cpu': 2, 'ram': 4}"
    weight: 20
    restrictions:
    - condition: "not ('advanced' in version:feature_groups) and
    not ('virt' in node:roles)"
    action: "hide"

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
   - Add new action in webUI which allows to configure virtual servers on
     given node.
   - Create script to migrate Fuel to VM
   - Create procedure/documentation how to move installed Fuel node to virtual
     machine located on compute.

Dependencies
============

None

Testing
=======

Acceptance criteria:

   - User can spawn VMs on node with role "virt".
   - VMs are visible in Fuel as standard physical server.
   - Show warning before delete node with "virt" role.

Documentation Impact
====================

We need to prepare new section in documentation describing new feature and
proper flow of deployment.
We will put BIG disclaimer about performance impact in case of using
reduced-footprint. User should be aware of all limitations.

References
==========

- https://blueprints.launchpad.net/fuel/+spec/reduced-footprint
