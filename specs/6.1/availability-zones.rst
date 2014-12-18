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

Currently Fuel deploys OpenStack that has only one availability zone 'nova'.
Lack of this functionality blocks an implementation of deploying dual
hypervisor OpenStack cloud (e.g. cloud that runs simultaneously on top of KVM
and vCenter).


Proposed change
===============

We can implicitly assign compute node or storage node to availability zone,
e.g. we will assign compute node with KVM hypervisor to availability zone
'kvm' and block storage node that uses VMDK backend to 'vcenter' availability
zone.

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

None.

Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

Availability zones will be available via Horizon dashboard.  Operator will be
able to select in which availability zone he is going to runs virtual
instance.

Performance Impact
------------------

None.

Other deployer impact
---------------------



Developer impact
----------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:

*  Igor Zinovik (izinovik)

Other contributors:

* Andrey Danin (adanin)
* Alexander Kosse (al.rem)

Work Items
----------

* Add parameter 'availability_zone' to puppet classes 'nova' and 'cinder'
* If user selected KVM as hypervisor we should configure as 'kvm'
* If user selected vCenter as hypervisor we should configure as 'vcenter'


Dependencies
============

None.

Testing
=======

#. Build new ISO and deploy OpenStack cloud.

#. Verify that availability zone 'kvm' exist in nova database by running
   'nova availability-zone-list'.
#. Verify that availability zone 'vcenter' exist in nova database by running
   'nova availability-zone-list'.


Documentation Impact
====================

Documentation must state that we explicitly configure availability zones based
on chosen hypervisor.

References
==========

None.
