..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
 Nailgun code testing improvements
===================================

https://blueprints.launchpad.net/fuel/+spec/nailgun-code-testing-improvements

Current unit/integration tests needs improvement and should follow a single
code testing policy.


Problem description
===================

Terms
-----

Unit testing is a software testing method by which individual units of source
code, sets of one or more computer program modules together with associated
control data, usage procedures, and operating procedures are tested to
determine if they are fit for use. The goal of unit testing is to isolate each
part of the program and show that the individual parts are correct. [1]_

Integration testing is the phase in software testing in which individual
software modules are combined and tested as a group. Integration testing takes
as its input modules that have been unit tested, groups them in larger
aggregates, applies tests defined in an integration test plan to those
aggregates, and delivers as its output the integrated system ready for system
testing. [2]_

Functional testing is a quality assurance (QA) process and a type of black box
testing that bases its test cases on the specifications of the software
component under test. Functions are tested by feeding them input and examining
the output, and internal program structure is rarely considered. Functional
testing usually describes what the system does. [3]_

Since functional testing is a part of QA process we don't consider its usage in
the scope if this document.

Problems
--------

* The project needs to have a policy which describes tests writing rules

* Not all classes and functions covered with tests

* There are no test coverage measurement and accordingly no lower test coverage
  threshold

* Unit and functional tests are spreaded in a mess and don't correspond
  their purpose

* Each module has to have described testing method (unit or/and functional)

* Some tests marked as skipped

* There are duplicated tests

* Some helper classes and functions don't have descriptive names


Proposed change
===============

``nailgun`` project needs improvements in code testing as follows:

* The project needs in a document(policy) which describes:

    - Tests creation technique;
    - Test categorization (integration/unit) and approaches of testing
      different code base

    Fuel project already has a policy scaffold on wiki page [4]_. It needs to
    be updated and placed to official development documentation source [5]_.

* All the classes and functions should be covered with tests. A test coverage
  percentage should be more than XX%

* Some of classes and functions should be covered with integration as well as
  unit tests

* There should be a policy which describes testing types used for particular
  classes and functions

* The policy sets unit tests grouping by modules

* Remove 'skipped' tests

* Lookup and remove duplicate tests

* Mimic Nailgun module structure in unit tests

* Rename class ``Environment`` to more descriptive ``EnvironmentManager`` [6]_

* Remove hardcoded self.clusters[0], etc. from ``Environment``. Let's use
  parameters instead [7]_. This will add an additional flexibility in writing
  tests

* run_tests.sh should invoke alternate syncdb() for cases where we don't need
  to test migration procedure, i.e. create_db_schema(). syncdb() executes
  migration procedure to create db schema. We need a procedure which creates
  the schema without running all the migrations, i.e.
  ``Base.metadata.create_all``. This is going to decrease tests running time

* Add tests for Alembic migrations [8]_

* Consider usage of custom fixture provider. The main functionality should
  combine loading from YAML/JSON source and support fixture inheritance

* Review refactor tests as exposed in test types application

Test types application to the Nailgun modules
---------------------------------------------

