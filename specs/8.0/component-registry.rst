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
cinder-vmware as Storage backend component or NSX network type plugin which
works only when ESX provided. In such case we should disable this options
if only inappropriate hypervisors like KVM was chosen.

----------------
Proposed changes
----------------

New entity called 'component' will be introduced. This abstraction shows which
part of OSt current plugin extend. According to this definition, component can
be one of next types:

* Hypervisor - extends OpenStack Compute part
* Network- extends OpenStack Networking part
* Storage - extends OpenStack Storage part
* Additional Service - extends other OpenStack parts (Murano, Sahara, etc.)

Plugin developers could and must specify compatibility matrix between
components, so one component could be compatible with a limited set of other
ones. It can be done through mechanism of subtypes. For example: some plugin
provide new Network type component which compatible only with core hypervisor
like (KVM, QEMU) or only with vmware (ESXi). Plugin can extend different parts
of OSt so it can provide many components but they must be compatible and
depend on each other for logical consistency. In other case components should
be provided by different plugins.

Nailgun
-------

Data model
``````````

Compatibility between components should be shown explicitly. To avoid direct
compatible relation between specific component we can group them in sets (or
subtypes) and then working in context of compatibility between subtypes. Such
aproach decrease dimension of compatibility matrix (K-map matrix) which
represents compatible relations. For example current list of subtypes can
be next (in future may be extended):

  * hypervisor:libvirt:kvm
  * hypervisor:libvirt:qemu
  * hypervisor:hyperv
  * hypervisor:vmware
  * hypervisor:xen
  * network:nova
  * network:neutron:core:ml2:ovs
  * network:neutron:core:ml2:dvs
  * network:neutron:core:ml2:linux_bridge
  * network:neutron:core:ml2:sr_iov
  * network:neutron:core:ml2:brocade
  * network:neutron:core:ml2:cisco
  * network:neutron:core:ml2:mellanox
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
  * storage:object:backend:ceph
  * storage:object:backend:gluster
  * storage:object:backend:sheepdog
  * storage:block:backend:ceph
  * storage:block:backend:nfs
  * storage:block:backend:lvm
  * storage:block:backend:zfs
  * storage:image:swift
  * storage:image:ceph
  * additional_services:sahara
  * additional_services:murano
  * additional_services:ceilometer

Compatibility matrix can be next (some subtypes skipped for simplifying):

+----------------+----------------+----------------+----------------+
|                |hypervisor:     |network:neutron:|network:neutron:|
|                |libvirt         |core:contrail   |core:ml2:       |
+----------------+----------------+----------------+----------------+
|hypervisor:     |                |                |                |
|libvirt         |                |                |                |
+----------------+----------------+----------------+----------------+
|network:neutron:|                |                |        X       |
|core:contrail   |                |                |                |
+----------------+----------------+----------------+----------------+
|network:neutron:|                |        X       |                |
|core:ml2        |                |                |                |
+----------------+----------------+----------------+----------------+

NOTE: In this representation incompatibility between elements marked as 'X'


From this matrix we can see that Contrail network type incompatible with
any ML2 type plugin. For DVS ML2 plugin we can show that it's compatible
only for hypervisor:vmware and so on. Another example: if user not choose
vCenter as compute platform then cinder-vmware Storage backend should be
disabled. In such case we can say that cinder-vmware Storage compatible
only with VMware vCenter Compute part.


All components chosen in Wizard tab should be enabled on Setting tab also.
This can be achieved in next way: wizard data populates with enabled options
and sends back to nailgun API. With this options we can find proper plugin
in CompatibilityMatrix table and extend ClusterAttributes data with it and
set flag for enabling on Settings tab.

releated attributes:

.. code-block:: json

    editable : {
        ...
        'contrail': {'value': true},
        'test_plugin': {'value': true}
    }


Nailgun DB changes:

**Component**

* `id` - unique identifier
* `name` - unique string component name
* `type` - one of 'hypervisor'|'network'|'storage'|'additional_component'
* `hypervisors` - array of compatible Compute subtypes
* `networks` - array of compatible Network subtypes
* `storages` - array of compatible Storage subtypes
* `additional_services` - array of compatible Additional Services subtypes
* `plugin_id` - foreign key on plugin table

**ComponentRelease**

