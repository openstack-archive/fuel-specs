..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================================
Check connectivity and credentials button for vCenter in UI
===========================================================

https://blueprints.launchpad.net/fuel/+spec/create-vcenter-check-credentials-button

User must be able to check vCenter settings before starting deployment.

Problem description
===================

Now users can start deployment with wrong vCenter settings, and deployment is
completed successfully However, as the result the user will receive non-working
OpenStack. It would be right to give the user the opportunity to check vCenter
settings before starting deployment.

Proposed change
===============

Create UI button
Create Nailgun functions
Create Astute functions

Alternatives
------------

if not, prior to deployment, user will not be able to make sure the settings
for vCenter are correct and will have to check vCenter settings manually.

Data model impact
-----------------

None

REST API impact
---------------

It is need to create new handler like for "Verify Networks" button.

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

Now users can check their vCenter credentials.

Performance Impact
------------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  srogov (Stepan Rogov)

Other contributors:
  None

Work Items
----------

* Writing UI enhancements.
* Writing Nailgun enhancements.
* Writing Atuste enhancements.
* Implements cred checks.
* Testing.

Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/create-vcenter-check-credentials-button

Testing
=======


Documentation Impact
====================

The documentation should describe how to use this button.

References
==========

https://blueprints.launchpad.net/fuel/+spec/create-vcenter-check-credentials-button
