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

The fuel-createmirror was written as a bash script by OSCI team.
At the moment it doesn't have an owner and nobody is to fix bugs in it.
It supports only Debian repositories.
It requires Docker to work.

----------------
Proposed changes
----------------

Move the common functional for working with packages and repositories
to separated python library - packetary.

The library will consist of components:

  * **Infrastructure**
    - Asynchronous command execution.
    - Control the number of simultaneously opened connections.

  * **Transport**
    - Remote files access
    - Streaming

  * **Technology**
    - Drivers to work with different formats of packages and repositories.

  * **Business logic**
    - Main functional for copying packages, creating repositories, etc.

  * **Public API**
    - The public methods to use for integration.

The fuel-createmirror will be rewritten by using API of packetary.


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

None

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

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  bgaifullin@mirantis.com

Mandatory design review:
  skulanov@mirantis.com
  vkozhukalov@mirantis.com


Work Items
==========

* Declare library interfaces and methods.

* Implement algorithm for dependency resolving.

* Implement file-transfer layer.

* Implement driver for Debian repositories.

* Implement driver for Yum repositories.

* Implement command-line interface for packetary.

* Rewrite fuel-createmirror interface by using API of packetary.


Dependencies
============

None

-----------
Testing, QA
-----------

**Precondition**
  Prepare repositories A and B, that met the requirements:
    - Repository A contains packages that depends on packages from the B.
    - Repository B is not depends on other repositories.

**Test cases**

* Copy repository B.
   Checks that all packages can be installed.

* Copy repository A and packages from B that is by A.
  Checks that all packages can be installed.

All cases should be checked for Debian and RPM repositories.


Acceptance criteria
===================

User is able to create local mirror or update existing.


----------
References
----------

None