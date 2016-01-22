..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================
Fuel plugins v5.0.0
===================

https://blueprints.launchpad.net/fuel/+spec/plugins-v5

Fuel plugins packages v5.0.0 is introduced for the purpose of deprecating
old-style v1.0.0 tasks format and providing cleaner and more consistent
interface for Fuel plugins developers and enhance multiple releases support in
single plugin package.


-------------------
Problem description
-------------------

We have several issues related to the Fuel plugins API:

* Old-style tasks description format in tasks.yaml making package more complex.

* Node role tasks groups and groups dependencies that are redundant declaration
  that makes tasks format harder to understand.

* It's not possible to customize settings and deployment tasks depending on
  the release version.

* Mixed tasks version is used: v1.0.0 and v2.0.0

* Lack of per-task orchestration sequencing directive


----------------
Proposed changes
----------------

Web UI
======

None


Nailgun
=======

During installation `tasks:` parameter of `node_roles.yaml` records should be
unwrapped and according tasks with `type: group` be added to relieve plugins
developers from creation of this tasks manually.

`id` and `roles` parameters of this group tasks should be equal to node
role name.


Data model
----------

Table `plugin_releases_configs` should be created in Nailgun DB:

+----------+-----------+---------------+---------------------+------------------+----------------+------------------------+---------------------+------------------+-------------+
| id       | plugin_id | release_info  | attributes_metadata | volumes_metadata | roles_metadata | network_roles_metadata | components_metadata | deployment_tasks | paths       |
+==========+===========+===============+=====================+==================+================+========================+=====================+==================+=============+
| id       | Integer   | JSON Dict     | JSON Dict           | JSON Dict        | JSON Dict      | JSON List              | JSON List           | JSON List        | JSON List   |
| required | required  | default: {}   | default: {}         | default: {}      | default: {}    | default: []            | default: []         | default: []      | default: {} |
|          |           |               |                     |                  |                |                        |                     |                  |             |
+----------+-----------+---------------+---------------------+------------------+----------------+------------------------+---------------------+------------------+-------------+

During plugin metadata(configuration) sync and queuing from plugin manager
this table should be used depending on specified release id instead of plugin
table fields.

This fields should be removed from `plugins` table:

- attributes_metadata (environment_config.yaml)
- components_metadata (components.yaml)
- deployment_tasks  (deployment_tasks.yaml)
- network_roles_metadata  (network_roles.yaml)
- releases (metadata.yaml -> releases)
- roles_metadata  (node_roles.yaml)
- volumes_metadata  (volumes.yaml)

Data migration from v8.0 should be performed. This migration will place
fields content to the appropriate 'plugins_configs' record.

`releases` plugin field should be separated into `paths` fields, containing:

.. code-block:: json

  {
    "deployment_scripts_path": "deployment_scripts/"
    "repository_path": "repositories/ubuntu"
  }

and `release_info` field with:

.. code-block:: json

  {
    "os": "ubuntu"
    "version": "liberty-8.0"
    "mode": ["ha"]
  }


REST API
--------

None


Orchestration
=============


RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

Plugins API is changed in v5.0.0.

v5.0.0 will be compatible with Fuel 8.0 (if Task-based deployment
engine (experimental feature) is enabled) and with Fuel 9.0 and higher
by default.


Changes in v5.0.0 against v4.0.0
--------------------------------

* `metadata.yaml`

  * In `releases` records it is possible to specify per-release paths including
    folders. See `Multi-release packages` section below.

* `node_roles.yaml`

  * optional `tasks: [“hiera”, “globals”, ... ]` parameter is added to
    replace tasks with `type: group` in `deployment_tasks.yaml` functionality.

* `deployment_tasks.yaml`

  * `version: 2.0.0` is required

  * `parameters: strategy: type: parallel|one_by_one` now could be defined
    for tasks

  * rename `role` to `roles`

Deprecated items
----------------

* In `deployment_tasks.yaml` file `groups: ["my_node_role", ...]` parameter in
  task definition is deprecated in deployment tasks parameters,
  `roles: ["my_node_role", ...]` is supposed to be used instead.

* `role` tasks parameter is renamed to `roles`.

* In `deployment_tasks.yaml` file: tasks with `type: group` which describe
  roles is no longer needed for plugin developers.
  The `tasks: ["task_for this_role"]` parameter is moved to `node_roles.yaml`.

* `tasks.yaml` file is deprecated and its content will be ignored.


Multi-release packages
----------------------

In metadata.yaml `releases` record is extending by additional optional path
fields specifying release-specific configuration files of folders with this
kind of files.

If no custom path is specified for the release then default path is used so
this approach is backward-compatible with 4.0.0 `metadata.yaml` format.

