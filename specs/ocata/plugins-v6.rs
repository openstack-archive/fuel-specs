..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================
Fuel plugins v6.0.0
===================

https://blueprints.launchpad.net/fuel/+spec/plugins-v5

Fuel plugins packages v6.0.0 is introduced for the purpose to deprecate and drop support of
several legacy directives in plugin manifests and enhance multiple releases support in single plugin
package.


-------------------
Problem description
-------------------

We have several issues related to the Fuel plugins:

* Plugin should rely on existing release.

* Supporting legacy located in ``tasks.yaml`` makes things complex.

* Node role tasks groups and groups dependencies that are redundant declaration
  that makes tasks format harder to understand.

* It's not possible to customize settings and deployment tasks only for
  one/several of the releases supported by plugin.

* Mixed tasks version is used: v1.0.0 and v2.0.0.
  2.0.0 is task-based deployment ready, v1.0.0 is for granular deployment.
  If v1.0.0 tasks is persist deployment is falling back to granular deployment
  that adsorbs all benefits from the task-based deployment.


----------------
Proposed changes
----------------

Web UI
======

None


Nailgun
=======

Data model
----------

Table ``plugin_releases_configs`` should be created in Nailgun DB:

+----------+-----------+---------------+---------------------+------------------+----------------+------------------------+---------------------+-----------------+----------------+-----------------+-------------+
| id       | plugin_id | release_info  | attributes_metadata | volumes_metadata | roles_metadata | network_roles_metadata | components_metadata | node_attributes | nic_attributes | bond_attributes | paths       |
+==========+===========+===============+=====================+==================+================+========================+=====================+=================+================+=================+=============+
| id       | Integer   | JSON Dict     | JSON Dict           | JSON Dict        | JSON Dict      | JSON List              | JSON List           | JSON Dict       | JSON Dict      | JSON Dict       | JSON List   |
| required | required  | default: {}   | default: {}         | default: {}      | default: {}    | default: []            | default: []         | default: {}     | default: {}    | default: {}     | default: {} |
|          |           |               |                     |                  |                |                        |                     |                 |                |                 |             |
+----------+-----------+---------------+---------------------+------------------+----------------+------------------------+---------------------+-----------------+----------------+-----------------+-------------+

During plugin metadata(configuration) sync and queuing from plugin manager
this table should be used depending on specified release id instead of plugin
table fields.

This fields should be removed from ``plugins`` table to the separate table
that store according fields linked to the combination of plugin and release:

- attributes_metadata (environment_config.yaml)
- components_metadata (components.yaml)
- network_roles_metadata  (network_roles.yaml)
- releases (metadata.yaml -> releases)
- roles_metadata  (node_roles.yaml)
- volumes_metadata  (volumes.yaml)
- node_attributes
- nic_attributes
- bond_attributes

Deployment tasks from the (deployment_tasks.yaml in plugins package v4.0.0) will be stored
in graph that have relation on the plugin-release record, provided by
the transitive table like ones for releases, clusters e.t.c.

Data migration from v9.0 should be performed. This migration will place
fields content to the appropriate ``plugin_releases_configs`` record.

[TBD] Also this table in theory could store releases metadata.

``releases`` plugin field is supplemented by ``*_paths`` fields like:

.. code-block:: yaml

  releases:
    - "os": "ubuntu"
      "version": "mitaka-9.0"
      "deployment_scripts_path": "deployment_scripts/"
      "repository_path": "repositories/ubuntu"


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

Plugins definition format will be changed in v6.0.0 what should be reflected in FPB and plugins
adapter validation logic.


Changes in v6.0.0 against v5.0.0 in FPB
---------------------------------------

* ``metadata.yaml``

  * In ``releases`` records it is possible to specify per-release paths including
    folders. See ``Multi-release packages`` section below.

* ``node_roles.yaml``

  * optional ``tasks: [“hiera”, “globals”, ... ]`` parameter is added to
    replace tasks with ``type: group`` in ``deployment_tasks.yaml`` functionality.

* ``deployment_tasks.yaml``

  * tasks ``version: 2.0.0`` is required

  * ``parameters: strategy: type: parallel|one_by_one`` now could be defined
    for tasks


Deprecated items
----------------

* In ``deployment_tasks.yaml`` file ``groups: ["my_node_role", ...]`` parameter in
  task definition is deprecated in deployment tasks parameters,
  ``roles: ["my_node_role", ...]`` is supposed to be used instead.

