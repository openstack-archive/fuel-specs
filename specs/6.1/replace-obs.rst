..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Replace OBS
==========================================

URL of the related launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/replace-obs

We are going to create a new packaging build system inside internal infrastructure and get rid from existing one due to issues related to building process.

Problem description
===================

A detailed description of the problem:

Currently OSCI team is using OBS as 'all in one' service for building, publishing and signing of DEB and RPM packages as well.We faced a number of challenges with OBS during the last year.

* OBS builds packages in its own way which is different from upstream. It causes an issues when upstream package can't be rebuilt without changing packages sources.
* OBS rebuilds package when its build dependency changed (and doesn't update revision number of such package)
* OBS uses base upstream packages for target in the building stage. Every change in the target causes rebuilding of each package which was built with this target.
* OBS doesn't support publishing udeb binary packages. This is due to the fact that it uses plain debian repository structure. But deb and udeb packages should not be published in one repository.
* Our current OBS version (2.4) doesn't support debian python:any dependencies. That's why we decided to create new OBS (2.6) instance. We can't update current version because it totally breaks supporting previously shipped releases.
* OBS doesn't support signing with predefined key. Only OBS auto generated keys can be used. Every OBS project has it's own key. Such keys can't be exported from OBS.
* It's quite hard to reproduce our CI due to OBS. Every MOS OBS project based on previously shipped project. (e.g. 6.1 and 6.0.1 based on 6.0 release, 6.0 based on 5.1 and so on). So if you need to reproduce our CI for 6.1 release, you need to rebuild all packages for all shipped releases since 3.2.
* OBS server side natively supported on openSUSE and SUSE Linux Enterprise Server.
* We cannot support OBS as well as distribute it for our customers.

Proposed change
===============
* Using of native build tools for building DEB and RPM packages shall help us to solve bugs with versioning and make the build process open and transparent. By 'native build tools' we mean:

 * 'sbuild' for DEB packages.
 * 'mock' for RPM packages.

* We can use Docker as wrapper for 'sbild' and 'mock' with our scripts inside.
* We can wrap host side scripts of interaction in a package for easy deployment.

Alternatives
------------

We can try to use another build system for packages which shall support RPM and DEB packaging at once.

Data model impact
-----------------

None

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

Infrastructure impact
---------------------

In case of full replacement of OBS from infrastructure we shall think about publishing our packages on mirrors since there is no way to use publishing part of OBS with any foreign package builder instead of OBS package builder.
 * Current workflow of bulding packages will be the same in general. 
 * We shall test and replace our current OBS related jenkins jobs on new ones.
 * We shall think about using Docker Hub as main repository of Docker Images
 * Deployment of infrastructure components shall be changed and reviewed.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
 `dburmistrov <https://launchpad.net/~dburmistrov>`_

Other contributors: 
 `dkaiharodsev <https://launchpad.net/~dkaiharodsev>`_


Work Items
----------

* Write a scripts for interaction with native build tools inside Docker Images and pack them into DEB package.
* Create Docker Images with packaging tools (sbuild and mockbuild) inside.
* Create a Jenkins job for bulding packages by using Docker based packaging system.
* Write a Puppet manifests for deploying buld system.
 
Dependencies
============

* https://blueprints.launchpad.net/fuel/+spec/replace-obs

* https://blueprints.launchpad.net/fuel/+spec/puppet-manifest-for-new-build-sysem

Testing
=======

All of the scripts and Jenkins jobs shall be tested in a sandbox environment for building packages.
We shall compare performance results of building inside Docker with currently used OBS.


Documentation Impact
====================

In case of using new build system we shall change workflow documentation where OBS mentioned.


References
==========

* OBS https://build.opensuse.org/
* Docker https://www.docker.com/
* Docker Hub https://hub.docker.com/
*  sbuild https://wiki.debian.org/sbuild
*  mock https://fedoraproject.org/wiki/Projects/Mock).
* Puppet https://puppetlabs.com/