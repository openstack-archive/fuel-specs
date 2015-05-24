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
directly describe deployment tasks for role. At last but not at least
we need implement network type role as plugin(custom network roles
will be implemented in context of [1]_).

Proposed change
===============

* Give the possibility for plugin developers introduce new custom node
  role through plugin such as already done for attributes.

* Provide disk volume partitions for node role in plugin

* Describe deployment tasks in specific order for current role

* Different plugins should support roles compatibility between each
  other and limitation for count of nodes.

Alternatives
------------

N/A

Data model impact
-----------------

Plugins node roles should be related to environment as core roles,
and have same format, so they will be directly mapped on `node_roles`
model which give us more flexibility then store them as JSON data. But
we need to know which roles are core and which come as plugin to be
able show proper roles set for cluster when some plugins are disabled.


Nailgun DB tables changes:

New relation table `plugin_roles` will be described

**PluginRoles**

* `id` - unique identifier
* `plugin_id` - relation key for plugin
* `role_id` - relation key for role

**NodeRoles**

* `is_plugin` - boolean flag to identify plugin role

**Cluster**

* `attributes` - plugin attributes data
* `volumes` - plugin volumes data


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

From Fuel web UI side:

If the plugin is enabled for cluster on setting tab, then user can
select plugin role from roles list on nodes tab and attach it to
specific nodes and vice versa it shouldn't be displayed in roles list
when the plugin is disabled for the cluster (environment)

If user want to disable plugin but have some nodes with this plugin
role in cluster then dialog should popup with message like this:
"Nodes [XXX, YYY] have plugin role attach, do you really want disable
plugin? Plugin role on all nodes will be detached in this case". If
node have only one role and it's plugin role then node will be
returned to unallocated set.

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
          items:
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
  networking [1]_. For example some models like `roles` can be changed
  to `node_roles`.

* It can affect plugin separate service [3]_. In current specification
  we describe realization of integration plugins in fuel through db
  wrappers for each entity such as role and volume (look work items
  section). This logic can be encapsulated in plugin service and
  provide some REST API for nailgun.

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
  wrapper around db model we need such wrappers for roles and volumes
  As alternative this plugin managing mechanism can be implemented
  in context of separate plugin service [3]_. During of installation
  process, plugin role extend core roles.

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
