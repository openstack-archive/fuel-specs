..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
Ceilometer support for vCenter
==============================

https://blueprints.launchpad.net/fuel/+spec/ceilometer-support-for-vcenter

Implement possibility to setup ceilometer compute agent on controller

Problem description
===================

A detailed description of the problem:

* Currently if vCenter installation is chosen, we need to install ceilometer
  compute agent on controller node to collect all metrics about instances and
  need to configure ceilometer to use vsphere hypervisor inspector. Also we
  should pass vcenter credentials into ceilometer configuration file.
  If we are using multiple nova-computes to connect to multiple vSphere
  clusters we should also use multiple ceilometer-agent-compute to collect
  metrics about instances from each vCenter

Proposed change
===============

To implement installation of compute agent on controller node we should check
in ceilometer puppet scripts that vCenter installation is chosen and then
install compute agent on controller node, pass hypervisor_inspector, vCenter
host_ip, host_password, host_username into ceilometer config file.

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Simple changes will be needed in puppet scripts:

* pass parameters for vCenter

* setup compute agent

Security impact
---------------

None

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

* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

  This will be enabled only if vCenter is chosen

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Ivan Berezovskiy (iberezovskiy)

Other contributors:
  Dina Belova (dbelova)

Reviewer:
  Andrey Danin (gcon-monolake)
  Igor Zinovik (izinovik)

Work Items
----------

* Edit puppet scripts to setup ceilometer compute agent on controller node
  (iberezovskiy)

* Set parameters for vCenter in ceilometer configuration file (iberezovskiy)

* Write a documentation (dbelova)

Dependencies
============

None

Testing
=======

Testing approach:

* Environment with ceilometer and vCenter should be
  successfully deployed

* Ceilometer should collect metrics from each vSphere cluster

Documentation Impact
====================

A note should be added about configuration options for ceilometer with vCenter

References
==========

None

