..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================================
Support extensions of NIC and Node attributes in plugins
========================================================

https://blueprints.launchpad.net/fuel/+spec/nics-and-nodes-attributes-via-plugin

Plugin developer should be able to extend NIC, Bond and Node properties
via plugin.

-------------------
Problem description
-------------------

Plugins should have a mechanism for providing additional attributes for NICs,
bonds and nodes. In future it can be useful when plugin provides some
technology which should work "per interface" or "per node". For example,
in case of Contrail we need support VF for vRouter on each network interface.


----------------
Proposed changes
----------------

Extend Fuel plugin framework with functionality of merging additional NIC,
Bond and Node attributes through plugins.

Web UI
======

* UI should properly represent schema and data for NIC, BOND and Node
  attributes provided by plugin on ``Configure Interfaces`` and ``Node``
  screens.

* Client can receive core and plugin NICs and BONDs attributes default
  state by ``/nodes/interfaces/default_assignment/`` and
  ``/nodes/bonds/attributes/defaults`` API calls.

* ``/nodes/:id/attributes`` should operate with both core and plugins Node
  attributes.

* ``Load defaults`` button on ``Configure Interfaces`` screen should return
  default data for NIC attributes.

* ``Load defaults`` button on ``Node`` details dialog should return default
  data for Node attributes.

* In case of bond creation, all slave interfaces should have the same set of
  attributes with identical structure and depend on availability conditions
  for different type of bonds [0]_.

* Current mechanism for attributes availability during bonding like DPDK
  will be the same and implemented on UI.


Nailgun
=======

Data model
----------

New default core attributes for NIC and BOND should be described in
``openstack.yaml`` file. They will be mapped on ``nic_attributes`` and
``bond_attributes`` in Release.

Plugin related information with NICs, BONDs and Nodes default attributes
will be stored in ``nic_attributes_metadata``, ``bond_attributes_metadata``
and ``node_attributes_metadata`` attributes of Plugin model (Can be changed
based on Plugins v5 spec [1]_).

Additional models ``NodeNICInterfaceClusterPlugin``, ``NodeClusterPlugin`` and
``NodeBondInterfaceClusterPlugin`` will be used to store actual state of plugin
related NICs, BONDs and Nodes attributes data per each interface, bond or
node. By default ``attributes`` fields of these models should be filled with
data from ``Plugin.nic_attributes_metadata``,
``Plugin.node_attributes_metadata`` and ``Plugin.bond_attributes_metadata``
respectively.

Fuel core NIC, BOND and Node ``attributes`` [2]_ can be stored in
``attributes`` field in each related table. Core NICs ``attributes`` will be
filled with default attributes from Release which are taken from
``nic_attributes`` and values will be generated in same way as for
``interface_properties``. Data from
``NodeNICInterfaceClusterPlugin.attributes`` will be mixed with
``NodeNICInterface.attributes`` based on info about disabled or enabled state
of plugins during ``/nodes/:id/interfaces/`` API call. And vice versa: data
from client will be split and stored between these two tables. Same logic will
be used for BOND and Node attributes.

``NodeNICInterface.meta`` will be used to store read-only metadata and filled
with ``Node.meta`` values.

If plugin does not provide NIC, BOND or Node additional attributes then
relations with empty ``attributes`` should not exist.

Plugin can override core interface attributes. If two plugins override the
same attribute, conflict exception should be raised.

Nailgun DB tables changes:


**Plugin**

``nic_attributes_metadata``
  Plugin attributes data taken from ``nic_attributes`` yaml

``bond_attributes_metadata``
  Plugin attributes data taken from ``bond_attributes`` yaml

``node_attributes_metadata``
  Plugin attributes data taken from ``node_attributes`` yaml


**NodeNICInterface**

``attributes``
  NIC attributes in DSL format

``meta``
  Read-only metadata


**NodeNICInterfaceClusterPlugin**

``id``
  unique identifier

``attributes``
  Actual state of plugin NIC attributes data

``cluster_plugin_id``
  Foreign key on cluster_plugins table

``interface_id``
  Foreign key on node_nic_interfaces table

``node_id``
  Foreign key on nodes table

Example of `attributes` field:

