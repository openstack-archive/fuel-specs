..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================
Ceilometer API as pacemaker resource
====================================

https://blueprints.launchpad.net/fuel/+spec/ceilometer-api-as-pacemaker-resource

Control ceilometer-api work by pacemaker

Problem description
===================

A detailed description of the problem:

* Currently we are having three ceilometer api services running in ha mode
  (one per controller). All of them are working simultaneously. Load even
  one of ceilometer-api services is really small because it can process
  a lot of requests that can be becoming only from admin users. That's why
  we need to run ceilometer-api service one per cluster and monitor it as
  a corosync resoruce.

Proposed change
===============

We need to create OCF script for ceilometer-api service and enable it
in pacemaker using puppet.

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

Need to enable support of ceilometer-api service for pacemaker in HA mode.
It requires changes in puppet: need to define service ceilometer-api that
will be provided by pacemaker and pacemaker will use ceilometer-api OCF
script for monitoring it.

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

 * This feature will be enabled by default in HA mode.

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  iberezovskiy

Other contributors:
  dbelova

Work Items
----------

* Add ceilometer-api service that will be provided
  by pacemaker to puppet scripts (iberezovskiy)
* Write ceilometer-api OCF script (iberezovskiy)
* Write a documentation (dbelova)

Dependencies
============

None

Testing
=======

Testing approach:

* If primary controller is done, ceilometer-api service should migrate
  to new primary controller node. Ceilometer should continue to responce
  on any api requests.

Documentation Impact
====================

A note should be added about this feature.

References
==========

None

