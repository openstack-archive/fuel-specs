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
  This method is deprecated

* there is no system user so it's hard to run queries from scripts
  i.e during upgrade

* Outdated tokens are not cleaned which in long term
  may lead to run out of space

* no cookies support so some GET requests from UI can not be validated

Proposed change
===============

* Create user with admin role which will be used
  to authenticate requests and during upgrade.

* Create cron script which deletes outdated tokens

* Add support for cookies, which also will allow to test API from browser


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

System user should be created during master node upgrade.

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
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>

Work Items
----------

TBD


Dependencies
============

None


Testing
=======

TBD



Documentation Impact
====================

All changes are internal, for end user nothing changes.

References
==========

None
