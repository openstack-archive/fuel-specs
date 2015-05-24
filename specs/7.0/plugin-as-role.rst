..
 This work is licensed under a Creative Commons Attribution 3.0
 Unported License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Define a new role in Fuel through a plugin
==========================================

https://blueprints.launchpad.net/fuel/+spec/role-as-a-plugin

Implement possibility to describe new node roles in plugin

Problem description
===================
Currently there's no way to introduce new node roles through Fuel
plugins, but plugin developers want to. So they use a bunch of hacks
and workarounds:

  * run deployment on all nodes with 'base-os' role, but each
    task really runs if node name is equal to some pre-defined one

  * deploy some stuff as a part of either pre- or post-deployment tasks

  * can't noop some tasks so they remove what was done by conflicting
    task

  * can't use custom disk partitioning layout, so they use disk
    partitioning tools as a part of deployment

Proposed change
===============

* Add ability to declare new node roles in the similar way to
  openstack.yaml

* Add ability to declare disk partitioning strategy for new node roles
  in the similar way to openstack.yaml

* Add ability to declare deployment tasks for new node roles, not only
  pre-/post-deployment ones

* Add ability to overwrite existing tasks by ID

* Add ability to re-use tasks from other roles


Alternatives
------------

N/A

Data model impact
-----------------

List of `core` roles will be represented as set of keys from release
`roles_metadata` json type attribute.

Instead of attributes which belongs to cluster, volumes and roles
related to node. All core roles belong to release and plugin roles to
plugin entity accordingly.

Metadata for roles, volumes, tasks and attributes are taken from
plugin yaml config files and stored once in DB as plugin entity
attributes to avoid parsing from file many times. In process of
cluster configuration plugin metadata attributes will be merged with
metadata from release.

When node is to be added into cluster, UI requires full list of
allowed node roles which consist from core roles(contained in release)
and plugin roles(contained in `roles_metadata` attribute for each
enabled plugin in cluster).

Set of chosen specific roles are kept by each node in `pending_roles`
attribute. After role tasks processed successfully pending role will be
moved to `deployed_roles`. Process continues until `pending_roles`
contains any role which is not in `deployed_roles`.

General deployment tasks gets from release. Then for specific
cluster nailgun build deployment graph which based on general
deployment tasks and plugin deployment tasks related to cluster.

If two plugins overwrites the same task or export two tasks with same
id - then raise exception in case when roles from this plugins
assigned on the same node. But if they assigned on different nodes
deployment should pass successfully. Check tasks compatibility every
time when roles assigned on nodes will be overwhelmed for performance
so it can be run once before deployment.


Nailgun DB tables changes:

drop `roles` table
drop `node_roles` table
drop `pending_node_roles` table

**Plugin**

* `attributes_metadata` - plugin attributes data taken from
                          `environment_config` yaml
* `volumes_metadata` - plugin volumes data taken from `volumes` yaml
* `roles_metadata` - plugin roles data taken from `node_roles` yaml
* `deployment_tasks` - deployment tasks related to current plugin role
                       taken from `tasks` yaml

**Node**

* `pending_roles` - set of specific roles which need to be deployed
* `deployed_roles` - set of roles which already have been deployed

REST API impact
---------------

There will be new API call provided to sync changes for plugin configs

Role API will be the same but inner logic changed (Role model will be
removed).


Upgrade impact
--------------

Migration of schema should be provided to support previously created
environments. Plugins with old task format also will be supported.

Security impact
---------------

N/A

Notifications impact
--------------------

N/A

Other end user impact
---------------------

From Fuel web UI side:

If the plugin is enabled for cluster on `setting tab`, then user can
select plugin role from roles list on nodes tab and attach it to
specific nodes and vice versa it shouldn't be displayed in roles list
when the plugin is disabled for the cluster (environment)

If user wants to disable plugin but there's some nodes with this plugin
role in cluster then it should be done clearly with existing
mechanism: on `nodes tab` user remove from all nodes plugin role and
then disable plugin on `settings tab`

When cluster will be deployed user can't disable plugin and as a result
remove plugin role(s) from nodes.


Performance Impact
------------------

None


Plugin impact
-------------

* New node roles with volume partition and tasks info can be described
  in config yaml files which will be integrated in Nailgun

* Fuel plugin builder should automatically create in yaml file new
  node role based on plugin name. Basic skeleton description for node
  role in `node_roles` yaml file:

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

  Description of volumes partition in `volumes` yaml file:

  .. code-block:: yaml

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

  Desciption of new group in `tasks` yaml file:

  .. code-block:: yaml

    - id: role-name
      type: group
      role: [role-name]
      requires: [controller]
      required_for: [deploy_end]
      parameters:
        strategy:
          type: parallel

  Also all basic types of volumes, limits, allocate_sizes, size
  generators needs be noticed in plugin user guide.

* In metadata for plugin role developer can describe conflicts with
  other roles such as already done in openstack.yaml. Each plugin
  should have document list of provided roles for proper name
  referencing

* Plugin version in metadata.yaml should be changed to 3.0.0

* User can declare many roles in one plugin. It can be useful for
  tasks order and provide granular way for plugin developer to build
  their plugins on top of others.


Other deployer impact
---------------------

None


Developer impact
----------------
* We keep custom roles API but there is no need in roles table. So
  inner logic for managing it in Nailgun should be rewritten.

* Data model impact for network type plugin role depends on advanced
  networking [1]_. For example some models like `roles` can be changed
  to `node_roles`.

* It can affect plugin separate service [3]_. In current specification
  we describe realization of integration plugins in Fuel through db
  wrappers for each entity such as role and volume (look at work items
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
  wrapper around db model we need such wrappers for roles, volumes
  and tasks. As alternative this plugin managing mechanism can be
  implemented in context of separate plugin service [3]_. During of
  installation process, plugin role extend core roles.

* [Nailgun] Change DB schema to suppport plugin roles and refactor code

* [Nailgun] Change `get_deployment_tasks` method for Cluster object to
  get all related plugin deployment tasks.

* [Nailgun] Add checking for deployment tasks compatibility in
  `CheckBeforeDeploymentTask`.

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
