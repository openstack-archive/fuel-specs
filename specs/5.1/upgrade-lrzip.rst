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

Our upgrade tarball is almost 5Gb in size. We can compress it with lrzip,
it will save about 2Gb of space and network traffic for users.

Proposed change
===============

Create separate build target with uncompressed fuel images inside of
compressed fuel-upgrade.tar.lrz

Alternatives
------------

* Do nothing. It will save time of build and unpack.
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

It takes about 15 minutes on my virtualbox environment to unpack tarball.
Looks like it does not have noticable impact on build time.

Upgrade procedure will be faster, because there is no need to unpack
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
* Handle compressed tarballs in system tests.
* Use compressed tarball in community build.
* Turn on compressed tarball for release iso job after HCF.

Dependencies
============

None

Testing
=======

Automated test for upgrade with compressed tarball is needed.

Acceptance criteria:
* User can upgrade master node with compressed tarball.

Documentation Impact
====================

Upgrade guide must be updated with new command line for unpack of tarball.

References
==========

Discussion in openstack-dev: https://www.mail-archive.com/openstack-dev@lists.openstack.org/msg32837.html
