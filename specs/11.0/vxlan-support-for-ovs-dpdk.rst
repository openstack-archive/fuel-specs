..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
VXLAN support for OVS-DPDK
==========================

https://blueprints.launchpad.net/fuel/+spec/vxlan-support-for-ovs-dpdk

We want to utilize a VXLAN-based networking with OVS/DPDK for a
high-performance scalable tenant networking.

-------------------
Problem description
-------------------

Currently, OVS-DPDK supports only VLAN segmentation. With VXLAN-based network
segmentation being adopted more widely, supporting VXLAN with OVS-DPDK is very
important for all NFV use cases.

----------------
Proposed changes
----------------

Currently, when using the VLAN-based networking with OVS-DPDK, we use the
`br-prv` bridge but we do not assign an IP to it.

To implement a VXLAN-based segmentation with DPDK, we should use a
`br-mesh` bridge whose configuration corresponds to the one of the `br-prv`
bridge in case of VLAN with DPDK.

Web UI
======

None

Nailgun
=======

The following changes are required in Nailgun:

* Remove restrictions for using DPDK in VXLAN-based segmentation case.
* Fix the Nailgun network serializer to generate transformations as
  described in the :ref:`Data model <data-model>` section.

.. _data-model:

Data model
----------

When operator enables DPDK for a particular interface with VXLAN-based
segmentation to use it for the Private network, ``astute.yaml`` will be
extended as follows:

* The network ``transformations`` field should include a vendor-specific
  attribute ``datapath_type: netdev`` for the `br-mesh` bridge::

    network_scheme:
      transformations:
      - action: add-br
        name: br-mesh
        provider: ovs
        vendor_specific:
          vlan_id: netgroup['vlan']
          datapath_type: netdev

* An interface should be added directly into the OVS `br-mesh` bridge using
  the ``add-port`` action with ``provider: dpdkovs``::

    network_scheme:
      transformations:
      - action: add-port
        name: enp1s0f0
        bridge: br-mesh
        provider: dpdkovs

  **No VLAN tag can be used here.**

* A bond should be added directly into the OVS `br-mesh` bridge using the
  ``add-bond`` action with ``provider: dpdkovs``::

    network_scheme:
      transformations:
      - action: add-bond
        bridge: br-mesh
        provider: dpdkovs
        bond_properties:
          mode: balance-rr
        interfaces:
        - enp1s0f0
        - enp1s0f1
        name: bond0

  **No VLAN tag can be used here.**


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

To achieve VLAN-tagged VXLAN, the vendor specific attribute ``vlan_id``
for ``add-br`` should be converted to
``ovs-vsctl set port br-mesh tag=<vlan_id>``.

------------
Alternatives
------------

Continue using the VLAN-based network segmentation.

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

Performance impact is not expected.

-----------------
Deployment impact
-----------------

This feature requires using the VXLAN segmentation and a dedicated
DPDK-capable network interface for the Private network.

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

* The feature will be tested on a virtual environment.
* The performance testing will be conducted on a hardware environment

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

* Remove restrictions for using DPDK in VXLAN-based segmentation case.
* Fix the network serializer so that the transformations are configured
  as described in the :ref:`Data model <data-model>` section.
* Convert the vendor specific attribute ``vlan_id`` for ``add-br`` to
  ``ovs-vsctl set port br-mesh tag=<vlan_id>``.
* Test manually.
* Create a system test for DPDK.
* Verify the :ref:`acceptance criteria <acceptance-criteria>`.

Dependencies
============

None

-----------
Testing, QA
-----------

* API/CLI test cases for configuring the DPDK with VXLAN segmentation.
* Web UI test cases for configuring the DPDK with VXLAN segmentation.
* Test case for DPDK with VXLAN segmentation being discovered and configured
  properly.
* Test case for using the multiple-node network groups.
* Functional testing.
* Performance testing.

.. _acceptance-criteria:

Acceptance criteria
===================

* Ability to run a DPDK application on top of OVS/DPDK + VXLAN-enabled host
* A 3 Mpps packet rate on the 64-bytes UDP traffic on a single PMD thread
  multiplied by a number of DPDK cores.
* Ability to work on the 40 Gb and 2x10 cards from Intel's Forteville family.

----------
References
----------

None
