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
it is available on mirrors and we can get builds broken again.


--------------
Upgrade impact
--------------

If this change set concerns any kind of upgrade process, describe how it is
supposed to deal with that stuff. For example, Fuel currently supports
upgrading of master node, so it is necessary to describe whether this patch
set contradicts upgrade process itself or any supported working feature that.


---------------
Security impact
---------------

Should fix security issues and bugs found recently if packages with fix
are available in updates repository.


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

* ISO build system should use mirror.centos.org instead of
  vault.centos.org and use correct version numbers.

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

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

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


Dependencies
============

No dependecies.


------------
Testing, QA
------------

No additional testing is needed, standard set of tests covers all the cases.


Acceptance criteria
===================

Product ISO uses CentOS-7.2 when deploying master node.


----------
References
----------

No references.
