..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
refactor create mirror scripts
==============================

https://blueprints.launchpad.net/fuel/+spec/refactor-local-mirror-scripts

The blueprint describes the existing problem with scripts
to manage local mirrors for repositories.

-------------------
Problem description
-------------------

The 2 scripts with common functional increases the costs of maintenance.
The project "perestroika" will requires the same functional to manage
package`s lifecycle as well, that means we will have 3 versions of
same functional.

Need a library that provides core functional to manage
package`s lifecycle including management of repositories as well.

The other utilities to create mirros, build packages may be based
on this library.

There is 2 scripts for local mirrors management.
(fuel-package-updates and fuel-createmirror).
They were created in scope of a different features,
but in general they serve the same purpose.
The project "perestroika" requires the repository management tool as well.

A detailed description of the problem:

* For a new feature this might be use cases. Ensure you are clear about the
  actors in each use case: End User vs Deploy engineer

* For a major reworking of something existing it would describe the
  problems in that feature that are being addressed.


----------------
Proposed changes
----------------

There should be the one library, that will provide functional
to manage package`s lifecycle including repositories management.

It will have clearly defined extension points, at first to support
new formats of packages.


Web UI
======

None

Nailgun
=======

None

Data model
----------

None

REST API
--------

None

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

Use native utilities like apt-mirror or rsync,
but this utilities does not cover case of partial mirroring:
when copied only packages that is required by depends.

--------------
Upgrade impact
--------------

It can impact upgrading packages in local mirror.

---------------
Security impact
---------------

None

--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

There will be new utility to deal with local repositories.


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

The developers will have library to deal with packages.

--------------------------------
Infrastructure/operations impact
--------------------------------

CI and build tasks.
Need to build third-party packages, that will be required.

--------------------
Documentation impact
--------------------

Update documentation for fuel-createmirror and fuel-upgrade-packages utilities.

--------------------
Expected OSCI impact
--------------------

None

--------------
Implementation
--------------

The all required functional will be implemented on python
with using third-party modules to deal with
DEB and RPM packages and repositories.

The logic to resolve dependencies will be implemented on module
side to abstract from any repository format and operate only
with interfaces that is provided by library.

The next API methods will exposed from library:

- get_packages: returns the list of packages from repository(es)

- get_depends: returns the list of external depends for package(s)

- find_packages: find packages by depends list

- copy packages: copy packages to another location

- createrepo: create repository according to list of packages


Assignee(s)
===========

Primary assignee:
  bgaifullin@mirantis.com

Mandatory design review:
  skulanov@mirantis.com
  vkozhukalov@mirantis.com


Work Items
==========

- Declare interfaces and methods to deal with them.

- Algorithm to resolve dependencies.

- File-transfer layer: rsync, http.

- Debian packages support.

- RPM packages support.



Dependencies
============

None

-----------
Testing, QA
-----------

All algorithms should be covered by unit-test.

Integration tests:

There is 2 repositories A, B.
The repository B contains packages is required by packages from A.
Repository B is not depends on other repository.

Test cases:

- copy full A or/and B: checks that all packages can be installed.

- copy A, packages from B, that is required by A.
  checks that all packages can be installed.

All cases should be check for Debian repository and RPM repository as well.


Acceptance criteria
===================

User is able to create local mirror or update existing.


----------
References
----------

None