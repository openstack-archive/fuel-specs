..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================
S3 API/Keystone Integration
===========================

Administrator should be able to decide whether the S3 API/Keystone integration
in Ceph RADOS Gateway is enabled or not through checkbox in Fuel.

Administrator should be informed about a trade-off that is associated with
enabling the integration.

--------------------
Problem description
--------------------

Ceph RADOS Gateway offers multiple backends for client authenication for both
OpenStack Open Storage v1 API (aka Swift API) and S3 API.

Unfortunately, request authentication in S3 API is very different in comparison
to its counterpart in OpenStack. Instead of providing tokens, a client
application always may access the object store with a frequently varying
zero-knowledge proof. This assures extra security guarantees but - conjuncted
with the principle that Keystone cannot reveal credentials it stores - also
increases load and latency as each S3 request will be reflected in request to
Keystone. This is an architectural limitation that cannot be addressed through
introduction of caching like in case of Swift API.

Thus, enabling the S3/Keystone integration in RadosGW is decision associated
with a fundamental trade-off and should be made after careful consideration.
However, administrator should be able to decide to turn on the integration
through graphical user interface.

----------------
Proposed changes
----------------

Enabling S3 API/Keystone integration requires changes in Ceph configuration
files:

On controller side:

* Put "rgw_s3_auth_use_keystone = True" into a section of /etc/ceph/ceph.conf
  dedicated to RadosGW.

Web UI
======

Interaction with the Web UI may be similar to the following scenario:

1. Administrator navigates to Storage section of Deployment Wizard or Settings
   tab.
2. Administrator is presented with an option "Enable S3 API Authentication via
   Keystone" (or other appropriate from existing ones) and hint - "Please note
   that enabling this will increase the load on Keystone service. Please
   consult with documentation (link) and Mirantis Support on mitigating the
   risks related with load."
3. If user checks the option from step 2 - S3 API on RadosGW is configured for
   authentication via Keystone

Nailgun
=======

Nailgun-agent
-------------

None

Bootstrap
---------

None

Data model
----------

::

  storage_ceph:
    gw_s3_auth_use_keystone: false

REST API
--------

None

Orchestration
=============

None

RPC Protocol
------------

Only payload changes

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

See items in Proposed changes section.

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

User will be able to authenticate requests made through S3 API basing solely
on credentials stored and handlded by Keystone.

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

Load on Keystone may be significantly increased. Latency of request to object
store made through S3 API will be increased.

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

TBD

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  xxx

Mandatory design review:
  yyy

Work Items
==========

* Enable S3 API/Keystone integration in fuel-library (already done)
* UI changes
* Manual testing

Dependencies
============

None

------------
Testing, QA
------------

* Automated API/CLI test cases for the configuring S3 authenication via
  Keystone.

Acceptance criteria
===================

* Administrator should be able to enable and disable the S3 API/Keystone in
  RadosGW through Web UI.

----------
References
----------

1. https://bugs.launchpad.net/mos/+bug/1540426

2. https://bugs.launchpad.net/fuel/+bug/1446704
