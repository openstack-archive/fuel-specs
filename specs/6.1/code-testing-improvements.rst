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
part of the program and show that the individual parts are correct. [5]_

Integration testing is the phase in software testing in which individual
software modules are combined and tested as a group. Integration testing takes
as its input modules that have been unit tested, groups them in larger
aggregates, applies tests defined in an integration test plan to those
aggregates, and delivers as its output the integrated system ready for system
testing. [6]_

Functional testing is a quality assurance (QA) process and a type of black box
testing that bases its test cases on the specifications of the software
component under test. Functions are tested by feeding them input and examining
the output, and internal program structure is rarely considered. Functional
testing usually describes what the system does. [7]_

Since functional testing is a part of QA process we don't consider its usage in
the scope if this document.

Changes
-------

``nailgun`` sub-project needs improvements in code testing as follows:

* All the components should be covered with tests. A test coverage percentage
  should be more than XX%

* Some of components should be covered with integration as well as unit tests

* There should be a policy which describes testing types used for particular
  component

* The policy sets unit tests grouping by modules

* Unit and functional tests are spreaded in a mess and don't correspond
   their purpose

* Remove 'skipped' tests


Proposed change
===============

* Rename class ``Environment`` to more descriptive ``EnvironmentManager`` [8]_

* Remove hardcoded self.clusters[0], etc. from ``Environment``. Let's use
  parameters instead [1]_. This will add an additional flexibility in writing
  tests

* run_tests.sh should invoke alternate syncdb() for cases where we don't need
  to test migration procedure, i.e. create_db_schema(). syncdb() executes
  migration procedure to create db schema. We need a procedure which creates
  the schema without running all the migrations. This is going to decrease
  tests running time

* Consider usage of custom fixture provider. The main functionality should
  combine loading from YAML/JSON source and support fixture inheritance

* The project needs in a document(policy) which describes:

    - Tests creation technique;
    - Test categorization (integration/unit) and approaches of testing
      different code base

    Fuel project already has a policy scaffold on wiki page [2]_. It needs to
    be updated and placed to official development documentation source [3]_.

* Review the tests and refactor unit tests as described in the test policy

* Mimic Nailgun module structure in unit tests

* Lookup and remove duplicate tests

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

Nailgun development documentation [3]_ will be updated with the tests writing
policy


References
==========

.. [1] https://bugs.launchpad.net/fuel/+bug/1398043
.. [2] https://wiki.openstack.org/wiki/Fuel/How_to_Test_Your_Code
.. [3] http://docs.mirantis.com/fuel-dev/develop/nailgun.html
.. [4] https://www.mail-archive.com/openstack-dev@lists.openstack.org/msg40919.html
.. [5] http://en.wikipedia.org/wiki/Unit_testing
.. [6] http://en.wikipedia.org/wiki/Integration_testing
.. [7] http://en.wikipedia.org/wiki/Functional_testing
.. [8] https://review.openstack.org/#/c/138823/
