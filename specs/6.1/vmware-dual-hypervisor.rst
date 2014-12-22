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

Term "dual hypervisor cloud" in this document has the following meaning:
OpenStack cloud that can provision virtual machines on two hypervisors
simultaneously.  This specification describes two possible dual hypervisor
cloud setups:

* KVM and vCenter

* QEMU and vCenter

Problem description
===================

As of Fuel 6.0, it allows end user to add compute nodes only with hypervisor
type that was selected during cluster creation step.  Fuel does not allow
increase compute resource pool by extending it with resources of another
hypervisor type.

Right now user chooses hypervisor type during "Create a new OpenStack
environment" step.  Then after cloud was deployed it is not possible to utilize
additional hypervisor resources.  If user wants to add existing vCenter server
to operating KVM cloud it's impossible to do that.

Proposed change
===============

It is not possible to add KVM/QEMU compute nodes to deployed cloud with
vCenter, since Fuel web UI restricts it and vice versa.

Right now Fuel deploys nova-compute services with vCenter compute driver on
OpenStack controllers, in this specification we do not propose to change this
behaviour.  Restriction that in Fuel web UI must be eliminated and cluster
creation wizard step where user selects hypervisor must be reworked.  Instead
of three radio buttons that represent possible hypervisors (KVM, QEMU,
vCenter), vCenter must present on this page as checkbox.  If user selected this
checkbox VMware settings tab [0] will appear on the cluster page after cluster
creation wizard is finished.  It is up to user to add vCenter to this
environment.  Compute nodes become optional for this cluster, user may
configure only vCenter related settings and deploy cluster with controller
nodes only.

It will be also possible to specify many vCenter hosts instead of one.  Each
vCenter will form a separate availability zone [2].

After implementing this specification, the following use case will be available
from end user perspective:

#. Create new HA OpenStack environment with *nova-network* as network provider

#. User adds 3 controllers and a bunch of KVM computes and cinder nodes

#. Deploy the cluster

#. User fills vCenter related settings on the VMware tab [0]

#. In OpenStack dashboard user sees that there are two availability zones

#. Now user is able to run VMs on KVM or vSphere

In order to support OpenStack Block storage for vCenter, we also have to
introduce new role for Cinder service with VMDK backend [1].

Specification does not cover a vCenter removal procedure.

Implementation of this change must not affect end user opportunity to deploy
KVM only or vCenter only cloud.

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

Fuel must be able to convert old single hypervisor cloud into a cloud with dual
hypervisor support.

Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

Fuel web UI cluster creation wizard will be modifed.

Performance Impact
------------------

None.

Other deployer impact
---------------------

Special attention must be payed to the fact that for vCenter Fuel deploys
*nova-network* service in non-multi host mode (there is a single *nova-network*
service for whole OpenStack cluster), while in KVM/QEMU case *nova-network* is
deployed on compute nodes (multi host mode).

Developer impact
----------------

* OSTF tests must be reworked to support proposed change.  Separate OSTF
  manager must be implemented.

* Ceilometer support for vCenter is affected by this change.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  izinovik (Igor Zinovik)
  srogov (Stepan Rogov)

Other contributors:
  gcon.monolake (Andrey Danin)
  okosse (Oleksandr Kosse)

Work Items
----------

* Modify cluster creation wizard that way that it allows select a combination
  of hypervisors KVM with vCenter or QEMU with vCenter.  Change vCenter radio
  button to checkbox.
* Remove restriction that forbids to add compute nodes with vCenter settings.
* Adapt Fuel library puppet manifests to new structure of astute.yaml that will
  be formed by Nailgun backend, due to VMware settings tab [0].
* Names of Cirros images that get loaded into Glance must be modified, so that
  user will able to distinguish easily, which image can be run on KVM/QEMU and
  which on vCenter.  Currently images are named as *TestVM*.
* Assign KVM/QEMU compute nodes and vCenter to availability zones.
* Implement vCenter OSTF manager.
* Implement system tests for dual hypervisor cluster.

Dependencies
============

* https://blueprints.launchpad.net/fuel/+spec/availability-zones

* https://blueprints.launchpad.net/fuel/+spec/cinder-vmdk-role

* https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings


Testing
=======

Existing tests that create KVM only or vCenter only must not be affected.

Following testing scenarios must be implemented:

* Create cloud with KVM compute nodes, fill settings for vCenter, run OSTF
  checks.  Expected result: cloud is successfully deployed, two images present
  in Glance, one for KVM and another for vCenter.

Documentation Impact
====================

Most part of documentation related to vCenter must be adjusted to reflect
changes described in this specification (Planning Guide, User Guide).  New
section must be added: instructions on planning and deployment of dual
hypervisor environment (limitations, reference architecture).

References
==========

[0] https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings

[1] https://blueprints.launchpad.net/fuel/+spec/cinder-vmdk-role

[2] https://blueprints.launchpad.net/fuel/+spec/availability-zones
