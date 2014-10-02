=====================================================
Integration of autotests for NSX and vCenter features
=====================================================

Related to blueprint:
https://blueprints.launchpad.net/fuel/+spec/nsx-vcenter-system-tests-smoke

Problem description
===================

We have a lot of acceptance and smoke test cases for NSX and vCenter features,
but we haven't got enough time to perform it manually during feature freeze
milestone.

Proposed change
===============

Enable support of automated acceptance test cases for vCenter and NSX features.

This will allow as to perform full scale acceptance testing of our features in
short time, according to manual test cases in this document below:

https://docs.google.com/a/mirantis.com/spreadsheets/d
12pxHDADqago_6PO4y0VZ1IrwymswqNiuvhMSUoCFaYc/edit?pli=1#gid=1778064828

See NSX and vCenter tabs

Alternatives
------------

If it not be implemented in time we will perform manually only tests with
'High' priority.

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

None.

Performance Impact
------------------

None.

Other deployer impact
---------------------

None.

Developer impact
----------------

None.


Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Tatyana Dubyk (tatka.donets)

Other contributors:

* Alexander Kosse (al.rem)
* Eugene Korekin (azkore)

Work Items
----------

* Creation of autotests according to test cases which have already been
  described in document in section 'Proposed change';
* Set up a test environment and debugging them on required hosts;
* Add these tests in already existing Jenkins jobs.

Dependencies
============

None.

Testing
=======

Check that all tests are implemented according to required workflow
and running stable in Jenkins jobs.

Documentation Impact
====================

None.

References
==========

None.