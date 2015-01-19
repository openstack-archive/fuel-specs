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
operating system separate from MOS and have them external to Fuel. We will
separate Linux distribution and MOS packages into the following repositories:

* repositories with vanilla untouched Linux packages
* repositories with Fuel packages (built during making of an ISO)
* repositories with MOS packages (built by OSCI)

Proposed change
===============

This document proposes to modify the following parts of the Fuel build
system:

* local mirrors creation module
* Fuel packages building module
* docker containers building module
* ISO assembly module

Handling of multiple package repositories in Nailgun will be extended
to allow setting of priorities during deployment.

Local mirrors creation module
-----------------------------

The mirrors creation module will be modified:

1) The MOS repositories for CentOS and Ubuntu will be fetched as-is
   from Fuel OSCI mirror and placed into "mos-centos" and "mos-ubuntu"
   repositories, respectively. Fuel packages built via OBS will be
   deleted from them, with further regeneration of repositories metadata.

2) A subset of vanilla Ubuntu packages that is required by Fuel but
   does not exist on Ubuntu ISO, will be placed into the separate
   "mos-plus" repository.

3) A subset of vanilla CentOS packages that is required by Fuel, will
   be placed into the separate "centos" repository.

4) Extra repositories added by EXTRA_*_REPOS variables will be 
   downloaded from OSCI build server as-is and used directly at
   the stage of nodes provisioning rather than during creation of
   local mirror.

5) Chroot creation routines will be modified to reflect the above
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
  |-- centos-fuel-6.1-stable-1607
  |   |-- centos
  |       |-- centos-fuel-6.1-stable-1607.repo
  |       |-- ...
  |       |-- repodata
  |-- fuel-centos
  |   |-- repodata
  |   |-- ...
  |   |-- nailgun-net-check-0.2-468.x86_64.rpm
  |-- fuel-ubuntu
  |   |-- Packages
  |   |-- ...
  |   |-- amd64
  |-- mos-centos
  |   |-- os
  |       |-- x86_64
  |           |-- images
  |           |-- ...
  |           |-- repodata
  |-- mos-plus
  |  |-- dists
  |  |-- ...
  |  |-- pool
  |-- mos-ubuntu
  |   |-- dists
  |   |-- ...
  |   |-- pool
  |-- ubuntu-fuel-6.1-stable-1622
      |-- ubuntu
          |-- Packages
          |-- ...
          |-- amd64

Where:

* centos - contains upstream CentOS packages
* mos-plus - contains a subset of required Ubuntu upstream packages missing on
  the Ubuntu relase ISO
* mos-centos and mos-ubuntu - contain CentOS and Ubuntu MOS packages
* fuel-centos and fuel-ubuntu - contain Fuel packages built during an ISO build
* centos-fuel-6.1-stable-1607 - example of repository added via EXTRA_RPM_REPOS
* ubuntu-fuel-6.1-stable-1622 - example of repository added via EXTRA_DEB_REPOS

.. note:: This step requires us to do the thorough cleanup of
  OSCI package repositores, because we need to keep there only
  those packages that differ from upstream ones. Keeping unneeded
  packages may break dependencies and affect nodes provisioning.

Packages building module
------------------------

Fuel packages build routine will be modified, instead of replacing Fuel
packages on local mirror, they will be moved into a separate repository.

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

* implement priorities and pinning for Nailgun - vkozhukalov
* implement downloading of OSCI MOS mirrors - vparakhin
* implement downloading of CentOS and Ubuntu upstream packages - vparakhin
* changes to building of Docker containers - vparakhin
* changes to building of Fuel packages - vparakhin
* changes to compilation of ISO - vparakhin

Dependencies
============

None

Testing
=======

As this document introduces structural changes to the ISO composition,
testing procedure must reflect the updated workflow for deploying Ubuntu
environments described in this blueprint. [1]_

* Test if master node can be bootstrapped
* Test if CentOS cluster can be provisioned
* Test if Ubuntu cluster can be provisioned

Documentation Impact
====================

None

References
==========

.. [1] related blueprint:  https://blueprints.launchpad.net/fuel/+spec/downloadable-ubuntu-release
