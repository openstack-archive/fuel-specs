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

-------------------
Problem description
-------------------

SR-IOV allows to bind network interface virtual functions to the different
virtual machines like a PCI device. It gives a boost to the networking
performance. This feature is already implemented in OpenStack, but requires
complex discovery process and configuration.

This feature is compatible with DVR: traffic between tenant networks from or to
SR-IOV enabled instances will be routed through the centralized router. L3 HA
is not affected by this feature and should be working as expected.

----------------
Proposed changes
----------------

Enabling SR-IOV requires:

* Discovering of compatible hardware and settings, and check that hardware is
  configured properly

* Providing operator with information about SR-IOV compatible interfaces and
  whether it's working or not

* Proper network configuration with dedicated Private network for VLAN
  segmentation

* Making configurations on both controller and compute sides, including nova,
  neutron, and interface setup

Web UI
======

On Nodes tab, in Interfaces configuration dialog for every interface should be:

* Information whether interface is SR-IOV capable

* Visual controls to enable SR-IOV and configure additional parameters:

  * Input how many virtual functions should be initialized on the interface
  * Input physical network name for `pci_passthrough_whitelist` configuration
    in Nova. Defaults to `physnet2`

The following validation should be done in both UI and API:

* In case of VLAN segmentation it should be possible to assign Private network
  to any NIC (with or without SR-IOV support). Physical network name should be
  equal to `physnet2`, other names are not allowed (in UI this text field
  should be disabled in such case, API should give 4xx reply)
* In case of tunneling segmentation it should be possible to assign Private
  (mesh) network only to NIC where SR-IOV is not enabled.
* SR-IOV can be enabled on SR-IOV capable interfaces where no networks are
  assigned. Physical network name could be set to any name, defaults to
  `physnet2`
* SR-IOV enabled interface(s) cannot be part of a bond

The following validation is needed in UI only:

* In case Operator specifies physical network name not equal to `physnet2`, a
  warning should be shown that only `physnet2` is going to be configured by
  Fuel in Neutron. Configuration of other physical networks is up to Operator
  or plugin. Fuel will just configure appropriate `pci_passthrough_whitelist`
  option in nova.conf for such interface and physical networks

The proposed change to Node Interfaces configuration screen will look like this:

  .. image:: ../../images/9.0/support-sriov/sriov-ui.png
      :scale: 75 %

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

Bootstrap
---------

In order to check SR-IOV availability, additional kernel parameters
`intel_iommu=on amd_iommu=on` should be passed to bootstrap.

Data model
----------

Information from the nailgun-agent and user input should be stored in
`interface_properties` field of `NodeNICInterface` in format that described:

* Whether SR-IOV is enabled by operator or not

* Number of enabled VFs (`sriov_numvfs`)

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


When operator configures interface as SR-IOV:

* Network transformations should add port using `add-port` action with provider
  `sriov` and fill vendor_specific attributes as following.

* Cluster-wide parameter `supported_pci_vendor_devs` will be generated and
  contains PCI-ID of NIC virtual functions from all interfaces where operator
  enabled SR-IOV. If this parameter is empty, it means SR-IOV is not enabled at
  all.

When Private network is assigned to SR-IOV enabled interface, deployment
information (astute.yaml) will be extended and will look like this:

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

When no network is assigned to SR-IOV enabled interface, deployment
information (astute.yaml) will be extended and will look like this:

::

  network_scheme:
    transformations:
    - action: add-port
      name: enp1s0f0
      provider: sriov
      vendor_specific:
        sriov_numvfs: <NUM>
  quantum_settings:
    supported_pci_vendor_devs:
      - <PCI-ID>

REST API
--------

Only payload for interfaces and node agent API handlers will be changed as
described in Nailgun-agent and Data model sections.

Network Checker
---------------

Network checker will not be able to check traffic through Private VLANs when
SR-IOV is enabled for the corresponding interface. So, this verification
should be disabled for such nodes after deployment.

Orchestration
=============

* Additional kernel parameters `intel_iommu=on amd_iommu=on` should be passed
  to SR-IOV enabled nodes.
* After compute nodes addition or removal, nova-scheduler and neutron-server
  configuration should be updated on controllers.

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

* l23network will configure interfaces virtual functions, set them up, and
  store network configuration into Operating System config

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

* Fuel supports configuration of SR-IOV in OpenStack services only when VLAN
  segmentation is in use and Private network is assigned to SR-IOV capable
  network interface. Handling SR-IOV enabled interfaces which are not in use
  for Private networks is up to cloud operators or plugin developers.

* VM Live Migration with SR-IOV attached instances is not supported.

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

This feature could not be tested on virtual environment. Special lab is
required for manual verification.

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

-----------
Testing, QA
-----------

* Manually test that SR-IOV is discovered properly
* Manually test that SR-IOV is configured properly via API/CLI/WEB UI
  (deployment information is correct)
* Manually test that SR-IOV is set up on nodes properly (manifests configure
  node interfaces properly)
* Performance testing

Acceptance criteria
===================

User should be able to deploy compute nodes with dedicated network interface
into SR-IOV mode, then create direct-attached port and boot a VM with it.

----------
References
----------

* `Using SR-IOV functionality
  <http://docs.openstack.org/liberty/networking-guide/adv_config_sriov.html>`_
