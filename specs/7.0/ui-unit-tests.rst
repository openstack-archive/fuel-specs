..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Intern-based Unit Tests for Fuel UI
===================================

https://blueprints.launchpad.net/fuel/+spec/ui-unit-tests

Implement unit test runner for Fuel UI.


Problem description
===================

Currently Fuel UI is covered only by functional tests based on CasperJS
functional testing framework. It allows end-to-end testing of Fuel UI, but
there are lots of cases which can't be covered (or covered with lots of
efforts) by functional testing. So we need also to be able to write and run
unit tests for Fuel UI.


Proposed change
===============

We should implement unit test runner for Fuel UI using Intern Framework:
* It should be available by running ``./run_tests.sh --ui-unit``.
* It should be voting.
* At least one test suite should be added (for Expression parser).

Alternatives
------------

There are quite a few JS unit test frameworks available, but we should go with
Intern as it also support functional testing and we plan to switch to it
someday.

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

Plugin impact
-------------

None.

Other deployer impact
---------------------

None.

Developer impact
----------------

If suitable, new changes to Fuel UI should be covered by unit tests.

Infrastructure impact
---------------------

Intern uses Selenium, so Java Runtime Environment (JRE) 1.6 or newer version
should be installed on Fuel CI workers.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
* Vitaly Kramskikh <vkramskikh@mirantis.com>

Other contributors:
* Przemyslaw Kaminski <pkaminski@mirantis.com>

Mandatory design review:
* Vitaly Kramskikh <vkramskikh@mirantis.com>

QA engineer:
* Anastasia Palkina <apalkina@mirantis.com>

Work Items
----------

* Rearrange the code in place where it is needed so it can be covered by
  unit tests.
* Update gulpfile so gulp can run unit tests by command ``gulp unit-tests``.
* Update ``run_tests.sh`` so in can run uint tests using ``--ui-unit``
  argument. Unit tests should be voting.
* Add a test suite for Expression parser.


Dependencies
============

None.


Testing
=======

None.

Acceptance criteria
-------------------

* It is possible to run unit tests by running ``./run_tests.sh --ui-unit``.
* Unit tests failure leads to failure of `verify-fuel-web` job.
* Documentation is updated to mention how to set up and run unit tests.
* Unit test suite for Expression parser exists.


Documentation Impact
====================

* Development environment setup docs should be modified to mention dependency
  on JRE for UI unit testing.

* There should be described how to run unit tests on development environments.


References
==========

* InternJS library - https://theintern.github.io
* Spec for Intern-based functional tests - https://review.openstack.org/195520
* Gulpfile -
  https://github.com/stackforge/fuel-web/blob/master/nailgun/gulpfile.js
* Expression parser -
  https://github.com/stackforge/fuel-web/tree/master/nailgun/static/expression
