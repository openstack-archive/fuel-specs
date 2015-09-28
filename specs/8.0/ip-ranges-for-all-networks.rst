..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================================
Support IP ranges management for all networks
=============================================

https://blueprints.launchpad.net/fuel/+spec/ip-ranges-for-all-networks

Extend Fuel UI with an ability to specify IP ranges for all networks, to use
the ranges with some omitted addresses which are reserved or already in use.

--------------------
Problem description
--------------------

When deploying an environment using Fuel it is often necessary to be able to
specify IPs to be excluded from Fuel's auto-provisioning so that
the deployment does not fail due to an IP already being assigned to or
reserved for another resource. But in current Fuel UI not all networks allow
to do this (storage and management does not).

----------------
Proposed changes
----------------

Web UI
======

All networks on Networks tab should have the same algorithm to set network
addresses, based on network notation ('ip_ranges' or 'cidr'), which is stored
in network metadata):

* specifying custom IP range(s) and gateway: in this case CIDR field
  is used for IP range(s) and gateway validation only (this mode corresponds
  to 'ip_ranges' notation).

  .. image:: ../../images/8.0/ip-ranges-for-all-networks/custom-ip-ranges.png
     :scale: 75 %

* specifying CIDR value: in this case network default IP range and gateway are
  set automatically according to the CIDR value and can not be configured by
  user (this mode corresponds to 'cidr' notation).

  .. image:: ../../images/8.0/ip-ranges-for-all-networks/fit-to-cidr.png
     :scale: 75 %

When switching between these two modes, Fuel UI set an appropriate notation
in network metadata.

To determine whether to specify network gateway or not, Fuel UI continues
to observe `use_gateway` flag from network metadata.

No changes required in network validation logic (IP range(s) should match
specified CIDR, gateway should not be included in IP range(s), IP range(s)
should not intersect each other, etc.).

Network base (first) and broadcast (last) addresses are not used, when
calculating default IP range and gateway from CIDR.

UI controls for a network should go in the following order:

* CIDR
* IP ranges
* Gateway (`use_gateway` flag is `True` for the network)
* VLAN tagging


Nailgun
=======

No changes required.


Data model
----------

No changes required.


REST API
--------

No changes required.


Orchestration
=============

No changes required.


RPC Protocol
------------

None


Fuel Client
===========

No changes required.


Plugins
=======

None


Fuel Library
============

No changes required.


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


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

User guide should be updated according to the changes.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  ashtokolov (ashtokolov@mirantis.com)

Other contributors:
  jkirnosova (jkirnosova@mirantis.com) - Fuel UI changes
  bdudko (bdudko@mirantis.com) - Fuel UI visual design

Mandatory design review:
  alekseyk-ru (akasatkin@mirantis.com)
  vkramskikh (vkramskikh@mirantis.com)


Work Items
==========

* Support specyfying custom IP ranges and gateway for all networks
* Support specifying network ranges by CIDR with autoupdating of corresponding
  default IP range and gateway


Dependencies
============

None

------------
Testing, QA
------------

* Manual testing
* UI functional tests should cover Fuel UI changes


Acceptance criteria
===================

* It should be possible to specify custom IP range(s) and gateway for all
  networks
* It should be possible to specify network addresses by CIDR
* When specifying network by CIDR, default IP range and gateway should be
  autoupdated


----------
References
----------
 None
