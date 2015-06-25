..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Introduce InternJS framework for UI functional tests
====================================================

https://blueprints.launchpad.net/fuel/+spec/ui-functional-tests-with-intern

Fuel front-end should be covered with functional tests to avoid regression.

Problem description
===================

Functional tests for the front-end layer of Fuel are currently created with
CasperJS framework, while tests are run against headless browser phantomjs
as a part of CI procedure.

Developer that works on bug fix or creates a new feature supposed to cover
them with both unit and functional tests to avoid regression. The way
functional tests are created and maintained currently is complex since
CasperJS is not that flexible with the single-page web applications as
InternJS. In addition there is no way to run tests against browsers with
UI for debugging purposes.

Proposed change
===============

Adopt InternJS as the primary testing framework for UI functional tests.

Test runner ``run_tests.sh`` should be updated correspondingly to utilize
Intern instead of Casper. Expected syntax:

* ``../run_tests.sh --ui-func`` - to run all tests
* ``../run_tests.sh -t static/tests/functional/test_welcome_page.js`` - to
  run single test suite


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

As soon Intern-based tests are run against Firefox browser it will take
additional time for CI to validate patchsets committed.

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

Front-end developers have to cover features and fixes they work on with
functional tests. These efforts should be taken into account while planning.

Infrastructure impact
---------------------

CI workers should be able to run Firefox browser in order to execute
functional tests against it.

Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Nikolay Bogdanov (nbogdanov@mirantis.com)

Other contributors:

* Vitaly Kramskikh (vkramskikh@mirantis.com)

Work Items
----------

* Research the way how Intern tests should be created and organized
* Update test runner ``run_tests.sh`` to utilize InternJS for ui tests
* Create initial helper library to cover the most frequent tasks (log
  in, skip welcome page, create cluster, remove cluster)
* Create several tests as an example

Dependencies
============

None

Testing
=======

None

Acceptance criteria
-------------------

* Functional tests for the UI are the part of the CI process and are executed
  on every commit. Execution result affects build status
* Helper library (page) that covers below use-cases is created:

  * Log In
  * Log Out
  * Skip Welcome page
  * Create Cluster
  * Remove Cluster
  * Add Cluster nodes

* The following pages (partially) covered with functional tests:

  * Log In
  * Welcome page
  * Clusters page
  * Cluster page

Documentation Impact
====================

Documentation should be modified to remove mentions of CasperJS and its
installation prerequisites.

References
==========

* InternJS library - https://theintern.github.io
* ChaiJS assertion library - http://chaijs.com
* Leadfoot library for consistency with Selenium WebDriver API - https://theintern.github.io/leadfoot
* Spec for UI unit-tests - https://review.openstack.org/#/c/195666
