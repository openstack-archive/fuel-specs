..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Support for DPDK for improved networking performance
====================================================

https://blueprints.launchpad.net/fuel/+spec/support-dpdk

In order to get as close to wire-line speed as possible for virtual machines,
we want to install and utilize OVS w/ DPDK on some compute nodes.

--------------------
Problem description
--------------------

DPDK-backed OpenVSwitch and vhostuser features is fully merged in OpenStack
Mitaka. With this set of features end user could achieve boost to the
networking performance, and unlike SR-IOV, end user can still control traffic
via OpenFlow rules.

----------------
Proposed changes
----------------

Enabling DPDK requires:

* Discover compatible hardware by driver list and provide user with information
  about compatible NICs

* Proper network configuration with dedicated Private network for VLAN
  segmentation.

* Making configurations on both controller and compute side, including nova,
  neutron, interface binding to the DPDK and OpenVSwitch.

Web UI
======

On Nodes tab, in Interfaces configuration dialog for every interface should be:

* Information whether interface is DPDK capable

* Options to enable DPDK on network interface

Only Private network with VLAN segmentation could be placed on DPDK enabled
interface.

Nailgun
=======

Enabling DPDK requires HugePages to be enabled on corresponding nodes.

Data model
----------

astute.yaml will be extended as following

::

  network_scheme:
    transformations:
    - action: add-br
      name: br-prv
      provider: ovs
      vendor_specific:
        datapath_type: netdev
    - action: add-port
      name: enp1s0f0
      provider: dpdk
      vendor_specific:
        driver: igb_uio
  use_dpdk: true

`use_dpdk` will enable dpdk on compute node.

If end user chooses to use DPDK for interface to Private network, we need to
add vendor specific attrubute `datapath_type: netdev` to bridge. NIC will be
added as DPDK interface using `dpdk` provider for `add-port` transformation.

REST API
--------

Only payload changes.

Orchestration
=============

None

RPC Protocol
------------

Only payload changes.

Fuel Client
===========

TBD

Plugins
=======

None

Fuel Library
============

Fuel library will consume data from astute.yaml.

* dpdk packages will be installed.

* l23network will configure interface as dpdk, connect it to ovs bridge and
  store it in config.

* `vhostuser_socket_dir` will be configured in plugin.ini on compute node to
  enable vhostuser in neutron.

* OpenVSwitch and libvirt will be configured to use vhostuser.

------------
Alternatives
------------

To achieve same networking performance SR-IOV could be used. Comparing to it,
DPDK allows to use experimental Security Groups engine.

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

User interface impact described in Web UI section.

------------------
Performance impact
------------------

Performance penalties is not expected.

-----------------
Deployment impact
-----------------

* This feature will require to use VLAN segmentation and dedicated DPDK capable
  network interface for Private network.

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

This feature could be possibly tested on virtual environment.

--------------------
Documentation impact
--------------------

TBD

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  yottatsa
  skolekonov

Mandatory design review:
  xenolog
  dteselkin

Work Items
==========

* Enable DPDK configuration in Fuel
* Support of configuring DPDK via fuel API
* Support of configuring DPDK via fuel CLI
* Support of DPDK on UI
* Manual testing
* Create a system test for DPDK

Dependencies
============

This feature depends on `HugePages feature
<https://blueprints.launchpad.net/fuel/+spec/support-hugepages>`_.

------------
Testing, QA
------------

TBD

Acceptance criteria
===================

User should be able to deploy compute nodes with network interface in DPDK
mode, and boot a VM with vhostuser and HugePages enabled.

----------
References
----------

* `Neutron Open vSwitch vhost-user support
  <http://docs.openstack.org/developer/neutron/devref/ovs_vhostuser.html>`_

* `OpenVSwitch DPDK Firewall implementation
  <https://github.com/openstack/networking-ovs-dpdk>`_

* `List of supported NICs
  <http://dpdk.org/doc/nics>`_
