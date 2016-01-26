..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================
Support for DPDK
================

https://blueprints.launchpad.net/fuel/+spec/support-dpdk

In order to get as close to wire-line speed as possible for virtual machines,
we want to install and utilize OVS with DPDK on some compute nodes.

--------------------
Problem description
--------------------

DPDK-backed OpenVSwitch and vhostuser features are fully merged in OpenStack
Mitaka. With this set of features end user could achieve boost to the
networking performance, and unlike SR-IOV, end user can still control traffic
via OpenFlow rules.

----------------
Proposed changes
----------------

Enabling DPDK requires:

* Discovering compatible hardware by hardcoded compatible driver and model list
  and provide user with information about compatible NICs.

* Proper network configuration with dedicated Private network for VLAN
  segmentation.

* Making configurations on compute side, including nova, neutron, interface
  binding to the DPDK and OpenVSwitch.

Web UI
======

On Nodes tab, in Interfaces configuration dialog for every interface should be:

* Information whether interface is DPDK capable.

* Visual control to enable DPDK on network interface.

Only Private network with VLAN segmentation could be placed on DPDK enabled
interface.

Bonds could not be used for DPDK. DPDK-enabled interfaces could not be bonded.

Nailgun
=======

* The nailgun-agent should collect information PCI-ID of NIC.

* The nailgun will compare PCI-ID and driver against hardcoded into `consts.py`
  list of supported hardware from dpdk website.

Data model
----------

Next DPDK-related information is stored in `interface_properties` field of
`NodeNICInterface`:

* DPDK availability for interface

* Whether DPDK is enabled by user or not

`astute.yaml` will be extended as following

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
      bridge: br-prv
      provider: dpdkovs
      vendor_specific:
        driver: igb_uio
  use_dpdk: true

When end user configures interface as DPDK and use it for Private network:

* Node-level parameter `use_dpdk` will enable DPDK on compute node.

* Network transformations should include vendor specific attrubute
  `datapath_type: netdev` to `br-prv` bridge.

* Interface should be added using `add-port` action with provider `dpdkovs`
  directly into `br-prv` bridge. New vendor specific attrubute `driver` should
  be added from hardcoded list of supported hardware.

REST API
--------

Payload for interfaces handlers will be changed as followed

.. code-block:: json

  [
     {
        "interface_properties" : {
           "dpdk" : {
              "enabled": Boolean or null,
              "available": Boolean
           }
        }
     }
  ]

New property `dpdk` will be added for every interface. It will contain
information about DPDK availability on NIC and end user's choice.

Orchestration
=============

None

RPC Protocol
------------

Only payload changes.

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

Fuel library will consume data from astute.yaml.

* OpenVSwitch will be configured to use dpdk.

* `vhostuser_socket_dir` will be configured in plugin.ini on compute node to
  enable vhostuser in neutron.

* l23network will configure interface as dpdk, connect it to ovs bridge and
  store it in config.

------------
Alternatives
------------

To achieve the same networking performance SR-IOV could be used. Comparing to
it, DPDK allows to use experimental Security Groups engine.

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

User interface impact is described in Web UI section.

------------------
Performance impact
------------------

Performance penalties are not expected.

-----------------
Deployment impact
-----------------

This feature will require to use VLAN segmentation and dedicated DPDK capable
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
