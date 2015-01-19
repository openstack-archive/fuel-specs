..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
Separate MOS from Linux repos
=============================

https://blueprints.launchpad.net/fuel/+spec/separate-mos-from-linux

Problem description
===================

* As a Cloud Operator I should be able to run OS updates as well as MOS updates
  during Product Life cycle

* As a Cloud Operator I would like to see what packages provided by MOS and
  what packages provided by OS Provider

* As a Cloud Operator I would like to have OS support contract as well as MOS
  support

* As a Cloud Operator I would like to get security updates as fast as possible
  independantly from OS Provider as well as from MOS

* As a Cloud Operator I should be able to see sources of OS and MOS packages

* As a Cloud Operator I should be able to see debug symbols of OS and MOS
  packages

* As a Developer, I would like to have the same approach for making changes to
  Fuel components and its dependencies.

To provide highest quality MOS should separate lifecycle OS and Cloud lifecycle
management. Meanwhile OS Updates shouldn't break MOS functionality and vice
versa.

Proposed change
===============

Organize MOS mirrors
--------------------

MOS mirrors should be organized in the same way as OS Provider mirrors.
MOS mirrors should follow industrial standards. The structure of mirror should
be done in the same way as OS Provider mirrors. Every supported OS will have
own repository containing MOS packages per release (mos6.1, mos7.0 ...)
Mirror should be publicly available and distributed. User should be able to
make local mirror to be able to perform offline installation

Top Level MOS mirror structure
------------------------------

.. note::This scheme will be fully implemented only for new MOS releases. For
         older releases that are still supported, we'll implement support of
         regular and security updates only.

::

  /
  +--+centos
  |  |
  |  +--+6
  |  |  |
  |  |  +--+mos6.0
  |  |  |
  |  |  +--+mos6.1
  |  |
  |  +--+7
  |     |
  |     +--+mos7.0
  |     |
  |     +--+mos7.1
  |
  +--+ubuntu
     |
     +--+dists
     |
     +--+pool
     |
     +--+...

Debian based mirror structure
-----------------------------
MOS mirror should include several channels (updates, security, partner) built
in the same way as OS Provider distributives mirrors (RHEL, Debian)


::

  $(OS_MIRROR)                 $(MOS_MIRROR)
  +                            +
  |                            |
  +--+ubuntu                   +--+ubuntu
     |                            |
     +--+dists                    +--+dists
     |  |                         |  |
     |  +--+precise-backport      |  +--+precise-proposed
     |  |                         |  |
     |  +--+precise-proposed      |  +--+precise-security
     |  |                         |  |
     |  +--+precise-security      |  +--+precise-updates
     |  |                         |  |
     |  +--+precise-updates       |  +--+precise
     |  |                         |  |
     |  +--+precise               |  +--+trusty-proposed
     |  |                         |  |
     |  +--+trusty-backport       |  +--+trusty-security
     |  |                         |  |
     |  +--+trusty-proposed       |  +--+trusty-updates
     |  |                         |  |
     |  +--+trusty-security       |  +--+trusty
     |  |                         |
     |  +--+trusty-updates        +--+indices
     |  |                         |  |
     |  +--+trusty                |  +--+...
     |                            |
     +--+indices                  +--+pool
     |  |                         |  |
     |  +--+...                   |  +--+main
     |                            |     |
     +--+pool                     |     +--+a
     |  |                         |     |
     |  +--+main                  |     +--+...
     |  |                         |     |
     |  +--+multiverse            |     +--+z
     |  |                         |
     |  +--+restricted            +--+project
     |  |                            |
     |  +--+universe                 +--+mos-archive-keyring.gpg
     |                               |
     +--+...                         +--+mos-archive-keyring.sig


RHEL based mirror structure
---------------------------

