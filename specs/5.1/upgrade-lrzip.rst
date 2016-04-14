..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Optionally pack upgrade tarball with lrzip
==========================================

https://blueprints.launchpad.net/fuel/+spec/upgrade-lrzip

Problem description
===================

Our upgrade tarball is almost 5Gb in size. We can compress it with lrzip.
It will save about 2Gb of space and network traffic for users.

Proposed change
===============

Create a separate build target with uncompressed Fuel images inside of
a compressed archive file called fuel-upgrade.tar.lrz. Start using LRZ
archives instead of TAR for upgrade tarballs everywhere.

Alternatives
------------

* Do nothing. It will save time of the process of building and unpacking.
* Decrease amount of data in tarball. This is out of scope for this small
  blueprint and will be done in next release.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Command line for upgrade will be changed. Size of tarball will be decreased.
Tarball unpack time will be increased.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

New command line for unpack of upgrade tarball: lrzuntar fuel-upgrade.tar.lrz.

Performance Impact
------------------

It takes about 15 minutes on a VirtualBox environment to unpack the LRZ
archive. It does not have a noticable impact on build time.

The upgrade process will be faster because there is no need to unpack
fuel-images.tar.lrz file

Other deployer impact
---------------------

None

Developer impact
----------------

There will be no changes in existing build scenarios. Developer can build
compressed tarball with 'make upgrade-lrzip' command. In order to build
tarball, iso and img, use 'make iso img upgrade-lrzip' command. 'make all'
command includes uncompressed upgrade tarball, so 'make all upgrade-lrzip'
will create both compressed and uncompressed tarballs, what is not needed in
common case.

Our system tests need update in order to work with compressed tarballs.
Existing test scenarios are not affected.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  lux-place

Other contributors:
  None

Work Items
----------

* Update upgrade.sh should work both with compressed fuel-images.tar.lrz and
  uncompressed fuel-images.tar.
* New 'make upgrade-lrzip' command is needed.
* Extend method 'untar' in fuelweb_test/helpers/checkers.py with support for
  LRZ archives.
* Use compressed tarball in community build.
* Turn on compressed tarball for all builds on product jenkins.
* Update upgrade instruction with new command line.

Dependencies
============

None

Testing
=======

Automated test for upgrade with compressed tarball is needed.

Acceptance criteria:
* User can upgrade Fuel Master using compressed tarball.

Documentation Impact
====================

Upgrade guide must be updated with new command line for unpacking of tarball.

References
==========

Discussion in openstack-dev:
https://www.mail-archive.com/openstack-dev@lists.openstack.org/msg32837.html
