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

To facilitate patching and to make Fuel more modular we need to keep the
operating system separate from MOS and have them external to Fuel. During
the first phase, which is covered by this document, we will separate
Linux distribution and MOS packages into the following repositories:

* repository with vanilla untouched Linux packages
* repository with Fuel packages (built during making of an ISO)
* repository with MOS packages (built by OSCI)

Proposed change
===============

This document proposes to modify the following parts of the Fuel build
system:

* local mirrors creation module
* Fuel packages building module
* docker containers building module
* ISO assembly module
* Nailgun settings for default repositories

Local mirrors creation module
-----------------------------

The mirrors creation module will be modified:

1) The MOS repository will be fetched as-is from Fuel OSCI mirror.

2) A subset of vanilla Linux packages that is required by Fuel but
   does not exist on CentOS/Ubuntu ISO, will be placed into a separate
   repository.

3) Extra repositories added by EXTRA_*_REPOS variables will be used
   directly at the stage of nodes provisioning rather than during
   creation of local mirror.

4) Chroot creation routines will be modified to reflect the above
   changes. Both CentOS and Ubuntu ones will be bootstrapped from
   upstream repositories. In case if there are MOS packages required
   inside these chroots, respective local MOS repository will be
   included to their yum/apt configuration with highest priority. 

Proposed packages structure for divided repositories on a local mirror:


:: 

  fuel-main/local_mirror
  |-- centos
  |   |-- os
  |       |-- x86_64
  |           |-- images
  |           |-- ...
  |           |-- repodata
  |-- centos-fuel
  |       |-- repodata
  |       |-- ...
  |-- centos-fuel-6.1-stable-1607
  |   |-- centos
  |       |-- centos-fuel-6.1-stable-1607.repo
  |       |-- ...
  |       |-- repodata
  |-- centos-mos
  |   |-- os
  |       |-- x86_64
  |           |-- images
  |           |-- ...
  |           |-- repodata
  |-- ubuntu
  |   |-- dists
  |   |-- ...
  |   |-- pool
  |-- ubuntu-fuel
  |   |-- Packages
  |   |-- ...
  |   |-- amd64
  |-- ubuntu-fuel-6.1-stable-1622
  |   |-- ubuntu
  |       |-- Packages
  |       |-- ...
  |       |-- amd64
  |-- ubuntu-mos
      |-- dists
      |-- ...
      |-- pool

Where:

* centos and ubuntu - contain a subset of required upstream packages missing
  on a respective upstream ISO
* centos-fuel and ubuntu-fuel - contain Fuel packages
* centos-mos and ubuntu-mos - contain MOS packages
* centos-fuel-6.1-stable-1607 - example of repository added via EXTRA_RPM_REPOS
* ubuntu-fuel-6.1-stable-1622 - example of repository added via EXTRA_DEB_REPOS

.. note:: This step requires us to do the thorough cleanup of
  OSCI package repositores, because we need to keep there only
  those packages that differ from upstream ones. Keeping unneeded
  packages may break dependencies and affect nodes provisioning.

Packages building module
------------------------

Fuel packages build routine will be modified, instead of replacing Fuel packages
on local mirror, they will be moved into a separate repository.

Docker containers building module
---------------------------------

All Dockerfile configs will be adjusted to include repositories
defined in EXTRA_RPM_REPOS.

ISO assembly module
-------------------

Appropriate parts of ISO assembly and kickstart template for master node
will be adjusted to include separate repositories.

Nailgun settings for default repositories
-----------------------------------------

Nailgun already supports usage of several repositories, however,
it does not support setting priorities/pinning for them. We will
implement handling of priorities via yum.conf and apt preferences,
respectively.

:: 

  /var/www/nailgun
  |-- centos
  |   |-- fuelweb
  |       |-- x86_64
  |           |-- images
  |           |-- ...
  |           |-- repodata
  |-- centos-fuel-6.1-stable-1607
  |   |-- centos
  |       |-- centos-fuel-6.1-stable-1607.repo
  |       |-- ...
  |       |-- repodata
  |-- centos-fuel
  |       |-- repodata
  |       |-- ...
  |-- ubuntu
  |   |-- dists
  |   |-- ...
  |   |-- pool
  |-- ubuntu-fuel
  |   |-- Packages
  |   |-- ...
  |-- ubuntu-fuel-6.1-stable-1622
      |-- ubuntu
          |-- Packages
          |-- ...
          |-- amd64


Alternatives
------------

There is no alternative to the repositories separation approach due to
legal considerations related to distribution policies of major OS vendors.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Upgrade repositories use their own paths inside /var/www/nailgun, so they
shouldn't be affected.

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

Mandatory Design Reviewers:
  Roman Vyalov <rvyalov@mirantis.com>
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>

QA:
  Artem Panchenko <apanchenko@mirantis.com>
  Denis Dmitriev <ddmitriev@mirantis.com>

Work Items
----------

Blueprint will be implemented in several stages:

* stage 1 - implement separation for Ubuntu - planned for 6.1
* stage 2 - implement separation for CentOS - to be discussed

Dependencies
============

None

Testing
=======

* Test if master node can be bootstrapped
* Test if CentOS cluster can be provisioned
* Test if Ubuntu cluster can be provisioned

Documentation Impact
====================

None

References
==========

.. [1] related blueprint:  https://blueprints.launchpad.net/fuel/+spec/downloadable-ubuntu-release
