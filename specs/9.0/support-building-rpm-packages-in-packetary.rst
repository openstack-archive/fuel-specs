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

We propose to use Docker because:

  - it allows to isolate build environment from host system with low-overhead
    resource allocation

  - it provides an easy way to parallelize building proccesses in a single host

  - it allows to use build tools without sudo privileges

---------
Isolation
---------

Each distribution type (e.g. rpm, deb) will have separate docker image with
necessary tools (mock for rpm based distributions) to perform building
operations. The docker images configuration will be described at separate
Dockerfiles for each image

Example of Dockerfile:

.. code-block:: Dockerfile
     FROM centos:centos7

     RUN yum -y --disableplugin=fastestmirror install mock && \
         useradd abuild -g mock

Packager will use short-lived docker containers to perform package building.
Docker images contain preconfigured build tools only. No chroots inside images.
Docker container destroyed after build stage is done.

-------------
Build targets
-------------

Each build target (e.g. CentOS6, CentOS7) will be described at separate config
file, which includes:

  - Target distribution type (rpm,deb)

  - Name of docker image, which will be used to run build stage

  - Path to chroot folder

  - Name of target chroot

  - URLs to upstream repositories for this distribution

  - Other configuration options

Example of build target config file:

.. code-block:: config
     CONTAINER_NAME=docker-builder-mock
     TYPE=rpm
     ROOT_DIR=/var/cache/docker-build/${TYPE}/root
     ROOT_NAME=centos-6-x86_64

     CONFIG_CONTENT="
     config_opts['plugin_conf']['tmpfs_enable'] = True
     config_opts['macros']['%dist'] = '.el6'
     config_opts['releasever'] = '6'

     config_opts['yum.conf'] = \"\"\"
     [base]
     baseurl=http://mirror.yandex.ru/centos/6/os/x86_64/
     \"\"\"
     "

Build chroot mounted to docker container on start in read-only mode. Inside
the container we mount tmpfs partition over r/o chroot folder with AUFS
overlays.

Goals of this scheme:

  - Could run a number of containers with the only chroot simultaneously

  - No need to perform cleanup operations after build; all changes matters
    inside container only and will be purged after container is destroyed

  - tmpfs works much faster than disk fs/lvm snapshots

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
