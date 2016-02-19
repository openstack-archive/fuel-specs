..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================================
Support extensions of NIC and Node attributes in plugins
========================================================

https://blueprints.launchpad.net/fuel/+spec/nics-and-nodes-attributes-via-plugin

Plugin developer should be able to extend NIC and Node properties
via plugin.

-------------------
Problem description
-------------------

Plugins should have mechanizm for providing additional interfaces(NICs and
bonds) and Nodes attributes. In future it can be useful when plugin provides
some technology which should work "per interface" or "per node". For example:
in case of Contrail we need support VF for vRouter on each network interface.


----------------
Proposed changes
----------------

Web UI
======

* UI should properly represent schema and data for NIC, BOND and Node
  attributes provided by plugin on `Configure Interfaces` and `Node`
  screens.

* For rendering core and plugin NIC and BOND attributes client can receive
  actual metadata by '/api/v1/releases/<:id>/metadata/' API call and data
  from `/nodes/:id/interfaces/`.

* In case of plugin Node attributes they should be returned with core Node
  attributes.

* `Load defaults` button on `Configure Interfaces` screen should return
  default plugin NIC data per interface.


Nailgun
=======

Data model
----------

Plugin releated information with NICs, BONDs and Nodes default attributes will
be stored in `nic_attributes_metadata`, `bond_attributes_metadata` and
`node_attributes_metadata` attributes of Plugin model (Can be changed based on
Plugins v5 spec [1]_).

Additional models `NodeNICInterfacePlugin`, `NodePlugin` and
`NodeBondInterfacePlugin` will be used to store actual state of plugin NICs,
BONDs and Nodes attributes data per each interface, bond or node. By default
they should be filled with 'value' data from plugin `nic_attributes_metadata`,
`bond_attributes_metadata`(it has different structure of DSL, look `Plugin
section` in spec) and copied data from `node_attributes_metadata`.

New default core attributes for NIC and BOND should be described in
`openstack.yaml` file. They will be mapped on `nic_attributes` and
`bond_attributes` in Release.

`/nodes/:id/interfaces/` API call should return `interface_properties` and
`bond_properties` mixed with data from NodeNICInterfacePlugin and
NodeBondInterfacePlugin `attributes` respectively.


Node `attributes` will be mixed with NodePlugin `attributes` based on info
about enabled|disabled state of plugins and will be returned in
`/nodes/:id/attributes/` API call.

If plugin doesn't provide NIC, BOND or Node additional attributes then
relations with empty `attributes` shouldn't exist.

Nailgun DB tables changes:

**Plugin**

`nic_attributes_metadata`
plugin attributes data taken from `nic_config` yaml

`bond_attributes_metadata`
plugin attributes data taken from `bond_config` yaml

`node_attributes_metadata`
plugin attributes data taken from `node_config` yaml

**NodeNICInterfacePlugin**

`id`
unique identifier

`attributes`
actual state of plugin NIC attributes data

`cluster_plugin_id`
foreign key on plugins table

`interface_id`
foreign key on node_nic_interfaces table

`node_id`
foreign key on nodes table

**NodeBondInterfacePlugin**

`id`
unique identifier

`attributes`
actual state of plugin NIC attributes data

`cluster_plugin_id`
foreign key on plugins table

`bond_id`
foreign key on node_nic_interfaces table

`node_id`
foreign key on nodes table

**NodePlugin**

`id`
unique identifier

`attributes`
actual state of plugin Node attributes data

`cluster_plugin_id`
foreign key on plugins table

`node_id`
foreign key on nodes table

**Release**

`nic_metadata`
default attributes with empty values for NICs

`bond_metadata`
default attributes with empty values for BONDs

In future all plugin related data (API, models, etc.) can be rewritten as part
of nailgun extension.

Data from `attributes` in `NodeNICInterface`, `NodeNICInterfacePlugin`,
`NodeBondInterface`, `NodeBondInterfacePlugin`, `Node` and `NodePlugin` should
be serialized in deployment scenario and send to astute with other attributes.
This is how an astute.yaml part will look like for additional NIC attributes:

.. code-block:: yaml

  interfaces:
    enp0s1:
      vendor_specific:
        driver: e1000
        bus_info: "0000:00:01.0"
      interface_properties:
        plugin_a:
          attribute_a: "test"
          attribute_b: false
    enp0s2:
      vendor_specific:
        driver: e1000
        bus_info: "0000:00:02.0"
      interface_properties:
        plugin_a:
          attribute_a: "another_test"
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
        plugin_a:
          attribute_a: "test"
          attribute_b: true
      interface_properties:
        vendor_specific:
          disable_offloading: true
      action: add-bond

for Node attributes:

.. code-block:: yaml

  nodes:
    - uid: 1
      attributes:
        plugin_a:
          attribute_a: "test"
          attribute_b: false


REST API
--------

There will be new API call provided metadata for NIC and BOND.

===== ========================================= ============================
HTTP  URL                                       Description
===== ========================================= ============================
GET   /api/v1/releases/<:id>/metadata/          Get metadata for specific
                                                release and releated plugins
===== ========================================= ============================


The response format for GET `/api/v1/releases/<:id>/metadata/`:

