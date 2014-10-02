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

As non functional type of testing, we will check what kind of performance
impact NSX can have on lab.

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
  vcenter features, to check that nsx and vcenter features are successfully
  integrated with each other;
* Verify that according to blueprints of this release our features with
  additional settings that in scope of release work fine;
* Set up a test environment and debug tests on host, that allocated for it;
* Add these tests in already existing Jenkins jobs.

Dependencies
============

None.

Testing
=======

Check that all tests are implemented according to the required workflow
and they ran stable in Jenkins jobs.

Documentation Impact
====================

All additional information related to nsx you can find there:
http://goo.gl/3Klbq3

References
==========

None.