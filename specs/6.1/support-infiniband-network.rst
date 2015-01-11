..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================================================
Support discovery over Mellanox Infiniband network using interface driver data
==============================================================================

https://blueprints.launchpad.net/fuel/+spec/support-infiniband-network

In Fuel 5.1, support for Mellanox high performance Ethernet virtualization
and storage features has been added.

Starting with version 6.0, Fuel supports a Pluggable architecture.

This blueprint suggests to publish interface driver and networks
allocation data, for new network / interface oriented features.
This will also ease the process of exporting core functionality
of partners into plugins and allowing them to access the required
nodes model information.

Moreover, this blueprint describes Mellanox Infiniband drivers installation
for the bootstrap discovery stage.

InfiniBand (abbreviated IB) is a computer network communications link
used in high-performance computing featuring very high throughput and
very low latency.


Problem description
===================

There are two main problems that this blueprint suggests to solve:

1. Currently in Fuel, Installation over Infiniband mode is not supported, and
   in particular bootstrap discovery and network verification over
   infiniband based network.

   Some of the high performance computing users, prefer to use Infinband due
   to its highest throughput and lowest latency preferences.

   A POC ISO already exists, and shows significant performance improvement
   from the 56Gb Ethernet solution.

   Adding Infiniband network support will allow users use IPOIB Virtual
   Functions with higher performance, and will bring them closer to the wire
   speed.

#. Network interfaces information, that was accessible via the nodes model
   in Fuel web serializers, is now missing, for implementing network oriented
   plugins.

   Moreover, in this blueprint, extensive network information publishment will
   be added, such as discovering port bus ID and vendor drivers information.
   This will allow to add more vendor and network based features.


Proposed change
===============

Support nodes discovery over a prepared Infiniband network via Fuel
(with a running and pre-configured switch IB and Subnet Manager).

The change should be transparent to users that already knows how to install
Mellanox components via Fuel installer, and be as standard as possible, without
harming the Infiniband performance.

The Fuel master will discover and use EIPOIB (Ethernet IP Over InfiniBand)
interfaces for the network roles.

In the complementary Fuel plugin for Infiniband, OVS will run over EIPOIB
interfaces that was discovered in the bootstrap stage.

Infiniband interfaces (IPOIB) will be used only for RDMA (Remote Direct
Memory Access), and for the guests Virtual Functions (Virtual Interfaces)
in case of SR-IOV.

The network mode will be calculated in the backend using the new interfaces
driver data - "eth_ipoib" for Infiniband or "mlx4_en" for Ethernet (RoCE).

**The main changes:**

*Packages:*

1. New Rethtool with bus and driver info (add a new cstruct for ethtool -i
   <interface>).
#. Adding kernel-ib driver to Fuel repository.

*Fuel-main (Bootstrap):*

1. Adding bus and drivers info to nailgun agent, in order to
   discover ports vendor, protocol and parents / bus ID.
#. Extracting the IB drivers.
#. Changing Mellanox drivers loading to auto link mode (Eth or IB).
#. Start eth_ipoib and ib_ipoib kernel modules if mlx4_core is loaded.
#. Adding daemon to convert SM PKEYs to VLANs for verify network,
   and execute it if Mellanox eth_ipoib kernel module started.

*Fuel-web:*

1. Adding bus and drivers info to nailgun NIC db and model.
#. Publish interfaces discovered driver and bus info data (under
   interfaces).
#. Publish the physical interface and VLAN tag for each network role (private,
   storage, management, admin) to astute.yaml (under roles).


Alternatives
------------

* Parsing ethtool output for drivers data in nailgun agent - very inelegant.
* Not using EIPOIB for Eth virtualization over IB - EIPOIB is the only method
  that currently supports OVS/Linuxbridge VLAN rules with PKEYs conversion.


Data model impact
-----------------

Adding bus_info and driver columns to the NIC model, as described at the
proposed change section under Fuel-web.

REST API impact
---------------

The parameters 'bus_info' and 'driver' are added into REST responses for Node
network interface parameters.

Upgrade impact
--------------

Upgrade impact in this case is more of Plugin upgrade impact, so it is out
of scope in this spec.

Security impact
---------------
None

Notifications impact
--------------------

None

Other end user impact
---------------------

Will add driver and bus_info parameter to the nailgun interfaces report
(in the Fuel web UI).

Performance Impact
------------------

No Such, but it will enable to support the Infiniband plugin that increases
default OVS performance dramatically, and increase 56Gb link performance
significantly from Eth mode, in VMs connection and Cinder volumes.


Other deployer impact
---------------------

None

Developer impact
----------------

Adding driver and bus_info may enable Fuel developers to add new features
based on the port vendor identification.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  aviramb <aviramb@mellanox.com>

Other contributors:
  gilmeir-d <gilmeir@mellanox.com>

Work Items
----------

*Packages:*

1. New Rethtool with bus and driver info (add a new cstruct for ethtool -i
   <interface>):

* Change /usr/lib/ruby/gems/1.8/gems/rethtool-0.0.3/lib/rethtool/
  interface_settings.rb to have bus and driver info getters.
* Change /usr/lib/ruby/gems/1.8/gems/rethtool-0.0.3/lib/rethtool.rb
  to include drivers CMD ID.
