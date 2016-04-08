..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================================================
Fuel-qa: generate report of failed tests and builds per failure reason group
============================================================================

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
Offen QA engineers do investigation simultaneously for different failed test
where failure reason is the same and they wasting time in this case.
Special report which combines failed tests and builds per one failure reason
group can help assign only one QA engineer per each failure reason group.
Moreover such statistics can be utilized in future in order to do automation
classification of failures and generate different measurement reports.


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
7. Make magic in order to do a grouping of all failed builds
and tests per failure reason. Failure type/error type, message fields
are going to be used for grouping:
-Do Regexp. We shall take a failure message body and extract IP/MAC, etc
because that info are less important for grouping and those info clatter
the message.
-clean up: IP/Mac, numbers separated by a spaces, brackets, quotes, dashes,
points and replace them by spaces. It helps to avoid creating a lot of groups
which have minor differences.
-find Levenshtein distance of failures between each other. We shall apply
Levenshtein or similar algorithm because we need to find degree of proximity.
If proximity more then threshold then we can combine those failures in one group
otherwise we keep they are separately.
-do grouping. We shall do grouping for all failures and combine failed builds
and failed tests per one group. In this case we'll got matrix between
failure group(s) and failed builds and tests.
8. Generate report which return list of failure reason groups and failed builds
and tests per each group.


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

None

Assignee(s)
===========

Primary assignee:
  * Kirill Rozin (krozin): krozin@mirantis.com

Other contributors:
  * Anton Studenov (astudenov): astudenov@mirantis.com

Mandatory design review:
  * Dennis Dmitriev (ddmitriev): ddmitriev@mirantis.com
  * Dmitry Tyzhnenko (dtyzhnenko): dtyzhnenko@mirantis.com

Work Items
==========

- Investigate the existing code
- Investigate script /fuel-qa/fuelweb_test/testrail/generate_statistics.py
- Add new report generator in fuel-qa
- Test the proof of concept and make sure that the output is correct enough


Dependencies
============

None


------------
Testing, QA
------------

1. run python script:
python generate_failure_group_statistics.py -n 69 -j 9.0.swarm.runner -o report -f json
2. double check that report.json. It shall not be empty if SWARM 69 build has any failures.


Acceptance criteria
===================

- If failure is observed in SWARM build then failure reason report
  should be generated. Several failed builds and tests must be combined
  per one failed reason group.
- If no failure is observed the empty report shall be generated

----------
References
----------

None


