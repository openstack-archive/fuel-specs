..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Migration to Ubuntu 16.04 (Xenial Xerus)
============================================

https://blueprints.launchpad.net/fuel/+spec/support-ubuntu-xenial-xerus

Problem description
===================

* At the moment Fuel provisions Ubuntu 14.04 (Trusty) as a Host OS, but
  Ubuntu 16.04 (Xenial Xerus) is coming.

* Systemd is a new system and service manager (Upstart is obsolete in
  Ubuntu 16.04 (Xenial Xerus) and is not to be used any more).

* Ubuntu 16.04 (Xenial Xerus) uses Ruby 2.3 by default. Fuel Puppet
  Providers was designed to work with ruby 1.9 currently used in Ubuntu
  14.04 (Trusty).

* There are backported system packages from Ubuntu 15.04 or 16.04 (Xenial
  Xerus), which should be updated to currently shipped with Ubuntu 16.04 to
  minimize such custom system packages as much as possible.


Proposed change
===============

- Adapt MOS specific initialization scripts to systemd service manager.

- Adapt Puppet's Manifests for Ruby 2.3

- Minimize the number of customized packages required by MOS.

- Build MOS specific packages for Ubuntu 16.04 (OpenStack Components and MOS
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

Due to significant difference between Ubuntu 14.04 (Trusty) and Ubuntu 16.04
(Xenial Xerus) Cloud Operators won't be able to upgrade already installed
clouds to Ubuntu 16.04 (Xenial Xerus). Ubuntu 16.04 (Xenial Xerus) will be
offered as option only for new cloud installations.

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

export OPENSTACK_RELEASE="Newton on Ubuntu 16.04.1"

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Albert Syriy <asyriy@mirantis.com>
  Dmitriy Teselkin <dteselkin@mirantis.com>
  Ivan Suzdal <isuzdal@mirantis.com>

QA assignee:

Other contributors:
  mos-linux
  mos-packaging
  fuel-library

Work Items
----------

* MOS specific initializing system scripts should be updated for systemd.

* Adapt Puppet Ruby providers for Ruby 2.3

* Build MOS Packages for Ubuntu 16.04 (Xenial Xerus)

* List of DKMS kernel modules shipped with Ubuntu 14.04 (Trusty) shall be
  reviewed for Ubuntu 16.04 (Xenial Xerus)

Dependencies
============

* OpenStack Patching Process

Testing
=======

* ISO with Ubuntu 16.04 passes all BVT & Swarm system tests
* All main clusters configurations can be successfully deployed
* All additional components like Sahara, Ceilometer, Zabbix
  are to be deployed

Documentation Impact
====================

None

References
==========

None
