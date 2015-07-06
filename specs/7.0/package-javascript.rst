..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================
Package javascript modules in rpm/deb
=====================================

https://blueprints.launchpad.net/fuel/+spec/package-js.spec

This blueprint describes a way to package nodejs modules as RPM (DEB)

Problem description
===================

Now we download javascript modules for nailgun during
ISO build from NPM registry. This operation could fail and
we end with broken ISO build jobs.

Proposed change
===============

Package every used NPM module in RPM (DEB) so we could patch it
and reuse as Fuel dependency.

Alternatives
------------

Local mirror of NPM registry.

Business impact
-----------------

* enable patching of JavaScript modules used in Fuel UI
* prevent a class of regression in ISO build process
* make it possible to package Fuel UI according to OS policies
* enabling handling JavaScript modules as reusable artifacts 

REST API impact
---------------

None 

Upgrade impact
--------------

None

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
  Artem Silenkov <asilenkov@mirantis.com>

Work Items
----------

* Prepare specs for every used JS module for RPM and DEB
* Package and place at repository every used JS module

Acceptance criteria
-------------------

Packages are ready and placed in base repository

Dependencies
============

None

Testing
=======

None

Documentation Impact
====================

None

References
==========

- https://blueprints.launchpad.net/fuel/+spec/
