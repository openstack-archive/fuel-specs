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
role name. After that `tasks:` parameter could be removed from plugin node role
information.


Data model
----------

Deployment graph could be different depending on release, so the different
plugin tasks and settings should be stored in Nailgun after plugin
installation.


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

v5.0.0 will be compatible with Fuel v8.0 in experimental mode and higher with
the default orchestrator enabled.

Changes in v5.0.0 against v4.0.0
--------------------------------

* `node_roles.yaml`
  * optional `tasks: [“hiera”, “globals”, ... ]` parameter is added to
    replace tasks with `type: group` in `deployment_tasks.yaml` functionality.

* `deployment_tasks.yaml`
  * `version: 2.0.0` is required
  * `parameters: strategy: type: parallel|one_by_one now` now could be defined
    for tasks
  * rename `role` to `roles`

Deprecated items
----------------

* In `deployment_tasks.yaml` file `groups: ["my_node_role", ...]` parameter in
  task definition is deprecated in deployment tasks parameters,
  `roles: ["my_node_role", ...]` is supposed to be used instead.

* In `deployment_tasks.yaml` file `type: group` tasks is not available for plugin
  developers and completely replaced with new `tasks` parameters
  in `node_roles.yaml`.

* `tasks.yaml` file is deprecated and its content will be ignored.


Multi-release packages
----------------------

Possible approaches to the multi-release packages:

Variant 1
^^^^^^^^^

OS release and fuel version constraints directives should be added to the
records in such kind of records:

* tasks
* node roles
* network roles
* components (TBD?)
* volumes_roles_mapping (TBD?)

Example of `deployment_tasks.yaml`:

.. code-block:: yaml

  - id: my-task
    os-version: "==2014.2,==2015.1"
    fuel-version: ">=7,<=8"
    parameters:
      puppet_manifest: "deploy_legacy.pp"
      puppet_modules: "."

  - id: my-task
    os-version: ">=liberty-8.0"
    fuel-version: ">=9"
    parameters:
      puppet_manifest: "deploy_10.pp"
      puppet_modules: "."

Please note that id is similar and this two records will form a multi-version
group that will be interpreted as a single record according to current env and
Fuel version.

Version constraint is not required and its absence should be considered as all
version supported.

When plugin is validating it should be checked that tasks is fit into supported
release.

Plugin package structure is not changing.

When plugin is activating for the environment all configuration records and
tasks should be passed through version pre-processor that looks at all
tasks/configs with version constraints then grouping records with the similar
id or name and choosing best fit record (selection policy may vary) among
those which satisfy current fuel and release version.

If any of given constrains (OS, Fuel) could not be satisfied for current env,
group should be ignored.

After this stage version constraints information become not important and
could be removed/ignored from the filtered tasks.

`metatada.yaml` -> releases manifest data will be used as usual before tasks
filtering process.


Variant 2
^^^^^^^^^
Per-release configuration files links

In metadata.yaml -> releases is extended by directives where to look for
configuration file for this release, or default path from current plugin
configuration is used:

.. code-block:: yaml

  conf_paths:

    - deployment_tasks
      node_roles
      network_roles
      volumes
      components
      environment_config

Example of `metadata.yaml`:

.. code-block:: yaml

  releases:

    - os: ubuntu
      version: 2015.1-8.0
      mode: ['ha']
      deployment_scripts_path: deployment_scripts/
      repository_path: repositories/ubuntu
      deployment_tasks_path: deployment_tasks_kilo.yaml
      node_roles_path: node_roles.yaml

    - os: ubuntu
      version: liberty-8.0
      mode: ['ha']
      deployment_scripts_path: deployment_scripts/
      repository_path: repositories/ubuntu
      deployment_tasks_path: deployment_tasks_liberty.yaml
      node_roles_path: node_roles_liberty.yaml


Variant 3
^^^^^^^^^
Per-release folders

Only folder with plugin config files is specified for all releases
in metadata.yaml. If no folder is defined or configuration file is missing
in given folder root path is used.

Example of `metadata.yaml`:

.. code-block:: yaml

  releases:

    - os: ubuntu
      version: 2015.1-8.0
      mode: ['ha']
      deployment_scripts_path: deployment_scripts/
      repository_path: repositories/ubuntu
      conf_path: librty-ubuntu/

    - os: ubuntu
      version: liberty-8.0
      mode: ['ha']
      deployment_scripts_path: deployment_scripts/
      repository_path: repositories/ubuntu
      conf_path: librty-ubuntu/


Fuel Library
============

* In tasks description `roles` alias for `role` parameter will occur.

* It will be possible to define `tasks` parameter for node roles.


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
    * Tasks with `version v2.0.0` not found:
      tell that it's recommended to be used in fuel 9.0.
    * Tasks with `version v2.0.0` found:
      Tell plugin developer about `version: 2.0.0`, how it's related
      to the experimental orchestrator in Fuel 8.0.
  * Errors:
    * if no `version: 2.0.0` in `deployment_tasks.yaml` record specified
    * if `type: group` found in `deployment_tasks.yaml`
    * `tasks.yaml` persist and it is not empty
  * Warnings:
    * Warn about experimental task-based orchestrator enabled requirements for
      Fuel v8.0.0 and no support for Fuel <= v7.0.0.

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

Multi-version plugins support could have some impact on recommended plugins
repo structure and package versions management.


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

TODO(ikutukov): add testing points for the multi-version packages when
implementation details will be clear.


Acceptance criteria
===================

* It should be possible to build and install plugins v5 for Fuel 8.0 and 9.0

* Multi-version packages should respect environment version.

----------
References
----------

None