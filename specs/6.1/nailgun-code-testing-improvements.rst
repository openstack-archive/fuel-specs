..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
 Nailgun code testing improvements
===================================

https://blueprints.launchpad.net/fuel/+spec/nailgun-code-testing-improvements

Current unit and integration tests needs improvement and should follow a single
code testing policy.


Problem description
===================

Terms
-----

Unit testing is a software testing method by which individual units of source
code are tested to determine if they are fit for use. The goal of unit testing
is to isolate each part of the program and show that the individual parts are
correct [1]_.

Integration testing is the phase in software testing in which individual
software modules are combined and tested as a group [2]_.

Functional testing is a quality assurance (QA) process and a type of black-box
testing that bases its test cases on the specifications of the software
component under test. Functions are tested by feeding them input and examining
the output [3]_.

Since functional testing is a part of QA process we don't consider its usage in
the scope of this document.

Problems
--------

* The project needs to have a policy which describes tests writing rules.

* Not all classes and functions are covered with tests.

* There's no test coverage measurement and, accordingly, no lower bound for
  test coverage.

* Unit and functional tests are not arranged properly and do not correspond
  with their purposes.

* Skipped tests lead to lack of coverage.

* Tests duplicate each other.

* Some helper classes and functions don't have descriptive names.

* ``nailgun.db.syncdb()`` is used for the test database creation. It runs all
  migrations one-by-one which is pretty slow.

Current test coverage
---------------------

Test coverage procedure is performed using
`py.test-cov <https://pypi.python.org/pypi/pytest-cov>`_ utility by running
the following command:

.. code:: bash

  py.test --cov-config .coveragerc --cov nailgun nailgun/test/

``.coveragerc`` file lists files and directories are not taken into account
when calculating code coverage:

