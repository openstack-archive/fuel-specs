..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Network verification service
==========================================

https://blueprints.launchpad.net/fuel/+spec/network-verify-service

Current network verification architecture has strong integration
with nailgun which performs another function such as deployment
configuration service. In future scaling network verification
functionality like adding new tasks for verify can be hard implemented
and support. Also now it has very pure output information like what’s
going behind the scene for client. Base on SOP it wiil be logically to
move network verification functionality into separate service.


Problem description
===================

* Network verification feature is independent enough to stop keeping the code in Nailgun/Astute and complicating them with it.

* It not so easy to extend verification with new checking task.

* Future scale of curent implementation will be hard to support.

* It doesn't support bonds checking.

* Results of tests in case of failures are discouraging now. It
doesn't try to collapse the results somehow (a single foreign DHCP
server produces a separate message for each node in cloud).


Proposed change
===============

* Create separate service to run tasks with different kind of checks
for network.

* It should provide an easy way to understand which checks are
available to a cluster, which is running right now, and what are the
results of checks in past.

* There should be a way to run not all of them but certain checks only.

Alternatives
------------

Make it as part of OSTF


Data model impact
-----------------

None


REST API impact
---------------

None

Upgrade impact
--------------

None

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

Plugin impact
-------------

None


Other deployer impact
---------------------

None

Developer impact
----------------

None

Infrastructure impact
---------------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Andrey Danin (gcon-monolake)
  Andriy Popovich (popovych-andrey)
  Anton Zemlyanov (azemlyanov)


Work Items
----------

None


Dependencies
============

None

Testing
=======

None

Documentation Impact
====================

None

References
==========

None
