..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Add central agent HA and workload partitioning
==============================================

https://blueprints.launchpad.net/fuel/+spec/ceilometer-central-agent-ha

Implement zookeeper installation and using it as coordination backend
for ceilometer central agent

Problem description
===================

A detailed description of the problem:

* Currentrly ceilometer central agent is the only one ceilometer component
  that didn't support HA and workload partitioning. During Juno release
  cycle this feature was intorduces to the ceilometer in the upstream code
  using tooz coordination openstack library. This library supports several
  backends (zookeeper, memcached among them). It was decided to introduce
  this built-in ceilometer feature to MOS as well.
  Zookeeper was chosen as the coordination backend.

Proposed change
===============

This feature implementation requires following things to be done:
* Implement zookeeper installation
  (note: zookepeer requires java for it's work)
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

* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

  This will be enabled by default only in HA mode

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

Documentation Impact
====================

A note should be added about zookeeper installation and
how ceilometer agent works in HA mode

References
==========

None
