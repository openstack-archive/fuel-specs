..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================
Dual hypervisor support
=======================

https://blueprints.launchpad.net/fuel/+spec/dual-hypervisor

Introduction paragraph -- why are we doing anything? A single paragraph of
prose that operators can understand.

Add a functionality to Fuel that allows end user deploy dual hypervisor
OpenStack cloud.

Term "dual hypervisor cloud" means OpenStack cloud that can provision virtual
machines on two hypervisors simultaneously.  This specification describes two
possible combinations of hypervisors:

* KVM and vCenter

* QEMU and vCenter

Problem description
===================

As of Fuel 6.0 it allows end user to add compute nodes only with hypervisor
type that was selected during cluster creation step.  Fuel does not allow
increase compute resource pool by extending it with resources of another
hypervisor type.

Right now user choose hypervisor type during "Create a new OpenStack
environment" step.  Then after cloud was deployed it is not possible to utilize
additional hypervisor resources.  If user wants to add existing vCenter server
to his cloud he is not able to do it.

After implementing this specification following use case will be available from
end user perspective:

#. Create new OpenStack environment

#. User adds 3 controllers and bunch of computes and cinder nodes

#. Cloud is deployed

#. User boots over PXE one more node from Fuel master node

#. Role "vcenter-compute" is assigned to unallocated node

#. User fills vCenter related settings on the VMware tab

#. New node is deployed

#. Now user is able to run VMs on KVM or vSphere

Proposed change
===============

Current implementation of vCenter support in Fuel library must be reworked.

In order to implement simultaneous support of vCenter and KVM/QEMU new role
must be introduced, e.g. "vcenter-compute" in addition to existing "compute"
role.

In order to support OpenStack Block storage for vCenter we also have to
introduce new role "vcenter-cinder".  Host with this role will configure Cinder
to use VMDK backend.

Proposed roles will be accessible only on environment with network provider
"nova-network", since this is the only networking option that is support by
both KVM/QEMU and vCenter.

Alternatives
------------

None.

Data model impact
-----------------

None.

REST API impact
---------------

None.

Upgrade impact
--------------

Fuel must be able to convert old single hypervisor cloud into cloud with
support of dual hypervisors.

Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

User will be able to add computing resources of vCenter on fly to existing
KVM/QEMU OpenStack cloud.

Performance Impact
------------------

None.

Other deployer impact
---------------------

None.

Developer impact
----------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  To be filled

Other contributors:
  gcon.monolake (Andrey Danin)

Work Items
----------

* Add new role to Nailgun database
* Implement restriction on Fuel web UI that allows selecting new roles only
  when 'nova-network' option was chosen
* Name of images that are load into Glance must be modifed, so that user will
  able easily distinct which image he can run on KVM/QEMU and which on vCenter

Dependencies
============

* https://blueprints.launchpad.net/fuel/+spec/availability-zones

* https://blueprints.launchpad.net/fuel/+spec/cinder-vmdk-role

* https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings


Testing
=======

Following test scenarios must be implemented:

* Create cloud with KVM compute nodes, then add vcenter-compute node.

Documentation Impact
====================

To be filled.

References
==========

None.
