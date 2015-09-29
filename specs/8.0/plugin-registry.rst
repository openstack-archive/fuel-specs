..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============
Plugin registry
===============

https://blueprints.launchpad.net/fuel/+spec/plugin-registry

Implement mechanism of compatibility between plugins.

--------------------
Problem description
--------------------

Currently when Fuel plugins provide deployment scenarios to install some
components for OpenStack Compute, Network or Storage parts there is no
way to check compatibility between them which causes fail of deployment
process or broken OpenStack environment in the end. For instance: in future
we want to have multi-networking functionality but not all Network core
plugins like Contrail can be combined via ML2 so we need restrict available
options before deployment. Another example: we have cinder-vmware as Storage
backend component which works only when ESX provided. In such case we should
restrict this option if inappropriate hypervisor was chosen.


----------------
Proposed changes
----------------

Plugin developers should be able to describe plugin compatibilites in context
of subtypes. For example: some plugin provide new Network type and compatible
only with hypervisor core plugins (KVM, QEMU) or only with vmware (ESX).

Nailgun
-------

Data model
``````````

Compatibility between plugins should be shown explicitly. To avoid direct
compatible relation between specific plugins we can group them in sets (or
subtypes) and then working in context of compatibility between subtypes. Such
aproach decrease dimension of compatibility matrix (K-map matrix) which
represents compatible relations. For example current list of subtypes can
be next (in future may be extended):

  * hypervisor:core
  * hypervisor:vmware
  * network:core
  * network:ml2
  * storage:object:backend
  * storage:block:backend
  * storage:image:backend
  * monitoring:core

Compatibility matrix can be next (some subtypes skipped for simplifying):

+-----------+-----------+-----------+-----------+-----------+-----------+
|           |hypervisor:|hypervisor:|network:   |network:ml2|monitoring:|
|           |core       |vmware     |core       |           |core       |
+-----------+-----------+-----------+-----------+-----------+-----------+
|hypervisor:|           |           |           |           |           |
|core       |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+
|hypervisor:|           |           |           |           |           |
|vmware     |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+
|network:   |           |           |     X     |     X     |           |
|core       |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+
|network:ml2|           |           |     X     |           |           |
|           |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+
|monitoring:|           |           |           |           |           |
|core       |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+

From this representation we can see that network:core plugins like Contrail
not compatible with others netwroking types. For DVS ML2 plugin we can show
that it's compatible only for hypervisor:vmware and so on.

Plugin should have ability to modify wizard tab like it already done for
settings page and describe new options in format similar to openstack.yaml.
Restrictions for this options should generates automatically and based on
compatibility matrix which represented in plugin metadata (look section
Plugins below).

Modifying of Wizard tab can be done through mixing of release wizard metadata
and plugin wizard metadata for all plugins compatible with chosen release. Mix
should be done in recursive way. For example release wizard networking section
can looks like:

.. code-block:: yaml

  Network:
    manager:
      type: "radio"
      values:
        - data: "neutron-vlan"
          label: "Neutron VLAN"
          restrictions:
            - "some_restriction_here"
          bind:
            - "cluster:net_provider": "neutron"
            - "cluster:net_segment_type": "vlan"

Plugin provides additional network type like Contrail (NOTE: actually Nailgun
can handle only limited list of network types so it may be 'neutron' + 'vlan'
with additional 'neutron-contrail' flag)

.. code-block:: yaml

  Network:
    manager:
      type: "radio"
      values:
        - data: "neutron-contrail"
          label: "Neutron with contrail"
          restrictions:
            - "some_restriction_here"
          bind:
            - "cluster:net_provider": "neutron"
            - "cluster:net_segment_type": "vlan"
            - "settings:contrail.value": true

So on output we should get something like this:

.. code-block:: yaml

  Network:
    manager:
      type: "radio"
      values:
        - data: "neutron-vlan"
          label: "Neutron VLAN"
          restrictions:
            - "some_restriction_here"
          bind:
            - "cluster:net_provider": "neutron"
            - "cluster:net_segment_type": "vlan"
        - data: "neutron-contrail"
          label: "Neutron with contrail"
          restrictions:
            - "some_restriction_here"
          bind:
            - "cluster:net_provider": "neutron"
            - "cluster:net_segment_type": "vlan"
            - "settings:contrail.value": true

