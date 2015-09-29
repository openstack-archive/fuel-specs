..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================
Component registry
==================

https://blueprints.launchpad.net/fuel/+spec/component-registry

Implement mechanism of compatibility between components in Fuel.

-------------------
Problem description
-------------------

Currently when Fuel plugins provide deployment scenarios to install some
components for OpenStack Compute, Network or Storage parts there is no
way to check compatibility between themselves (or with core components) which
causes fail of deployment process or broken OpenStack environment in the end.
For instance: in future we want to have multi-networking functionality but
not all Network core plugins like Contrail can be combined via ML2 so we need
to restrict available options before deployment. Another example: we have
NSX network type plugin which works only when ESX provided. In such case we
should disable this options if only inappropriate hypervisors like KVM was
chosen.

----------------
Proposed changes
----------------

New entity called 'component' will be introduced. This abstraction shows which
part of OpenStack current plugin extend. According to this definition,
component can be one of next types:

* Hypervisor - extends OpenStack Compute part
* Network- extends OpenStack Networking part
* Storage - extends OpenStack Storage part
* Additional Service - extends other OpenStack parts (Murano, Sahara, etc.)

Plugin developers can specify incompatibility matrix between components when
they defently in conflict and compatibility matrix when not. It can be done
through mechanism of subtypes. For example: some plugin provide new Network
type component which compatible only with core hypervisor like (KVM, QEMU) or
only with vmware (ESXi). Plugin can extend different parts of OpenStack so
it can provide many components but they must be not in incompatible state
and depend on each other for logical consistency. Also some components can
know nothing about compatiblity/incompatibility but requires other, for
example DVS requires vCenter.

Nailgun
=======

Data model
----------

Compatibility and inncompatibility and requires between components should be
shown explicitly.To avoid direct incompatible relation between specific
component we can group them in sets (or subtypes) and then working in context
of compatibility between subtypes. Such aproach decrease dimension of
compatibility matrix (K-map matrix) which represents incompatible relations.
For example current list of subtypes can be next (in future may be extended):

  * hypervisor:libvirt:kvm
  * hypervisor:libvirt:qemu
  * hypervisor:hyperv
  * hypervisor:vmware
  * hypervisor:xen
  * network:neutron:ml2:ovs
  * network:neutron:ml2:dvs
  * network:neutron:ml2:linux_bridge
  * network:neutron:ml2:sr_iov
  * network:neutron:ml2:brocade
  * network:neutron:ml2:cisco
  * network:neutron:ml2:mellanox
  * network:neutron:core:nsx
  * network:neutron:core:contrail
  * network:neutron:core:midonet
  * network:neutron:service:vpnaas
  * network:neutron:service:fwaas
  * network:neutron:service:lbaas
  * network:neutron:service:l3
  * network:neutron:service:l2
  * network:neutron:ipam:builtin
  * storage:object:backend:swift
  * storage:object:backend:gluster
  * storage:object:backend:sheepdog
  * storage:block:backend:nfs
  * storage:block:backend:lvm
  * storage:block:backend:zfs
  * storage:image:swift
  * storage:ceph
  * additional_service:sahara
  * additional_service:murano
  * additional_service:ceilometer

Сompatibility matrix can be next (some subtypes skipped for simplifying):

+----------------+----------------+----------------+----------------+
|                |hypervisor:     |network:neutron:|network:neutron:|
|                |libvirt         |core:contrail   |ml2             |
+----------------+----------------+----------------+----------------+
|hypervisor:     |        C       |        C       |        C       |
|libvirt         |                |                |                |
+----------------+----------------+----------------+----------------+
|network:neutron:|        C       |        C       |        X       |
|core:contrail   |                |                |                |
+----------------+----------------+----------------+----------------+
|network:neutron:|        C       |        X       |        C       |
|ml2             |                |                |                |
+----------------+----------------+----------------+----------------+

NOTE: In this representation incompatibility between elements marked as 'X'
and compatible as 'C'


From this matrix we can see that Contrail network type incompatible with
any ML2 type plugin. For DVS ML2 plugin we can show that it requires
hypervisor:vmware and so on. We follow next rule: if there are 3 components
A, B, C where A, B from one type(ex. hypervisor) and C from other(ex. network)
and C incompatible B then C incompatible A + B in any case. For instance:
NSX incompatible with KVM, so user can't use it for multi-HV case KVM +
vCenter. 'requires' attribute can work as follow: there is small number of
cases(if they even exist) when for some component requires two or more
components of same type. Another suggestion: usual component requires many
components in same time but with different types. So relation between elements
in 'requires' can be implicitly described as next: use OR for components of
same type and AND for components of different type. For example list
of components next:

