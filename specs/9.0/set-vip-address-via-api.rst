..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================================
Allow VIP to be manually set to ANY valid IP address via API
============================================================

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
address. Data model is changed also so that VIP address and namespace are saved
into DB. Also, there is a new flag in ip_addrs table that determines whether to
allocate IP for that VIP automatically or not. Address allocation methods for
VIPs should be changed to skip allocation of IP for VIP if user configured it
with manually set IP. Validation should be added before deployment that all
VIPs have IPs either assigned automatically or by user.

VIPs will be checked and re-allocated in ip_addrs table at these points:

#. create cluster

#. modify networks configuration

#. modify one network

#. modify network template

#. change nodes set for cluster

#. change node roles set on nodes

#. modify cluster attributes (change set of plugins)

#. modify release

#. deployment start (final check)

VIPs allocation procedure should not overwrite information in DB
(IP, namespace) if it was set by user already.

Data model
----------

ip_addrs table:

- rename `vip_type` to `vip_name`,
- add `is_user_defined` field,
- add `vip_namespace` field.

`vip_type` is actually a VIP name since 7.0 release.
`is_user_defined` is a new boolean field, False by default. It determines
whether IP is allocated automatically (False) or it is set by user (True).
`vip_namespace` now presents in VIP description (inside network roles) and we
need to have it changeable as VIPs with manually set IPs can be the external
resources (external LB) which should not be set up with manifests.

REST API
--------

Setting of IP addresses for VIPs will be allowed via urls:
`/clusters/<cluster_id>/network_configuration/ips/vips/`,
`/clusters/<cluster_id>/network_configuration/ips/<ip_id>/vips/`.

`/ips/` is introduced here as root qualifier because it can be used later not
for VIPs only, i.e. for nodes addresses and other reserved IPs.
There will be GET and PUT(PATCH) requests for both single object and
collection.

Only `ip_addr`, `vip_namespace` and `is_user_defined` fields can be changed via
API. It should be possible to pass full output of GET request to the input of
PUT request (as for other handlers). Check for read-only fields should be done
in API validator.

The following fields of `ip_addrs` table should be serialized:

.. code-block:: python

    fields = (
        "id",
        "network",
        "node",
        "ip_addr",
        "vip_name",
        "vip_namespace",
        "is_user_defined"
    )

Example of serialized data (yaml):

.. code-block:: yaml

  ---
  - id: 5
    network: 3
    node: null
    ip_addr: 192.169.1.33
    vip_name: public
    vip_namespace: haproxy
    is_user_defined: false

`node` is always null for VIP.

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

    fuel vip --env 1 --ip 1 --download

#. Set VIP parameters by its id.

    fuel vip --env 1 --ip 1 --upload ip_address.yaml

    TBD, do we need this separate request. Seems, Id from yaml should be
    ignored here.

#. Get all VIPs for environment, optional filter by network/network role.

    fuel vip --env 1 --download

    fuel vip --env 1 --download --network 1

    fuel vip --env 1 --download --network-role "public/vip"

#. Set VIPs parameters by their ids (within one environment).

    fuel vip --env 1 --upload ip_address.yaml

    Arbitrary number of existing VIPs for given environment can be changed via
    this command.

ip_address.yaml is the default file name where VIP (IPAddress) information is
stored.

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
