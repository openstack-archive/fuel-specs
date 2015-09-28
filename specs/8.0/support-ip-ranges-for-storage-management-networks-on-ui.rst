..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================================
Support IP ranges management for all networks
=============================================

https://blueprints.launchpad.net/fuel/+spec/ip-ranges-for-all-networks

It's often needed to specify IP ranges for networks to use them with some
omitted addresses which are reserved or already in use.

--------------------
Problem description
--------------------

When deploying an environment using Fuel it is often necessary to be able to
specify IPs to be excluded from Fuel's auto-provisioning so that the deployment
does not fail due to an IP already being assigned to or reserved for another
resource but in current Fuel UI not all networks allow to do this (storage and
management does not).

With introducing this ability users could omit the IPs that are in use by
setting the range to begin after or end before these IPs - in addition,
multiple IP ranges can be specified, so for users who have an IP in use in the
middle of their range, they can split the range to exclude the IP in use.

----------------
Proposed changes
----------------

Web UI
======

All networks on Networs tab in Fuel UI does not handle network 'notation' meta
data any more and should have the same algorithm to set network address
ranges:

* (default) specifying CIDR value: in this case network IP range gateway are
  set automatically according to the CIDR value and can not be configured by
  user.

* specifying custom IP ranges and gateway: in this case CIDR field is used for
  IP ranges and gateway validation only.

No changes in network validation logic (IP ranges should match specified CIDR,
gateway should not be included in specified IP range(s), IP ranges should not
intersect each other).

[TBD] Are there any changes for Floating IP ranges setting?

Proposed mockups for Fuel UI:

[TODO]

Nailgun
=======

[TODO]


Data model
----------

[TODO]


REST API
--------

[TODO]


Orchestration
=============

[TBD]


RPC Protocol
------------

None


Fuel Client
===========

[TBD]


Plugins
=======

None


Fuel Library
============

[TBD]


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

None


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

None


-----------------
Deployment impact
-----------------

None


----------------
Developer impact
----------------

None


--------------------------------
Infrastructure/operations impact
--------------------------------

None


--------------------
Documentation impact
--------------------

User guide should be updated according to the changes.


--------------------
Expected OSCI impact
--------------------

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  ashtokolov (ashtokolov@mirantis.com)

Other contributors:
  ikliuk (ikliuk@mirantis.com) - Nailgun changes
  jkirnosova (jkirnosova@mirantis.com) - Fuel UI changes
  bdudko (bdudko@mirantis.com) - Fuel UI visual design

Mandatory design review:
  alekseyk-ru (akasatkin@mirantis.com)
  vkramskikh (vkramskikh@mirantis.com)

QA engineer:
  [TBD]


Work Items
==========

[TODO: Nailgun items]

* Support specifying network ranges by CIDR with auto update of corresponding
  default IP range and default gateway
* Support specyfying custom IP ranges and gateway for a network


Dependencies
============

None

------------
Testing, QA
------------

[TODO: Nailgun items]

* Manual testing
* UI functional tests should cover Fuel UI changes
* UI unit tests


Acceptance criteria
===================

* It should be possible to specify network ranges by CIDR
* When specifying network by CIDR, default IP range and gateway shoule be
  auto-calculated
* It should be possible to specify custom IP ranges and gateway for any
  network


----------
References
----------
 None
