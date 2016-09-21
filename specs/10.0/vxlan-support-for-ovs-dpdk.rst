..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
VXLAN support for OVS-DPDK
==========================

https://blueprints.launchpad.net/fuel/+spec/vxlan-support-for-ovs-dpdk

We want to utilize VXLAN based networking with OVS/DPDK for high performance
scalable tenant networking.

-------------------
Problem description
-------------------

Currently OVS-DPDK supports only VLAN segmentation. With VxLAN based network
segmentation being adopted more widely, supporting VXLAN with OVS-DPDK is very
important for all NFV use cases.

----------------
Proposed changes
----------------

Currently in case of using VLAN based networking with OVS-DPDK we use `br-prv`
bridge but we don't assign IP on it. In case of VXLAN based segmentation with
DPDK we should use the bridge is named `br-mesh` that has configuration such as
`br-prv` bridge in case of VLAN with DPDK, but additionally we should assign
local IP on this bridge.

Web UI
======

None

Nailgun
=======

We should remove restrictions for using DPDK in VXLAN based segmentation case.
Also we should use the same transformations as we use for configure DPDK in
the VLAN case [0]. Also we should rename `br-prv` bridge to `br-mesh` and
assign the local IP on it.

Data model
----------

None

REST API
--------

None

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

Continue to use VLAN based network segmentation.

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

Performance penalties are not expected.

-----------------
Deployment impact
-----------------

This feature will require to use VXLAN segmentation and dedicated DPDK capable
network interface for Private network.

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

This feature will be tested on virtual environment.

--------------------
Documentation impact
--------------------

The user guide should be updated according to the described feature.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Anastasia Balobashina <atolochkova@mirantis.com>
Mandatory design review:
  Aleksey Kasatkin <akasatkin@mirantis.com>
  Sergey Matov <smatov@mirantis.com>

Work Items
==========

* Remove restrictions for using DPDK in VXLAN based segmentation case
* Fix network serializer so that we use the bridge is named `br-mesh` that has
  configuration such as `br-prv` bridge in case of VLAN with OVS-DPDK, but
  additionally we should assign local IP on this bridge
* Test manually
* Create a system test for DPDK
* Verify acceptance criterias

Dependencies
============

None

-----------
Testing, QA
-----------

* Test API/CLI cases for the configuring DPDK with VXLAN segmentation
* Test WEB UI cases for the configuring DPDK with VXLAN segmentation
* Test that DPDK with VXLAN segmentation is discovered and configured properly
* Test for case of using multiple node network groups

Acceptance criteria
===================

* Ability to run a DPDK application on top of OVS/DPDK + VXLAN enabled host
* 3 Mpps packet rate on 64bytes UDP traffic on single PMD thread per count of
  DPDK core(s)
* Working on 40 gig and 2x10 cards from Intel's forteville family

----------
References
----------

[0] - https://github.com/openstack/fuel-specs/blob/master/specs/9.0/support-dpdk.rst#data-model
