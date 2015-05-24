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
describe new network-type role(custome network roles will be
implemented in context of [1]).


Proposed change
===============

* Give possability for plugin developers introduse new custome node
  role through plugin such as already done for attributes. Plugin node
  role should be related to specific environments not releases, for
  example from UX side: if plugin enabled in cluster(environment) user
  can select plugin role from roles list and attach it to nodes and
  vice versa it shouldn't displayed in roles list when plugin disabled
  for cluster

* Provide volume partitions node-role in plugin and set deployment
  tasks in order

* Introduce network-type role as plugin with behavior similar to node
  role


Alternatives
------------

New roles can be created directly through CLI

Data model impact
-----------------

There is at least two ways of data model representation:

1. Plugin node|network roles directly mapped on `node_roles` and
`network_roles` models. But we need to know which roles are core
and which come as plugin. (more acceptable)

2. Separate entities for plugin node|network roles and core roles
which generate duplications in data models.


Nailgun DB tables changes for 1st option:

New relation table `plugin_roles` will be described
**PluginRoles**

* `id` - unique identifier
* `plugin_id` - relation key for plugin
* `role_id` - relation key for role
* `type` - model type (node|network)

Based on advanced network [1]
**NetworkRoles**

* `is_plugin` - boolean flag to identify plugin role

**NodeRoles**

* `is_plugin` - boolean flag to identify plugin role


REST API impact
---------------

None


Upgrade impact
--------------

N/A

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

* New (node|network) oles with volume partition(for node) info
  should be describe in 'environment_config.yaml' file which will
  be mapped on Nailgun DB

* Fuel plugin builder should automatically create in yaml file new node
  role based on plugin name.

Other deployer impact
---------------------

None

Developer impact
----------------

Data model impact for network type plugin role depends on advanced
networking [1].
It can affect plugin separate service if it will be in scope of 7.0

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

* [Nailgun] Develop functionality for basic get/set operations for
  (nodes|networks) roles through plugin manager using existing API for
  node roles(network roles API will be implmented in context of [1]).
  As alternative this plugin managing mechanism can be implemented
  in context of separate plugin service [3]

* [FPB] Change default template which will describe basic info for
  role. Also `environment_config` data should mapping on Nailgun DB.
  (Or should we have separate DB for plugins?)


Dependencies
============

* Advanced networking [1]
* Volume partition functionality [2]
* Separate plugin service [3]
* Task base deployment


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
