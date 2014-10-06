==========================================
VLAN manager support for vCenter
==========================================

https://blueprints.launchpad.net/fuel/+spec/vcenter-vlan-manager

Now, in a 5.0 and 5.1 releases Fuel doesn't support Nova-Network in VLANmanager
mode for vCenter as a hypervisor. We want to add this feature in Fuel 6.0.


Problem description
===================

Now only FlatDHCPManager (among nova networks mode) works properly with
vCenter. In this case all virtual machines (even used by different tenants) be
contained in one L2 broadcast domain. Also only one pool of ip adresses used
for all tenants. It is a problem for security and scalability.


Proposed change
===============

There are some changes must be implement for full support VlanManager:

* Deblock 'VLAN Manager' --- element of UI in 'Network Settings' tab for
  choosing this variant of networking mode.

* Teach nova go to vCenter and make portgroup in it when nova create new vlan.


Alternatives
------------

We could use VlanManager without full igtegration with vCenter. For it all
vlan networks in OpenStack deployment and all portgroups in vCenter's
distribution switch must be created manually. As it works for John Deere's
deployment.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Maybe additional packages will be installed for interaction with vCenter.

Security impact
---------------

Because in this mode virtual machines from different tenants works in different
L2 segments, security of environment will be increased by this changes.

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

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
  gcon-monolake

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============

None


Testing
=======

Doesn't need special methods of test for this. We must use ostf tests for
network connectivities which we use for testing VlanManager with qemu hypervisor.


Documentation Impact
====================

None


References
==========

None
