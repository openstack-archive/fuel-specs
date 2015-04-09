..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================
Admin network on bond
=====================

https://blueprints.launchpad.net/fuel/+spec/admin-network-on-bond

This blueprint describes a way to bond admin interface using non-lacp
bond modes.

Problem description
===================

In some cases user wants to bond admin interface. It is not possible
for FUEL 6.0 and earlier release using UI. It is possible to bond admin
interface via API and CLI, but in this case there is a problem with
determining admin interface mac address during the provisioning stage.
This is nailgun provisioning serializer issue. If admin interface was
bonded, serializer returns mac of the bond interface(empty value) and
it breaks provisioning process.

It is proposed to use only non-lacp bond modes for admin interface
due to complex and unclear implementation.

Proposed change
===============

Nailgun provisioning serializer should be fixed to handle case when
admin interface is bonded. Serializer may return first bonded slave
interface mac address instead bond mac address. Non-lacp modes should
be denied for admin interface via nailgun API(add validator rules).
Possibility to bond admin interface via UI should be added. Availiable
bond modes for admin interface in UI should be
limited(only non-lacp modes).

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

Additional validator rules should be added to prevent passing of
lacp bond mode for admin interface.

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

User will be abble to bond admin interface via UI, API and CLI
using non-lacp modes.

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

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Valyavskiy Viacheslav <slava-val-al>

Work Items
----------

* Fix provisioning serializer to proper handle case when admin interface is
  bonded
* Deny non-lacp modes for admin interface via nailgun API
* Add possibility to bond admin interface via UI
* Limit bond modes for admin interface via UI


Dependencies
============

None

Testing
=======

It is necessary to improve devops to support tests
with admin interface bonding.


Documentation Impact
====================

Extend Deployment Guide with following items:
* add new possible network topologies
* how to prepare an env for installation with bonded admin interface
* how to deploy OpenStack env with bonded admin interface


References
==========

- https://blueprints.launchpad.net/fuel/+spec/admin-network-on-bond