* Add /usr/lib/ruby/gems/1.8/gems/rethtool-0.0.3/lib/rethtool/ethtool_cmd.rb
  with the driver CStruct.
* Example code in
  `this example <https://github.com/avirambh/rethtool/commit/dce5d747c1ea654ff6c4430a2fa4c6337f7e9527>`_
  .

2. Add kernel-ib rpm to the bootstrap image:

* Compile OFED on the bootstrap kernel and add the OFED kernel-ib rpm to
  the Nailgun repo.

*Fuel-main (Bootstrap):*

1. Adding bus and driver information to nailgun agent and rethtool, in order to
   discover ports vendor, protocol and parents / bus ID:

* Replace rethtool package in repo with the new package that includes
  the drivers functions (already built it for the POC ISO using Fuel packaging
  spec in
  `Fuel repository <http://fuel-repository.mirantis.com/repos/centos-fuel-6.0-stable-916/centos/noarch/>`_
  ).

* Add to fuel-web/bin/agent interfaces report the bus_info and driver rethtool
  functions call.

2. Adding IB drivers:

* Change /bootstrap/module.mk to extract kernel-ib package and its
  dependencies.

3. Changing mellanox drivers loading to auto link mode:

* Remove /bootstrap/sync/etc/modprobe.d/mlnx4_core.conf

4. Start EIPOIB and IPOIB kernel modules with mlx4_core:

* Create /bootstrap/sync/etc/modprobe.d/eth_ipoib.conf

5. Adding a daemon to create SM PKEYs conversion for verify network:

* Adding /bootstrap/sync/usr/bin/init_eipoib.sh
* Implement A daemon that reads once in 30 seconds the PKEYs configured at the
  SM machine (published in /sys/class/infiniband/<HCA>/ports/<port>/pkeys/),
  and verifies all pkeys are converted to vlans on all ports.
* Execute this daemon in bootstrap/sync/etc/modprobe.d/eth_ipoib.conf after
  ib_ipoib and eth_ipoib, if mlx4_ib is executed (mlx4_ib and mlx4_en are
  executed if mlx4_core kernel module is executed, which occurs only if
  Mellanox card has been found - as in Fuel 5.1).

6. Adding script to convert SM pkeys to VLANs for verify network, and append
   it to rc.local if Mellanox kmods started:

* Change /bootstrap/sync/etc/modprobe.d/eth_ipoib.conf
* Increase buffers in /bootstrap/sync/etc/modprobe.d/ipoib.conf
  (for large amount of PKEYs)

7. Example code can be found in `Mellanox fuel-main fork <https://github.com/Mellanox/fuel-main/commit/6788f44acbcdae06e5f77a1fa4350808b5bbe5fa>`_.

*Fuel-web:*

1. Adding bus and driver info to nailgun db and model:

* Change bin/agent to call drivers functions (int.driver and int.bus_info),
  as described in the Bootstrap section.
* Change the relevant upgrade/downgrade modules in
  nailgun/nailgun/db/migration/alembic_migrations/versions/
  to have the driver and bus info columns.
* Change nailgun/nailgun/db/sqlalchemy/models/node.py NodeNICInterface to
  include driver and bus_info columns.
* Change nailgun/nailgun/objects/serializers/node.py
  NodeInterfacesSerializer nic_fields dict to include driver and bus_info.

2. Publish interfaces discovered driver and bus info data:

* Add to the networking dict of deployment serializers the driver and bus ID
  of the nodes interfaces, under the interfaces dict.

3. Publish the physical interface and VLAN tag for each network role (private,
   storage, management, admin) to astute.yaml:

* Add to the networking dict of deployment serializers the physical interfaces
  for each role and its VLAN tag (as selected in the Fuel UI).
  This data is required for SR-IOV vNIC alocation and for establishing RDMA
  connection on the storage interface parent / probbed interface
  (OVS bridge/LB does not support RDMA).

4. Example code can be found in `Mellanox fuel-web fork <https://github.com/Mellanox/fuel-web/commit/3386c6cc787d2d0ae48a386023b8b5c1998c0eeb>`_ (serializers and UI code are not relevant in this link).


Dependencies
============

None


Testing
=======

1. Integration tests for Fuel-Web:

* Integration tests for testing creation of a node with driver and bus_info
  parameters.
* Integration tests for testing access to the node driver and bus_info
  parameters after creation.

2. CI and Verificaiton an Mellanox Lab:

* Nodes discovery over Infiniband network.
* Network verification over Infiniband network.
* Host and switch based SM.
* Large number of PKEYs.
* Verifying that bootstrap is loaded without Mellanox drivers if now Mellanox
  HW has been discovered.


Documentation Impact
====================

1. Instructions for "How to configure SM" will be added to the Planning guide.
#. Instructions for "Network drivers identification" will be added to the
   User guide.
#. Instructions for "How to install Mirantis Openstack with Infiniband Network"
   will be added to the Mellanox community, similarly to `this post <https://community.mellanox.com/docs/DOC-2036>`_
   that has been made to the 5.1 based Fuel IB POC.


References
==========

* Infiniband network - http://en.wikipedia.org/wiki/InfiniBand
* Configuring EIPOIB interfaces - https://community.mellanox.com/docs/DOC-1316

