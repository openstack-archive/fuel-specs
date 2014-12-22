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
In case of Multi-HV support with both vCenter and KVM Compute nodes deployed
it's necessary to deploy Cinder with multiple backends - VMDK plus LVM/Ceph.
A new role "Cinder with VMDK" should be introduced to provide this opportunity.


Problem description
===================

As it was said before there is no universal Block Storage solution for both
vCenter and KVM hypervisors in Fuel out-of-box. Fuel can deploy separate Block
Storage types for different hypervisors:

* For KVM it's Cinder with LVM or Ceph backend
* For vCenter it's Cinder with VMDK backend

Fuel 6.0 uses the only role 'cinder' to deploy both backend types. An actual
backend type is selected in Puppet in depends of hypervisor type. Such workflow
contrasts with the main Fuel idea - keep as more business logic in Nailgun as
we can. Also the only 'cinder' role make it hard to deploy VMDK and LVM/Ceph
backends in one environment simultaneously.

The use case I want to cover with this blueprint is:

Be able to deploy Cinder VMDK backend simultaneously with any other Cinder
backends.


Proposed change
===============

Introduce a new node role called 'cinder-vmdk'. The role will deploy Cinder
with VMDK backend. A Puppet code should be slightly refactored to use
'node[role]' value instead of 'libvirt_type==vcenter' to deploy Cinder VMDK
backend.

An old role 'cinder' should keep deploy Cinder with LVM. For clarification sake
it can be also renamed to 'cinder-lvm'.

What should be done:

- Remove the 'Cinder VMDK' option from the UI wizard and the Settings tab.
  Keep 'Default (LVM)' and 'Ceph' only.
- vCenter settings for Cinder should be always available on the Settings tab.
- The new role should be also always available and can be shared with any other
  role.
- It's allowed to deploy more than one node with the 'cinder-vmdk' role.
- It's not necessary to use Pacemaker for that Cinder service. HA will be
  achieved by deploying multiple Cinder instances with the same 'hostname'
  stanza and vCenter settings in cinder.conf.
- It's better to use an unique name for cinder.conf file. For instance
  'cinder-vmdk.conf'. It allows to combine 'cinder-vmdk' role with other Cinder
  roles on the same node.
- Nailgun should validate parameters before starting deployment to ensure that
  all the necessary vCenter credentials are provided.


Alternatives
------------

There is no vital alternatives from my point of view.


Data model impact
-----------------

None.


REST API impact
---------------

None.


Upgrade impact
--------------

No special upgrade impact.
The new role will be provided with a new release. A Nailgun
part should respect a release version and disable itself for old releases.
Puppet manifests are located in different directories for different Fuel
versions.


Security impact
---------------

None.


Notifications impact
--------------------

Two more notifications will be added.

# In "Deployed Changes" window: if there is one or more vCenter compute roles
  added but no Cinder VMDK roles. The message is: "In order to use volumes with
  vCenter instances, please add at least one 'Cinder with VMDK' role."
# In "Deployed Changes" window: if there is a HA environment but an only node
  with "Cinder with VMDK" role provided. The message is: "To perform HA for
  Cinder with VMDK backend, please deploy the 'Cinder with VMDK' role to
  at least two nodes."

One error message will be added.

# If the role 'cinder-vmdk' is used for environment but vCenter credentials for
  Cinder are incomplete, Nailgun should fail 'CheckBeforeDeploymentTask' task
  with the message: "The following vCenter credentials are required for Cinder
  with VMDK backend: <list of credentials>"


Other end user impact
---------------------

The new role should be presented on UI. It can be combined with any other role.


Performance Impact
------------------

Nothing more than some network bandwidth consuming is required.


Other deployer impact
---------------------

None.


Developer impact
----------------

New notifications should be discussed with UI team.

A probability to use the 'Granular deployment' feature to deploy the
'cinder-vmdk' role should be discussed with Dima Ilyin and Dima Shulyak.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Igor Gajsin - igajsin

Other contributors:
  UI part: Anton Zemlyanov - azemlyanov
  Nailgun part: Andriy Popovych - apopovych
  QA section: Alex Kosse - akosse, Tanya Dubyk - tdubyk


Work Items
----------

..
 Work items or tasks -- break the feature up into the things that need to be
 done to implement it. Those parts might end up being done by different
 people, but we're mostly trying to understand the timeline for
 implementation.


Dependencies
============

No strict dependencies.

Possible dependencies are:
* Granular deployment feature.
* Separate vCenter Compute role
* Multiple Availability Zones for vCenter and KVM.


Testing
=======

Should be discussed with QA.

..
 Please discuss how the change will be tested. It is assumed that unit test
 coverage will be added so that doesn't need to be mentioned explicitly, but
 discussion of why you think unit tests are sufficient and we don't need to add
 more functional tests would need to be included.

..
 Is this untestable in gate given current limitations (specific hardware /
 software configurations available)? If so, are there mitigation plans (3rd
 party testing, gate enhancements, etc).


Documentation Impact
====================

Will be filled soon.

..
 What is the impact on the docs team of this change? Some changes might require
 donating resources to the docs team to have the documentation updated. Don't
 repeat details discussed above, but please reference them here.

References
==========

* Granular deployment feature
  (https://blueprints.launchpad.net/fuel/+spec/granular-deployment-based-on-tasks)
* Separate vCenter Compute role
  (https://blueprints.launchpad.net/fuel/+spec/vmware-dual-hypervisor)
* Multiple Availability Zones for vCenter and KVM
  (https://blueprints.launchpad.net/fuel/+spec/availability-zones)