In case of concurrent changes: each 'data' attribute in radio values can
be checked during plugin certification to avoid duplication. Such approach
gives unique radio options for each plugin.

If plugin enables in Wizard then it should be enabled on Setting tab also.
This can be achive in next way: default attributes metadata for release can
be extend with all compatible plugins like it done now when we get cluster
releated attributes:

.. code-block:: json

    editable : {
        ...
        'contrail': {'value': false},
        'test_plugin': {'value': false}
    }

And then ``value`` should be changed to true only for some of them which was
chosen on Wizard tab.

Nailgun DB tables changes:

=========  ====================================================
  Table    Operation
=========  ====================================================
 plugins   Add new column ``wizard_metadata`` of ``JSON`` type
=========  ====================================================


REST API
````````
There will be a new API call for getting mixed wizard metadata for release
and all compatible plugins with it.

===== ========================================= ==============================
HTTP  URL                                       Description
===== ========================================= ==============================
GET   /api/v1/releases/<id>/wizard/             Get mixed with plugins wizard
                                                config for specific release
===== ========================================= ==============================

The response format:

.. code-block:: json

    {
        "mode": {},
        "compute": {},
        ...
        "ready": {}
    }


Web UI
------

UI should support calls for new WizardHandler. It's part of 'Extend Wizard'
blueprint [1]_


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

To describe compatibilities between components plugin metadata yaml
file can be extended with additional structure like:

.. code-block:: yaml

  provides:
    - name: 'hypervisor:xen'
      compatible_hypervisors: ['all']
      compatible_networking: ['core']
      compatible_storages: ['all']
      compatible_monitoring: ['all']
    - name: 'networking:core:contrail'
      compatible_hypervisors: ['core']
      compatible_storages: ['all']
      compatible_monitoring: ['all']

NOTE: Data described in structure above shows concept and does not claim to
reality.

In this example plugin provides additional component for Compute (new
hypervisor Xen) and new Network (Contrail). There are can be many components
in 'provides' list but usually plugin has only one. Each component has 5 keys:

* name - has next pattern: type:subtype:specific_name. 'type' can be one of [
  'hypervisor', 'networking', 'storage', 'monitoring', 'additional_service']
  similar to what we have on wizard tab. 'subtype' mark provided component in
  plugin with more specific tag for example: 'core', 'object', 'block',
  'ml2:mech', etc. 'specific_name' uses when 'provides' have more then one
  item in other case it's optional and plugin name can replace this attribute.
  Example: 'networking:ml2:mech:arista' - here type is 'networking',
  subtype is 'ml2:mech' and specific_name is 'arista'.

* compatible_hypervisors - if not exist means that plugin component not
  compatible with any other components from this type. If 'all' then
  compatible with all in other case compatible only with some group(subtype)
  of components

* compatible_networking - same as for compatible_hypervisors

* compatible_storages  - same as for compatible_hypervisors

* compatible_monitoring - same as for compatible_hypervisors

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

N/A


--------------------------------
Infrastructure/operations impact
--------------------------------

N/A


--------------------
Documentation impact
--------------------

There are should be documented notes how plugin developers can modify wizard
tab for their needs.


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

* [Nailgun] Extend the ``Plugin`` database model and plugin sync method to
  store wizard into DB.

* [Nailgun] Implement functionality for proper mixing plugin wizard
  metadata with related release wizard and WizardHandler which returns this
  data.

* [Nailgun] Implement mechanisme for generation restrictions based on
  compatiblity matrix for wizard options which provided by plugins.

* [FPB] Provide additional validation for new structure in plugin metadata
  file.

* [FPB] Change default template skeleton for wizard metadata file generation.
  This file can be optional.



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

[1] https://blueprints.launchpad.net/fuel/+spec/extend-wizard-via-plugin