.. code-block:: json

  {
    "nic_metadata": [
      {
        "name": "disable_offloading",
        "label": "Disable offloading",
        "type": "checkbox"
      },
      {
        "name": "mtu",
        "label": "MTU",
        "type": "text"
      },
      {
        "name": "plugin_a",
        "type": "object",
        "fields": [
          {
            "name": "attribute_a",
            "label": "NIC attribute A"
            "description": "Some description",
            "type": "text"
          },
          {
            "name": "attribute_b",
            "label": "NIC attribute B"
            "description": "Some description",
            "type": "checkbox"
          }
        ]
      }
    ],
    "bond_metadata": [
      {
        "name": "mode",
        "label": "Mode",
        "type": "select"
      },
      {
        "name": "plugin_a",
        "type": "object",
        "fields": [
          {
            "name": "attribute_a",
            "label": "Bond attribute A"
            "description": "Some description",
            "type": "text"
          }
        ]
      }
    ]
  }


In case of additional NIC and BOND attributes, GET `/nodes/:id/interfaces/`
method should return data with the following structure:

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
      "interface_properties": {
        "disable_offloading": False,
        "mtu": null,
        "plugin_a": {
          "attribute_a": "test_nic",
          "attribute_b": False
        }
      },
      "offloading_modes": [],
      "pxe": False,
      "bus_info": "0000:01:00.0",
    },
    {
      "type": "bond"
      "name": "bond0",
      "state": null,
      "assigned_networks": [],
      "bond_properties": {
        "type__": "linux",
        "mode": "balance-rr",
        "plugin_a": {
          "attribute_a": "test_bond"
        }
      },
      "mac": null,
      "mode": "balance-rr",
      "slaves": [],
      "interface_properties": {
        "disable_offloading": true,
        "mtu": 5000,
        "plugin_a": {
          "attribute_a": "test_nic",
          "attribute_b": False
        }
      },
      "offloading_modes": [],
    }
  ]

In case of Node attributes, GET `/nodes/:id/attributes/`:

.. code-block:: json

  {
    "cpu_pinning": {},
    "hugepages": {},
    "plugin_a": {
      "section_a": {
        "metadata": {
          "group": "some_new_section"
          "label": "Section A"
        },
        "attribute_a": {
          "label": "NIC attribute A"
          "description": "Some description",
          "type": "text",
          "value": "test"
        },
        "attribute_b": {
          "label": "NIC attribute B"
          "description": "Some description",
          "type": "checkbox",
          "value": False
        }
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
  config yaml files which will be integrated in Nailgun. NIC and BOND
  DSL has different format from others. It has separated metadata and
  value data.

* Basic skeleton description for NICs in `nic_config` yaml file:

  .. code-block:: yaml

    metadata:
      attribute_a:
        label: "NIC attribute A"
        description: "Some description"
        type: "text"
      attribute_b:
        label: "NIC attribute B"
        description: "Some description"
        type: "checkbox"
    value:
      attribute_a: ""
      attribute_b: false

  For Bond in `bond_config` yaml file:

    .. code-block:: yaml

      metadata:
        attribute_a:
          label: "Bond attribute A"
          description: "Some description"
          type: "text"
        attribute_b:
          label: "Bond attribute B"
          description: "Some description"
          type: "checkbox"
      value:
        attribute_a: ""
        attribute_b: false

  For Node in `node_config` yaml file:

  .. code-block:: yaml

    section_a:
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
  `openstack.yaml` file.

* New specific DSL boolean attrbiute `multiconfiguration` which means that
  current plugin NIC or BOND or Node attribute is global for all instances.

* Fuel plugin builder should provide validation of schema for NICs and Nodes
  attributes in relevant config files if they exist.


Fuel Library
============

None


------------
Alternatives
------------

Fuel core NIC, BOND and Node `attributes` [0]_ can be stored in
`attributes` field in each related table. Core NICs `attributes` will be
filled with default attributes from Release which are taken from
`nic_attributes` and merged with `interface_properties` data as values. Data
from NodeNICInterfacePlugin `attributes` will be mixed with NodeNICInterface
`attributes` based on info about disabled or enabled state of plugins during
`/nodes/:id/interfaces/` API call.

Instead of models `NodeNICInterfacePlugin`, `NodeBondInterfacePlugin` and
`NodePlugin` we can use one model with similar structure but additional
attribute `type`. This attributes will contain 'node', 'nic' or 'bond' value
of relation type.

Data from `nic_config` and `bond_config` yaml files can be described in one
file.


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

Mandatory design review:
  * Igor Kalnitsky <ikalnitsky@mirantis.com>
  * Evgeniy L <eli@mirantis.com>
  * Vitaly Kramskikh <vkramskikh@mirantis.com>


Work Items
==========

* [Nailgun] Provide changes in DB model and new plugin config files sync.
* [Nailgun] Provide mixing of core and plugin NICs and Nodes attributes
  and proper data storing.
* [Nailgun] Refresh NICs and Nodes attributes with default data.
* [Nailgun] Provide serialization of plugin releated attributes for astute.
* [UI] Handle plugin NICs and Nodes attributes on `Node` and
  `Configure Interfaces` screens.
* [FPB] Templates and validation for optional yaml files: `nic_config`
  and `node_config`


Dependencies
============

* Based on implementation of Node attributes [0]_
* Plugins v5 [1]_


------------
Testing, QA
------------

TBD


Acceptance criteria
===================

* Plugin developers can provide new attributes per network interface, bond
  and node via plugin.


----------
References
----------

.. [0] https://blueprints.launchpad.net/fuel/+spec/support-numa-cpu-pinning
.. [1] https://blueprints.launchpad.net/fuel/+spec/plugins-v5
