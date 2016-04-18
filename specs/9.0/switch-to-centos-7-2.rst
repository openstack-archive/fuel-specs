..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================
Switch to CentOS-7.2.1511
=========================

URL of launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/switch-to-centos-7-2

Currently we build MOS ISO with CentOS-7.1.1503 repositories pinned and
can't get any updates from 7.2 until start using it.


--------------------
Problem description
--------------------

After switching to CentOS-7 there was a short period of time when we use
CentOS-7 repositories without minor version index. We had to switch to fixed
version shortly after that because CentOS-7.2 was released and we got several
ISOs broken because of that change. The decision was made to switch back to
CentOS-7.1 by pinning this version in build and packaging CIs.

This could be only a temporaly solution because the only version of
CentOS that could receive any updates is the latest one. In our case
it is CentOS-7.2.1511, so we have to switch to it to use the latest
packages and receive updates.


----------------
Proposed changes
----------------


Proposed change is to use snapshotting mechanism that will make it possible
to use the latest available snapshot each time new ISO is built, and will
provide configuration options to switch to older snapshots if latest is
broken or incompatible with MOS.

Web UI
======

No changes.


Nailgun
=======


Data model
----------

No changes.


REST API
--------

No changes.


Orchestration
=============


RPC Protocol
------------

No changes.


Fuel Client
===========

No changes.


Plugins
=======

No changes.


Fuel Library
============

No changes.


------------
Alternatives
------------

The only alternative is to use CentOS-7 (without minor version) directly
on master node. This is quite dangerous because it will switch master node
to next minor release immediately it is available on mirrors and could
break it.

For example, we faced the following issues while switching to CentOS-7.2:

* e1000 'Tx Unit Hung' issues. We've never saw it on CentOS-7.1, but started
  to see in once switched to 7.2. One can think that it's CentOS related
  issue but it is not. This issue is common for many distributions, there
  are bugs in CentOS, RedHat, Ubuntu, Novell, some of them are several years
  old and some of them even open. There is a workaround to solve this issue -
  disable TSO offloading [2]_, and it looks suitable solution for master node.
  Another solution is to use virtio drivers, but it requires a bit more work
  and significantly more testing.

* libxml2 regression [3]_ that prevents postgresql to be built.

* upstream docker images were updated with a delay that caused several
  builds to fail because of transition from systemd-container-\* packages
  to actual systemd [1]_.


--------------
Upgrade impact
--------------

The following key things should be kept in mind:

* Packages for MOS-9 should be built for CentOS-7.1 target before the upgrade
  so they will work on MOS-8 (CentOS-7.1 based) and will work on MOS-9
  because 7.2 backward compatible with 7.1. And we assume that QA testing
  finds any other issues.

* Switching from CentOS-7.1 to CentOS-7.2 affects only packages that will
  be fetched from upstream mirrors and placed into ISO repositories.


There are several possible ways to upgrade master node:

* Upgrade using full set of packages - in this case a repository (or multiple
  repositores) with full set of packages that forms the MOS-9 release is
  required. It can be either repositories on MOS-9 ISO, or repositories on
  our mirror, or even a tarball. This set of packages should be copied to
  master node or enabled in yum config prior the upgrade. After that it
  should be possible to update MOS-8 packages from MOS-9 packages set with
  ``yum`` command. In either way that set of packages is combined from MOS-9
  packages and CentOS packages fetched from upstream. MOS-9 packages
  are the same regardless of CentOS version used.

* Upgrade from mirror.fuel-infra.org - in this case at least two set of
  repositories located on mirror.fuel-infra.org are required:

  * Upstream CentOS snapshot (os, extras, updates)

  * MOS-9 packages repositories (os, updates)

  Both sets of repositories should be enabled on master node prior the
  upgrade. MOS-9 repositories will have the same packages regardless
  are we using CentOS-7.1 or 7.2.


So in both upgrade cases there is no difference are we upgrading from
MOS-8 to MOS-9 (CentOS-7.1) or to MOS-9 (CentOS-7.2).

---------------
Security impact
---------------

This update will help us to fix security issues and bugs found recently.
Here is a bit of statistics for bugs related to MOS for January,
February 2016:

January:

* Total - 11

  * Normal - 3

  * Moderate - 6

  * Important - 2

  * Critical - 0


February:

* Total - 13

  * Normal - 9

  * Moderate - 1

  * Important - 2

  * Critical - 1

So, 24 bug for just 2 months. For those who interested in details there is
an etherpad [0]_ with links to every bug I've counted here.


--------------------
Notifications impact
--------------------

No changes.


---------------
End user impact
---------------

No changes.


------------------
Performance impact
------------------

No changes.


-----------------
Deployment impact
-----------------

No changes.


----------------
Developer impact
----------------

No changes.


---------------------
Infrastructure impact
---------------------

To switch to CentOS-7.2 the following things should be done:

* CentOS-7.2 has the same system requirements as CentOS-7.1, but lets
  check that the are comply with our infrastructure:

  * RAM - At least 1024 MB RAM is required to install and use CentOS-7.2

  * CPU - At least one (logical) CPU is required to install and use CentOS-7.2

* Snapshots of CentOS base repositories (os, extras, updates) must be
  created regularly and include CentOS release number as part of their
  names to avoid conflicts when snapshots for different releases are
  created at the same time.

* ISO build job should support environment variables that allow setting
  snapshot URL to use when building ISO. By default it should point to the
  latest snapshot. In case build starts to fail because of issues with
  packages ISOs could be built from older snapshot until the issue is resolved.
  The same will work for situation when next CentOS release is out - we
  could build ISO from latest snapshot (next release), or use older snapshot
  (previous release) until the issues are resolved.

* Packaging CI should use CentOS-7.1 until it was decided that 7.2 will not
  be reverted and we can start rebuilding our packages using dependencies
  from CentOS-7.2.

* Packaging CI should include some switch (a set of options and documentation)
  to switch dependencies source to any CentOS we're using in our product.


--------------------
Documentation impact
--------------------

No changes.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  amogylchenko

Other contributors:
  teselkin-d

Mandatory design review:
  kozhukalov
  bookwar


Work Items
==========

* Verify that ISO with CentOS-7.2 packages passes standard tests.

* Improve snapshotting by adding CentOS release number to snapshots names.

* Update ISO building CI to add option to select custom snapshot.

* Update documentation with description of rollback process and switching
  to the next release.

* Prepare and merge changes to switch to CentOS-7.2 according the
  documentation from previous point.

* Also it worth rebuilding all MOS packages for new CentOS target. However,
  this shouldn't be done immediately, because packages built for 7.1 will
  work on 7.2 platform, but not vice versa.


Dependencies
============

No dependecies.


------------
Testing, QA
------------

No additional testing is needed to verify switching from one stable release
to another, standard set of tests covers all the cases.

If we decide to support truly rolling releases or test proposed updates then
a separate tests should be added. Those tests should use CR / FastTrack
repositories. This is out of scope of this document.


Acceptance criteria
===================

Fuel ISO uses CentOS-7.2 when deploying master node.


----------
References
----------

.. [0] https://etherpad.openstack.org/p/r.a7fe0b575d891ed81206765fa5be6630
.. [1] http://seven.centos.org/2015/12/fixing-centos-7-systemd-conflicts-with-docker/
.. [2] https://bugs.launchpad.net/mos/+bug/1534638
.. [3] https://review.openstack.org/#/c/285306/
