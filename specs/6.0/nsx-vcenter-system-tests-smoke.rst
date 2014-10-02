==================================================================
Integration of automated system tests for NSX and vCenter features
==================================================================

Related to blueprint:
https://blueprints.launchpad.net/fuel/+spec/nsx-vcenter-system-tests-smoke

Problem description
===================

We have a lot of acceptance and smoke test cases for NSX and vCenter features,
but we haven't got enough time to perform it manually during feature freeze
milestone.

Proposed change
===============

Enable support of automated system tests which are based on manual
acceptance test cases of vCenter and NSX features.
It will allow us to reduce the time to perform a comprehensive acceptance
testing, according to manual test cases that we've already created
considering different parameters and modes.

Alternatives
------------

If it is not implemented in time, we will perform only manual tests with
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

* Create automated system tests according to manual acceptance test
  cases with different configuration and parameters for nsx and
  vcenter features;
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