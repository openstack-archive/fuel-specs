..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================
Fuel Pluggable Architecture
===========================

https://blueprints.launchpad.net/fuel/+spec/nailgun-plugins

Problem description
===================

Our product is already able to install OpenStack in some default
configurations. But there are a lot of additional features our users want.
It is almost impossible to leave all of them in Fuel Core, so we need
pluggable architecture to implement certain things as separate parts. Also
there may be bundled versions of Fuel including exact plugins user wants.

As a first step, this architecture will probably include these points:

* Ability to install additional packages on target nodes
* Ability to run custom shell commands on target nodes
* Cinder drivers
* Neutron drivers
* Extending UI

Also, we need to provide well-documented SDK and instructions on how to write
custom Fuel plugin and to distribute it.

Proposed change
===============

There are already:

Basic infrastructure for plugins (described below):
https://review.openstack.org/97827
https://review.openstack.org/110288

A plugin prototype for Ceph:
https://review.openstack.org/104608

From Nailgun side prototype uses `Stevedore <http://stevedore.readthedocs.org/en/latest/>`_..
This package is already used in OpenStack Nova project as hooks providing
mechanism. It uses 'entry points' approach provided by setuptools/distutils,
which basically allows to lookup and execute code from Python packages
known to expose certain functionality.

Advantages:

  * well-known and widely used solution
  * provides three basic types: Driver, Hook and Extension
  * allows to "query" installed Python packages to find plugins which
    implement certain features
  * flexible error processing and logging
  * used by a number of OpenStack projects

Disadvantages:

  * approach used in prototype requires a lot of entry points to be specified
    in plugin's setup.py (this may be improved as well, additional research
    is needed)
  * needs very clear description for each hook which arguments does it accept
    and what format should returned value be in
  * some probable issues with merging results provided by different plugins
    implementing the same hook
  * need to restart Nailgun process after plugin was installed (if it's done
    dynamically on working master node)


Alternatives
------------

Without Stevedore it may be written by hand, using dynamic reload() or the
same entry points. Though, it is a production-grade solution already.

Data model impact
-----------------

Plugins will rely on their own DB table in PostgreSQL, which will be similar
to key-value storage (using native JSON field). This allows them to store
any custom structures, also we won't have a headache with writing migrations.

In current approach, all plugin-related data is stored in this "storage",
including custom roles, volumes/partitions and so on. Nailgun executes code
from plugins through hooks and updates it's data by returned values.

REST API impact
---------------

API Serializers execute hooks while serializing DB model, extending JSON
with data returned from plugins. Hooks are added to certain fields only, so
risk of any massive incompatible API modification is minimal, but not
completely impossible.

Also, plugins may provide custom URLs matching ** /api/plugins/plugin_name/* **
scheme. This is done by inheriting from RESTAPIPlugin class and exposing
WSGI application written in any web framework via *application* attribute.

Upgrade impact
--------------

Each plugin has to be tested and approved to work with current Fuel version.
Backward compatibility should also be provided, meaning code should work with
old environments on new Fuel version, if needed.

Security impact
---------------

None

Notifications impact
--------------------

None

Performance Impact
------------------

Performance decrease will surely depend on the number of plugins to execute.
There is almost nothing we can do about that.

Other end user impact
---------------------

None

Other deployer impact
---------------------

Each plugin, depending on what it does, should be provided as one or multiple
RPM packages, which will be installed into corresponding Docker containers.
All plugins will be installed simultaneously, but user should be able to
select which of them to use during environment creation process.

Developer impact
----------------

From Nailgun side, plugin will be introduced as one or multiple Python
packages. Each such package should include entry points in setup.py and its
own tests.

Implementation
==============

Assignee(s)
-----------

nmarkov@mirantis.com, akislitsky@mirantis.com

Work Items
----------

Dependencies
============

None

Testing
=======

Each plugin should have its own tests written using tox, unittests, casperjs,
Selenium or some other corresponding testing framework.

Documentation Impact
====================

In most common cases documentation may be presented by Sphinx docs, some RST
files or just README.txt.

References
==========

None