.. code-block:: json

  {
    "attribute_a": {
      "label": "NIC attribute A",
      "weight": 10
      "description": "Some description",
      "type": "text",
      "value": "test"
    },
    "attribute_b": {
      "label": "NIC attribute B",
      "weight": 20
      "description": "Some description",
      "type": "checkbox",
      "value": False
    }
  }


**NodeBondInterface**

``attributes``
  BOND attributes in DSL format


**NodeBondInterfaceClusterPlugin**

``id``
  Unique identifier

``attributes``
  Actual state of plugin Bond attributes data

``cluster_plugin_id``
  Foreign key on cluster_plugins table

``bond_id``
  Foreign key on node_bond_interfaces table

``node_id``
  Foreign key on nodes table


**NodeClusterPlugin**

``id``
  Unique identifier

``attributes``
  Actual state of plugin Node attributes data

`cluster_plugin_id`
  Foreign key on cluster_plugins table

``node_id``
  Foreign key on nodes table


**Release**

``nic_attributes``
  Attributes with default values for NICs

``bond_attributes``
  Attributes with default values for BONDs


Data from ``attributes`` in ``NodeNICInterface``,
``NodeNICInterfaceClusterPlugin``, ``NodeBondInterface``,
``NodeBondInterfaceClusterPlugin``, ``Node`` and ``NodeClusterPlugin`` should
be serialized in deployment scenario and sent to astute with other attributes.
This is how an astute.yaml part will look like for additional NIC attributes:

.. code-block:: yaml

  interfaces:
    enp0s1:
      vendor_specific:
        driver: e1000
        bus_info: "0000:00:01.0"
        attribute_a: "spam"
        attribute_b: false
    enp0s2:
      vendor_specific:
        driver: e1000
        bus_info: "0000:00:02.0"
        attribute_a: "egg"
        attribute_b: true

for BOND attributes:

.. code-block:: yaml

  transformations:
    - bridge: br-mgmt
      name: bond0
      interfaces:
        - enp0s1
        - enp0s2
      bond_properties:
        mode: balance-rr
      interface_properties:
        vendor_specific:
          disable_offloading: true
          attribute_a: "test"
          attribute_b: true
      action: add-bond

for Node attributes:

.. code-block:: yaml

  plugin_section_a:
    attribute_a: "test"
    attribute_b: false


REST API
--------

There will be new API call provided metadata for NIC and BOND.

===== ============================================ ===========================
HTTP  URL                                          Description
===== ============================================ ===========================
GET   /api/v1/nodes/:id/bonds/attributes/defaults/ Get default bond attributes
                                                   for specific release
GET   /api/v1/nodes/:id/attributes/defaults/       Get default node attributes
                                                   for specific release
===== ============================================ ===========================


The response format for GET ``/nodes/:id/bonds/attributes/defaults``:

.. code-block:: json

  {
    "additional_attributes": {
      "metadata": {
        "label": "Plugins attributes section for bonds",
        "weight": 50
      },
      "attribute_a": {
        "label": "BOND attribute A",
        "weight": 10
        "description": "Some description",
        "type": "text",
        "value": "test"
      },
      "attribute_b": {
        "label": "BOND attribute B",
        "weight": 20
        "description": "Some description",
        "type": "checkbox",
        "value": False
      }
    }
  }


GET ``/nodes/:id/interfaces/`` method should return data with the following
structure:

