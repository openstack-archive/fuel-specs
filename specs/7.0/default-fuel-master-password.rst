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

* Notification will be emitted periodically until the default
  password changes.

  * Listener will wait for authentication event from keystone [1]

  * Handler will try to authenticate with default admin/admin credentials.
    If authentication would succeed, the notification will be send.

Alternatives
------------

1. We could set a cron job instead of listening to keystone events.

2. We could force End User to change password at some stage of Fuel Master
   deployment. But it brings up other issues:

   * compatibility with custom deploy scripts would break because of fuel
     asking for password change

   * How to resolve this in non-intrusive way in case of WebUI?

   * How to resolve this in non-intrusive way in case of CLI?

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

oslo.messaging will be added as nailgun requirement

Security impact
---------------

The feature is intended to improve End User's security in matter of
unauthorized access to the cloud

Notifications impact
--------------------

There will be new "general" (not assigned to specific cluster) notification
about password change

Other end user impact
---------------------

None

Performance Impact
------------------

Fuel will check whether End User uses default password on each login or not.
That involves another request to keystone.

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

Nonea

Infrastructure impact
---------------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  sbrzeczkowski

Work Items
----------

* set up listener for keystone authentication events

* set up handler which will run on listener's command and will check
  whether default password has been changed.

Dependencies
============

oslo.messaging will be added as nailgun requirement

Testing
=======

Integration tests will be needed to test entire story, from login action to
notification.

Acceptance criteria
-------------------

User, who didn't change default password should be notified about it in WebUI.

Documentation Impact
====================

None

References
==========

[1] http://docs.openstack.org/developer/keystone/event_notifications.html#example-notification-authentication
