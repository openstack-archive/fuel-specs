..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
VXLAN support for OVS-DPDK
==========================================

https://blueprints.launchpad.net/fuel/+spec/vxlan-support-for-ovs-dpdk

We want to utilize VXLAN based networking with OVS/DPDK for high performance
scale-able tenant networking.

--------------------
Problem description
--------------------

Currently we can use OVS-DPDK only with VLAN based network segmentation.
It would be good to have an opportunity of supporting VXLAN with OVS-DPDK.
It is very important for all NFV use cases.

----------------
Proposed changes
----------------

The proposal is to enable interface `br-prv` on `br-prv` bridge  and to use
this bridge for the tunneling instead of `br-mesh`.

Web UI
======

None

Nailgun
=======

We have to remove restrictions for using DPDK mode only with VLAN based
segmentation and have to use endpoint as in the VLAN case.

Data model
----------

When operator configures interface as DPDK to use it for Private network and
segmentation type is VXLAN, `astute.yaml` will be extended as following

* Endpoint for Private network should be `br-prv` instead of `br-mesh`::

    network_scheme:
      endpoint:
      - br-prv

REST API
--------

None

Orchestration
=============

None

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

We have to enable interface `br-prv` on `br-prv` bridge.

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

* Add possibility for using DPDK mode with VXLAN segmentation type
* Remove utilization of `br-mesh` bridge in case of tunneling segmentation
* Enable interface `br-prv` on `br-prv` bridge with appropriate ip and mask
* Test manually
* Create a system test for DPDK

Dependencies
============

None

------------
Testing, QA
------------

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
