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


----------------
Proposed changes
----------------

Add custom Exception classes for each type of possible error that can be
identified by fuel-qa code.

Examples:

  * FuelMasterSetupFailed
  * NodeProvisioningFailed
  * OSTFTestFailed
  * etc

also use full path to the Exception in the code:
fuel_qa.errors.FuelMasterSetupFailed

These changes helps to separate product error from framework errors because
all errors that are not defined in fuel_qa are errors of the framework code.



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

- Investigate the existing code to find list of errors which can be identified
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

- TBD


----------
References
----------

None


