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

It is proposed to move common functional to separate library - packetary.

In order to implement the main feature of the utility – an ability to copy
only part of packages from a repository that is required to install
the product, a mechanism for building the dependencies tree between
the packages is needed. Since that functionality is common for all
types of repositories, it should not depend on the specific
repository or package format. To meet this requirement we need to elaborate
a separate substance “Package” that will be abstracting from
the physical format of the package and providing all the necessary
interfaces for search and resolving dependency basing on the
version and name of the package.
The dependency tree itself will be implemented based on the red-black tree,
where the keys are the name and version of the package.

When searching for a package it`s needed to consider information about
obsolete and virtual packages, hence there will be three trees instead of one:
- tree of package
- tree of obsolete packages
- tree of virtual packages

During the search for a package, these trees will be following
in a certain order:
- main tree (e.g. tree of package)
- tree of obsolete packages
- tree of virtual packages

When a suitable package is found, the search stops.

It is assumed to support multiple repository formats, hence it is needed
to distinguish the code to work with specific repository formats
into the separate classes - drivers. In this case, to maintain the desired
repository format it is needed to implement an appropriate driver,
the business logic works with the data provided by the driver.
Since creating a mirror implies download packages, then a separate
layer of abstraction over the transport is required.
Due to the fact that the rsync mechanism is slower on partial mirrors;
it is proposed to support only HTTP-transport with possibility
of resuming downloads and multiple threads download
(which will make it possible to use the entire network bandwidth).

It is proposed to use the thread pool and the network connections pool
to implement that functionality. There should be a check if a package needs
to be downloaded. The check mechanism will be divided into two stages
just to make that simpler:
- Full check, that checks the checksum of packages on demand.
- Fast check, that checks file size only when copying a package.

Thread pool allows running file checks in parallel, and network connections
pool allows controlling the number of concurrent network connections.

Createmirror utility will depend on the packetary and python-client libraries.
The first library will be used for creation and synchronization of the mirrors,
the second one to update meta-information on the Fuel-backend.

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

We are going to test functionality on 3 levels:
Unit testing;
Functionl testing;
Integration testing.

------------
Unit testing
------------
Tests on fuel-createmirror sub units. Will cover code by developer.

-----------------
Functionl testing
-----------------
**Precondition**
  Prepare repositories A and B, that met the requirements:
    - Repository A contains packages that depends on packages from the B.
    - Repository B is not depends on other repositories.

**Test cases**

* Copy repository B.
   Checks that all packages can be installed.

* Copy repository A and packages from B that is by A.
   Checks that all packages can be installed.

* Copy repository with network issues.
   Checks that correctly created mirror is done under
   network failures. Or it is failed with message.

* Copy repository via proxy.
   Checks that user can create mirror without full access
   to Internet.

All cases should be checked for Debian and RPM repositories.

-------------------
Integration testing
-------------------
Tests which cover fuel-createmirror in fuel eco-system.
To deploy environment we should add custom packages to create
bootstrap image. So simple mirror copying is not enough to
have a successful deployment.

**Test cases**

* Install environment with 3 controllers, 1 cinder and 1 compute
   with custom mirror.
* Install environment with 3 controllers, 1 ceph and 1 compute
   with custom mirror.


Acceptance criteria
===================

User is able to create local mirror or update existing and 
to deploy environment with that mirror.


----------
References
----------

None