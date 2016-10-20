..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================
Tasks inheritance
=================

https://blueprints.launchpad.net/fuel/+spec/tasks-inheritance

Tasks inheritance allows us handle custom tasks configuration
without copy/paste task.


-------------------
Problem description
-------------------

When we have set of similar tasks a deployment engineer had to
copy/paste the origin task and make small changes of the original task.

When group of similar tasks should be changed a deployment engineer
have to make changes in each task.


----------------
Proposed changes
----------------

As solution it is proposed to introduce tasks inheritance.


Web UI
======

None


Nailgun
=======

We are adding 'inherited' field into task - the list of parent tasks.
Parents resolution made with the
`C3 superclass linearization<https://en.wikipedia.org/wiki/C3_linearization>`_
algorithm used as the `Methods Resolution Order
<https://www.python.org/download/releases/2.3/mro/>`_
in `Python<https://www.python.org/>`_.


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

Tasks can be refactored to using the inheritance feature.


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

The tasks hierarchy calculation does not make significan performance impact.


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

Inheritance tasks should be reflected in the Fuel documentation.


--------------
Implementation
--------------

Assignee(s)
===========


Primary assignee:
  Alexander Kislitsky <akislitsky@mirantis.com>


Mandatory design review:
  Vladimir Kuklin <vkuklin@mirantis.com>


Work Items
==========

* Implement inherited tasks processor.
* Include inherited tasks processor into tasks serialization.


Dependencies
============

None


-----------
Testing, QA
-----------

System and deployment tests should be passed as well as without
tasks inheritance.


Acceptance criteria
===================

1. We have tasks with inheritance in the upstream.
2. System and deployment tests are successfully passed.


----------
References
----------

None