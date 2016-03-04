..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Example Spec - The title of your blueprint
==========================================

Launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/master-node-upstream-centos


MOS 7.0 master node was released based on CentOS 6.6. New releases of
CentOS 6.* are being shipped from time to time, current version is CentOS-6.7.
Once new release is shipped it becomes the only supported release of CentOS,
packages with updates and bug fixes are distributed only through repositories
of latest release (as of this writing - CentOS 6.7).

This is called rolling update. This means that packages on master node are
becoming obsolete and can't be updated unless we update master node to next
current release (do not mix up with CR repository, it's a different thing).
This is not good because gradually there are vulnerabilities found which there
are no fixes for in CentOS 6.6 (in case of MOS-7) repositories.

The same is applicable to MOS-8, since it was released with CentOS-7.1 and
shortly after that CentOS-7.2 was released.

To address this issue an upgrade workflow should be developed that will allow
to align master node with upstream packages.


--------------------
Problem description
--------------------

Existing repository structure on master node looks like shown below:

                                +-----------------------------------------+
                                |         mirror.fuel+infra.org           |
                                |                                         |
  +---------+                   | +-----------------+  +----------------+ |
  | MOS ISO |         ???       | | mos7.0-security |  | mos7.0-updates | |
  +----+----+          +        | +--------+--------+  +--------+-------+ |
       |               |        |          |                    |         |
       |               |        +-----------------------------------------+
       |               |                   |                    |
       |               |                   |                    |
+-------------------------------------------------------------------------+
|      |               |                   |                    |         |
| +----+----+  +-------+-------+  +--------+--------+  +--------+-------+ |
| | Nailgun |  | 7.0_auxiliary |  | mos7.0-security |  | mos7.0-updates | |
| +----+----+  +-------+-------+  +--------+--------+  +--------+-------+ |
|      |               |                   |                    |         |
|      +---------------+---------+---------+--------------------+         |
|                                |                                        |
|                                |                                        |
|      +--------------+----+-----+------------------------------+         |
|      |              |    |                                    |         |
| +----+-----------+  |    |                           +--------+-------+ |
| | Docker         +--+-+  |                           | Local          | |
| | containers     |    +--+-+                         | system         | |
| +----------------+    |    |                         +----------------+ |
|      +----------------+    |                                            |
|           +----------------+                                            |
|                                                                         |
|                            Master node                                  |
+-------------------------------------------------------------------------+

The following repositories are available on master node:

* 7.0_auxiliary

  * type - local
  
  * location - file:///var/www/nailgun/2015.1.0-7.0/centos/auxiliary/

* mos7.0-security

  * type - mirror

  * location - http://mirror.fuel-infra.org/mos-repos/centos/mos7.0-centos6-fuel/security/x86_64/

* mos7.0-updates

  * type - mirror

  * location - http://mirror.fuel-infra.org/mos-repos/centos/mos7.0-centos6-fuel/updates/x86_64/

* nailgun

  * type - local

  * location - file:/var/www/nailgun/2015.1.0-7.0/centos/x86_64


----------------
Proposed changes
----------------

Proposed repository structure is shown below.

                                +---------------------------------------------------------+
                                |         mirror.fuel+infra.org                           |
                                |                                          +------------+ |
  +---------+                   | +-----------------+  +----------------+  | MOS CentOS | |
  | MOS ISO |         ???       | | mos7.0-security |  | mos7.0-updates |  | Snapshot   | |
  +----+----+          +        | +--------+--------+  +--------+-------+  +-----+------+ |
       |               |        |          |                    |                |        |
       |               |        +---------------------------------------------------------+
       |               |                   |                    |                |
       |               |                   |                    |                |
+-------------------------------------------------------------------------+      |
|      |               |                   |                    |         |      |
| +----+----+  +-------+-------+  +--------+--------+  +--------+-------+ |      |
| | Nailgun |  | 7.0_auxiliary |  | mos7.0-security |  | mos7.0-updates | |      |
| +----+----+  +-------+-------+  +--------+--------+  +--------+-------+ |      |
|      |               |                   |                    |         |      |
|      |               +-------------------+--------------------+         |      |
|      |                                   |                              |      |
|      |                                   |                              |      |
|      |   +----------+   +-------------+  |           +----------------+ |      |
|      +---+ Whitlist +---+ mos7.0-base |  |    +------+   base         +--------+
|      |   +----------+   +----------+--+  |    |      +----------------+ |      |
|      |                             |     |    |      +----------------+ |      |
|      |                             |     |    +------+   extras       +--------+
|      +--------------+----+         |     |    |      +----------------+ |      |
|      |              |    |         |     |    |      +----------------+ |      |
| +----+-----------+  |    |         |     |    +------+   updates      +--------+
| | Docker         +--+-+  |         |     |    |      +----------------+ |
| | containers     |    +--+-+    +--+-----+----+--+                      |
| +----------------+    |    |    | Local          |                      |
|      +----------------+    |    | system         |                      |
|           +----------------+    +----------------+                      |
|                                                                         |
|                            Master node                                  |
+-------------------------------------------------------------------------+

Three additional repository to receive updated packages from upstream should be
added:

* base - CentOS-6 base repository

* extras - CentOS-6 extras repository

* updates - CentOS-6 updates repository

These repositories are not CentOS direct upstream repos. It’s a snapshot of
those repos made by Mirantis and published after some tests that can guarantee
that upgrade should be successfull. So it’s a kind of ‘delayed updates’,
because we create a full snapshot of those repos.

There are packages in nailgun repository that conflict with upstream packages
and will not allow packages from upstream to be installed. In general, to solve
this issue a new repository should be built based on packages from nailgun repo.
It should provide only packages that couldn’t be taken from upstream or aren’t
exist there. We suggest it will be named mos7.0-base.

There are the following ways to build mos7.0-base:

* Use a script that will create this repo based on nailgun repository,
  using some kind of whitelist / blacklist to filter packages.

* Build a new repository on Mirantis side, put there only the packages we need
  and attach it to master node.

This document describes the first one.


Web UI
======

None


Nailgun
=======


Data model
----------

None


REST API
--------

None


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

None


Fuel Library
============

None


------------
Alternatives
------------

There are two alternative ways to deliver updates to master node:

* Fetch some packages from upstream, create micro repositories and deliver
  them in form of tarballs. This might work several times, but at some moment
  it might happen that a lot of dependent packages must be included to the
  tarball.

* Fetch sources, rebuild packages, deliver them via mos7.0-updates repository.
  That's a bad approach since we will end up with rebuilding glibc, kernel, etc.

Both variants requires a lot of manual work, and every security update made
by any way will differ from previous one.


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

The proposed solution allows to fix security / bugs the fastest way.


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None


------------------
Performance impact
------------------

Some performance impact might exist caused by fixes or regressions introduced
to base system packages. However we may detect such issues before publishing
snapshots, so customers are safe here.


-----------------
Deployment impact
-----------------

None


----------------
Developer impact
----------------

None


---------------------
Infrastructure impact
---------------------

Explain what changes in project infrastructure will be required to support the
proposed change. Consider the following:

* Will it increase the load on CI infrastructure by making build or test jobs
  consume more CPU, network, or storage capacity? Will it increase the number
  of scheduled jobs?

* Will it require new workflows or changes in existing workflows implemented in
  CI, packaging, source code management, code review, or software artifact
  publishing tools?

  * Will it require new or upgraded tools or services to be deployed on project
    infrastructure?

  * Will it require new types of Jenkins jobs?

  * Will it affect git branch management strategies?

  * Will it introduce new release artifacts?

  * Will it require changes to package dependencies: new packages, updated
    package versions?

  * Will it require changes to the structure of any package repositories?

* Will it require changes in build environments of any existing CI jobs? Would
  such changes be backwards compatible with previous Fuel releases currently
  supported by project infrastructure?


--------------------
Documentation impact
--------------------

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.


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
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


------------
Testing, QA
------------

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly.

This should include changes / enhancements to any of the integration
testing. Most often you need to indicate how you will test so that you can
prove that you did not adversely effect any of impacts sections above.

If there are firm reasons not to add any other tests, please indicate them.

After reading this section, it should be clear how you intend to confirm that
you change was implemented successfully and meets it's acceptance criteria
with minimal regressions.

Acceptance criteria
===================

Please specify clearly defined acceptance criteria for proposed changes.


----------
References
----------

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
