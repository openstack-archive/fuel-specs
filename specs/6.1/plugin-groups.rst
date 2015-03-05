..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============
Plugin groups
=============

https://blueprints.launchpad.net/fuel/+spec/plugin-groups

Plugin developer should be able to define what part of the
system his plugin implements network, storage, monitoring,
or something else, this information can be used for plugins
list page generation, also might be useful for Nailgun backend.

Problem description
===================

Currently to generate plugins page devops team manually
adds each plugin in specific group.

Proposed change
===============

Each plugin have description of groups, groups is a fixed
list which can be empty, it can have the next possible
options:

* network

* storage

* storage::cinder

* storage::glance

* hypervisor

Alternatives
------------

None

Data model impact
-----------------

For Nailgun model Plugins json field "groups" should be added,
in order to store this information.

REST API impact
---------------

Nailgun should return "groups" field from backend.

Upgrade impact
--------------

By default group is empty, no upgrade impact.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Plugin impact
-------------

Described above.

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

  eli@mirantis.com

Work Items
----------

* Fix validator and template in Fuel Plugin Builder
* Fix Nailgun migration scripts and searilization

Dependencies
============

None

Testing
=======

Create a plugin with groups, check that it represented
in the database after installation.

Documentation Impact
====================

Describe the list of groups.

References
==========

* https://www.fuel-infra.org/plugins/catalog.html

* https://github.com/stackforge/fuel-plugins
