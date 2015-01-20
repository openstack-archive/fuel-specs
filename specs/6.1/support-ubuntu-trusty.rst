..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Support Ubuntu 14.04 (Trusty)
============================================

https://blueprints.launchpad.net/fuel/+spec/support-ubuntu-trusty

Problem description
===================

* At the moment Fuel provisions Ubuntu 12.04 (Precise) as a Host OS.

* ISO Build System is specifically designed for Precise. It doesn't allow to
  build Ubuntu 14.04 (Trusty) as Host System. It doesn't have any flexibility
  for any further Ubuntu Releases.

* Ubuntu 14.04 (Trusty) uses Ruby 1.9 by default. Fuel Puppet Providers have
  not been designed for Ruby 1.9.

* Many Packages were backported from Ubuntu 14.04 (Trusty). In MOS 6.1 the
  number of modified system packages (haproxy, MySQL, Galera) should be
  minimized as much as possible.

* Package Versioning and Metadata Handling is not standartized.


Proposed change
===============

- Adapt Build System to make iso with Ubuntu 14.04 (Trusty) packages.

- Adapt Puppet's Manifests for Ruby 1.9

- Minimize the number of customized packages required by MOS.

- Build MOS specific packages for Ubuntu 14.04 (OpenStack Components and MOS
  related such as Ceph)

Debian Package Versioning
-------------------------

#. When adding a new package add the suffix ~mos${MOS_VERSION} to the original
   presumably Debian style Version.  MOS_VERSION is the target MOS release.
   Adding packages without such a version suffix is strictly forbidden.

  - Package name, metadata shouldn't contain any Registered trademarks.

  - We need to track the modifications both for technical and for legal
    reasons. Adding ~mos${MOS_VERSION} suffix makes such tracking very trivial.

  .. example :

  suppose the package foo version 1.2.3-0ubuntu13.10 should be added to MOS
  6.1. The suffix ~mos6.1 should be added to the version, thus the version of
  the backported foo package is 1.2.3-0mos6.1.

  Technically, CI should track any changes to disallow upstream packages with
  higher suffixes to override suffix


#. When updating the backported package (such as applying a custom patch) an
   extra +${PKG_REVISION} suffix.

   - We need to identify the patched packages without having to look at the
     actual source.

  .. example :

  suppose the package foo version 1.2.3-0mos6.1 needs a bugfix
  (which is not available in Upstream). After adding a patch the version should
  be changed to 1.2.3-0mos6.1+1

#. The only permitted modification of version is adding the above mentioned
   suffixes. In particular incrementing the original version or truncating it
   is strictly forbidden.

   - make it possible to backport newer revisions (which might contain new
     bugfixes) from Ubuntu without introducing version conflicts.

   .. example :

   OK: 1.2.2-0ubuntu13.1 -> 1.2.2-0mos6.1

#. When Suffix in Upstream package becomes higher than package in our
repository package in our repository should be bumped to have higher suffix
version.

  .. example:
  1.2.2-1ubuntu14.4 -gt 1.2.2-0mos6.1
  1.2.2-1mos6.1 -gt 1.2.2-1ubuntu14.4 (Version bumped)

Debian Package Metadata
-----------------------

When adding a new package to Product repository there several rules that must
be followed.

#. Latest record in changelog should contain Mirantis
#. Maintainer in Debian Control should be MOS Team

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

Due to significant difference between Ubuntu 12.04 (Precise) and Ubuntu 14.04
(Trusty) Cloud Operators won't be able to upgrade already installed clouds to
Ubuntu 14.04 (Trusty). Ubuntu 14.04 (Trusty) will be offered as option only for
new cloud installations. Meanwhile already deployed clusters will be able to
add compute nodes as well as controllers as Ubuntu 12.04 (Precise) repo won't
be changed.

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

Deployment Engineers as well as System Test will require to use

export OPENSTACK_RELEASE="Juno on Ubuntu 14.04.1"

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Sergii Golovatiuk <sgolovatiuk@mirantis.com>
  Aleksei Sheplyakov <asheplyakov@mirantis.com>

QA assignee:
  Andrey Sledzinskiy <asledzinskiy@mirantis.com>
  Aleksandr Kurenyshev <akurenyshev@mirantis.com>

Other contributors:
  mos-linux
  fuel-osci
  fuel-library

Work Items
----------

* Modify Build System to allow to build ISO with Ubuntu 14.04 (Trusty)

* Adapt Puppet Ruby providers for Ruby 1.9

* Build MOS Packages for Ubuntu 14.04 (Trusty)

Dependencies
============

* `Separate MOS from Linux Repositories <https://blueprints.launchpad.net/fuel/+spec/separate-mos-from-linux>`_

* `Fetch Ubuntu Packages as external source <https://blueprints.launchpad.net/fuel/+spec/downloadable-ubuntu-release>`_

* OpenStack Patching Process

Testing
=======

* ISO with Ubuntu 14.04 passes all BVT/Swarm tests
* All main clusters configurations can be successfully deployed
* All additional components like Sahara, Murano, Ceilometer, Zabbix
  are to be deployed

Documentation Impact
====================

None

References
==========

None
