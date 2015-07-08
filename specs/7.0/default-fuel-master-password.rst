..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Default Fuel Master password
===============================

https://blueprints.launchpad.net/fuel/+spec/default-fuel-master-password

Decrease possibility to access the cloud using default credentials

Problem description
===================

We use default credentials for Fuel Master which are **admin/admin**.
The vulnerability can be exploited to get access to the cloud by the intruder.

Proposed change
===============

* We will leave default credentials (admin/admin) to save custom scripts
  compatibility which is relying on this. End User will be notified about
  the risk it brings and be advised to change the password.

* User will be notified periodically until the default
  password changes:

  * Password will be checked on every login. If it equals to "admin",
    warning box will be shown on WebUI.

* User will be ask (not forced) to change default password in Fuel Menu

  * **Fuel User** screen will be the first screen user will see after
    Fuel Menu opened and also it's position in left menu will be changed to 1.

  * There will be non-intrusive warning (above password input fields)
    suggesting to change the password.

Alternatives
------------

1. We could listen to keystone events to catch "authorization" event, but:

   * it requires to spawn another daemon which would listen to the events,
     and it's too complex solution for such simple feature.

2. We could force End User to change password at some stage of Fuel Master
   deployment.

   * it is very secure but we do not want to force user to do anything so we
     give a choice whether to change it or not.


3. We could generate random password instead of "admin", but:

   * How to provide the password to End User in secure way?

   * How to save compatibility with existing scripts?


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

The feature is intended to improve End User's security in matter of
unauthorized access to the cloud

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Infrastructure impact
---------------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <sbrzeczkowski@mirantis.com>

Work Items
----------

* add password checker to login view in WebUI
* add new warning box
* add waring in Fuel User screen (in Fuel Menu) and change it's position
  in left menu to 1.

Dependencies
============

None

Testing
=======

* check if warning box is visible after logging in using password 'admin'
* add default password checking to ostf tests in Health Check

Acceptance criteria
-------------------

* warning box should be shown after logging in using 'admin' password

Documentation Impact
====================

None

References
==========

None
