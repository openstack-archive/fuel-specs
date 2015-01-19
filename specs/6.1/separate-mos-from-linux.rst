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
* repository with everything else (repository with other Linux packages,
  OpenStack packages, Fuel packages etc)

Proposed change
===============

This bluprint proposes to modify the following parts of the Fuel build
system:

* configuration variables
* local mirrors creation module
* image-based provisioning module
* bootstrap creation module
* docker containers building module
* ISO assembly module
* Nailgun settings for default repositories

Introduce new configuration variables
-------------------------------------

The following variables and their respective default values will be added
to config.mk:

+-------------------------------------+-----------------------------------------------+
| Variable                            | Default value                                 |
+=====================================|===============================================+
| LOCAL_MIRROR_CENTOS_BASE            | $(LOCAL_MIRROR)/centos-base                   |
| LOCAL_MIRROR_CENTOS_BASE_OS_BASEURL | $(LOCAL_MIRROR_CENTOS_BASE)/os/$(CENTOS_ARCH) |
| LOCAL_MIRROR_CENTOS_FUEL            | $(LOCAL_MIRROR)/centos-fuel                   |
| LOCAL_MIRROR_CENTOS_FUEL_OS_BASEURL | $(LOCAL_MIRROR_CENTOS_FUEL)/os/$(CENTOS_ARCH) |
| LOCAL_MIRROR_UBUNTU_BASE            | $(LOCAL_MIRROR)/ubuntu-base                   |
| LOCAL_MIRROR_UBUNTU_BASE_OS_BASEURL | $(LOCAL_MIRROR_UBUNTU_BASE)                   |
| LOCAL_MIRROR_UBUNTU_FUEL            | $(LOCAL_MIRROR)/ubuntu-fuel                   |
| LOCAL_MIRROR_UBUNTU_FUEL_OS_BASEURL | $(LOCAL_MIRROR_UBUNTU_FUEL)                   |
+-------------------------------------+-----------------------------------------------+

Local mirrors creation module
-----------------------------

The mirrors creation module will be modified. The Fuel repository will be
fetched as-is from Fuel OSCI mirror. Packages from upstream Linux repository
will be downloaded into a separate repository.

Proposed packages structure for divided repositories on a local mirror:

:: 

  fuel-main/local_mirror
  |-- centos-fuel
  |   |-- os
  |       |-- x86_64
  |           |-- images
  |           |-- ...
  |           |-- repodata
  |-- centos-base
  |   |-- os
  |       |-- x86_64
  |           |-- images
  |           |-- ...
  |           |-- repodata
  |-- ubuntu-fuel
  |   |-- dists
  |   |-- ...
  |   |-- pool
  |-- ubuntu-base
      |-- dists
      |-- ...
      |-- pool

centos-base and ubuntu-base - contains upstream Linux packages
centos-fuel and ubuntu-fuel - contains all other packages

.. note:: This step requires us to do the thorough cleanup of
  OSCI package repositores, because we need to keep there only
  those packages that differ from upstream ones.

Image-based provisioning module
-------------------------------

<TBD>

Bootstrap creation module
-------------------------

<TBD>

Docker containers building module
---------------------------------

All Dockerfile configs will be adjusted to include "centos-base"
and "centos-fuel" repositories instead of a current "nailgun" one.

ISO assembly module
-------------------

Appropriate parts of ISO assembly and kickstart template for master node
will be adjusted to work with separated repositories.

Proposed structure of separated repositories on an ISO:

<TBD>

Nailgun settings for default repositories
-----------------------------------------

Nailgun settings in settings.yaml from fuel-web repository will
be adjusted to include \*-fuel and \*-base repositories instead of
old "centos" and "ubuntu" entries.

Proposed structure of separated repositories on a master node:

:: 

  /var/www/nailgun
  |-- centos-fuel
  |   |-- fuelweb
  |       |-- x86_64
  |           |-- images
  |           |-- ...
  |           |-- repodata
  |-- centos-base
  |   |-- fuelweb
  |       |-- x86_64
  |           |-- images
  |           |-- ...
  |           |-- repodata
  |-- ubuntu-fuel
  |    |-- fuelweb
  |        |-- x86_64
  |            |-- dists
  |            |-- ...
  |            `-- pool
  |-- ubuntu-base
      |-- fuelweb
          |-- x86_64
              |-- dists
              |-- ...
              |-- pool

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

None