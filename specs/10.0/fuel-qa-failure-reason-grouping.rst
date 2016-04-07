..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Fuel-qa: generate report of failed tests and builds per failure reason group
=========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-qa-failure-reason-grouping

This spec propose changes in fuel-qa to generate report for SWARM failed build.
Report combines failed tests and builds per failure reason group.
All found failure reasons in each build shall be combined to several groups
of Levenshtein distance of failure reason string smaller than the threshold.


--------------------
Problem description
--------------------

Failed SWARM builds requires to do investigation through logs and code
and to answer what type of failure reason happened per each test and build.
Offen QA engineers do investigation simultaneously for different failed test where
failure reason is the same and they wasting time in this case.
Special report which combines failed tests and builds per one failure reason group
can help assign only one QA engineer per each failure reason group.
Moreover such statistics can be utilized in future in order to do automation classification
of failures and generate different measurement reports.


----------------
Proposed changes
----------------

Add new failure reason report generator.
It shall be similar to /fuel-qa/fuelweb_test/testrail/generate_statistics.py

This script should do:
1. Get SWARM build by build number and Jenkins job name
2. Get all Jenkins sub builds
3. Get all nosetests.xml files per each sub Jenkins build
4. Extract all FAILED test results from all nosetests.xml files
5. Get "failure type" and "message" like failure reason
6. Generate list of all found failures
7. Make magic:
    Do Regexp
    clean up: IP/Mac, numbers separated by a spaces, brackets, quotes, dashes, points and replace them by spaces.
    find Levenshtein distance of failures between each other.
    do grouping
8. Generate report which return list of failure reason groups and failed builds and tests per each group.


Web UI
======

None


Nailgun
=======

None

Data model
----------

None


REST API
--------

None


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

None


Fuel Library
============

None


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

None


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None


------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

None


----------------
Developer impact
----------------

None


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  * Kirill Rozin (krozin): krozin@mirantis.com

Other contributors:
  * Dennis Dmitriev (ddmitriev): ddmitriev@mirantis.com
  * Dmitry Tyzhnenko (dtyzhnenko): dtyzhnenko@mirantis.com
  * Anton Studenov (astudenov): astudenov@mirantis.com

Mandatory design review:
  None


Work Items
==========

- Investigate the existing code
- Investigate similar script /fuel-qa/fuelweb_test/testrail/generate_statistics.py
- Add new report generator in fuel-qa


Dependencies
============

None


------------
Testing, QA
------------

None


Acceptance criteria
===================

- If failure is observed in SWARM build then failure reason report should be generated.
  Several failed builds and tests must be combined per one failed reason group.
- If no failure is observed the empty report shall be generated

----------
References
----------

None


