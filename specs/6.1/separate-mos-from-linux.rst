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
split Linux distribution and MOS packages into the following parts:

* repository with vanilla untouched Linux packages (for CentOS)
* list of vanilla packages from upstream mirror (for Ubuntu)
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

The following changes will be introduced to the mirroring routine.

1. Upstream mirroring mode (USE_MIRROR=none):

a) The MOS repositories for CentOS and Ubuntu will be composed of a
   subset of packages from internal Fuel OSCI mirror. List of packages
   to download will be obtained by parsing requirements-[rpm|deb].txt
   files with yumdownloader/apt-get.Fuel packages will be excluded
   from download lists. Downloaded packages will be placed on the local
   mirror (LOCAL_MIRROR) into repositories called "mos-centos" and 
   "mos-ubuntu", respectively.

b) A subset of upstream vanilla CentOS packages that is required by
   Fuel, will be placed into the separate "centos-base" repository.

c) A list of upstream vanilla Ubuntu packages required by Fuel will
   be placed into the separate "ubuntu" repository under the
   download_urls_upstream.list filename. File format:

:: 
   /pool/main/a/accountsservice/accountsservice_0.6.15-2ubuntu9.7_amd64.deb
   /pool/main/a/accountsservice/libaccountsservice0_0.6.15-2ubuntu9.7_amd64.deb
   /pool/main/a/acct/acct_6.5.5-1ubuntu1_amd64.deb
   ....

2. Fuel mirroring mode (USE_MIRROR=<fuel_mirror_here>)

a) All objects listed above (MOS repositories for CentOS and Ubuntu
   repository with vanilla CentOS upstream packages, a list of vanilla
   Ubuntu upstream packages) will be downloaded as-is from specified
   Fuel mirror (MIRROR_CENTOS/MIRROR_UBUNTU) and placed on the local
   mirror (LOCAL_MIRROR).

Handling of extra repositories added by EXTRA_*_REPOS variables will
be moved out of the mirrors building context. Repositories specified
in these variables will be used as-is directly at the stage of nodes
provisioning rather than during creation of local mirror.


Proposed packages structure for divided repositories on a local mirror:


:: 

  $(LOCAL_MIRROR)
  |-- centos-base
  |   |-- os
  |       |-- x86_64
  |           |-- images
  |           |-- ...
  |           |-- repodata
  |-- fuel-centos
  |   |-- repodata
  |   |-- ...
  |-- fuel-ubuntu
  |   |-- Packages
  |   |-- ...
  |-- mos-centos
  |   |-- os
  |       |-- x86_64
  |           |-- images
  |           |-- ...
  |           |-- repodata
  |-- mos-ubuntu
  |   |-- dists
  |   |-- ...
  |   |-- pool
  |-- ubuntu
      |-- download_urls_upstream.list

Where:

* centos-base - contains upstream CentOS packages
* mos-centos and mos-ubuntu - contain CentOS and Ubuntu MOS packages
* fuel-centos and fuel-ubuntu - contain Fuel packages built during an ISO build
* ubuntu/download_urls_upstream.list - list of upstream Ubuntu packages

Packages building module
------------------------

Fuel packages build routine will be modified, instead of replacing Fuel
packages on local mirror, they will be moved into a separate repositories
named "fuel-centos" and "fuel-ubuntu:.

Docker containers building module
---------------------------------

All Dockerfile configs will be adjusted to include divided "centos-base"
and "mos-centos" repositories.

ISO assembly module
-------------------

Appropriate parts of ISO assembly and kickstart template for master node
will be adjusted to include divided repositories.

On Fuel ISO, all repositories mentioned in the "Local mirrors creation
module" chapter, will be placed into root folder as-is.

On a master node, all repositories mentioned in the "Local mirrors creation
module" chapter, will be copied into the /var/www/nailgun/{openstack-version}/
folder as-is.

Nailgun settings for default repositories
-----------------------------------------

Nailgun already supports usage of several repositories, however,
it does not support setting priorities/pinning for them. We will
implement handling of priorities via yum.conf and apt preferences,
respectively.

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
