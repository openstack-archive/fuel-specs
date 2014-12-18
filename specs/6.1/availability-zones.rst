..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Availability zones support
==========================================

https://blueprints.launchpad.net/fuel/+spec/availability-zones

Implement opportunity to configure availability zones for storage and compute
nodes.

Problem description
===================

Currently Fuel, deploys OpenStack that has only one availability zone **nova**,
which is configured implicitly (it is a default value when no availability
zones are configured).  Lack of this functionality blocks an implementation of
dual hypervisor support [0].


Proposed change
===============

We should be able to explicitly assign nova-compute service or cinder-volume
service to an availability zone, e.g. we will assign compute node with KVM/QEMU
hypervisor to availability zone *nova* and block storage node that uses VMDK
backend to *vCenter* availability zone.

Opportunity to create/delete/rename availability zones and assign particular
nodes to zones via the Fuel web UI or via Fuel CLI is not covered by this
specification.

Alternatives
------------

We can configure availability zones in our own puppet modules.

Data model impact
-----------------

None.

REST API impact
---------------

None.

Upgrade impact
--------------

None.

Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

Availability zones will be available via OpenStack dashboard or may be
specified as parameters for CLI clients *nova* and *cinder*.  Operator will be
able to select in which availability zone he is going to run a virtual machine
if there are several availability zones.

Performance Impact
------------------

None.

Other deployer impact
---------------------

None.

Developer impact
----------------

Change should be proposed to upstream, otherwise it will require backport
effort when Fuel library developers decide to synchronize puppet modules with
upstream.

Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Stepan Rogov (srogov)

Other contributors:

* Andrey Danin (adanin)
* Alexander Kosse (okosse)

Work Items
----------

* Add support for configuring *availability_zone* to puppet classes *nova*.

* Add support for configuring *availability_zone* to puppet classes *cinder*.

* If user assigned role *vcenter-compute*, we should create an availability
  zone named *vCenter*.

* Provide system tests for availability zones support.

Dependencies
============

None.

Testing
=======

#. Deploy OpenStack cloud with vCenter as hypervisor.

#. Verify that availability zone *vCenter* exists in nova database by running
   'nova availability-zone-list'.


Documentation Impact
====================

*User Guide* must state that we explicitly configure availability zones based
on chosen hypervisor and block storage backend.

References
==========

[0] https://blueprints.launchpad.net/fuel/+spec/vmware-dual-hypervisor