.. code-block:: yaml

  - name: 'hypervisor:sub:A'
  - name: 'hypervisor:sub:B'
  - name: 'network:C'
  - name: 'network:D'
  - name: 'storage:C'
    requires: ['hypervisor:sub:A', 'hypervisor:sub:B', 'network:C']

Condition should be next: (A OR B) AND C

We can even use wildcard for hypervisor:

.. code-block:: yaml

  - name: 'storage:C'
    requires: ['hypervisor:sub:*', 'network:C']

Reuslt should be the same.

All components chosen in Wizard tab should be enabled on Setting tab also.
This can be achieved by enabling proper plugins based on [2]_ and for core
components by changing default cluster attributes with binded values.


Nailgun DB changes:

**Plugin**

`components_metadata`
JSON field with info about compatiblity/incompatibility between
plugin components

**Release**

`components_metadata`
JSON field with info about compatiblity/incompatibility between
release(or core) components

**Cluster**
`components`
JSON field with specific components for cluster


REST API
--------

There will be a new API call for getting JSON data of compatible components
for release and all plugins releated with it.

===== ========================================= ===========================
HTTP  URL                                       Description
===== ========================================= ===========================
GET   /api/v1/releases/<:id>/components/        Get components data
                                                for specific release
===== ========================================= ===========================

The response format for ``GET /api/v1/releases/<:id>/components/``:

.. code-block:: json

    [
      {
        "name": "network:core:contrail",
        "label" "Contrail",
        "description": "Contrail network",
        "weight": 10,
        "incompatible": [
            {
              "name": "hypervisor:vmware",
              "description": "Contrail not compatible with VMware for now"
            }
        ]
      },
      {
        "name": "hypervisor:libvirt:kvm",
        "label": "KVM",
        "description": "KVM hypervisor",
        "weight": 10,
        "incompatible": {
            {
              "name": "hypervisor:libvirt:qemu",
              "description": "KVM not compatible with QEMU"
            }
        }
      },
      {
        "name": "network:core:test_net",
        "label": "TestNet",
        "description": "Test network"
        "weight": 20,
        "compatible": [
          {"name": "hypervisor:xen"}
        ]
        "incompatible": [
          {
            "name": "hypervisor:libvirt:*",
            "message": "TestNet not compatible with libvirt type computes"
          }
        ]
      }
      ...
    ]

Here hypervisors:libvirt:* means that TestNet incompatible with both KVM and
QEMU. It's defently compatible with Xen hypervisor and we can say nothing
about compatiblity with vCenter so user can choose it on his own risk.

Cluster creation API should be changed for handling choosed components on
wizard tab.

The request format for ``POST /api/v1/clusters/``:

.. code-block:: json

  {
    id: 1,
    name: "Some cluster",
    components: [
      "hypervisors:kvm",
      "networks:neutron_vlan",
      "storages:ceph",
      "additional_services:murano"
    ],
    changes: [...],
    fuel_version: "8.0",
    is_customized: false,
    mode: "ha_compact",
    pending_release_id: null,
    release_id: 2,
    status: "new"
  }


Web UI
======

Algorithm of processing components is next:

Wizard tab uses new component API for retriving all components from nailgun.

Compute components will be checkboxes. It give us possiblity to choose multiple
hypervisors or only vCenter. For them we can describe incompatibilities between
hypervisors. For example we can use only KVM or QEMU but not both of them. So
we can say that KVM not compatible with QEMU and when KVM checked QEMU checkbox
element should be disabled and vice versa.

Currently network support only Neutron and Nova as depricated option. Neutron
has core plugins which are incompatible with each other and core ML2 plugin
which helps some specific plugins work together(like OVS, DVS, etc.). So nova
and neutron core components should be radio buttons. But under ML2 radio button
option we can group ML2 plugins options as checkboxes. If some ML2 component
not in incompatible state with previous choosen components and all requires
options(if they exist) enabled, this ML2 component also should be enabled for
checking. If all checkboxes under ML2 radio button disabled then it should be
also disabled. For example: we have OVS which requires KVM or QEMU and DVS
which requires vCenter then in case of multi-HV we can choose both.

Currently multi-storage backend is not supported. So storage components will
be displaed as radio buttons with hypervisor, network and storage components
in incompatible list.

Additional components should be checkboxes. Incompatible list can have all
types of components.

Every type can have compatible list or whitelist. It will be used to highlight
defently compatible components with 'green light'.

