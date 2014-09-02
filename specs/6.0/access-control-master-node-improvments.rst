..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Fuel master access control improvements
==========================================

https://blueprints.launchpad.net/fuel/+spec/access-control-master-node-improvments

In 5.1 release cycle fuel master node access control was introduced.
In next release some configuration tunning is required to make it easier
to use and upgrade.

Problem description
===================

With current implementation we have following problems:

* each request is validated by middleware using keystone admin token.
  This method is deprecated.

* if user changes his password it is not possible to run upgrade.

* Outdated tokens are not cleaned which in long term
  may lead to run out of space.

* no cookies support so some GET requests from UI can not be validated.

* after login password is stored in browser cache.

Proposed change
===============

* Create user with admin role which will be used
  to authenticate requests in middleware.

* Ask user for password before upgrade.

* Create cron script which deletes outdated tokens.

* Add support for cookies, which also will allow to test API from browser.

* Increase token expiration time to 24h, so it will not be necessary to
  store password in browser cache.


Alternatives
------------

None

Data model impact
-----------------

There will be new user in keystone database.

REST API impact
---------------

None

Upgrade impact
--------------

During the upgrade user will be asked to give a UI password.

Security impact
---------------

Using service user instead of admin_token to verify is safer.

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

When cookies support is added developer will be able to test API from browser.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
    skalinowski@mirantis.com
    loles@mirantis.com

Work Items
----------

Each item from "Proposed change" can be done separately.


Dependencies
============

None


Testing
=======

All tests from previous blueprint should still apply here.

Documentation Impact
====================

Documentation describing internal architecture should be created.

References
==========

None
