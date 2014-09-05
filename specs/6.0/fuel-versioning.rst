..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================================
Versioning and backward compatibility in Fuel
=============================================

https://blueprints.launchpad.net/fuel/+spec/nailgun-versioning


Problem description
===================

One of the first and foremost issues is supporting environments deployed with
a previous Fuel version. Also we need to support deployment with some older
releases, e.g. user may prefer Havana over Juno.

Besides, versioning plays an important part in pluggable architecture.


Proposed change
===============

There are two known entry/exit points in Nailgun which need to use versioning:

* REST API

* RPC Serializers

If user updates old Fuel version to a new one, he already has both old and new
releases in DB, and he can use any of them for deploying an environment.

UI and CLI will support only current version of API, but backend will have
backward compatibility code which will convert new data into old format
before storing it in database and/or sending it to Astute.

Also, we need to decide how many versions back we should support.

Alternatives
------------

We can implement REST API versioning as it's done in OpenStack, this means
using versioning prefixes like '/v1/', '/v2/' and so on. This will require
a lot of complex changes in UI code instead of backend (where we can just call
the old version). But our UI is rather heavy already, so more complexity will
only make situation worse.

Data model impact
-----------------

One of the biggest issues here is advanced networking, which implies lots of
structural changes both in code and DB models structure. There are two
possible solutions:

  * Keep some default models and relations as they are and implement
    translating from new API/data format to an old one (in RPC serializers
    or as a 'pre-save hook')
  * Rewrite network-related DB structure to JSON format, allowing to store
    different JSON versions in the same PostgreSQL table. This gives us
    better flexibility, but needs more research and also requires rewriting
    all current code to follow this approach


REST API impact
---------------

In 6.0 some additional handlers will be added and there will be some changes
in data format, but no API version change is really required. Disadvantage is,
some deployment engineers may use tools which rely on old API format. We can
solve this by improving our CLI and fuel-client documentation, promoting
them as a stable tools covering most possible cases.

Upgrade impact
--------------

Versioning feature is strongly entangled with upgrades. The main point is that
we continue supporting old environments after upgrade is completed.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

After upgrade most of configurable options for old environments will become
locked. The only action available will be adding and removing nodes from
existing environment deployed with one of the previous versions of Fuel.

Performance Impact
------------------

Some actions on old environments may become a little slower due to additional
translating logic.

Other deployer impact
---------------------

None

Developer impact
----------------

Each new feature implemented in next Fuel release should be tested that it
doesn't break backward compatibility.

Implementation
==============

Assignee(s)
-----------

nmarkov@mirantis.com, eli@mirantis.com

Work Items
----------

Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/nailgun-versioning-api
https://blueprints.launchpad.net/fuel/+spec/nailgun-versioning-rpc


Testing
=======

Tests should be run on all supported Fuel versions to ensure we didn't break
support for old environments.


Documentation Impact
====================

Each change that isn't supported in previous release should be mentioned in
documentation as well as in release notes.

References
==========

None
