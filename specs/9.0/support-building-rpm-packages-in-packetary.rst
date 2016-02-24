..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Support building rpm packages in Packetary
==========================================

We need to support building of rpm packages in Packetary

--------------------
Problem description
--------------------

Perestroika build system will not be available in the future and we need to
implement package building module in Packetary to provide single application to
solve full range of tasks of packaging and repositories management

----------------
Proposed changes
----------------

We propose to re-implement Perestroika rpm packages building scripts to
integrate it in the Packetary and provide a Python application that wraps the
process to create a rpm package, relying on Docker and Mock to build rpm
packages in isolated environment.

------------------------
Supported source layouts
------------------------

Packager shoud support followins source layouts:

- Source rpm file (.srpm .src.rpm)

- Standard source layout (git project):

  .
  ├── source tarball (.tar.*z)
  ├── rpm specfile (.spec)
  └── other files related to package (.patch .init etc)

- Openstack source layout (two git projects):

  - source git project:

    .
    ├── source
    ├── files
    └── and folders

  - spec git project

    .
    └── build target name (centos7)
        └── rpm
            ├── SOURCES
            │   └── files related to package (.patch .init etc)
            └── SPECS
                └── rpm specfile (.spec)

    This layout should be converted to the standard one before build stage.
  Source tarball should be generated using `git-archive`.


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

* Koji:
  Supports rpm based distributions only
  https://fedoraproject.org/wiki/Koji

* Automated build farm (ABF):
  Supports rpm based distributions only
  http://www.rosalab.ru/products/rosa_abf
  https://abf.io/

* Delorean
  Supports rpm based distributions only
  Supports python packages only
  Requires separate docker image for each supported distribution
  https://github.com/openstack-packages/delorean

* docker-rpm-builder
  Supports rpm based distributions only
  Requires separate docker image for each supported distribution
  https://github.com/alanfranz/docker-rpm-builder

--------------
Upgrade impact
--------------

None

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

None

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

None

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Uladzimir Niakhai <uniakhai@mirantis.com>

Mandatory design review:
  Dmitry Burmistrov <dburmistrov@mirantis.com>

Work Items
==========

* Create interface to run docker command from python

* Implement rpm packages build

------------
Testing, QA
------------

None

Acceptance criteria
===================

The tests described above need to be passed.

----------
References
----------
