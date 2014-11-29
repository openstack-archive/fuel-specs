..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================
 Code testing improvements
===========================

https://blueprints.launchpad.net/fuel/+spec/code-testing-improvements

Current unit/integration tests needs improvement and should follow a single code testing policy.


Problem description
===================

Terms
------

Test type stands for unit, integration, functional testing methodology.

Changes
-------

``fuel-web`` project needs improvements in code testing as follows:

* All the components should be covered with unit tests

* Some of components should be covered with integration and/or functional as well as unit tests

* There should be a policy which describes testing types used for particular component

* The policy sets unit tests grouping by modules

* Unit and functional tests are spreaded in a mess and don't correspond
   their purpose

* Remove 'skipped' tests

Proposed change
===============

* Rename class ``Environment`` to more descriptive ``EnvironmentManager``

* Remove hardcoded self.clusters[0], etc. from ``Environment``. Let's use parameters instead [1]_

* run_tests.sh should invoke alternate syncdb() for cases where we don't need to test migration procedure, i.e. create_db_schema()

* Consider usage of custom fixture provider. The main functionality should combine loading from YAML/JSON source and support fixture inheritance

* The project needs in a document(policy) which describes:

    - Tests creation technique;
    - Test categorization (integration/unit) and approaches of testing different code base

    Fuel project already has a policy scaffold on wiki page [2]_. It needs to be updated and placed to official development documentation source [3]_.

* Review the tests and refactor unit tests as described in the test policy

* Mimic Nailgun module structure in unit tests

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

None


References
==========

.. [1] https://bugs.launchpad.net/fuel/+bug/1398043
.. [2] https://wiki.openstack.org/wiki/Fuel/How_to_Test_Your_Code
.. [3] http://docs.mirantis.com/fuel-dev/develop/nailgun.html

