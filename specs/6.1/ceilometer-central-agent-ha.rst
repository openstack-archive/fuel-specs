..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Add central agent HA and workload partitioning
==============================================

https://blueprints.launchpad.net/fuel/+spec/ceilometer-central-agent-ha

Implement zookeeper installation and using it as a coordination backend
for ceilometer central agent

Problem description
===================

A detailed description of the problem:

* Currentrly ceilometer central agent is the only one ceilometer component
  that didn't support HA and workload partitioning. During Juno release
  cycle this feature was intorduced to the ceilometer in the upstream code
  using tooz coordination openstack library. This library supports several
  backends (zookeeper, memcached among them). It was decided to introduce
  this built-in ceilometer feature to MOS as well.
  Zookeeper was chosen as the coordination backend.

Proposed change
===============

This feature implementation requires following things to be done:
* Implement zookeeper installation on controller nodes only in HA mode
  (note: zookepeer requires java for it's work). Zookeeper requires
  3 node to correctly work (1 leader and 2 followers)
* Zookeeper packages and it's dependencies
* Configure ceilometer central agents to work with zookeeper

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

These changes will be needed in puppet scripts:

* Add zookeeper module

* Configure ceilometer central agent to use zookeeper as backend

This change will be needed in packages:

* Build zookeeper packages and it's dependencies

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
--------------------

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

* Implement zookeeper installation from puppet (iberezovskiy)

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

* Zookeeper cluster should be with one leader and two followers

* Ensure that after one central agent was broken, during the next polling
  cycle all measurements will be rescheduled between two another,
  and still all of them will be collected

Documentation Impact
====================

A note should be added about zookeeper installation and
how ceilometer agent works in HA mode

References
==========

None
