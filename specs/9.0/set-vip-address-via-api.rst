..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Support for multi-rack deployment with static routes
====================================================

https://blueprints.launchpad.net/fuel/+spec/allow-any-vip

API must allow VIP to be manually set to ANY valid IP address.

--------------------
Problem description
--------------------

There are cases when it is required to set exact IP addresses for VIPs.
Fuel API does not support that for now. It is required to add an ability of
setting arbitrary IP address for VIP via API.
This will allow the user to override if the automatic allocation doesn't match
their needs or in the case that they want to use external LB.
See https://bugs.launchpad.net/fuel/+bug/1482399


----------------
Proposed changes
----------------

API must allow VIP to be manually set to any valid IP address.

User-defined VIP addresses may match some networks known by Fuel or do not
match any known networks. Anyway, VIP address provided is saved into DB as
occupied. So, it cannot be used for other purposes.

Changes are proposed for API and CLI only. Spec for UI changes should be
created separately if such changes will be required.

Web UI
======

None

Nailgun
=======

API will be extended to provide an ability to set VIP to almost any valid IP
address. Data model is changed also so that VIP description is saved into DB
and this description contains flag that determines whether to allocate IP for
that VIP automatically or not. Address allocation methods for VIPs should be
changed to skip allocation of IP for VIP if user configured it with manually
set IP. Validation should be added before deployment that all VIPs have IPs
either assigned automatically or by user.

Data model
----------

ip_addrs table: replace vip_type (it contains VIP name now) with the following
vip_info structure:

.. code-block:: json

vip_info = {
    name,
    namespace,
    alias,
    node_roles,
    vendor_specific,
    network_role,
    manual
}

First five fields of vip_info structure are defined in VIP metadata in network
role. So, it is required to copy all fields from VIP metadata and add
`network_role` and `manual` fields. `network_role` is taken as root of current
VIP. `manual` is a new boolean field, False by default. It determines whether
to allocate IP automatically (False) or it is set by user (True). vip_info is
saved into DB when VIPs are allocated initially. After that user can read this
info via API, change IP address and `manual` flag.

REST API
--------

Setting of IP addresses for VIPs will be allowed via urls:
`/clusters/<cluster_id>/network_configuration/ips/vips/`,
`/clusters/<cluster_id>/network_configuration/ips/<ip_id>/vips/`.

`/ips/` is introduced here as root qualifier because it can be used later not
for VIPs only, i.e. for nodes addresses and other reserved IPs.
There will be GET and PUT requests for both single object and collection.
Only ip_addr and vip_info.manual fields can be changed via API.

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

Fuel CLI should support operations with VIPs:
#. Get VIP by its id.
#. Set VIP parameters by its id.
#. List VIP for environment, filter by network/network role.
#. Set VIPs parameters by their ids (within one environment).

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

N/A

--------------
Upgrade impact
--------------

N/A

---------------
Security impact
---------------

N/A

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

TBD

------------------
Performance impact
------------------

N/A

-----------------
Deployment impact
-----------------

TBD

----------------
Developer impact
----------------

None

--------------------------------
Infrastructure impact
--------------------------------

TBD

--------------------
Documentation impact
--------------------

TBD

--------------------
Expected OSCI impact
--------------------

N/A

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee: Aleksey Shtokolov

Other contributors: Aleksey Kasatkin, Ilya Kutukov, Ivan Kliuk

Mandatory design review: Alex Didenko, Igor Kalnitsky


Work Items
==========

- Add new vip_info into ip_addrs table
- Extend Nailgun REST API
- Use `manual` flag to disable IP auto-allocation.
- Validate VIPs before deployment.
- Add VIP-related commands to CLI.


Dependencies
============

N/A

------------
Testing, QA
------------

In order to verify the quality of new features, automatic system tests will be
expanded by the cases listed below:

1. Part of IPs for VIPs are set manually inside env networks.

2. IP for VIP is set manually outside env networks.

Acceptance criteria
===================

It should be allowed to set user-defined IP for any VIP. This IP can even be
out of any environment's networks.

----------
References
----------

https://blueprints.launchpad.net/fuel/+spec/allow-any-vip
