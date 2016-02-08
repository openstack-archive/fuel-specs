..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================
Support for SR-IOV
==================

https://blueprints.launchpad.net/fuel/+spec/support-sriov

User should be able to deploy compute nodes with dedicated network interface
into SR-IOV mode, then create direct-attached port and boot a VM with it.

--------------------
Problem description
--------------------

SR-IOV allows to bind network interface virtual functions to the different
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

* Discovering compatible hardware and settings, and check that hardware is
  configured properly

* Providing user with information about SR-IOV compatible interfaces and whether
  it's working or not

* Proper network configuration with dedicated Private network for VLAN
  segmentation.

* Making configurations on both controller and compute sides, including nova,
  neutron, and interface setup.

Web UI
======

On Nodes tab, in Interfaces configuration dialog for every interface should be:

* Information whether interface is SR-IOV capable and SR-IOV is configured
  properly

* Visual controls to enable SR-IOV, and to input how much virtual functions
  should be initialized on the interface

Only Private network with VLAN segmentation could be placed on SR-IOV enabled
interface. This validation should be done in API as well.

Nailgun
=======

Nailgun-agent
-------------

The nailgun-agent should collect and send information about SR-IOV enabled
NIC:

* Number of available virtual functions (`sriov_totalvfs`)

* SR-IOV availability (IOMMU groups should be checked)

* PCI-ID of NIC virtual functions of this NIC (it's same for all VFs)

Collected information should be passed to nailgun in the next format

.. code-block:: json

  {
    'meta': {
      'interfaces': [
        {
          "sriov" : {
            "sriov_totalvfs": Number,
            "available": Boolean,
            "pci_id": String
          }
        }
      ]
    }
  }

Bootstrap image should be booted with enabled SR-IOV.

Data model
----------

Information from the nailgun-agent and user input should be stored in
`interface_properties` field of `NodeNICInterface` in format that described in
REST API section:

* Whether SR-IOV is enabled by user or not and number of enabled VFs
  (`sriov_numvfs`)

* Number of available virtual functions (`sriov_totalvfs`)

* SR-IOV availability (IOMMU groups should be checked)

* PCI-ID of NIC virtual functions of this NIC (it's same for all VFs)

.. code-block:: json

  [
    {
      "interface_properties" : {
        "sriov" : {
          "enabled": Boolean or null,
          "sriov_numvfs": Number or null,
          "sriov_totalvfs": Number, Read only,
          "available": Boolean, Read only,
          "pci_id": String, Read only
        }
      }
    }
  ]


When end user configures interface as SR-IOV and use it for Private network:

* Network transformations should add port using `add-port` action with provider
  `sriov` and fill vendor_specific attributes as following. If sriov ports
  are not presented in transformations it means that SR-IOV is not enabled for
  this node (because no interfaces will be set up).

* Cluster-wide parameter `supported_pci_vendor_devs` will be generated and
  contains PCI-ID of NIC virtual functions from all interfaces where user
  enabled SR-IOV. If this parameter is empty, it means SR-IOV is not enabled at
  all.

According to this, astute.yaml will be extended and looks like this

::

  network_scheme:
    transformations:
    - action: add-port
      name: enp1s0f0
      provider: sriov
      vendor_specific:
        sriov_numvfs: <NUM>
        physnet: physnet2
  quantum_settings:
    supported_pci_vendor_devs:
      - <PCI-ID>

where <NUM> is number and <PCI-ID> is string like "8086:1515".

REST API
--------

Only payload for interfaces and node agent API handlers will be changed as
described in Nailgun-agent and Data model sections.

Orchestration
=============

* Custom kernel boot line should be passed to SR-IOV enabled nodes.
* After compute nodes addition or removal, neutron configuration should be
  updated on controllers.

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

Library will consume data from astute.yaml.

* l23network will configure interface virtual function, set it up, and store
  network configuration into Operating System config

* additional filters will be enabled for nova-scheduler

* additional mechanism driver will be enabled for Neutron

* `firewall_driver` for Neutron ML2 plugin will be set to Noop

* `pci_passthrough_whitelist` will be configured in nova-compute. New function
  will be introduced, that returns this mapping between interface name and
  physical network from network_scheme transformations.

* `supported_pci_vendor_devs` will be configured in neutron-server directly
  from corresponding field from astute.yaml.

------------
Alternatives
------------

SR-IOV is more hardware-specific feature than DPDK. However, SR-IOV should
provide less overhead than DPDK.

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

* This feature requires to use VLAN segmentation and dedicated SR-IOV capable
  network interface for Private network.

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
* Enable SR-IOV configuration in fuel-library
* Enable SR-IOV related orchestrations
* Support of configuring SR-IOV via fuel API
* Support of SR-IOV on UI
* Manual testing

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
