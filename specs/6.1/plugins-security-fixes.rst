..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Security fixes for Fuel plugins
===============================

https://blueprints.launchpad.net/fuel/+spec/plugins-security-fixes-delivery

Fuel user should be able to get security fixes for plugin's packages.


Problem description
===================

Each Fuel plugin can provide a set of repositories with packages,
currently there is no easy way to update the packages in the repositories


Proposed change
===============

Packaging (fpb, fuel client)
----------------------------

When plugin developer builds the plugin i.e. runs command
**fpb --build plugin_name**, fpb builds RPM with all of the
repositories, deployment scripts and required metadata. The package
has version in metadata.yaml **1.0.2**, name of RPM package is
**plugin_name-1.0** and RPM version is **1.0.2**.

Major version of the plugin is included into the name because,
we can have several major plugin versions in a single installation.

We do not want to break backward compatibility, hence fuel client
should be able to install both package formats, the old **fp** and
the new **rpm**. Fuel client will define installation method by
plugin extension **plugin_name-1.0.2.fp** and
**plugin_name-1.0-1.0.2.noarch.rpm**.

When new plugin with security fixes is released, minor version of the
plugin should be increased to **1.0.3**, version in the name will be
unchanged i.e. **1.0**, but RPM version is going to be **1.0.3**, after
that user can run **yum update plugin_name-1.0-1.0.3.noarch.rpm** which
updates plugin's repositories, and user can performs packages updates.

If user uses fuel client to install rpm, it performs installation with
yum, and registers the plugins in Nailgun, if user uses yum to install
the plugin he should manually register the plugin with register command,
e.g. **fuel plugins --register plugin_name==1.0.3**.

Backend (Nailgun)
-----------------

* currently in Cluster attributes we have version of the plugin,
  right in the json, to determine which version of the plugin
  should be enabled/deisabled, this version should be replaced
  with plugin id, in migration scripts. It's required because
  version of the plugin can get changed after update.

* Nailgun should generate paths to major version of the directory,
  **plugin_name-1.0**, instead of **plugin_name-1.0.0** or
  **plugin_name-1.0.1**.

* Nailgun should not break compatibility with previous plugins,
  it means if user has plugins with versions 1.0.1, 1.0.2, 1.0.3,
  they should work just perfectly, for plugins with packaging_version
  **1.0.0**. In order to do this Nailgun should have different paths
  formatting layer for different package versions.


Installation/Update (fuelclient)
--------------------------------

Installation:

* .fp plugin should be installed as it was before

* .rpm plugin should be installed with yum, but after
  installation REST API call should be performed

* if rpm was installed manually user should be able
  to register plugin in Nailgun database with special
  command **fuel plugins --register plugin_name-1.0**,
  which performs POST request.

For update fuel client should provide a new command
**fuel plugins --update plugin_name-1.0.0.rpm**

* if user runs **yum update**, he should run **fuel plugins --sync**
  to get all plugins registered in REST API service.

* REST API call with PUT should be performed for
  plugin with the same major version, e.g. if
  there was plugin with version 1.0.1 in Nailgun database,
  after update it should become 1.0.2 for plugins with
  package version 1.0.0.

Removal:

* user can use command **fuel plugins --remove plugin_name==version**
  to remove the plugin from file system and from API Service.

* if user uses yum to remove the plugin, he can use
  **fuel plugins --unregister plugin_name==version** command
  to remove the plugin from API Service only.

Downgrade:

* user should be able to downgrade his plugin if he finds any errors
  or problems with updated version
  **fuel plugins --downgrade plugin_name-1.0.0.rpm**

Backward compatibility
----------------------

Backward compatibility matrix for different Fuel releases:

.. code::

    |-----+-------------+---------------|
    |     | .fp (1.0.0) | .rpm (2.0.0)  |
    |-----+-------------+---------------|
    | 6.0 | Supported   | Not supported |
    | 6.1 | Supported   | Supported     |
    |-----+-------------+---------------|

Lets consider several cases. User has the next plugins