::

  $(OS_MIRROR)                           $(MOS_MIRROR)
  +                                      +
  |                                      |
  +--+centos-6                           +--+centos-6
  |  |                                   |  |
  |  +--+...                             |  +--+mos6.1
  |                                      |  |
  +--+centos-7                           |  +--+mos7.0
     |                                   |     |
     +--+7                               |     +--+os
        |                                |     |  |
        +--+os                           |     |  +--+x86_64
        |  |                             |     |     |
        |  +--+x86_64                    |     |     +--+Packages
        |     |                          |     |     |  |
        |     +--+Packages               |     |     |  +--+*.rpm
        |     |  |                       |     |     |
        |     |  +--+*.rpm               |     |     +--+RPM-GPG-KEY-MOS7.0
        |     |                          |     |     |
        |     +--+RPM-GPG-KEY-CentOS-7   |     |     +--+repodata
        |     |                          |     |        |
        |     +--+repodata               |     |        +--+*.xml,*.gz
        |        |                       |     |
        |        +--+*.xml,*.gz          |     +--+updates
        |                                |        |
        +--+updates                      |        +--+x86_64
           |                             |           |
           +--+x86_64                    |           +--+Packages
              |                          |           |  |
              +--+Packages               |           |  +--+*.rpm
              |  |                       |           |
              |  +--+*.rpm               |           +--+repodata
              |                          |              |
              +--+repodata               |              +--+*.xml,*.gz
                 |                       |
                 +--+*.xml,*.gz          +--+centos-7
                                            |
                                            +--+mos7.1
                                            |
                                            +--+mos8.0

Development mirrors
-------------------
Build system should allow developers to build packages, these packages should
be placed to special mirror which can be specified in Nailgun to deliver these
packages to environment. Later, this functionality should be exposed to
community allowing Community engineer (nova, cinder) to put own git repository
and commit, build system should build packages and provide link which will be
specified in Nailgun.

Local mirrors creation
----------------------
Handling of multiple repositories in Nailgun will be extended to allow setting
of priorities during deployment. By default user will use public mirrors,
though he will have option to create mirror on his facilities (including master
node).

Package Lifecycle management
----------------------------
To deliver high quality of product MOS teams should push package updates during
Product lifecycle.

Package flow should be specified from building package, passing SRU channel
(trusty-mos6.1-proposed as a sample), acceptance testing, security testing
before it will appear in "updates" in MOS mirror

Debian Package versioning
-------------------------

#. When adding a new package add the suffix ~mos${MOS_VERSION} to the original
   presumably Debian style version.  MOS_VERSION is the target MOS release.
   Adding packages without such a version suffix is strictly forbidden.

  - We need to track the modifications both for technical and for legal
    reasons.  Adding version suffix makes such tracking very trivial.

  - Switching back to the Ubuntu version of a package should be as easy as
    possible. Adding ~something suffix to the version makes our package
    formally older than the original (this is a common practice of
    backporting).

  .. example :

  suppose the package foo version 1.2.3-0ubuntu13.10 should be added to MOS
  6.1. The suffix ~mos6.1 should be added to the version, thus the version of
  the backported foo package is 1.2.3-0ubuntu13.10~mos6.1

#. When updating the backported package (such as applying a custom patch) an
   extra +${PKG_REVISION} suffix.

   - We need to identify the patched packages without having to look at the
     actual source.

  .. example :

  suppose the package foo version 1.2.3-0 ubuntu13.10~mos6.1 needs a bugfix
  (which is not available in Ubuntu). After adding a patchthe version should
  be changed to 1.2.3-0ubuntu13.10~mos6.1+1

#. The only permitted modification of version is adding the above mentioned
   suffixes. In particular increm enting the original version or truncating it
   is strictly forbidden.

   - make it possible to backport newer revisions (which migh tcontain new
     bugfixes) from Ubuntu without introducing version conflicts.

   .. example :

   OK: 1.2.2-0ubuntu13.1 -> 1.2.2-0ubuntu13.1~mos6.1+1
   WRONG: 1.2.2-0ubuntu13.1 -> 1.2.2-0ubuntu13.2
   WRONG: 1.2.2-0ubuntu13.1 -> 1.2.2-ubuntu1
   WRONG: 1.2.2-0ubuntu13.1 -> 1.2.3-0ubuntu13.1

