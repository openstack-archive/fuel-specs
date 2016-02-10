..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Support building rpm packages in Packetary
==========================================

We need support in building rpm packages in Packetary

--------------------
Problem description
--------------------

Perestroika build system will not be available in the future and we need
implement package building in Packetary to provide single application to solve
full range of tasks of packages and repositories management

----------------
Proposed changes
----------------

We proposed to re-implement Perestroika rpm packages building scripts to
integrate it in Packetary and provide a Python application that wraps the
process to create a rpm package, relying on Docker and Mock to build clean 
packages in chrooted environment.

We propose to use Docker because it allows to build both rpm and deb packages
in one host machine using standard upstream Linux distribution build tools for
particular packege type (Mock, rpmbuild for rpm).  Also using the docker it is
easier to parallelize building proccess in a single host machine. For using
docker will be created proper Docker Images for each supported Linux
distribution with necessary tools and scripts.

Every package is built in a clean and up-to-date buildroot. Packages, their
dependencies, and build dependencies are fully self-contained for each Mirantis
OpenStack release. Any package included in any release can be rebuilt at any
point in time using packages from that release and upstream distribution
packages.

Package build CI will be reproducible and can be recreated from scratch in a
repeatable way.

New build system is based on Docker, which provides easy distribution.

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
