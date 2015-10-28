..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================================
Template based test cases with external configuration
=====================================================

Improve the system test for using external configuration

--------------------
Problem description
--------------------

We have a permanent growing product with a lot of features. From release to
release we should cover more and more cases and current approach can not keep
up with the changes.

* Tests have a lot of copy-paste code

* Many tests have a hardcoded cluster configuration

* For test aditional configuration with the same steps, we should write another test

----------------
Proposed changes
----------------

Write extension for current test framework which might works with external
configuration and has template structure for the test cases.

**Pros**:

* Configuration for test be at the external human readable yaml file

* Unified library for steps of test, checkers and actions

* Inheritance, simple expanding and composition new cases with already existing

Web UI
======

N/A

Nailgun
=======

N/A

Data model
----------

N/A

REST API
--------

N/A

Orchestration
=============

N/A

RPC Protocol
------------

N/A

Fuel Client
===========

N/A

Plugins
=======

N/A

Fuel Library
============

N/A

------------
Alternatives
------------

N/A

--------------
Upgrade impact
--------------

N/A

---------------
Security impact
---------------

N/A

--------------------
Notifications impact
--------------------

N/A

---------------
End user impact
---------------

N/a

------------------
Performance impact
------------------

N/A

-----------------
Deployment impact
-----------------

N/A

----------------
Developer impact
----------------

N/A

--------------------------------
Infrastructure/operations impact
--------------------------------

N/A

--------------------
Documentation impact
--------------------

N/A

--------------------
Expected OSCI impact
--------------------

N/A

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Dmytro Tyzhnenko

Other contributors:
  Denys Dmytriiev

Mandatory design review:
  Anastasiia Urlapova, Denys Dmytriiev

Work Items
==========

* Create configuration structure

* Code base models for templated tests

* Implement collector of test + configuration combination

* Integrate with current framework

* Update reporting tools

Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


------------
Testing, QA
------------

All existed tests and tools should work as worked befour.

Acceptance criteria
===================

Tool which can combine templated tests and exterrnal confiuration files on same
inrastructure as exist today.

----------
References
----------

https://blueprints.launchpad.net/fuel/+spec/template-based-testcases