.. code-block:: json

  [
    {
      "id": 1,
      "type": "ether",
      "name": "enp0s1",
      "assigned_networks": [],
      "driver": "igb",
      "mac": "00:25:90:6a:b1:10",
      "state": null,
      "max_speed": 1000,
      "current_speed": 1000,
      "pxe": False,
      "bus_info": "0000:01:00.0",
      "meta": {
        "sriov": {
          "available": true,
          "pci_id": "12345"
        },
        "dpdk": {
          'available': true,
        },
        "offloading_modes" : [
          {
            "state": null,
            "name": "tx-checksumming",
            "sub": [
              {
                "state": null,
                "name": "tx-checksum-sctp",
                "sub": []
              }
            ]
          }
        ]
      }
      "attributes": {
        "offloading": {
          "metadata": {
            "label": "Offloading",
            "weight": 10
          },
          "disable_offloading": {
            "label": "Disable offloading",
            "weight": 10,
            "type": "checkbox",
            "value": False,
          },
          "offloading_modes": {
            "label": "Offloading modes"
            "weight": 20
            "description": "Offloading modes"
            "type": "offloading_modes"
            "value": {
              "tx-checksumming": true,
              "tx-checksum-sctp": false
            }
          }
        },
        "mtu": {
          "metadata": {
            "label": "MTU",
            "weight": 20,
          },
          "mtu_value": {
            "label": "MTU",
            "weight": 10,
            "type": "text",
            "value": ""
          }
        },
        "sriov" : {
          "metadata": {
            "group": "sriov",
            "label": "SRIOV",
            "weight": 30
          },
          "sriov_enabled": {
            "label": "SRIOV enabled",
            "type": "checkbox",
            "enabled": True,
            "weight": 10
          },
          "sriov_numvfs": {
            "label": "virtual_functions"
            "type": "number",
            "min": "0",
            "max": "10", // taken from sriov_totalvfs
            "value": "5",
            "weight": 20
          },
          "physnet": {
            "label": "physical_network",
            "type": "text",
            "value": "",
            "weight": 30
          }
        },
        "dpdk": {
          "metadata": {
            "group": "nfv",
            "label": "DPDK",
            "weight": 40
          },
          "dpdk_enabled": {
            "label": "DPDK enabled",
            "type": "checkbox",
            "enabled": False,
            "weight": 10
          },
        }
        "additional_attributes": {
          "metadata": {
            "label": "All plugins attributes section",
            "weight": 50
          },
          "attribute_a": {
            "label": "NIC attribute A",
            "weight": 10
            "description": "Some description",
            "type": "text",
            "value": "test",
            "nic_plugin_id": 1
          },
          "attribute_b": {
            "label": "NIC attribute B",
            "weight": 20
            "description": "Some description",
            "type": "checkbox",
            "value": False,
            "nic_plugin_id": 1
          }
        }
      }
    },
    {
      "type": "bond",
      "name": "bond0",
      "state": null,
      "assigned_networks": [],
      "bond_properties": {
        "type__": "linux",
        "mode": "balance-rr",
      },
      "mac": null,
      "mode": "balance-rr",
      "slaves": [],
      "attributes": {
        "mode": {
          "metadata": {
            "label": "Mode",
            "weight": 10
          }
          "mode_value": {
            "label": "Mode",
            "weight": 10,
            "type": "select",
            "values": [
              {"label":"balance-rr", "data": "balance-rr"},
              {"label":"some-label-1", "data": "some-value-1"},
              {"label":"some-label-n", "data": "some-value-n"}
            ]
            "value": "balance-rr"
          }
        },
        "offloading": {
          "metadata": {
            "label": "Offloading",
            "weight": 20
          },
          "disable_offloading": {
            "label": "Disable offloading",
            "weight": 10,
            "type": "checkbox",
            "value": False,
          },
          "offloading_modes": {
            "label": "Offloading modes"
            "weight": 20
            "description": "Offloading modes"
            "type": "offloading_modes"
            "value": {
              "tx-checksumming": true,
              "tx-checksum-sctp": false
            }
          }
        },
        "mtu": {
          "metadata": {
            "label": "MTU",
            "weight": 30,
          },
          "mtu_value": {
            "label": "MTU",
            "weight": 10,
            "type": "text",
            "value": ""
          }
        },
        "additional_attributes": {
          "metadata": {
            "label": "All plugins attributes section",
            "weight": 40
          },
          "attribute_a": {
            "label": "BOND attribute A",
            "weight": 10,
            "description": "Some description",
            "type": "text",
            "value": "test",
            "bond_plugin_id": 1
          },
          "attribute_b": {
            "label": "BOND attribute B",
            "weight": 20,
            "description": "Some description",
            "type": "checkbox",
            "value": False,
            "bond_plugin_id": 1
          }
        }
      }
    }
  ]

In case of Node attributes, GET ``/nodes/:id/attributes/``:

.. code-block:: json

  {
    "cpu_pinning": {},
    "hugepages": {},
    "plugin_section_a": {
      "metadata": {
        "group": "some_new_section",
        "label": "Section A",
      },
      "attribute_a": {
        "label": "Node attribute A"
        "description": "Some description",
        "type": "text",
        "value": "test"
      },
      "attribute_b": {
        "label": "Node attribute B"
        "description": "Some description",
        "type": "checkbox",
        "value": False
      }
    }
  }


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

