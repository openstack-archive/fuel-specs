..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Refactoring of FuelWebClient in System Tests
============================================

The FuelWebClient model is very huge and contains more then 2.5K LOC. It's very
difficult to analize and improve methods of. Furthermore, the model combines
test methods and methods related to api manipulation.

--------------------
Problem description
--------------------

Common problem when we use actual implementation of FuelWebClient model:

* Engineers waist a lot of time to find necessary method.

* A lot of misunderstanding where we should put new method that assert
  something. In the model or the test class.

* Very difficult to make decomposition of the model because it contais a lot of
  method not related to work with API.


----------------
Proposed changes
----------------

We should move all method not related to API into separate classes and use it as
mixins in test case class.

* All methods with assertion should move to separete classes.

* Wrappers and waiters need move from the model and use them independent in test
  case.

Web UI
======

n/a


Nailgun
=======

No changes in Nailgun

Data model
----------

n/a


REST API
--------

n/a


Orchestration
=============

No changes in Orchestration


RPC Protocol
------------

n/a


Fuel Client
===========

n/a


Plugins
=======

n/a


Fuel Library
============

n/a

------------
Alternatives
------------

What are other ways of achieving the same results? Why aren't they followed?
This doesn't have to be a full literature review, but it should demonstrate
that thought has been put into why the proposed solution is an appropriate one.


--------------
Upgrade impact
--------------

n/a


---------------
Security impact
---------------

n/a


--------------------
Notifications impact
--------------------

n/a


---------------
End user impact
---------------

n/a


------------------
Performance impact
------------------

n/a


-----------------
Deployment impact
-----------------

n/a


----------------
Developer impact
----------------

n/a


---------------------
Infrastructure impact
---------------------

n/a


--------------------
Documentation impact
--------------------

n/a


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  dtyzhnenko

Other contributors:
  None

Mandatory design review:
  apanchenko-8, asledzinskiy, aurlapova, ddmitriev, tatyana-leontovich


Work Items
==========

* create several classes with methods that grouped by services for using it to
  assesrt some result

* waiters and result of task should be independent and controlled in test case

* assertion should described only in test case

Dependencies
============

n/a


------------
Testing, QA
------------

Changes covered by already existing test cases in system tests.

Acceptance criteria
===================

* The model contains the methods only needs for interaction with API.

* The methods related to test cases placed only in test classes.

* The test cases in system test work as usual.


----------
References
----------

https://blueprints.launchpad.net/fuel/+spec/fuelwebclient-refactoring