For disabled options we should have alerts with messages for user. In case of
'incompatible' options component has message and in case of 'requires' just
'Not all requires options enabled'. In future we enhance it to dynamically
generate informative text based on 'requires' elements relations.


Orchestration
=============

N/A


RPC Protocol
------------

N/A


Fuel Client
===========

TODO


Plugins
=======

To describe incompatiblities/requires between components, new yaml
file called 'components' will be provided with additional structure:

.. code-block:: yaml

  - name: 'hypervisor:xen'
    label: 'Xen'
    description: 'Xen hypervisor'

  - name: 'network:core:contrail'
    label: 'Contrail'
    description: 'Contrail network'
    incompatible:
      - name: 'hypervisor:vmware',
        description: 'Contrail not compatible with VMware for now'

  - name: 'network:ml2:dvs'
    label: 'DVS'
    description: 'Vmware DVS network'
    compatible:
      - name: 'hypervisor:vmware'
    requires: ['hypervisor:vmware']

NOTE: Data described in structure above shows concept and does not claim to
reality.

In this example plugin provides additional component for Compute (new
hypervisor Xen) and new Network (Contrail). There are can be many components
for plugin but usually it has only one. Each component can has follow keys:

* name - has next pattern: type:subtype:specific_name. 'type' - can be one of
  ['hypervisor', 'network', 'storage','additional_service'] similar to what we
  have on wizard tab.'subtype' mark provided component in plugin with more
  specific tag for example: 'core', 'object','block','core:ml2', etc.
  'specific_name' - concreate name of component like 'contrail' Example:
  'ml2:arista' - subtype is 'ml2' and specific_name is 'arista'.

* label - component label for UI.

* description - component descriptio for UI.

* compatible - section which describes compatiblity between different
  components through array of objects. Component object has attribute `name`
  which is similar to main component name. If `name` has * after type it
  means that component compatible with all subtypes for current type.

* incompatible - section which describes incompatibility between different
  components. As compatible sections it also provides array of component
  objects which have two attributes `name` and `msg` which describes why
  components are not compatible.

* requires - section which describes components which needed for component.
  For example: we can say nothing about incompatiblity DVS with KVM but
  vCenter should be present for success working.

Also plugin version in metadata.yaml should be changed to 4.0.0


Fuel Library
============

N/A


------------
Alternatives
------------

Keep notes about plugin compatibility in documentation for end users. In such
case they should manually handle combinations for possible plugins and core
components.


--------------
Upgrade impact
--------------

N/A


---------------
Security impact
---------------

N/A


--------------------
Notifications impact
--------------------

N/A


---------------
End user impact
---------------

N/A


------------------
Performance impact
------------------

N/A


-----------------
Deployment impact
-----------------

N/A


----------------
Developer impact
----------------

Multi-hypervisor and multi-networking case implements in context of [1]_


---------------------
Infrastructure impact
---------------------

N/A


--------------------
Documentation impact
--------------------

Fuel Plugin SDK should describe the metadata which required for compatibility
matrix.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  * Andriy Popovych <apopovych@mirantis.com>

Developers:
  * Elena Kosareva <ekosareva@mirantis.com>
  * Anton Zemlyanov <azemlyanov@mirantis.com>

Mandatory design review:
  * Igor Kalnitsky <ikalnitsky@mirantis.com>


Work Items
==========

* [Nailgun] Provide component entity and loading fixture for core components

* [Nailgun] Sync plugin metadata for compatibility matrix into DB

* [Nailgun] Implement logic for automatical enabling of plugins and settings
  based on components provided by wizard

* [UI] New wizard for support components

* [FPB] Generate new templates for plugins version 4.0.0 and provide additional
  validation of correctness for new structure which describes compatibility of
  plugin component in metadata file.

* [FPB] Example plugin for new version


Dependencies
============

N/A


------------
Testing, QA
------------

TBA


Acceptance criteria
===================

* Wizard can expose all options of a specific type (e.g. Networking,
  Compute, Cinder storage)

* Wizard can expose compatibility (and incompatibility) between selections
  (e.g. if vCenter is selected as only Compute option, then Contrail should
  not be a valid Networking option)

* Metadata required by plugins to self-define compatibility, type and
  sub-type has been defined and added to plugin SDK, shared with Partner
  Enablement team


----------
References
----------

.. [0] https://blueprints.launchpad.net/fuel/+spec/extend-wizard-via-plugin
.. [1] https://blueprints.launchpad.net/fuel/+spec/fuel-multiple-hv-networking
.. [2] https://blueprints.launchpad.net/fuel/+spec/store-plugins-attributes