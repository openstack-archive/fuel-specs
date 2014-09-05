..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
100 nodes support (fuel only)
==========================================

https://blueprints.launchpad.net/fuel/+spec/100-nodes-support

If we want Fuel to be enterprise tool for deploying OpenStack it should be
able to deploy large clusters. Fuel also should be fast and responsive.
It does not run any processor consuming tasks so there is no reason
for it to be slow.

Problem description
===================

For large numbers of nodes fuel(nailgun, astute and GUI) are getting slow.

Proposed change
===============

All bottlenecks should be found and removed.
In the first step we should write tests which will show places in code which
are not optimal.
Such tests should include(all in fake mode):

* add 100 nodes, add roles for nodes and run deploy, delete env
* add 100 nodes, add roles for nodes, delete env
* add 100 nodes, add roles for nodes and run network verification, delete env
* add 100 nodes, add roles for nodes change settings, delete env
* add 100 nodes, add roles for nodes change network configuration, delete env
* ...

Similar tests should be written for GUI.

After this, required code will be refactored.

Alternatives
------------

Leave it as it is.

Data model impact
-----------------

Depends on bottlenecks found, but unlikely.

REST API impact
---------------

No API changes. All optimization have to be backward compatible.

Upgrade impact
--------------

Only if database is changed, but unlikely.

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

After blueprint is implemented Fuel should be able to work smoothly
with 100 nodes.

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
  loles@mirantis.com
  ksambor@mirantis.com

Work Items
----------

Blueprint will be implemented in several stages:

Stage 1
^^^^^^^^

Write load tests in which standard actions will be run when 100 nodes are
in database. This includes tests for:

* nailgun
* fuelclient
* astute
* GUI

Stage 2
^^^^^^^^

After writing tests and profiling the code, all bottlenecks will be fixed.


Dependencies
============

None


Testing
=======

When all bottlenecks are fixed. Load test will be added to CI infrastructure,
so we can immediately notice non optimal code.

Documentation Impact
====================

None

References
==========

* https://docs.google.com/a/mirantis.com/document/d/1GJHr4AHw2qA2wYgngoeN2C-6Dhb7wd1Nm1Q9lkhGCag
* https://docs.google.com/a/mirantis.com/document/d/1O2G-fTXlEWh0dAbRCtbrFtPVefc5GvEEOhgBIsU_eP0