* NIC, BOND and Node attributes can be described in additional optional
  config yaml files.

* Basic skeleton description for NICs in ``nic_attributes`` yaml file:

  .. code-block:: yaml

    attribute_a:
      label: "NIC attribute A"
      description: "Some description"
      type: "text"
      value: ""
    attribute_b:
      label: "NIC attribute B"
      description: "Some description"
      type: "checkbox"
      value: false

  For Bond in ``bond_attributes`` yaml file:

  .. code-block:: yaml

    attribute_a:
      label: "Bond attribute A"
      description: "Some description"
      type: "text"
      value: ""
    attribute_b:
      label: "Bond attribute B"
      description: "Some description"
      type: "checkbox"
      value: false


  For Node in ``node_attributes`` yaml file:

  .. code-block:: yaml

    plugin_section_a:
      metadata:
        group: "some_new_section"
        label: "Section A"
      attribute_a:
        label: "Node attribute A for section A"
        description: "Some description"
        type: "text"
      attribute_b:
        label: "Node attribute B for section A"
        description: "Some description"
        type: "checkbox"

  Actually NICs and Nodes attributes should have similar structure as in
  ``openstack.yaml`` file.

* Fuel plugin builder should provide validation of schema for NICs and Nodes
  attributes in relevant config files if they exist.


Fuel Library
============

None


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

Provide migrations to transform NIC and Bond ``interface_properties`` into
``nic_attributes`` and ``bond_attributes`` respectively.


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

All the plugin NIC attributes will use the same UI representation as core
attributes, no direct UI impact. UI code should be adapted to work with
attributes instead of interface_properties.


------------------
Performance impact
------------------

None


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

None


--------------------
Documentation impact
--------------------

Describe in docs how plugin developers can provide additional NICs and Nodes
attributes via plugins.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  * Andriy Popovych <apopovych@mirantis.com>

Other contributors:
  * Anton Zemlyanov <azemlyanov@mirantis.com>

QA assignee:
  * Ilya Bumarskov <ibumarskov@mirantis.com>

Mandatory design review:
  * Aleksey Kasatkin <akasatkin@mirantis.com>
  * Vitaly Kramskikh <vkramskikh@mirantis.com>


Work Items
==========

* [Nailgun] Provide changes in DB model and new plugin config files sync.
* [Nailgun] Implement API handlers for Node default attributes.
* [Nailgun] Provide mixing for core and plugin Node attributes.
* [Nailgun] Provide serialization of plugin releated attributes for astute.
* [Nailgun network extension] Implement API handlers for Bond and default
  attributes.
* [Nailgun network extension] Provide mixing of core and plugin NICs and
  Bonds attributes and proper data storing.
* [Nailgun network extension] Change current API for NICs to support plugin
  attributes.
* [Nailgun network extension] Refresh NICs attributes with default data.
* [UI] Handle plugin Bond, NICs and Nodes attributes on ``Node`` details
  dialog and ``Configure Interfaces`` screens.
* [FPB] Templates and validation for optional yaml files: ``nic_attributes``,
  ``bond_attributes`` and ``node_attributes``.


Dependencies
============

* Plugins v5 [1]_
* Based on implementation of Node attributes [2]_
* Based on network manager extension [3]_


------------
Testing, QA
------------

* Extend TestRail with WEB UI cases for the configuring NIC, Bond and Node
  attributes.
* Extend TestRail with API/CLI cases for the configuring NIC, Bond and Node
  attributes.
* Manually test that FPB provide validation for additional attributes in
  relevant config files


Acceptance criteria
===================

* Plugin developers can provide new attributes per network interface, bond
  and node via plugin.


----------
References
----------

.. [0] https://github.com/openstack/fuel-web/blob/stable/mitaka/nailgun/nailgun/fixtures/openstack.yaml#L378-L409
.. [1] https://blueprints.launchpad.net/fuel/+spec/plugins-v5
.. [2] https://blueprints.launchpad.net/fuel/+spec/support-numa-cpu-pinning
.. [3] https://blueprints.launchpad.net/fuel/+spec/network-manager-extension