* `component_id` - foreign key on component table
* `release_id` - foreign key on release table


REST API
````````
There will be a new API call for getting JSON data of compatible components
for release and all plugins releated with it.

===== ========================================= ===========================
HTTP  URL                                       Description
===== ========================================= ===========================
GET   /api/v1/releases/<id>/components/         Get compatible matrix data
                                                for specific release
===== ========================================= ===========================

The response format:

.. code-block:: json

    [
        {
          "name": "core:contrail",
          "type": "network",
          "plugin_id": 1,
          "releases_ids": [],
          "compatible": {
            "hypervisors": ["libvirt"],
            "networks": [],
            "storages": "*",
            "additional_services": "*"
          }
        },
        {
          "name": "libvirt:kvm",
          "type": "hypervisor",
          "plugin_id": null,
          "releases_ids": [1],
          "compatible": {
            "hypervisors": "*",
            "networks": "*",
            "storages": "*",
            "additional_services": "*"
          }
        },
        {
          "name": "core:test_net",
          "type": "network",
          "plugin_id": 2,
          "releases_ids": [],
          "compatible": {
            "hypervisors": ["libvirt:kvm"],
            "networks": [],
            "storages": "*",
            "additional_services": "*"
          }
        },
        ...
    ]

Here "hypervisors": ["libvirt"] means that Contrail compatible with both
KVM and QEMU and some TestNet only with KVM.

Web UI
------

UI should support calls for new ComponentHandler. It can be part of
'Extend Wizard' blueprint [0]_


Orchestration
-------------

N/A


RPC Protocol
````````````

N/A


Fuel Client
-----------

TODO


Plugins
-------

To describe compatibilities between components, new yaml file called
'components' will be provided with additional structure:

.. code-block:: yaml

  - type: 'hypervisor'
    name: 'xen'
    compatible:
      hypervisors: ['*']
      networks: ['core']
      storages: ['*']
  - type: 'network'
    name: 'core:contrail'
    compatible:
      hypervisors: ['core']
      storages: ['*']

NOTE: Data described in structure above shows concept and does not claim to
reality.

In this example plugin provides additional component for Compute (new
hypervisor Xen) and new Network (Contrail). There are can be many components
in 'provides' list but usually plugin has only one. Each component can has 3
keys:

* type - can be one of ['hypervisor', 'network', 'storage',
  'additional_service'] similar to what we have on wizard tab.

* name - has next pattern: subtype:specific_name. 'subtype' mark provided
  component in plugin with more specific tag for example: 'core', 'object',
  'block','core:ml2', etc. 'specific_name' - concreate name of component like
  'contrail' Example: 'core:ml2:arista' - subtype is 'core:ml2:' and
  specific_name is 'arista'.

* compatible - section which describes compatibility between different types:

  # `hypervisors` - if not exist means that plugin component not
    compatible with any other components from this type. If '*' then
    compatible with all in other case compatible only with some group(subtype)
    of components

  # `networks` - same as for hypervisors

  # `storages`  - same as for hypervisors

  # `additional_services`  - same as for hypervisors


Also plugin version in metadata.yaml should be changed to 4.0.0


Fuel Library
------------

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


--------------------------------
Infrastructure/operations impact
--------------------------------

N/A


--------------------
Documentation impact
--------------------

Fuel Plugin SDK should describe the metadata which required for compatibility
matrix.


--------------------
Expected OSCI impact
--------------------

N/A


--------------
Implementation
--------------

Assignee(s)
-----------

Primary assignee:
  * Andriy Popovych <apopovych@mirantis.com>
  * Elena Kosareva <ekosareva@mirantis.com>

Mandatory design review:
  * Igor Kalnitsky <ikalnitsky@mirantis.com>


Work Items
----------

* [Nailgun] Provide component model and loading fixture for core components

* [Nailgun] Sync plugin metadata for compatibility matrix into DB

* [Nailgun] Implement functionality for retriving compatibility matrix
  through API.

* [Nailgun] Refactor functionality for support new wizard config

* [FPB] Generate new templates for plugins version 4.0.0 and provide additional
  validation of correctness for new structure which describes compatibility of
  plugin component in metadata file.


Dependencies
------------

N/A


------------
Testing, QA
------------

TBA


Acceptance criteria
-------------------

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