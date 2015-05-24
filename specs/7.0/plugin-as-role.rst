..
 This work is licensed under a Creative Commons Attribution 3.0 Uported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Define a new role in Fuel through a plugin
==========================================

https://blueprints.launchpad.net/fuel/+spec/role-as-a-plugin

Implement possibility to describe specific node roles in plugin

Problem description
===================
Currently only 'base-os' role can be declarative described in plugin
which makes problems with identification of specific role on
fuel-library side. Also plugins can't provide disk partition and
describe new network-type role(custom network roles will be
implemented in context of [1]_).


Proposed change
===============

* Give the possibility for plugin developers introduce new custom node
  role through plugin such as already done for attributes. Plugin node
  role should be related to specific environments not to releases, for
  example from UX side: if the plugin is enabled in cluster, then user
  can select plugin role from roles list and attach it to nodes and
  vice versa it shouldn't be displayed in roles list when the plugin is
  disabled for the cluster (environment)

* Provide volume partitions for node role in plugin

* Describe deployment tasks in specific order for current role



Alternatives
------------

New roles can be created directly through CLI

Data model impact
-----------------

There is at least two ways of data model representation:

1. Plugin node roles directly mapped on `node_roles` model. But we
need to know which roles are core and which come as plugin. (more
acceptable)

2. Separate entities for plugins node roles and core roles
which generate duplications in data models.


Nailgun DB tables changes for 1st option:

New relation table `plugin_roles` will be described

**PluginRoles**

* `id` - unique identifier
* `plugin_id` - relation key for plugin
* `role_id` - relation key for role

**NodeRoles**

* `is_plugin` - boolean flag to identify plugin role


REST API impact
---------------

None


Upgrade impact
--------------

Migration of schema should be provided to support previously created
environments

Security impact
---------------

N/A

Notifications impact
--------------------

N/A

Other end user impact
---------------------

None

Performance Impact
------------------

None

Plugin impact
-------------

* New node roles with volume partition info can be describe in
  environment_config.yaml (or as alternative in some roles.yaml)
  file which will be integrated in Nailgun

* Fuel plugin builder should automatically creates in yaml file new
  node role based on plugin name. Basic skeleton description for node
  role in yaml file:

  .. code-block:: yaml
    role_name:
      metadata:
        name: "Some plugin role"
        description: "Some description"
        conflicts:
          - some_not_compatible_role
        limits:
          min: 1
        restrictions:
          - condition: "some logic condition"
            message: "Some message for restriction warning"
      volumes_mapping:
        - {allocate_size: "min", id: "os"}
        - {allocate_size: "all", id: "role_volume_name"}
      volumes:
        - id: "role_volume_name"
          type: "vg"
          min_size: {generator: "calc_min_os_size"}
          label: "Role specific volume"
          volumes:
            - mount: "/"
              type: "lv"
              name: "root"
              size: {generator: "calc_total_root_vg"}
              file_system: "ext4"
            - mount: "swap"
              type: "lv"
              name: "swap"
              size: {generator: "calc_swap_size"}
              file_system: "swap"

  Also all basic types of volumes, limits, allocate_sizes, size
  generators needs be noticed in plugin user guide.


Other deployer impact
---------------------

None

Developer impact
----------------

* Data model impact for network type plugin role depends on advanced
  networking [1]_
* It can affect plugin separate service [3]_

Infrastructure impact
---------------------

None


Implementation
==============

Assignee(s)
-----------


Primary assignee:
  * ikalnitsky
  * popovych-andrey


Work Items
----------

* [Nailgun] Develop functionality of basic processing for node roles
  through existing plugin manager. Accordingly to plugin attributes
  wrapper around db model we need such wrappers for:
    - roles
    - volumes
  As alternative this plugin managing mechanism can be implemented
  in context of separate plugin service [3]_. During of installation
  process, plugin role extend core roles and related to it volume data
  merged into release volumes metadata.

* [Nailgun] Change DB schema to suppport plugin roles

* [FPB] Change default template skeleton which will describe basic
  metadata info for role.



Dependencies
============

* Advanced networking [1]_
* Volume partition functionality [2]_
* Separate plugin service [3]_
* Task based deployment


Testing
=======

Nailgun unit tests
Nailgun integration tests
FPB unit tests


Documentation Impact
====================

We should have documented notice which help plugin developers describe
new role in plugin.


References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/granular-network-functions
.. [2] https://blueprints.launchpad.net/fuel/+spec/volume-manager-refactoring
.. [3] https://blueprints.launchpad.net/fuel/+spec/plugin-manager-as-separate-service
