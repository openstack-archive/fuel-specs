==========================================
VLAN manager support for vCenter
==========================================

https://blueprints.launchpad.net/fuel/+spec/vcenter-vlan-manager

Now, in a 5.0 and 5.1 releases Fuel doesn't support Nova-Network in VLANmanager
mode for vCenter as a hypervisor. We want to add this feature in Fuel 6.0.


Problem description
===================

Now only FlatDHCPManager (among nova networks mode) works properly with
vCenter. In this case all virtual machines (even used by different tenants) are
contained in one L2 broadcast domain. Also only one pool of ip addresses is
used for all tenants. It is a problem for security and scalability.


Proposed change
===============

We can avoid problems which described in previous point by using vlan
technology. Thereafter fuel-clouds will be better corresponds for conditionals
of huge, enterprise deployment. For full support VlanManager some changes must
be implement:

* Unlock 'VLAN Manager' --- element of UI on the Networks tab for choosing this
  variant of networking mode.

* Provide correct configuration of nova-network service for manage port groups,
  vlans and networks as described in [1].


Alternatives
------------

We could use VlanManager without full integration with vCenter. In this way for
all vlan networks in OpenStack deployment we must create appropriate portgroups
in vCenter's distrubution switch manually.

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

Because in this mode virtual machines from different tenants work in different
L2 segments, security of environment will be increased by this changes.

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

Some network performance improvement is awaited due to segregating virtual
machines into different broadcast domains. This effect will be increased with
growth of cloud and amount of virtual machines.

Other deployer impact
---------------------

Because this technology is based on vlan tagging before deploy you need to make
sure, that your switch support 802.1q standard. 

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  igajsin (Igor Gajsin)

Feature Lead: gcon-monolake (Andrey Danin)

QA: tdubyk (Tatyana Dubyk)

Documentations: ipovolotskaya

Work Items
----------

* Unlock UI element to enable 'VLAN Manager' option.

* Understand how it works.

* Make changes manually.

* Write puppet manifests.


Dependencies
============

None


Testing
=======

* Perform manual acceptance testing of this feature to verify that with Vlan
  Manager we can create env that will pass network connectivity.  

* Check that all ostf tests, which are linked with network connectivity will
  be passed.

Documentation Impact
====================

Fuel documentations which describe networking in vCenter based deployment must
be rewrited with taking into account new features:

* New work mode of nova-network.

* New UI with unlocked element.


References
==========

http://docs.openstack.org/grizzly/openstack-compute/admin/content/vmware.html#VMWare_networkin