+-----------------------------------------------+-----------+-------------+
|                Component                      |        Test types       |
+===============================================+===========+=============+
|                                               |    Unit   | Integration |
+-----------------------------------------------+-----------+-------------+
| | api/v1/handlers/*                           |   |       |    | ✓      |
| | api/v1/urls.py                              |   |       |    | ✓      |
| | api/v1/validators/*                         |   | ✓     |             |
| | api/v1/validators/json_schema/*             |   |       |             |
+-----------------------------------------------+-----------+-------------+
| | app.py                                      |           |    | ✓      |
+-----------------------------------------------+-----------+-------------+
| | assassin/assassind.py                       |           |    | ✓      |
+-----------------------------------------------+-----------+-------------+
| | autoapidoc.py                               |   | ✓     |             |
| | consts.py                                   |           |             |
+-----------------------------------------------+-----------+-------------+
| | db/api.py                                   |           |             |
| | db/deadlock_detector.py                     |   | ✓     |             |
| | db/migration/alembic_migrations/__init__.py |           |    | ✓      |
| | db/migration/alembic_migrations/*           |           |    | ✓      |
| | db/sqlalchemy/__init__.py                   |           |    | ✓      |
| | db/sqlalchemy/fixman.py                     |           |    | ✓      |
| | db/sqlalchemy/models/*                      |           |             |
+-----------------------------------------------+-----------+-------------+
| | errors/*                                    |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | expression/*                                |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | fake_keystone/__init__.py                   |   | ✓     |             |
| | fake_keystone/handlers.py                   |           |    | ✓      |
| | fake_keystone/urls.py                       |           |    | ✓      |
+-----------------------------------------------+-----------+-------------+
| | fsm/*                                       |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | logger.py                                   |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | middleware/connection_monitor.py            |           |    | ✓      |
| | middleware/http_method_override.py          |   | ✓     |    | ✓      |
| | middleware/keystone.py                      |   | ✓     |    | ✓      |
| | middleware/static.py                        |   | ✓     |    | ✓      |
| | middleware/utils.py                         |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | network/checker.py                          |           |    | ✓      |
| | network/manager.py                          |           |    | ✓      |
| | network/neutron.py                          |           |    | ✓      |
| | network/nova_network.py                     |           |    | ✓      |
| | network/utils.py                            |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | notifier.py                                 |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | objects/*                                   |   | ✓     |    | ✓      |
| | objects/serializers/*                       |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | openstack/common/db/*                       |           |    | ✓      |
| | openstack/common/db/sqlalchemy/*            |           |    | ✓      |
| | openstack/common/*                          |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | orchestrator/*                              |           |    | ✓      |
+-----------------------------------------------+-----------+-------------+
| | plugins/attr_plugin.py                      |           |    | ✓      |
| | plugins/manager.py                          |           |    | ✓      |
+-----------------------------------------------+-----------+-------------+
| | rpc/__init__.py                             |           |    | ✓      |
| | rpc/receiver.py                             |           |    | ✓      |
| | rpc/receiverd.py                            |           |    | ✓      |
| | rpc/threaded.py                             |           |    | ✓      |
| | rpc/utils.py                                |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | settings.py                                 |           |             |
+-----------------------------------------------+-----------+-------------+
| | statistics/installation_info.py             |           |    | ✓      |
| | statistics/openstack_info_collector.py      |           |    | ✓      |
| | statistics/params_white_lists.py            |           |             |
| | statistics/statsenderd.py                   |           |    | ✓      |
+-----------------------------------------------+-----------+-------------+
| | task/*                                      |           |    | ✓      |
+-----------------------------------------------+-----------+-------------+
| | urls.py                                     |           |             |
+-----------------------------------------------+-----------+-------------+
| | utils/*                                     |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | volumes/manager.py                          |   | ✓     |             |
+-----------------------------------------------+-----------+-------------+
| | webui/handlers.py                           |           |    | ✓      |
| | webui/urls.py                               |           |             |
+-----------------------------------------------+-----------+-------------+
| | wsgi.py                                     |           |             |
+-----------------------------------------------+-----------+-------------+

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

None

Other deployer impact
---------------------

None

Developer impact
----------------

Developers have to follow the code testing policy

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ivankliuk

Other contributors:
  fuel-python

Work Items
----------

None


Dependencies
============

None


Testing
=======

This document describes testing itself.


Documentation Impact
====================

Nailgun development documentation [5]_ will be updated with the tests writing
policy


References
==========

`Mailing list discussion <https://www.mail-archive.com/openstack-dev@lists.openstack.org/msg40919.html>`_

.. [1] http://en.wikipedia.org/wiki/Unit_testing
.. [2] http://en.wikipedia.org/wiki/Integration_testing
.. [3] http://en.wikipedia.org/wiki/Functional_testing
.. [4] https://wiki.openstack.org/wiki/Fuel/How_to_Test_Your_Code
.. [5] http://docs.mirantis.com/fuel-dev/develop/nailgun.html
.. [6] https://review.openstack.org/#/c/138823/
.. [7] https://bugs.launchpad.net/fuel/+bug/1398043
.. [8] https://bugs.launchpad.net/fuel/+bug/1391553

