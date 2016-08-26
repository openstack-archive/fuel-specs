..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================================
Consolidate fuel CLI client capabilities in single version
==========================================================

This change is a follow up on the original feature described in the following
blueprint:
https://blueprints.launchpad.net/fuel/+spec/re-thinking-fuel-client

This blueprint describes replacing the old fuel client with the new fuel
client.


--------------------
Problem description
--------------------

There are two versions of fuelclient which are respectively available with fuel
and fuel2 commands. There is no feature parity between them and it is often
quite confusing which version of client a user needs to run. It is necessary to
leave only one version.


----------------
Proposed changes
----------------


Web UI
======

N/A


Nailgun
=======

N/A


Data model
----------

N/A


REST API
--------

N/A


Orchestration
=============

N/A


RPC Protocol
------------

N/A


Fuel Client
===========

* Implement all commands that are missing in the new fuel client.

* Delete old fuel client from the package.

* Add a deprecation warning about deleting fuel2 entry point in the next
  release.

* Set fuel entry point to start the new CLI.

* Make sure old fuel client is installable from PyPi.


Plugins
=======

N/A


Fuel Library
============

N/A


------------
Alternatives
------------

Basically this change is about resolving an old technical debt so there are
no alternatives.


--------------
Upgrade impact
--------------

If this change set concerns any kind of upgrade process, describe how it is
supposed to deal with that stuff. For example, Fuel currently supports
upgrading of master node, so it is necessary to describe whether this patch
set contradicts upgrade process itself or any supported working feature that.


---------------
Security impact
---------------

Removing old fuel client will also remove a lot of self-written code and
replace it with 3rd party libraries. This will make it easier to control
published CVEs and execute required actions.


--------------------
Notifications impact
--------------------

N/A


---------------
End user impact
---------------

Users will gain the following advantages of the new CLI:

* One unified CLI for all operations

* Possibility to use interactive mode

* Better compliance with OpenStack traditions of making command line clients.


The following problems are expected:

* Users will have to learn the new CLI

* Users may need to adapt their scripts


------------------
Performance impact
------------------

N/A


-----------------
Deployment impact
-----------------

* Deployment engineers will have to use new CLI.

* Automaded deployment tools will be able to use convenient Python API wrapper.

----------------
Developer impact
----------------

* No impact for fuel developers

* 3rd party developers will be able to use conveniend API wrapper to operate
  Fuel.


---------------------
Infrastructure impact
---------------------

CI scripts will have to be adapted to use new CLI before the old one is
deleted.


--------------------
Documentation impact
--------------------

* Release notes must be updated

* A comparision table of the old CLI and the new CLI must be included


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  romcheg

Other contributors:
  akalashnikov

Mandatory design review:
  dpyzhov


Work Items
==========

* Implement all missing commands in the new CLI.

* Adapt CI scripts to use fuel2 instead of fuel command.

* Delete the old fuel client.

* Make old fuel client available on PyPi.


Dependencies
============

N/A


------------
Testing, QA
------------

fuel-devops, fuel-qa and some tests need to be updated to use the new CLI
or the API wrapper instead of the old CLI.

Acceptance criteria
===================

* All capabilities of the old CLI are present in new CLI.

* Modules, tests and data files related to the old CLI are deleted from the
  package.

* Both fuel and fuel2 entry points start the new CLI.

* fuel2 entry point shows a deprecation warning saying it is going to be
  removed in the next release.

* The old CLI is installable from PyPi but not maintained.


----------
References
----------

# https://blueprints.launchpad.net/fuel/+spec/re-thinking-fuel-client
