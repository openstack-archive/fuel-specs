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
`roles_metadata` json type column.

Unlike attributes, volumes and roles are related to nodes, not to
clusters. All core roles belong to release and plugin roles to
plugin entity accordingly.

Metadata for roles, volumes, tasks and attributes are taken from
plugin yaml config files and stored once in DB as plugin entity
attributes to avoid parsing from file many times.

When node is to be added into cluster, UI requires full list of
allowed node roles which consist from core roles(contained in release)
and plugin roles(contained in `roles_metadata` column for each
enabled plugin in cluster).

Set of chosen specific roles are kept by each node in `pending_roles`
column. After role tasks processed successfully pending role will be
moved to `deployed_roles`. Process continues until `pending_roles`
contains any role which is not in `roles`.

General deployment tasks gets from release. Then for specific
cluster nailgun build deployment graph which based on general
deployment tasks and plugin deployment tasks related to cluster.

If two plugins overwrite the same task or export two tasks with the
same ID, an exception has to be raised. Check tasks compatibility every
time when roles assigned on nodes will be overwhelmed for performance
so it can be run once during deployment graph building.


Nailgun DB tables changes:

drop `roles` table
drop `node_roles` table
drop `pending_node_roles` table

**Plugin**

* `attributes_metadata`
plugin attributes data taken from `environment_config` yaml

* `volumes_metadata`
plugin volumes data taken from `volumes` yaml

* `roles_metadata`
plugin roles data taken from `node_roles` yaml

* `deployment_tasks`
deployment tasks data taken from `deployment_tasks` yaml

* `tasks`
pre/post deployment tasks taken from `tasks` yaml

**Node**

* `pending_roles`
set of specific roles which need to be deployed

* `roles`
set of roles which already have been deployed


REST API impact
---------------

There will be new API call provided to sync changes for plugin
metadata from yaml files to DB

====== ========================== ===================================
method URL                        action
====== ========================== ===================================
POST   /api/v1/plugins/sync/      Sync metadata for plugins
====== ========================== ===================================

request:

.. code-block:: json

    {
        "ids": [3, 4]
    }

Where ``ids`` is list of plugin ids which should be synced. If it's
empty then all plugins will be synced.


Role API will be the same but inner logic changed (Role model will be
removed).


Upgrade impact
--------------

Migration of schema should be provided to support previously created
environments. Plugins with old format also will be supported.


Security impact
---------------

N/A


Notifications impact
--------------------

N/A


Other end user impact
---------------------

Fuel python client should be extened to support plugin's metadata sync

Proposal CLI commands:

Sync all plugins

::

  fuel plugins sync

Sync specific plugins

::

  fuel plugins sync --id 1 2 3


Web UI impact
-------------

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

  Pre/Post deployment tasks are kept in `tasks` yaml as before and
  deployment tasks will be described in `deployment_tasks` yaml file.
  Description of new group in `deployment_tasks`:

  .. code-block:: yaml

    - id: role-name
      type: group
      role: [role-name]
      requires: [controller]
      required_for: [deploy_end]
      parameters:
        strategy:
          type: parallel

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

* It can affect plugin separate service [0]_. In current specification
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
  * Igor Kalnitsky <ikalnitsky@mirantis.com>

Developers:
  * Andriy Popovych <apopovych@mirantis.com>

Mandatory design review:
  * Evgeniy L <eli@mirantis.com>
  * Dmitriy Shulyak <dshulyak@mirantis.com>

QA engineers:
  * Maksym Strukov <mstrukov@mirantis.com>


Work Items
----------

* [Nailgun] Refactor internal representation of node roles. Remove
  "roles" table and relation tables "pending_node_roles" and
  "node_roles", use roles from release's "roles_metadata",
  add general method to retrieve roles list -
  ``objects.Cluster.get_roles``.

* [Nailgun] Extend the ``Plugin`` database model to store roles,
  volumes and deployment tasks declarations.

* [Nailgun] Add API call to sync roles, volumes, and other stuff from
  plugins (filesystem) to Nailgun's database.

* [Nailgun] Mix plugin's node roles and volumes with core ones
  everywhere it's used.

* [Nailgun] Mix plugin's deployment tasks with core ones everywhere
  it's used.

* [FPB] Change default template skeleton.


Dependencies
============

N/A


Testing
=======

Nailgun unit tests
Nailgun integration tests
FPB unit tests

Test Scenario
-------------

#. Install fuel_example_plugin.
#. Create new environment (1 controller, 1 compute).
#. Enable fuel_example_plugin for this env.
#. Assign the TestRole to separate node.
#. Deploy env.
#. Check OSTF is passed.
#. Check that the TestRole is deployed and ready.
#. Check that an entire disk is allocated on the TestRole node.
#. Check that deployment tasks are applied on the TestRole node.
#. Check that some task wasn't executed on the compute node because it
   was overwritten by plugin.
#. Check that some additional task was executed on the controller node
   during deployment.


Acceptance criteria
-------------------

* A new node role - TestRole - has to be exported.

* The new role has to use custom volumes. Currently the base-os role
  allocates only one partition with minimum space (for OS installation
  ), and left space are kept as unallocated. The TestRole has to
  allocate an entire disk: min partition for os, and what is left for
  personal using.

* The TestRole has to export deployment tasks which perform some
  simple actions (e.g. package installation or file creation).

* One of deployment tasks for the TestRole has to overwrite some task
  of the compute role.

* One new deployment task has to be injected to controller deployment.
  In other words, it has to be executed only on controller node.


Documentation Impact
====================

We should have a documented notice which help plugin developers
describe new role in plugin and how plugin deployment tasks can
overwrite existing ones. Also all basic types of volumes, limits,
allocate_sizes, size generators needs be noticed in plugin user guide.


References
==========

.. [0] https://blueprints.launchpad.net/fuel/+spec/plugin-manager-as-separate-service
