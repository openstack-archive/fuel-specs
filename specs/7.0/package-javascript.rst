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
ISO build from NPM registry and bower. This operation could fail and
we end with broken ISO build jobs.

Proposed change
===============

Package every used NPM module in RPM (DEB) so we could patch it
and reuse as Fuel dependency.
All necessary modules are described in package.json and bower.json
for nailgun as follows:
* https://github.com/stackforge/fuel-web/blob/master/nailgun/package.json
* https://github.com/stackforge/fuel-web/blob/master/nailgun/bower.json
All built node packages must be installed prior to compiling nailgun.
Nailgun specs must be changed to obtain modules from local cache
instead of the internet.

Alternatives
------------

* internet mirrors of NPM registry or bower
* local mirror of NPM registry or bower.
* upstream packages

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

Other impact
---------------------

* Operating system has nodejs modules already built. But they are outdated.
Every our packaged module must obsolete or replace upstream version
correct way


Performance Impact
------------------

None

Plugin impact
-------------

None

Other deployer impact
---------------------

Package names must be explicitly written in all necessary specs and in requirements files.

Developer impact
----------------

* Developer should adapt spec file or config file to obtain modules 
from local cache insted of the internet.

Implementation
==============

* Use script for generating spec files. It could be used automatically by Jenkins.
Or ondemand in any need.
Script could parse package.json or bower.json for any sensitive information like
module name and version.
* (Optionally) Jenkins job which is able to automatically check NPM or bower upstream
versus our repository and compile new version if any.
* Repository must contain every version we ever built to maintain compatibility.
* We must complaint packaging policies Debian or Centos if any.
Every spec must pass lintian. Every our package must not ruine existing
upstream package tree.

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

* Packages are ready and placed in base repository
* Packages version are the same as described in package.json and bower.json
* Packages are installable and removeable inside OS
* There are no conflicts in existing upstream package tree
* Nailgun compiling successfuly with no need of the internet just
using our packages like local cache

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
- https://wiki.debian.org/Javascript/Nodejs/Manual
