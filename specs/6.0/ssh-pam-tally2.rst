..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
Protect SSH from brute forcing
==============================

https://blueprints.launchpad.net/fuel/+spec/ssh-pam-tally2

Problem description
===================

There is no locking policy configured for SSH Failed Login Attempts
in Fuel for Openstack environments and that is a major security issue.

Proposed change
===============

Pam_tally2 module should be used to lock user accounts after certain number
of failed ssh login attempts made to the system, and unlock it later as well.

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

Improves system security by lowering brute forcing risks.

Notifications impact
--------------------

None

Other end user impact
---------------------

Locking and unlocking policy could cause some SSH login outages for nodes.

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

None

Assignee(s)
-----------

Primary assignee:
  mmaxur

Other contributors:
  None

Work Items
----------

* Add pam puppet module
* Adapt it for Fuel as well

Dependencies
============

None

Testing
=======

Manual testing scenario for some given node:

* Issue ``pam_tally2 --user=tecmint`` in order to verify there is no locking
(parse its output for ``tecmint``, it should be ``0``):
Login           Failures   Latest   failure     From
tecmint            0

* Fail SSH logins for root by specifying wrong creds by 3 times

* Verify if locking was issued - you shouldn't be able to login by SSH
using correct creds for root within 5 min time range

* After 5 min timeout passed, verify there is no locking anymore:
Use ``pam_tally2 --user=tecmint`` and parse its output for ``tecmint``,
it should be ``0``.

Documentation Impact
====================

Locking policy should be explained in docs as well.
We configure it as
``file=/var/log/tallylog deny=3 even_deny_root unlock_time=300``
Which is

* ``file=/var/log/tallylog`` – Default log file is used to keep login counts.
* ``deny=3`` – Deny access after 3 attempts and lock down user.
* ``even_deny_root`` – Policy is also apply to root user.
* ``unlock_time=300`` – Account will be locked till 5 Min.

References
==========

None
