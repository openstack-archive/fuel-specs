..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================================
Support extensions of NIC and Node attributes in plugins
========================================================

https://blueprints.launchpad.net/fuel/+spec/example

Plugin developer should be able to extend NIC and Node properties
via plugin.

-------------------
Problem description
-------------------

Plugins should have mechanizm for providing additional NICs and Nodes
attributes. In future it can be useful when plugin provides some technology
which should work "per interface" or "per node". For example: in case of
Contrail we need support VF for vRouter on each network interface.


----------------
Proposed changes
----------------

Web UI
======

* UI should proper represent schema and data for NIC and Node attributes
  provided by plugin on `Configure Interafaces` and `Node` screens.

* `Load defaults` button on `Configure Interfaces` screen should return
  default plugin NIC data per interface.


Nailgun
=======

Data model
----------

Plugin releated information with NICs and Nodes default attributes will be
stored in `nic_attributes_metadata` and `node_attributes_metadata` attributes
of Plugin model. Additional models `PluginNodeNICInterface` and `PluginNode`
will be used to store actual state of plugin NICs and Nodes attributes data
per each interface or node. By default they should be filled with data from
plugin `nic_attributes_metadata` and `node_attributes_metadata`. Fuel core
NICs `interface_properties` and Node `attributes` [0]_ will be mixed with
data from `PluginNodeNICInterface` and `PluginNode` based on info about
disabled/enabled state of plugins during `/nodes/:id/interfaces` and
`/nodes/:id/attributes` API calls.

If plugin doesn't provide NIC or Node additional attributes then relations
with empty `attributes` shouldn't exist.

Nailgun DB tables changes:

**Plugin**

`nic_attributes_metadata`
plugin attributes data taken from `nic_config` yaml

`node_attributes_metadata`
plugin attributes data taken from `node_config` yaml


**PluginNodeNICInterface**

`id`
unique identifier

`attributes`
actual state of plugin NIC attributes data

`plugin_id`
foreign key on plugins table

`node_nic_interface_id`
foreign key on node_nic_interfaces table


**PluginNode**

`id`
unique identifier

`attributes`
actual state of plugin Node attributes data

`plugin_id`
foreign key on plugins table

`node_id`
foreign key on nodes table


Data from `attributes` in `PluginNodeNICInterface` and `PluginNode` should
be serialized in deployment scenario and send to astute with other attributes.


REST API
--------

TBD


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

* NIC and Node attributes can be described in additional optional
  config yaml files which will be integrated in Nailgun.

* Basic skeleton description for NICs in `nic_config` yaml file:

  .. code-block:: yaml

    attribute_a:
      label: "NIC attribute A"
      description: "Some description"
      type: "text"
    attribute_b:
      label: "NIC attribute B"
      description: "Some description"
      type: "checkbox"

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

  Actually NICs and Nodes attributes can have similar structure as in
  `openstack.yaml` file.

* Fuel plugin builder should provide validation of schema for NICs and Nodes
  attributes in relevant config files if they exist.


Fuel Library
============

None


------------
Alternatives
------------

Instead of two models `PluginNodeNICInterface` and `PluginNode` we can use one
model with similar structure but additional attribute `type`. This attributes
will contain 'node' or 'nic' value of relation type.


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
  TBD


Work Items
==========

* [Nailgun] Provide changes in DB model.
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


------------
Testing, QA
------------

TBD


Acceptance criteria
===================

TBD


----------
References
----------

.. [0] https://blueprints.launchpad.net/fuel/+spec/support-numa-cpu-pinning
