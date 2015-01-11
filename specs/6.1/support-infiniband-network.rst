..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================================================
Support Mirantis Openstack installation over Mellanox Infiniband network
========================================================================

https://blueprints.launchpad.net/fuel/+spec/support-infiniband-network

Mirantis and Mellanox teams added support for high performance Ethernet
virtualization and storage features in Fuel 5.1.

The current blueprint suggests to add support for Mirantis Openstack
installation over Mellanox Infinband network.

InfiniBand (abbreviated IB) is a computer network communications link
used in high-performance computing featuring very high throughput and
very low latency.


Problem description
===================

Currently in MOS, when installing Openstack with Mellanox High performance
features and on top of Mellanox Network components, Infiniband mode is not
supported.

Some of the High performance computing users, prefer to use Infinband due
to its highest throughput and lowest latency preferences.

Moreover, in this blueprint, extensive networking features will be implemented,
such as discovering port bus ID and vendor drivers information. this will
allow to add more vendor based network features.

A POC ISO already exists, and shows significant performance improvement from
the 56Gb Ethernet solution.

Adding Infiniband network support will allow users use IPOIB Virtual Functions
with higher performance, and will bring them closer to the wire speed.

Proposed change
===============

Support MOS installation over a prepared Infiniband network
(with running and pre-configured switch IB and SM).

The change should be transparent to the Users that already knows how to install
Mellanox components via Fuel installer, and be as standard as possible, without
harming the Infiniband performance.

In the proposed implementation, Fuel master will discover and use EIPOIB
(Ethernet IP Over InfiniBand) interfaces for the network roles (OVS will run
over EIPOIB), and will use IB only for RDMA and for the guests VFs in case of
SR-IOV.

The network mode will be calculated in the backend using the new interfaces
driver data - "eth_ipoib" for Infiniband or "mlx4_en" for Ethernet (RoCE).

**The main changes:**

*Packages:*

1. Change OFED light to full MLNX_OFED with OVS support over EIPOIB.
#. New Rethtool with bus and driver info (add a new cstruct for ethtool -i
   <interface>).
#. Adding mlnx dnsmasq package to repo : converts dnsmasq to work with GUIDs
   instead of MACs in case of IB NIC on the guests.
#. Adding Mellanox test VM with support for IPOIB interfaces.

*Fuel-main (Bootstrap):*

1. Adding bus and driver info to nailgun agent and rethtool, in order to
   discover ports vendor, protocol and parents / bus ID.
#. Adding IB drivers.
#. Changing mellanox drivers loading to auto link mode.
#. Start EIPOIB and IPOIB kernel modules with mlx4_core.
#. Adding script to convert SM pkeys to VLANs for verify network, and append
   it to rc.local if Mellanox kmods started.
#. Adding script to create SM PKEYs conversion for verify network.

*Fuel-web:*

1. Adding bus and driver info to nailgun NIC db and model.
#. Calculate the network modes + interfaces and drivers of the network
   roles (private, storage, management, admin) in deployment and provisioning
   serializers.
#. Removing the Ethernet mode from the UI descriptions.
#. Setting storage network to work on IB child for tagged iSER or IB parent of
   EIPOIB interface if untagged iSER.

*Fuel-library:*

1. Adding manifests for iSER child create for tagged iSER over IB.
#. Adding manifests to install and configure MlnxDnsmasq.
#. Change cobbler OFED snippet to VPI mode and to set port types and load
   EIPOIB if needed.
#. Adding manifests for restart EIPOIB daemon mode if needed.


Alternatives
------------

* Parsing ethtool output for drivers data in nailgun - very inelegant.
* Not using EIPOIB for Eth virtualization over IB for OVS/Linuxbridge
  support, but EIPOIB is the only method that support OVS/Linuxbridge VLAN
  rules conversion to PKEYs and slaves.


Data model impact
-----------------

Adding bus_info and driver columns to the NIC model, as described at the
proposed change section under Fuel-web.

REST API impact
---------------

None

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

Will add driver and bus_info parameter to the nailgun interfaces report.

Performance Impact
------------------

The IB solution increase default OVS performance dramatically, and
increase 56Gb link performance significantly from Eth mode, due to
its highest throughput and lowest latency for VMs and storage read/write
interactions with volumes.


Other deployer impact
---------------------

None

Developer impact
----------------

Adding driver and bus_info may enable Fuel developers to add new features
based on port's vendor identification.

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

1. Change OFED light to full MLNX_OFED with OVS support over EIPOIB:

* Add full OFED package (including Infiniband, network diagnostics
  and HPC capabilities).
* Change /sbin/ipoibd to support OVS VLAN conversions and to map infiniband
  PKEYs.

2. New Rethtool with bus and driver info (add a new cstruct for ethtool -i
   <interface>):

* Change /usr/lib/ruby/gems/1.8/gems/rethtool-0.0.3/lib/rethtool/
  interface_settings.rb to have bus and driver info getters.
* Change /usr/lib/ruby/gems/1.8/gems/rethtool-0.0.3/lib/rethtool.rb
  to include drivers CMD ID.
* Add /usr/lib/ruby/gems/1.8/gems/rethtool-0.0.3/lib/rethtool/ethtool_cmd.rb
  with the driver CStruct.