Packages building module
------------------------

Fuel DEB packages build routine will be dropped. Fuel DEB packages will be
consumed from the MOS mirror directly on master node. [1]_

Control files for Fuel DEB packages will be moved to the public MOS Gerrit
instance.

Explicit list of Fuel DEB packages is below:

* fencing-agent
* nailgun-mcagents
* nailgun-net-check
* nailgun-agent
* python-tasklib

Docker containers building module
---------------------------------

All Dockerfile configs will be adjusted to include both upstream and MOS
repositories.

ISO assembly module
-------------------

ISO assembly module will be adjusted to exclude all parts mentioned above.

Offline installations
---------------------

To support the offline installations case we will implement the script that
mirrors the public MOS and Upstream mirrors locally on master node, and
puts these local sources as input during the "Installation Wizard".

Alternatives
------------

There is no alternative to the repositories separation approach due to
considerations related to distribution policies of major OS vendors.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

None. By following the packaging policies of respective OS vendors, we
will make upgrades as simple as the ones in an upstream OS. So, instead
of rolling upgrades from a new release ISO, packages will be consumed
directly from MOS mirrors.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

In case of offline installations, user will be required to create a
copy of MOS/Upstream mirrors by using a script described in this
document.

Performance Impact
------------------

If packages are consumed from remote 3rd party servers, overall deployment
time may be increased. In case of offline installation, no deployment speed
degradation is expected.

Other deployer impact
---------------------

Changes described in this document allow to increase product flexibility,
by making possible to choose an operating system and install it independent
of MOS.

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Vitaly Parakhin <vparakhin@mirantis.com>
  Dmitry Burmistrov (make build system with updates and security updates)
  DevOPS (organize mirror, organize status page)

QA:
  Artem Panchenko <apanchenko@mirantis.com>
  Denis Dmitriev <ddmitriev@mirantis.com>

Mandatory Design Reviewers:
  Sergii Golovatiuk <sgolovatiuk@mirantis.com>
  Tomasz Napierala <tnapierala@mirantis.com>
  Vladimir Kuklin <vkuklin@mirantis.com>
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>
  Roman Vyalov <rvyalov@mirantis.com>

Work Items
----------

* Create local OS mirrors for CI purposes
* Change Fuel make system to exclude Ubuntu packages from ISO
* Create MOS mirror with the same structure as OS vendor
* Deb package build process should be changed. All packages should be put in
  MOS mirror
* Create CI Jobs to test against OS vendor SRU [2]_
* Create status page to notify customers in case of problems with OS updates.
   - Create apt hooks to notify the customer in case of "apt-get upgrade"
* Adapt system tests of Ubuntu for the new repositories workflow
* Implement script for creating of local Upstream and MOS mirrors on master
  node.

Dependencies
============

None

Testing
=======

As this document introduces structural changes to the ISO composition and
MOS mirrors layout, testing procedure must reflect the updated workflow
for deploying Ubuntu environments described in this blueprint. [1]_

* Test if master node can be bootstrapped
* Test if CentOS cluster can be provisioned
* Test if Ubuntu cluster can be provisioned

Documentation Impact
====================

The documentation should cover the case of using a script for creating of local
Upstream and MOS mirrors on master node for offline installations.

The documentation should cover the description of a new packages lifecycle
in MOS.

References
==========

.. [1] `Consume External Ubuntu <https://blueprints.launchpad.net/openstack/?searchtext=consume-external-ubuntu`_
.. [2] `Ubuntu SRU procedure <https://wiki.ubuntu.com/StableReleaseUpdates#Examples>`_
.. [3] `Building target images with Ubuntu on master node <https://blueprints.launchpad.net/fuel/+spec/ibp-build-ubuntu-images>`_