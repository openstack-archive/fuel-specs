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

When plugin developer builds the plugin i.e. runs command `fpb --build plugin_name`,
fpb should build an RPM with all of the repositories, deployment scripts and required
metadata. The package has name **plugin_name-1.0.0** and RPM version **0.0.1**.

Then fpb puts the package in **plugin_name-1.0.0.fp** archive.

.. code-block:: text

    .
    |-- plugin_name-1.0.0-0.0.1.noarch.rpm
    `-- metadata.yaml

Fuel client during the plugin installation gets **package_version** version
from **metadata.yaml** file, if the version is '1.0.0' then old installation
method should be performed, if the version is '2.0.0' then the plugin should
be installed as a package.

When new plugin is released it has the same version **1.0.0**, but RPM version
should be increased, i.e. version should be **0.0.2**, after that user
can run `yum update plugin_name-1.0.0` which updates plugin repositories.


Restrictions and problems
=========================

* such solution is going to be a huge problem if Fuel master is not Centos based,
  but Ubuntu/Debian based

* user have to go and run `yum update package_name` twice, first
  on the master node to get repositories updated, and the second time
  on OpenStack nodes

* versions duplication, we have plugin version and RPM version, because
  in RPM world you cannot install two packages with the same name, but with
  different versions. By desing user should be able to install several plugins
  with different versions.

* user won't be able to install plugin using yum, because we have additional
  REST API call to register the plugin, it means that user should always use
  fuel client to install the plugin


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

* user will not be able to get updates for his old plugins, because they
  are not represented as RPM in the system
* user will not be able to install the plugin on old environments

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

* TODO


Work Items
----------

* Changes for Nailgun

* Changes for Fuel plugin builder, to build package from a plugin


Dependencies
============

TODO clairfy dependencies for package build

Testing
=======

The changes can be tested with the next test case

* install plugin with version 1.0.0

* deploy the cluster with enabled plugin

* update plugin package

* check that new packages are available on OpenStack nodes

Documentation Impact
====================

* Update plugin developer documentation, with information about new plugin format
  and how to migrate from old format to new one

* Update user documentation

References
==========

None