.. code:: ini

  [run]
  omit =
      nailgun/test/*
      nailgun/openstack/common/*
      nailgun/unit_test*

where ``nailgun/tests/`` and ``nailgun/unit_test.py`` contain the tests itself,
``nailgun/openstack/common`` is a part of ``oslo-incubator``.

Here's the report generated on December 23, 2014:

==========================================================  ======  ====  =====
Name                                                        Stmts   Miss  Cover
==========================================================  ======  ====  =====
nailgun/__init__                                                0      0   100%
nailgun/api/__init__                                            0      0   100%
nailgun/api/v1/__init__                                         0      0   100%
nailgun/api/v1/handlers/__init__                                2      0   100%
nailgun/api/v1/handlers/assignment                             24      0   100%
nailgun/api/v1/handlers/base                                  187     22    88%
nailgun/api/v1/handlers/capacity                               66      4    94%
nailgun/api/v1/handlers/cluster                                96     10    90%
nailgun/api/v1/handlers/disks                                  34      1    97%
nailgun/api/v1/handlers/logs                                  227     63    72%
nailgun/api/v1/handlers/master_node_settings                   28     15    46%
nailgun/api/v1/handlers/network_configuration                 101      5    95%
nailgun/api/v1/handlers/node                                  109      6    94%
nailgun/api/v1/handlers/node_group                             31      9    71%
nailgun/api/v1/handlers/notifications                          21      0   100%
nailgun/api/v1/handlers/orchestrator                          103     10    90%
nailgun/api/v1/handlers/plugin                                 16      1    94%
nailgun/api/v1/handlers/registration                           12      0   100%
nailgun/api/v1/handlers/release                                32      0   100%
nailgun/api/v1/handlers/removed                                15      1    93%
nailgun/api/v1/handlers/tasks                                  27      4    85%
nailgun/api/v1/handlers/version                                13      0   100%
nailgun/api/v1/urls                                            64      0   100%
nailgun/api/v1/validators/__init__                              0      0   100%
nailgun/api/v1/validators/assignment                           79      2    97%
nailgun/api/v1/validators/base                                 36      3    92%
nailgun/api/v1/validators/cluster                              55     10    82%
nailgun/api/v1/validators/json_schema/__init__                  2      0   100%
nailgun/api/v1/validators/json_schema/assignment                2      0   100%
nailgun/api/v1/validators/json_schema/base_types               19      0   100%
nailgun/api/v1/validators/json_schema/cluster                   4      0   100%
nailgun/api/v1/validators/json_schema/disks                     1      0   100%
nailgun/api/v1/validators/json_schema/networks                  2      0   100%
nailgun/api/v1/validators/json_schema/node                      3      0   100%
nailgun/api/v1/validators/json_schema/plugin                    3      0   100%
nailgun/api/v1/validators/json_schema/release                   4      0   100%
nailgun/api/v1/validators/master_node_settings                 11      5    55%
nailgun/api/v1/validators/network                             131     21    84%
nailgun/api/v1/validators/node                                144     10    93%
nailgun/api/v1/validators/node_group                           17      3    82%
nailgun/api/v1/validators/notification                         37     10    73%
nailgun/api/v1/validators/plugin                               15      2    87%
nailgun/api/v1/validators/release                              58      2    97%
nailgun/api/v1/validators/task                                 10      0   100%
nailgun/app                                                    48     22    54%
nailgun/assassin/__init__                                       0      0   100%
nailgun/assassin/assassind                                     27      8    70%
nailgun/autoapidoc                                             48     20    58%
nailgun/consts                                                 33      0   100%
nailgun/db/__init__                                             6      0   100%
nailgun/db/deadlock_detector                                   35      1    97%
nailgun/db/migration/__init__                                  34     16    53%
nailgun/db/migration/alembic_migrations/env                    22      4    82%
nailgun/db/migration/alembic_migrations/versions/fuel_5_0      60     49    18%
nailgun/db/migration/alembic_migrations/versions/fuel_5_1      72     40    44%
nailgun/db/migration/alembic_migrations/versions/fuel_6_0      84     60    29%
nailgun/db/sqlalchemy/__init__                                 79     30    62%
nailgun/db/sqlalchemy/fixman                                  148     50    66%
nailgun/db/sqlalchemy/models/__init__                          26      0   100%
nailgun/db/sqlalchemy/models/action_logs                       22      0   100%
nailgun/db/sqlalchemy/models/base                              13      0   100%
nailgun/db/sqlalchemy/models/cluster                           64      1    98%
nailgun/db/sqlalchemy/models/fields                            18      0   100%
nailgun/db/sqlalchemy/models/master_node_settings              10      0   100%
nailgun/db/sqlalchemy/models/network                           45      0   100%
nailgun/db/sqlalchemy/models/network_config                    37      0   100%
nailgun/db/sqlalchemy/models/node                             204     11    95%
nailgun/db/sqlalchemy/models/notification                      18      0   100%
nailgun/db/sqlalchemy/models/plugins                           25      0   100%
nailgun/db/sqlalchemy/models/release                           86      8    91%
nailgun/db/sqlalchemy/models/task                              37      2    95%
nailgun/db/sqlalchemy/utils                                     5      0   100%
nailgun/errors/__init__                                        11      0   100%
nailgun/errors/base                                            14      0   100%
nailgun/expression/__init__                                     9      0   100%
nailgun/expression/expression_parser                           66      0   100%
nailgun/expression/objects                                     51      4    92%
nailgun/fake_keystone/__init__                                  8      0   100%
nailgun/fake_keystone/handlers                                 25      9    64%
nailgun/fake_keystone/urls                                      7      0   100%
nailgun/fixtures/__init__                                       0      0   100%
nailgun/fsm/__init__                                            0      0   100%
nailgun/fsm/state_list                                          6      6     0%
nailgun/logger                                                 64     38    41%
nailgun/middleware/__init__                                     0      0   100%
nailgun/middleware/connection_monitor                          63     45    29%
nailgun/middleware/http_method_override                         9      5    44%
nailgun/middleware/keystone                                    64      1    98%
nailgun/middleware/static                                      36     26    28%
nailgun/middleware/utils                                       18      0   100%
nailgun/network/__init__                                        0      0   100%
nailgun/network/checker                                       260      4    98%
nailgun/network/manager                                       533     38    93%
nailgun/network/neutron                                        28      1    96%
nailgun/network/nova_network                                   22      0   100%
nailgun/network/utils                                           6      0   100%
nailgun/notifier                                                3      0   100%
nailgun/objects/__init__                                       22      0   100%
nailgun/objects/action_log                                     21      0   100%
nailgun/objects/base                                          156     11    93%
nailgun/objects/capacity                                        8      0   100%
nailgun/objects/cluster                                       270      8    97%
nailgun/objects/master_node_settings                           18      7    61%
nailgun/objects/node                                          309      8    97%
nailgun/objects/node_group                                     30      4    87%
nailgun/objects/notification                                   40      1    98%
nailgun/objects/plugin                                         20      0   100%
nailgun/objects/release                                        81      0   100%
nailgun/objects/serializers/__init__                            0      0   100%
nailgun/objects/serializers/action_log                          3      0   100%
nailgun/objects/serializers/base                               22      2    91%
nailgun/objects/serializers/cluster                             5      0   100%
nailgun/objects/serializers/master_node_settings                3      0   100%
nailgun/objects/serializers/network_configuration              34      0   100%
nailgun/objects/serializers/node                               22      0   100%
nailgun/objects/serializers/node_group                          3      0   100%
nailgun/objects/serializers/notification                        3      0   100%
nailgun/objects/serializers/plugin                              3      0   100%
nailgun/objects/serializers/release                            12      0   100%
nailgun/objects/serializers/task                                3      0   100%
nailgun/objects/task                                          144      7    95%
nailgun/openstack/__init__                                      0      0   100%
nailgun/orchestrator/__init__                                   0      0   100%
nailgun/orchestrator/deployment_serializers                   520     25    95%
nailgun/orchestrator/plugins_serializers                      113     14    88%
nailgun/orchestrator/priority_serializers                      86      5    94%
nailgun/orchestrator/provisioning_serializers                  83      1    99%
nailgun/plugins/__init__                                        0      0   100%
nailgun/plugins/attr_plugin                                    88      8    91%
nailgun/plugins/manager                                        24      0   100%
nailgun/rpc/__init__                                           31     12    61%
nailgun/rpc/receiver                                          492     82    83%
nailgun/rpc/receiverd                                          53     16    70%
nailgun/rpc/threaded                                           42     42     0%
nailgun/rpc/utils                                               8      5    38%
nailgun/settings                                               45      6    87%
nailgun/statistics/__init__                                     0      0   100%
nailgun/statistics/installation_info                           85     76    11%
nailgun/statistics/openstack_info_collector                    50     46     8%
nailgun/statistics/params_white_lists                           3      0   100%
nailgun/statistics/statsenderd                                114    114     0%
nailgun/task/__init__                                           0      0   100%
nailgun/task/fake                                             325     38    88%
nailgun/task/helpers                                          187     26    86%
nailgun/task/manager                                          393     37    91%
nailgun/task/task                                             353     11    97%
nailgun/urls                                                    9      0   100%
nailgun/utils/__init__                                         87      9    90%
nailgun/utils/migration                                       145     33    77%
nailgun/utils/zabbix                                           66     51    23%
nailgun/volumes/__init__                                        0      0   100%
nailgun/volumes/manager                                       416     20    95%
nailgun/webui/__init__                                          0      0   100%
nailgun/webui/handlers                                          9      4    56%
nailgun/webui/urls                                              6      0   100%
nailgun/wsgi                                                    6      6     0%
----------------------------------------------------------  ------  ----  -----
TOTAL                                                        9521   1453    85%
==========================================================  ======  ====  =====

Proposed change
===============

``nailgun`` project needs improvements in code testing as follows:

* Create a policy which describes:

  - Tests creation technique.
  - Test categorization (integration/unit/performance) and approaches of
    testing different Nailgun modules.

  Fuel project already has a policy scaffold on wiki page [4]_. It needs to
  be updated and placed to official development documentation source [5]_.

* All the classes and functions should be covered with tests. A test coverage
  percentage should be more than 90%.

* Some of classes and functions should be covered with integration as well as
  unit tests. This is left at the discretion of the developer.

* Fix 'skipped' tests.

* Remove duplicated tests.

* Mimic Nailgun module structure in unit tests.

* Rename <Environment> class to a more descriptive <EnvironmentManager> [6]_.

* Remove hardcoded <clusters>, <releases> and <nodes> attributes from
  <Environment> class. Let's use parameters instead [7]_. These parameters will
  provide additional flexibility in writing tests

* Remove ``nailgun.db.syncdb()`` logic from ``run_tests.sh``. Add database
  schema creation to the test base class by means of
  ``Base.metadata.create_all``.

* Add tests for Alembic migrations [8]_.

* Considering usage of custom fixture provider is beyond the scope of this
  document.

* Review and refactor tests as exposed in the code testing policy.

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

Developers have to follow the code testing policy [9]_.

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

Nailgun development documentation [5]_ is updated with the code testing policy
[9]_ by primary assignee.


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
.. [9] http://docs.mirantis.com/fuel-dev/develop/nailgun/development/code_testing.html

