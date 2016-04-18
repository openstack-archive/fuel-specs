..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Fuel-qa: Make assertions more informative
=========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-qa-assertions-enhancement

This spec propouses changes in fuel-qa to enchance output of system_test.log
and xunit xml file by adding custom exception classes for different types of
errors.

--------------------
Problem description
--------------------

In current implementation of fuel-qa, assertion errors provide only small
messages about what exactly was checked. And nearly all failed builds require
an engineer to investigate the logs and code to answer what type of component
or API was responsible for the issue.

Major task is to identify 3 categories of errors:

- Infrastracture error - in case if wrong or defective envioronment was used
  for testing
- Product error - an error detected by test (assertions)
- Test error - a error in test code


----------------
Proposed changes
----------------

Add custom Exception classes for infrastracture and product errors

  * InfraError
  * ProdError

These classes should be used instead of assert statements.

All other errors should be considered as errors of test framework.

Information about class of Exception will be available in nosetest.xml for
automatic processing.

Also timeout errors should be replaced with ProdError.


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
  * Anton Studenov (astudenov): astudenov@mirantis.com

Other contributors:
  * Dennis Dmitriev (ddmitriev): ddmitriev@mirantis.com
  * Dmitry Tyzhnenko (dtyzhnenko): dtyzhnenko@mirantis.com
  * Kirill Rozin (krozin): krozin@mirantis.com

Mandatory design review:
  None


Work Items
==========

- Investigate the existing code
- Make the changes in fuel-qa


Dependencies
============

None


------------
Testing, QA
------------

None


Acceptance criteria
===================

- All assert methods in fuel-qa are replaced by custom Exception classes
- TimeoutError replaced by ProdError

----------
References
----------

None