.. code::

    |-------------+---------+------------------|
    | Name        | Version | Package version* |
    |-------------+---------+------------------|
    | plugin_name |   2.0.0 |            1.0.0 |
    | plugin_name |   2.0.1 |            1.0.0 |
    | new_plugin  |   1.0.1 |            2.0.0 |
    |-------------+---------+------------------|

    * Package version is a version which identifies
      plugin format, in 6.0 we had 1.0.0 format,
      in the next release we will get 2.0.0 plugin
      format

User gets new version 2.0.2 with security fixes,
also he has upgraded Fuel from 6.0 to 6.1.

**Package version 1.0.0 -> 1.0.0, plugin name is plugin_name**

If user tries to run update error should be shown,
that he cannot perform update with old (1.0.0) version
of package, also we can provide a manual instruction,
how to perform update. But in this case we will not be
able to get consistent information about the plugin from
the database, which version is used on the environment.

* install plugin

* create symlinks

.. code::

  /var/www/nailgun/plugins/plugin_name-2.0.2 ->
  /var/www/nailgun/plugins/plugin_name-2.0.1

  /var/www/nailgun/plugins/plugin_name-2.0.2 ->
  /var/www/nailgun/plugins/plugin_name-2.0.0

**Package version 1.0.0 -> 2.0.0, plugin name is plugin_name**

The same as for case from above, user has to perform manual actions
to get repositories updated.

**Package version 2.0.0 -> 2.0.0, plugin name is new_plugin**

Should work fine, no manual actions required.

Restrictions and problems
-------------------------

* such solution is going to be a huge problem if Fuel master is not
  Centos based, but Ubuntu/Debian based

* user will not be able to get updates for his old plugins, because they
  are not represented as RPM in the system

* user will not be able to install the plugin on old environments

Alternatives
------------

Leave it as is
^^^^^^^^^^^^^^

If we leave it as is user won't be able to get patches with existing tools,
like `yum`, which is a huge problem, because in this case many things should
be reimplemented in fuel client.

Data model impact
-----------------

None


REST API impact
---------------

None


Upgrade impact
--------------

Plugins which are installed in old format cannot be updated as rpm packages,
but it's possible to deliver manual fixes.

Security impact
---------------

User will have easy way to apply security fixes.


Notifications impact
--------------------

None


Other end user impact
---------------------

None

Performance Impact
------------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:

* eli@mirantis.com

QA:

* akurenyshev@mirantis.com


Work Items
----------

* Changes for Nailgun

  * instead of `plugin_name-1.0.0` directories Nailgun
    should generate paths to `plugin_name-1.0` directory,
    for 2.0.0 package version plugins.

  * if plugin `plugin_name` with version `1.0.0` exists and
    user performs installation of the same plugin, but with
    version `1.0.1`, plugin version should be updated from
    `1.0.0` to `1.0.1` with PUT REST API call on /api/plugins/1
    handler.

  * for all items above backward compatibility is mandatory

* Changes for Fuel Plugin Builder

  * generate RPM instead of fp archives for `2.0.0` package version,
    for `1.0.0` package version fpb should build fp archives as it
    was before

  * use full version as a version for RPM
    and major version as a part of plugin name

Dependencies
============

* rpmbuild is required to build package with fuel plugin builder

Testing
=======

Unit and System tests are required.

Acceptance Criteria
-------------------

* fpb should be able to build to build .fp plugins for plugins with
  package version '1.0.0'

* fpb should be able to build to build .rpm plugins for plugins with
  package version '2.0.0'

* by default fpb should generate '2.0.0' package version plugin template

* fuel client should be able to **install** .fp plugins

* fuel client should be able to **install** .rpm plugins

* fuel client should be able to **remove** plugins

* fuel client should be able to **update** plugins from package
  version 2.0.0 to another plugin with package version 2.0.0

* fuel client should be able to **downgrade** plugins from package
  version 2.0.0 to another plugin with package version 2.0.0

* with fuel client user should be able to **register** plugin in Nailgun
  if it was installed with yum

* also user should be able to remove plugin from Nailgun
  (**unregister** action) if it was removed manually

Documentation Impact
====================

* Update plugin developer documentation, with information about new plugin
  format and how to migrate from old format to new one

* Update user documentation

References
==========

None
