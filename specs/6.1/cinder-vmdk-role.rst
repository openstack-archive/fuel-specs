..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Add a separate role for Cinder with VMDK backend
================================================

https://blueprints.launchpad.net/fuel/+spec/cinder-vmdk-role

When vCenter is used as a hypervisor it can use volumes only from Cinder VMDK.
And vise versa: KVM as a hypervisor cannot mount volumes from Cinder VMDK.
In case of Multi-HV support with both vCenter and KVM Compute nodes deployed,
it's necessary to deploy Cinder with multiple backends - VMDK plus LVM/Ceph.
A new role "Cinder with VMDK" should be introduced to provide this opportunity.


Problem description
===================

As it was said before, there is no universal Block Storage solution for both
vCenter and KVM hypervisors in Fuel out-of-box. Fuel can deploy separate Block
Storage types for different hypervisors:

* For KVM, it's Cinder with LVM or Ceph backend
* For vCenter, it's Cinder with VMDK backend

Fuel 6.0 uses the only 'Cinder' role to deploy both backend types. An actual
backend type is selected in Puppet depending on hypervisor type. Such workflow
contradicts with the main Fuel idea - keep as more business logic in Nailgun as
we can. Also, the only 'Cinder' role makes it hard to deploy VMDK and
LVM/Ceph backends in one environment simultaneously.

I want to cover the following use case within this blueprint:

Be able to deploy Cinder VMDK backend simultaneously with any other Cinder
backends.


Proposed change
===============

Introduce a new node role called 'cinder-vmdk'. The role will deploy Cinder
with VMDK backend. A Puppet code should be slightly refactored to use
'node[role]' value instead of 'libvirt_type==vcenter' to deploy Cinder VMDK
backend.

An old role 'cinder' should keep deploying Cinder with LVM. For clarification
sake, it can be also renamed to 'cinder-lvm'.

The following should be done:

- Remove the 'VMware vCenter for volumes (Cinder)' option from the UI wizard
  and the Settings tab of the Fuel web UI. Keep 'Default (LVM)' and 'Ceph'
  only.
- vCenter settings for Cinder should be always available on the VMware Tab of
  the Fuel web UI.
- The new role should always be available if vCenter instance was added to
  environment so that it can be shared with any other role.
- It's allowed to deploy more than one node with the 'cinder-vmdk' role.
- It's not necessary to use Pacemaker for that Cinder service. HA will be
  achieved by deploying multiple Cinder instances with the same 'hostname'
  stanza and vCenter settings in cinder.conf.
- It's better to use an unique name for cinder.conf file; for instance,
  'cinder-vmdk.conf'. It allows to combine 'cinder-vmdk' role with other Cinder
  roles on the same node.
- Nailgun should validate parameters before starting deployment to ensure that
  all the necessary vCenter credentials are provided.


Alternatives
------------

There are no vital alternatives from my point of view.


Data model impact
-----------------

None.


REST API impact
---------------

None.


Upgrade impact
--------------

No special upgrade impact.
The new role will be provided with a new release. A Nailgun part should take
proper account of release version and disable itself for old releases. Puppet
manifests are located in different directories for different Fuel versions.


Security impact
---------------

None.


Notifications impact
--------------------

Two more notifications will be added into the Fuel web UI.

#. In "Deployed Changes" window: if there is one or more vCenter instance
   added and cinder VMDK backend is enabled , but no Cinder VMDK roles. The
   message should be the following: "In order to use volumes with vCenter
   instances, please add at least one 'Cinder with VMDK' role."

#. In "Deployed Changes" window: if there is an HA environment but the only
   node with "Cinder with VMDK" role is provided. The message should be the
   following:  "To provide HA for Cinder with VMDK backend, please select the
   'Cinder with VMDK' role for at least two nodes."

One error message will be added.

#. If the role 'cinder-vmdk' is used for environment but vCenter credentials
   for Cinder incomplete or has wrong format, Nailgun should fail
   'CheckBeforeDeploymentTask' task with the message:
   "The following errors happend:
   <list of errors>"



Other end user impact
---------------------

The new role should be presented on UI. It can be combined with any other role.


Performance Impact
------------------

A little more network bandwith will be consumed.


Other deployer impact
---------------------

None


Developer impact
----------------

New notifications should be discussed with UI team.

A probability to use the 'Granular deployment' feature to deploy the'c
inder-vmdk' role should be discussed with Dima Ilyin and Dima Shulyak.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Igor Gajsin - igajsin

Other contributors:
  UI part: Anton Zemlyanov - azemlyanov
  Nailgun part: Andriy Popovych - apopovych
  QA section: Oleksandr Kosse - okosse, Tanya Dubyk - tdubyk


Work Items
----------

There are three nearly independent parts of implementation:

#. Append to Fuel new role and notifications. Provide possibilities for
   separate configuration of cinder and cinder-vmdk nodes.
#. Change puppet manifests for create and configure new role. Clean old class
   from parameters of vmdk.
#. Create or modify the corresponding system and OSTF tests.

Dependencies
============

No strict dependencies.

Possible dependencies are:

* Granular deployment feature [1].
* VMware: Dual hypervisor support (vCenter and KVM in one environment) [2].
* VMware UI Settings Tab for FuelWeb [3].


Testing
=======

Our system tests are already good enough covers use-case of using cinder. But
this tests depend on ostf tests, which know nothing about availability zones.
Therefore OSTF tests can't test how cinder works in multiple availability zones
environment. And surely tests, which based on OSTF, are also useless.

This problem will be fixed in blueprint [3]. When it happens, system tests
should be changed for using with availability zones.

Before it the QA team may perform manual testing of declared features.


Documentation Impact
====================

There are several changes in Users' Guide:
#. Change the corresponding screenshots.
#. Add description of new role.

References
==========

[1] Granular deployment feature
  (https://blueprints.launchpad.net/fuel/+spec/granular-deployment-based-on-tasks)
[2] VMware: Dual hypervisor support (vCenter and KVM in one environment)
  (https://blueprints.launchpad.net/fuel/+spec/vmware-dual-hypervisor)
[3] VMware UI Settings Tab for FuelWeb
  (https://blueprints.launchpad.net/fuel/+spec/vmware-ui-setting)