If folder is specified as path then all .yaml files in this folder
during plugin building process will be combined into single file with a
name pattern: `[config type]-[release version]-[release os].yaml` in the
plugin root folder.

Folder links will be replaced with the link to this combined files,
initial folder will be removed from final package.

Example of `metadata.yaml`:

.. code-block:: yaml

  releases:

    - os: ubuntu
      version: 2015.1-8.0
      mode: ['ha']
      deployment_scripts_path: deployment_scripts/
      repository_path: repositories/ubuntu

      components_path: custom_components.yaml
      deployment_tasks_path: custom_deployment_tasks.yaml
      environment_config_path: custom_environment_config.yaml
      network_roles_path: custom_network_roles.yaml
      node_roles_path: custom_node_roles.yaml
      volumes_path: custom_volumes.yaml

    - os: ubuntu
      version: liberty-8.0
      mode: ['ha']
      deployment_scripts_path: deployment_scripts/
      repository_path: repositories/ubuntu

      components_path: components_liberty.yaml
      deployment_tasks_path: deployment_tasks_liberty/ # <- folder
      environment_config_path: environment_config_liberty.yaml
      network_roles_path: network_roles_liberty.yaml
      node_roles_path: node_roles_liberty.yaml
      volumes_path: volumes_liberty.yaml


Fuel Library
============

* In tasks description `roles` alias for `role` parameter will occur.

* It will be possible to define `tasks` parameter inside node roles.


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

Plugins compatibility should be re-checked during upgrade according to new
multi-version directives/packaging.


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

Fuel Plugin Builder
===================

Fuel Plugin Builder validator should allow to make warnings without failing
validation.

* During validation of Plugin package v5.0.0

  * Info:

    * Tasks with `version v2.0.0` found:
      Tell plugin developer about `version: 2.0.0`, how it's related
      to the experimental orchestrator in Fuel 8.0.

  * Errors:

    * if no `version: 2.0.0` in `deployment_tasks.yaml` record specified

    * if `type: group` found in `deployment_tasks.yaml`

    * `tasks.yaml` persist and it is not empty

  * Warnings:

    * Warn about experimental task-based orchestrator enabled requirements for
      Fuel 8.0 and no support for Fuel <= 7.0.

* During validation of Plugin package v4.0.0

  * Info:

    * Tasks with `version v2.0.0` not found:
      tell that it's recommended to be used in fuel 9.0.

    * Tasks with `version v2.0.0` found:
      Tell plugin developer about `version: 2.0.0`, how it's related
      to the experimental orchestrator in Fuel 8.0.

  * Errors:

    * `cross-depended-by` and `cross-depends` are found
      without `version: 2.0.0`

    * `parameters: strategy: type: parallel|one_by_one` are found
      without `version: 2.0.0`

  * Warnings:

    * `tasks.yaml` will be deprecated in next release and not recommended to
      use

    * `groups: [...]` is used with `version: 2.0.0`

    * Recommend for plugin developer to use package v5.0.0 if tasks
      `version: 2.0.0` is used


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

This feature is highly affects Fuel plugins developers.


---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Add documentation of fuel plugins format v4.0.0 v5.0.0 according to the
Fuel plugins builder examples.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  ikutukov@mirantis.com

Other contributors:


Mandatory design review:
  bgaifulin@mirantis.com
  ikalnitsky@mirantis.com


Work Items
==========

* add v5 support to Nailgun v8.0 and Nailgun v9.0
  https://bugs.launchpad.net/fuel/+bug/1534235

* Add plugins v5 examples and templates for Fuel Plugin Builder 9.0
  https://bugs.launchpad.net/fuel/+bug/1534126

* Update plugins v5 validation for Fuel Plugin Builder 9.0 including warnings
  https://bugs.launchpad.net/fuel/+bug/1534126

* Update Nailgun to support node roles tasks

* Update Nailgun to support multi-version package or multi-version directives

Dependencies
============

None

-----------
Testing, QA
-----------

* Manual testing

* Plugins v5.0 should be tested for Fuel 8.0 with enabled task-based deployment
  and for Fuel 9.0 with default orchestrator.
  Also plugins v5.0 should not be enabled for Fuel 8.0 environments with
  disabled task-based deployment.

* `tasks.yaml` file should not affect Fuel 9.0 plugins and induce according
  warning for fuel plugin builder.

* Example v5 plugins for fuel plugin builder should work.

* Proper work of plugin validator should be tested.

* All version-related Fuel Plugin builder and notifications should work.

Acceptance criteria
===================

* It should be possible to build and install plugins v5 for Fuel 8.0 and 9.0

* Multi-version packages should respect environment version.

----------
References
----------

None