3. Adding mlnx dnsmasq package to repo : converts dnsmasq to work with GUIDs
   instead of MACs in case of IB NIC on the guests.
4. Adding Mellanox test VM with support for IPOIB interfaces.

*Fuel-main (Bootstrap):*

1. Adding bus and driver info to nailgun agent and rethtool, in order to
   discover ports vendor, protocol and parents / bus ID:

* Replace rethtool package in repo with the new package that includes
  the drivers functions (already built it for the POC ISO using Fuel packaging
  spec in http://fuel-repository.mirantis.com/repos/centos-fuel-6.0-stable-916/
  centos/noarch/).
* Add to fuel-web/bin/agent interfaces report the bus_info and driver rethtool
  functions call.

2. Adding IB drivers:

* Change /bootstrap/module.mk to add kernel-ib package and its dependencies.

3. Changing mellanox drivers loading to auto link mode:

* Remove /bootstrap/sync/etc/modprobe.d/mlnx4_core.conf

4. Start EIPOIB and IPOIB kernel modules with mlx4_core:

* Create /bootstrap/sync/etc/modprobe.d/eth_ipoib.conf

5. Adding script to convert SM pkeys to VLANs for verify network, and append
   it to rc.local if Mellanox kmods started:

* Change /bootstrap/sync/etc/modprobe.d/eth_ipoib.conf
* Increase buffers in /bootstrap/sync/etc/modprobe.d/ipoib.conf
  (for large amount of PKEYs)

6. Adding script to create SM PKEYs conversion for verify network:

* Adding /bootstrap/sync/usr/bin/init_eipoib.sh

*Fuel-web:*

1. Adding bus and driver info to nailgun db and model:

*  Change bin/agent to call drivers functions, as described in the
   Bootstrap section.
* Change nailgun/nailgun/db/migration/alembic_migrations/versions/fuel_5_0.py
  upgrade function to have driver and bus info columns.
* Change nailgun/nailgun/db/sqlalchemy/models/node.py NodeNICInterface to
  include driver and bus_info columns.
* Change nailgun/nailgun/objects/serializers/node.py
  NodeInterfacesSerializer nic_fields dict to include driver and bus_info.

2. Calculate the network modes + interfaces and drivers of the network
   roles (private, storage, management, admin) in deployment and provisioning
   serializers:

* Change nailgun/nailgun/orchestrator/deployment_serializers.py:

  - Calculate network mode (Eth/IB).
  - Set the private/storage networks on the parent of the
    private/storage ports in case of SRIOV with EIPOIB driver (the parent
    interface of an EIPOIB interface is the IB interface who has the VFs and
    the RDMA support).

* Change nailgun/nailgun/orchestrator/provisioning_serializers.py to support
  both port types (ETH/IB) in case of using Mellanox ports for one or more of
  the network roles.

3. Removing the Ethernet mode from the UI descriptions:

* Change nailgun/nailgun/fixtures/openstack.yaml (remove Ethernet word from
  descriptions).

4. Setting storage network to work on IB child for tagged iSER or IB parent of
   EIPOIB interface if untagged iSER.

* Change nailgun/nailgun/orchestrator/deployment_serializers.py
  fix_iser_port function.

*Fuel-library:*

1. Adding manifests for iSER child create for tagged iSER over IB:

* Add deployment/puppet/mellanox_openstack/manifests/iser_child.pp .
* Add deployment/puppet/mellanox_openstack/templates/iser_child_create.erb .
* Change deployment/puppet/osnailyfacter/examples/site.pp to call it in stage
  zero (if IB).

2. Adding manifests to install and configure MlnxDnsmasq:

* Create deployment/puppet/mellanox_openstack/manifests/mlnx_dnsmasq.pp to
  install additional dnsmasq package.
* Change deployment/puppet/openstack/manifests/controller_ha.pp to pass
  dhcp_driver.
* Change deployment/puppet/openstack/manifests/neutron_router.pp to pass
  dhcp_driver.
* Change deployment/puppet/osnailyfacter/manifests/cluster_ha.pp to pass
  configurable dhcp_driver and call mlnx_dnsmasq.pp.
* Change deployment/puppet/osnailyfacter/manifests/cluster_simple.pp to pass
  configurable dhcp_driver and call mlnx_dnsmasq.pp.

3. Change cobbler OFED snippet to VPI mode and to set port types and load
   EIPOIB if needed:

* Change
  deployment/puppet/cobbler/templates/snippets/ofed_install_with_sriov.erb.

4. Adding manifests for restart EIPOIB daemon mode if needed:

* Add deployment/puppet/mellanox_openstack/manifests/ipoibd.pp.
* Call in deployment/puppet/osnailyfacter/examples/site.pp with a
  new net-daemons stage.

Dependencies
============

None


Testing
=======

* Unit tests will be added for the Infinband cases.

Documentation Impact
====================

* Network drivers identification documentation will be added.
* Infiniband and EIPOIB explanations will be added to the terminogy section.


References
==========

* Infiniband network - http://en.wikipedia.org/wiki/InfiniBand
* Configuring EIPOIB interfaces - https://community.mellanox.com/docs/DOC-1316

