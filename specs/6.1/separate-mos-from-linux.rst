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

* local mirrors creation module
* docker containers building module
* ISO assembly module
* Nailgun settings for default repositories

Local mirrors creation module
-----------------------------

The mirrors creation module will be modified:

* The Fuel packages repository will be fetched as-is from Fuel
  mirror. Packages from upstream Linux repository will be downloaded
  into a separate repository.

.. note:: This step requires us to do the thorough cleanup of
  OSCI package repositores, because we need to keep there only
  those packages that must differ from upstream ones.

Packages structure for divided repositories on a local mirror:

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


Docker containers building module
---------------------------------

All Dockerfile configs will be adjusted to include "centos-base"
and "centos-fuel" repositories instead of a current "nailgun" one.


ISO assembly module
-------------------

The structure of separated repositories on a master node:

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

Appropriate parts of ISO assembly and kickstart template for master node
will be adjusted to work with separated repositories.

Nailgun settings for default repositories
-----------------------------------------

Nailgun settings in settings.yaml from fuel-web repository will
be adjusted to include \*-fuel and \*-base repositories instead of
old "centos" and "ubuntu" entries.

Alternatives
------------

None

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

None

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

* Phase 1 - implement separation for Ubuntu - planned for 6.1
* Phase 2 - implement separation for CentOS - to be discussed

Dependencies
============

* The "Local mirrors creation module" chapter will require list of
  packages to keep on the internal Fuel mirrors, it is prepared in
  terms of the following blueprint:

https://blueprints.launchpad.net/fuel/+spec/support-ubuntu-trusty

Testing
=======

<TBD>

Documentation Impact
====================

None

References
==========

None