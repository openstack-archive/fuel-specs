..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
VXLAN support for OVS-DPDK
==========================

https://blueprints.launchpad.net/fuel/+spec/vxlan-support-for-ovs-dpdk

We want to utilize VXLAN based networking with OVS/DPDK for high performance
scale-able tenant networking.

-------------------
Problem description
-------------------

Currently we can use OVS-DPDK only with VLAN based network segmentation.
It would be good to have an opportunity of supporting VXLAN with OVS-DPDK.
It is very important for all NFV use cases.

----------------
Proposed changes
----------------

Since the physical interface in DPDK case doesn't support VXLAN segmentation
we need to bring the internal interface `br-prv` on `br-prv` bridge to the UP
state and assign local IP.

Web UI
======

None

Nailgun
=======

We should remove restrictions for using DPDK mode only with VLAN based
segmentation. Also we need to use the same transformations as we use for
configure DPDK in the VLAN case.

Data model
----------

As in case of using VLAN based segmentation.

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

We should bring the internal interface `br-prv` on `br-prv` bridge to the UP
state and assign local IP.

.. code-block:: bash

    ifconfig br-prv <IP/MASK> up

------------
Alternatives
------------

Continue to use VLAN base network segmentation.

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

None

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

Work Items
==========

* Remove restrictions for using DPDK mode only with VLAN based segmentation
* Change network serializer to node using `br-mesh` in case of DPDK
  configuration
* Modify fuel-library to enable interface `br-prv` on `br-prv` bridge with
  appropriate ip and mask
* Test manually
* Create a system test for DPDK

Dependencies
============

None

-----------
Testing, QA
-----------

* Test API/CLI cases for the configuring DPDK with VXLAN segmentation
* Test WEB UI cases for the configuring DPDK with VXLAN segmentation
* Test that DPDK with VXLAN segmentation is discovered and configured properly

Acceptance criteria
===================

* Ability to run a DPDK application on top of OVS/DPDK + VXLAN enabled host
* Achieve 80% of wire speed
* Working on 40 gig and 2x10 cards from Intel's forteville family

----------
References
----------

None
