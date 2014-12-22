..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
VMware: dual hypervisor support
===============================

https://blueprints.launchpad.net/fuel/+spec/vmware-dual-hypervisor

Add a functionality to Fuel that allows end user deploy dual hypervisor
OpenStack cloud.

Term "dual hypervisor cloud" in this document has following meaning: OpenStack
cloud that can provision virtual machines on two hypervisors simultaneously.
This specification describes two possible dual hypervisor cloud setups:

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
to operating KVM cloud he is not able to do it.

Proposed change
===============

Current implementation of vCenter support in Fuel library must be reworked.

Right now Fuel deploys nova-compute services (vCenter as compute driver) on
OpenStack controllers.  It is not possible to add KVM compute nodes to deployed
cloud, since Fuel web UI restricts it and vice versa.

In order to implement simultaneous support of vCenter and KVM/QEMU new role
must be introduced.

This specification introduces new role - **vcenter-compute**.

On host with role *vcenter-compute* service nova-compute will be installed and
configured to use vCenter compute driver.  *vcenter-compute* roles cannot be
combined with following roles:

* compute
* mongo
* zabbix-server

Proposed role will be accessible only on environment with network provider
*nova-network*, since this is the only network provider that is supported by
both KVM/QEMU and vCenter.

No high availability will be provided for services that run on nodes with
*vcenter-compute* role.  Even when *vcenter-compute* role is combined with
*controller* role in HA deployment mode nova-compute service will not be
protected by pacemaker.

After implementing this specification following use case will be available from
end user perspective:

#. Create new HA OpenStack environment with *nova-network* as network provider

#. User adds 3 controllers and bunch of KVM computes and cinder nodes

#. Cloud is deployed

#. User boots over PXE one more node (e.g. it could be virtual machine inside
   of his vSphere cluster) from Fuel master node

#. Role "vcenter-compute" is assigned to unallocated node

#. User fills vCenter related settings on the VMware tab [0]

#. New node is provisioned and deployed

#. In OpenStack dashboard user sees that there are two availability zones
   (*KVM* and *vCenter*)

#. Now user is able to run VMs on KVM or vSphere

In order to support OpenStack Block storage for vCenter we also have to
introduce new role for cinder service with VMDK backend [1].  Host with this
role will configure Cinder to use VMDK backend.

Specification does not cover node removal procedure.

OpenStack health checks (OSTF) must modified in such way that it will allow to
test functionality of both hypervisors.


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

* OSTF tests must be reworked to support proposed change.

* Ceilometer support for vCenter is affected by this change.

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

* Add new role *vcenter-compute* to Nailgun database.
* Add partition scheme to new role.
* Implement restrictions on combining *vcenter-compute* with other roles
* Implement restriction on Fuel web UI that allows selecting new role only
  when *nova-network* option was chosen.
* Rework nova-compute service deployment in Fuel library.  Deploy nova-compute
  (vCenter compute driver) when user assigned *vcenter-compute* role.
* Name of images that are get loaded into Glance must be modified, so that user
  will able easily distinguish which image he can run on KVM/QEMU and which on
  vCenter.  Currently images are named as *TestVM*.
* Add support of dual hypervisor to OSTF.
* Implement system tests for dual hypervisor feature.

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

[0] https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings

[1] https://blueprints.launchpad.net/fuel/+spec/cinder-vmdk-role
