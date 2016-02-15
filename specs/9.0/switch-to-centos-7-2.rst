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

The only alternative is to use CentOS-7 (without minor version). This is
quite dangerous because it will switch us to next minor release immediately
it is available on mirrors and we can get builds broken again. For example,
we've met the following issues:

* e1000 'Tx Unit Hung' issues. We've never saw it on CentOS-7.1, but started
  to see in once switched to 7.2. One can think that it's CentOS related
  issue but it is not. This issue is common for many distributions, there
  are bugs in CentOS, RedHat, Ubuntu, Novell, some of them are several years
  old and some of them even open. There is a workaround to solve this issue -
  disable TSO offloading, and it looks suitable solution for master node.
  Another solution is to use virtio drivers, but it requires a bit more work
  and significantly more testing.

* libxml2 regression that prevents postgresql to be built.

* upstream docker images were updated with a delay that caused several
  builds to fail because of transition from systemd-container-\* packages
  to actual systemd [1].


--------------
Upgrade impact
--------------

N/A

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
an etherpad [0] with links to every bug I've counted here.


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

* CentOS mirror 'mirror.centos.org' should be used instead of 
  'vault.centos.org'. CentOS release number should be corrected
  (7.2.1511 instead of 7.1.1503). What to do when CentOS-7.3 is out
  depends on whether we switch to rolling releases / separate deployment
  of master node, or not:

  * If we start supporint CentOS rolling releases then we might do nothing
    since there will be no 7.2.1511 tag, or there must be a workflow how
    to switch to next release.

  * If nothing changed then we must replace 'mirror.centos.org' back with
    'vault.centos.org' when packages for 7.2 moved to vault, usually this
    takes two weeks.

* Snapshots of CentOS base repositories (os, extras, updates) must be
  created regularly and include CentOS release number as part of their
  names to avoid conflicts when snapshots for different releases are
  created at the same time.

* ISO build job should include new option that allow to use any existing
  snapshot to build ISO with it's packages. This is useful when ISO becomes
  broken because of packages from latest snapshot.

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

[0] https://etherpad.openstack.org/p/r.a7fe0b575d891ed81206765fa5be6630
[1] http://seven.centos.org/2015/12/fixing-centos-7-systemd-conflicts-with-docker/
