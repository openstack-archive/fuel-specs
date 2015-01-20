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

Proposed change
===============

- Adapt Build System to make iso with Ubuntu 14.04 (Trusty) packages.

- Adapt Puppet's Manifests for Ruby 1.9

- Minimize the number of customized packages required by MOS.

- Build MOS specific packages for Ubuntu 14.04 (OpenStack Components and MOS
  related such as Ceph)

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

All changes should pass whole testing cycle including manual testing, BVT and
OSTF.

Documentation Impact
====================

None

References
==========

None
