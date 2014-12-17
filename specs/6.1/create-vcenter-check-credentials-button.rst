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
Now users can start deployment with wrong vCenter settings , and deployment has
successfully completed. However, the user will receive non-working openstack.
It would be right to give the user the opportunity to check vCenter settings
before starting deployment.

Proposed change
===============

Alternatives
------------

Data model impact
-----------------

REST API impact
---------------

Upgrade impact
--------------

Security impact
---------------

Notifications impact
--------------------

Other end user impact
---------------------

Performance Impact
------------------

Other deployer impact
---------------------

Developer impact
----------------

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

Dependencies
============


Testing
=======


Documentation Impact
====================

The documentation should describe how to use this button.

References
==========