* ``role`` tasks parameter is renamed to ``roles``.

* In ``deployment_tasks.yaml`` file: tasks with ``type: group`` which describe
  roles is no longer needed for plugin developers.
  The ``tasks: ["task_for this_role"]`` parameter is moved to ``node_roles.yaml``.

* ``tasks.yaml`` file is deprecated and its content will be ignored
  (see Notifications impact section for the details).

* Release ``mode:`` parameter should be removed.


Multi-release packages
----------------------

In ``metadata.yaml`` ``releases`` records now could contain path fields specifying release-specific
configuration files of folders with this kind of files.

If no custom path is specified for the release then default path is used so
this approach is backward-compatible with 4.0.0 ``metadata.yaml`` format.

Old ``releases`` section with old syntax is supposed to be deprecation
candidate.

Example of ``metadata.yaml``:

.. code-block:: yaml

  releases:

    - os: ubuntu
      version: 2015.1-8.0
      deployment_scripts_path: deployment_scripts/
      repository_path: repositories/ubuntu

      components_path: custom_components.yaml
      deployment_tasks_path: custom_deployment_tasks.yaml
      environment_config_path: custom_environment_config.yaml
      network_roles_path: custom_network_roles.yaml
      node_roles_path: custom_node_roles.yaml
      volumes_path: custom_volumes.yaml

      nic_attributes_path: nic_attributes.yaml
      bond_attributes_path: bond_attributes.yaml
      node_attributes_path: node_attributes.yaml

    - os: ubuntu
      version: liberty-8.0
      deployment_scripts_path: deployment_scripts/
      repository_path: repositories/ubuntu

      components_path: components_liberty.yaml
      deployment_tasks_path: deployment_tasks_liberty/ # <- folder
      environment_config_path: environment_config_liberty.yaml
      network_roles_path: network_roles_liberty.yaml
      node_roles_path: node_roles_liberty.yaml
      volumes_path: volumes_liberty.yaml

      nic_attributes_path: nic_attributes.yaml
      bond_attributes_path: bond_attributes.yaml
      node_attributes_path: node_attributes.yaml


Fuel Library
============

* It will be possible to define ``tasks`` parameter inside node roles.


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

    * Tasks with ``version v2.0.0`` found:
      Tell plugin developer about ``version: 2.0.0``, how it's related
      to the experimental orchestrator in Fuel 8.0.

  * Errors:

    * if no ``version: 2.0.0`` in ``deployment_tasks.yaml`` record specified

    * if ``type: group`` found in ``deployment_tasks.yaml``

    * ``tasks.yaml`` persist and it is not empty

  * Warnings:

    * Warn about experimental task-based orchestrator enabled requirements for
      Fuel 8.0 and no support for Fuel <= 7.0.

* During validation of Plugin package v4.0.0

  * Info:

    * Tasks with ``version v2.0.0`` not found:
      tell that it's recommended to be used in fuel 9.0.

    * Tasks with ``version v2.0.0`` found:
      Tell plugin developer about ``version: 2.0.0``, how it's related
      to the experimental orchestrator in Fuel 8.0.

  * Errors:

    * ``cross-depended-by`` and ``cross-depends`` are found
      without ``version: 2.0.0``

    * ``parameters: strategy: type: parallel|one_by_one`` are found
      without ``version: 2.0.0``

    * ``tasks.yaml`` is deprecated if ``tasks.yaml`` is found.

  * Warnings:

    * ``groups: [...]`` is used with ``version: 2.0.0``

    * Recommend for plugin developer to use package v5.0.0 if tasks
      ``version: 2.0.0`` is used


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

* Update Nailgun to support multi-version package or multi-version directives

Dependencies
============

None

-----------
Testing, QA
-----------

* Manual testing

* Plugins v5.0 should be tested for Fuel 8.0 with enabled task-based deployment
  for Fuel Fuel 9.x releases with default orchestrator.
  Also plugins v5.0 should not be enabled for Fuel 8.0 environments with
  disabled task-based deployment.

* ``tasks.yaml`` file should not affect Fuel 9.x plugins and induce according
  warning for fuel plugin builder.

* Example v6 plugins for fuel plugin builder should work.

* Proper work of plugin validator should be tested.

* All version-related Fuel Plugin builder and notifications should work.

Acceptance criteria
===================

* It should be possible to build and install plugins v6 for Fuel 8.0 and 9.x

* Multi-version packages should respect environment version.

----------
References
----------

None
