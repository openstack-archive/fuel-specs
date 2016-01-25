..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================================
Support for SR-IOV for improved networking performance
======================================================

https://blueprints.launchpad.net/fuel/+spec/support-sriov

User should be able to deploy compute nodes with dedicated network interface
into SR-IOV mode, then create direct-attached port and boot a VM with it.

--------------------
Problem description
--------------------

SR-IOV allows to bind network interface's virtual functions to the different
virtual machines like a PCI device. That gives boost to the networking
performance. Feature is already implemented in OpenStack, but requires complex
discovery and configuration.

This feature is compatible with DVR: traffic between tenant networks from or to
SR-IOV enabled instances will be routed through the centralized router. L3 HA
is not affected by this feature and should be working as expected.

----------------
Proposed changes
----------------

Enabling SR-IOV requires:

* Discover compatible hardware and settings, and check that hardware is
  configured properly

* Provide user with information about SR-IOV compatible interfaces and wheter
  it's working or not

* Proper network configuration with dedicated Private network for VLAN
  segmentation.

* Making configurations on both controller and compute side, including nova,
  neutron, and interface setup.

Web UI
======

On Nodes tab, in Interfaces configuration dialog for every interface should be:

* Information whether interface is SR-IOV capable and SR-IOV is configured
  properly

* Options to enable SR-IOV, and to input how much virtual functions should be
  initialized on the interface

Only Private network with VLAN segmentation could be placed on SR-IOV enabled
interface.

Nailgun
=======

nailgun-agent should collect and send information about SR-IOV enabled hardware
in order to configure OpenStack properly.

Data model
----------

Next data should be stored for every node for every SR-IOV interface:

* Number of available virtual functions

* PCI-ID of virtual function

astute.yaml will be extended as

::

  network_scheme:
    transformations:
    - action: add-port
      name: enp1s0f0
      provider: sriov
      vendor_specific:
        function: pf
        sriov_numvfs: <NUM>
        physnet: physnet2
  quantum_settings:
    supported_pci_vendor_devs:
      - <PCI-ID>

where <NUM> is number and <PCI-ID> is string like "8086:1515".
If sriov ports isn't presented in transformations it means that SR-IOV is
not enabled in for this node. If `supported_pci_vendor_devs` is empty, it means
SR-IOV is not enabled in at all.

Information from network_scheme's transformations will be used for interface
set up, and for generating `pci_passthrough_whitelist`.

`supported_pci_vendor_devs` will be passed as is.

REST API
--------

Only payload changes.

Orchestration
=============

Custom kernel boot line should be passed to SR-IOV enabled nodes.

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

Library will consume data from astute.yaml.

* l23network will configure interface's virtual function, set it up, and store
  it in config

* `pci_passthrough_whitelist` will be configured in nova-compute. There is new
  function will be introduced, that returns this mapping between interface name
  and physical network from network_scheme's transformations.

* `supported_pci_vendor_devs` will be configured in neutron-server directly
  from corresponding field from astute.yaml.

------------
Alternatives
------------

SR-IOV is more hardware-specific feature that DPDK. Hovewer, SR-IOV  should be
less overheaded than DPDK.

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

Security Groups can not currently be used with SR-IOV enabled ports.

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

* Information about PCI devices will be periodically sent by nova-compute.

* Additional `PciPassthroughFilter` scheduler filter is required.

-----------------
Deployment impact
-----------------

* This feature will require to use VLAN segmentation and dedicated SR-IOV
  capable network interface for Private network.

* VM migration with SR-IOV attached instances is not supported.

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

This feature could not be tested on virtual environment.

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

Work Items
==========

* Collecting information about SR-IOV interfaces
* Enable SR-IOV configuration in Fuel
* Support of configuring SR-IOV via fuel API
* Support of configuring SR-IOV via fuel CLI
* Support of SR-IOV on UI
* Manual testing
* Create a system test for SR-IOV

Dependencies
============

None

------------
Testing, QA
------------

TBD

Acceptance criteria
===================

User should be able to deploy compute nodes with dedicated network interface
into SR-IOV mode, then create direct-attached port and boot a VM with it.

----------
References
----------

* `Using SR-IOV functionality
  <http://docs.openstack.org/liberty/networking-guide/adv_config_sriov.html>`_
