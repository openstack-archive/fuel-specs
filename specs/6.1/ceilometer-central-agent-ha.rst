..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Add central agent HA and workload partitioning
==============================================

https://blueprints.launchpad.net/fuel/+spec/ceilometer-central-agent-ha

Implement Redis installation and using it as a coordination backend
for ceilometer central agents

Problem description
===================

A detailed description of the problem:

* Currentrly ceilometer central agent is the only one ceilometer component
  that didn't support HA and workload partitioning. During Juno release
  cycle this feature was intorduced to the ceilometer in the upstream code
  using tooz coordination openstack library. This library supports several
  backends (zookeeper, redis, memcached among them). It was decided
  to introduce this built-in ceilometer feature to MOS as well.
  Redis was chosen as the coordination backend.

Proposed change
===============

This feature implementation requires following things to be done:
* Implement Redis installation on controller nodes only in HA mode
* Prepare Redis packages and it's dependencies
* Configure ceilometer central agents to work with redis

Alternatives
------------

This feature could be implement as non-default, it could be a fuel plugin
for workload partitioning and HA of ceilometer central agents

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

These changes will be needed in puppet scripts:

* Add redis module

* Configure ceilometer central agent to use redis as backend

This change will be needed in packages:

* Build redis packages and it's dependencies

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

This will be enabled by default only in HA mode

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
  None

Work Items
----------

* Implement redis installation from puppet (iberezovskiy)

* Configure ceilometer central agent (iberezovskiy)

* Write a documentation (dbelova)

Dependencies
============

None

Testing
=======

Testing approach:

* Environment with ceilometer in HA mode should be succesfully deployed

* Ceilometer should collect all enabled polling meters for deployed
  environment

* Polling meters should be divided on groups by ceilometer central agents

* Redis cluster should be with one master and two slaves

* Ensure that after one central agent was broken, during the next polling
  cycle all measurements will be rescheduled between two another,
  and still all of them will be collected

* Ensure that after node with redis master was broken ceilometer central
  agents can work with new redis master and can poll meters

Documentation Impact
====================

A note should be added about redis installation and
how ceilometer agent works in HA mode

References
==========

None
