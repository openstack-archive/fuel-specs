..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Upgrade ceph to the latest stable release
==========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/upgrade-ceph

Problem description
===================

Now we deploy ceph version 0.80.7 but new stable version 0.87 is released now
http://ceph.com/docs/master/release-notes/#v0-87-giant

* RADOS Performance: a range of improvements have been made in the OSD and client-side librados code that improve the throughput on flash backends and improve parallelism and scaling on fast machines.

* Local Recovery Codes: the OSDs now support an erasure-coding scheme that stores some additional data blocks to reduce the IO required to recover from single OSD failures.

* Tiering improvements: we have made several improvements to the cache tiering implementation that improve performance. Most notably, objects are not promoted into the cache tier by a single read; they must be found to be sufficiently hot before that happens.
  
* Monitor performance: the monitors now perform writes to the local data store asynchronously, improving overall responsiveness.

* For a new feature this might be use cases. Ensure you are clear about the
  actors in each use case: End User vs Deployer

* For a major reworking of something existing it would describe the
  problems in that feature that are being addressed.


Proposed change
===============

Here is where you cover the change you propose to make in detail. How do you
propose to solve this problem?

If this is one part of a larger effort make it clear where this piece ends. In
other words, what's the scope of this effort?

Alternatives
------------
* None

Data model impact
-----------------

* It is not supposed to change data models

REST API impact
---------------

* It is not supposed to change REST API

Upgrade impact
--------------

* None

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

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

smakar

Work Items
----------

#. Prepare the repository mirror with packages

Dependencies
============

None

Testing
=======

#. We need to build new fuel ISO and test if deployment work as expected.

Documentation Impact
====================

#. Add to docs that we are using the latest stable ceph version (0.87).

References
==========

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
