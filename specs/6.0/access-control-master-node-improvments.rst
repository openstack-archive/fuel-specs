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

* each request is validated using keystone admin token.
  This method is depracted

* there is no system user so it's hard to run queries from scripts
  i.e during upgrade

* Outdated tokens are not cleaned which in long term
  may lead to run out of space

* all requests are using HTTP protocol and are not protected
  so all passwords and tokens are sent in plain text

* no cookies support so some GET requests from UI can not be validated

Proposed change
===============

* Create user with admin role which will be used
  to authenticate requests and during upgrade.

* Create cron script which deletes outdated tokens

* Use HTTPS to connect to master node(this may require new blueprint)

* Add support for cookies, which also will allow to test API from browser


Alternatives
------------

None

Data model impact
-----------------

There will be new user in keystone database.

REST API impact
---------------

All API requests will be encrypted using HTTPS.

Upgrade impact
--------------

System user should be created during master node upgrade.

Security impact
---------------

Using HTTPS and not using admin token will increase master node security.

Notifications impact
--------------------

None

Other end user impact
---------------------

If we use self signed certificates for SSL user will get warning
on the browser.

Performance Impact
------------------

HTTPS may add some latency but it shouldn't be a problem.

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

HTTPS change should be described


References
==========

None
