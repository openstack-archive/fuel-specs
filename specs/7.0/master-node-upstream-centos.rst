..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================
Upstream CentOS on MOS-7 master node
====================================

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

::

                                  +-----------------------------------------+
                                  |         mirror.fuel-infra.org           |
                                  |                                         |
    +---------+                   | +-----------------+  +----------------+ |
    | MOS ISO |                   | | mos7.0-security |  | mos7.0-updates | |
    +----+----+                   | +--------+--------+  +--------+-------+ |
         |                        |          |                    |         |
         |                        +-----------------------------------------+
         |                                   |                    |
         |                                   |                    |
  +-------------------------------------------------------------------------+
  |      |                                   |                    |         |
  | +----+----+  +---------------+  +--------+--------+  +--------+-------+ |
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

The problem with this setup is that the only way to update a package is to put
it into one of mos7.0-* repositories. 'nailgun' repository is local only, and
there is no source for '7.0_auxiliary'.

Using 'mos7.0-security' or 'mos7.0-updates' is OK if a package being updated
was re-built by Mirantis. If it is not and we need to update a package that was
taken from upstream then the following ways are possible:

* get required packages only and create micro-repository that will be available
  to customer

* re-build packages that should be updated and put them into our repositories

Both ways are bad since they require significant amount of work from the teams
involved. A better solution is to provide access to upstream packages so that
customer could install latest packages without any significant help from our
side.


----------------
Proposed changes
----------------

Proposed repository structure is shown below.

::

                                  +---------------------------------------------------------+
                                  |         mirror.fuel-infra.org                           |
                                  |                                          +------------+ |
    +---------+                   | +-----------------+  +----------------+  | MOS CentOS | |
    | MOS ISO |                   | | mos7.0-security |  | mos7.0-updates |  | Snapshot   | |
    +----+----+                   | +--------+--------+  +--------+-------+  +-----+------+ |
         |                        |          |                    |                |        |
         |                        +---------------------------------------------------------+
         |                                   |                    |                |
         |                                   |                    |                |
  +-------------------------------------------------------------------------+      |
  |      |                                   |                    |         |      |
  | +----+----+  +---------------+  +--------+--------+  +--------+-------+ |      |
  | | Nailgun |  | 7.0_auxiliary |  | mos7.0-security |  | mos7.0-updates | |      |
  | +----+----+  +-------+-------+  +--------+--------+  +--------+-------+ |      |
  |      |               |                   |                    |         |      |
  |      |               +-------------------+--------------------+         |      |
  |      |                                   |                              |      |
  |      |  +-----------+   +-------------+  |                              |      |
  |      +--+ whitelist +---+ mos7.0-base |  |           +----------------+ |      |
  |      |  +-----------+   +-----------+-+  |    +------+   base         +--------+
  |      |                              |    |    |      +----------------+ |      |
  |      +--------------------------+   |    |    |      +----------------+ |      |
  |      |                          |   |    |    +------+   extras       +--------+
  |      +--------------+----+      |   |    |    |      +----------------+ |      |
  |      |              |    |      |   |    |    |      +----------------+ |      |
  | +----+-----------+  |    |      |   |    |    +------+   updates      +--------+
  | | Docker         +--+-+  |      |   |    |    |      +----------------+ |
  | | containers     |    +--+-+  +-+---+----+----+--+                      |
  | +----------------+    |    |  |   Local          |                      |
  |      +----------------+    |  |   system         |                      |
  |           +----------------+  +------------------+                      |
  |                                                                         |
  |                            Master node                                  |
  +-------------------------------------------------------------------------+


The goal is to add three additional repositories to receive updated packages
from upstream:

* base - CentOS-6 base repository

* extras - CentOS-6 extras repository

* updates - CentOS-6 updates repository

These repositories shouldn't be directly connected to CentOS upstream mirrors
because we want to verify that upgrading master node with upstream packages
works before our customers face any issues with that. Because of that we will
use snapshots of upstream repositories made by Mirantis and published after
some verification tests that can guarantee that upgrade is successfull. We
create, test and publish all packages from upstream mirrors, so it’s a kind of
‘delayed updates’ rather then 'selected updates'.

The process of creating, testing and publishing should be the following:

* CI starts creating upstream CentOS snapshots. Those snapshot names must
  include full CentOS release number (e.g. 6.7 instead of just 6) because there
  might be more than one CentOS snapshot created at the same time (e.g. for
  CentOS-6 and CentOS-7).

* Periodic job runs verification tests against latest (at the moment of test
  run) snapshot. Periodic job should run once per several days, however this is
  a topic to discuss. If the job fails then there are two possible ways:

  * Run verification job against previous snapshot (and so on if that one
    fails too).

  * Wait for the next scheduled run.

* If there are packages that fix critical security issues then verification
  job should be triggered immediately. If the job fails then it should be
  investigated and fixed. As soon as verification test passes we publish
  corresponding snapshot to our mirror *and* issue release notes to notify
  customer that they have to upgrade master node.

* When periodic verification test passes we publish corresponding snapshot to
  our mirror. Then we either send a notification to customers that new packages
  are available, or do nothing.

But using only snapshots is not enough. Second part of the problem is local
'nailgun' repository that contains all the packages that were shipped on
installation ISO. Some packages in that repository have versions less then
in upstream, and will be reinstalled when upstream repository enabled. We are
going to solve this using the following approach:

* Create a separate repository named 'mos7.0-base' using whitelist. Only those
  packages that were rebuilt by Mirantis and can't be replaced with upstream
  packages are listed there.

* On master node disable 'nailgun' repository.

* On master node enable 'mos7.0-base' repository with priority 10 (that is
  higher then default value of 100).

The last problem is package naming - we've built some packages that have
different names in upstream, and can't be updated by ``yum`` because it doen't
know anything about their relations. So we have to use ``yum shell`` and
explicitely define packages that should be removed and installed instead.


**Updating docker containers**

The only way to update a container is to rebuild it from updated image.
Updated images can be received from 'mos7.0-updates' channel as
'fuel-docker-images' RPM package.

Every docker container have only one repository enabled - local 'nailgun'
repository. It is used only once, when a container is being created by
'dockerctl build' command. Since no updates can be received via 'nailgun'
repository, no packages can be updated inside a container during its lifecycle.

We keep original 'nailgun' repository intact, but we also changing content of
'/etc/yum.repos.d/' folder on master node. This folder is shared with every
container, and as soon as we change it and enable upstream CentOS repositories
(via published snapshots of course) a container can install updates if there
is ``yum update`` somewhere.

To avoid the following is suggested:

* configure upstream repositories (base, extras, updates) and immediately
  disable them all

* set priority 10 for 'mos7.0-base' repository and disable it

* keep 'nailgun' repository enabled

In such configuration containers will not receive any updates from other
repositories since they are disabled by default. In such case the following
command should be used to install packages to the host system:

::

  $ sudo yum --disablerepo=* --enablerepo=mos7.0-base --enablerepo=base \
  > --enablerepo=extras --enablerepo=updates <yum arguments>


Another way is to create a copy of /etc/yum.repos.d and modify mounts for
every container:

* copy original /etc/yum.repos.d to /etc/yum.repos.d.nailgun

* modify default mounts in dockerctl's config file so that it will use
  /etc/yum.repos.d.nailgun instead of /etc/yum.repos.d

* rebuild every docker container to apply the changes made


**Master node upgrade tool**

To upgrade master node a tool named fuel-distupgrade was developed. It's
a POC written in bash and will be implemented as part of fuel-upgrade tool.

fuel-distupgrade does the following actions:

* fuel-distupgrade prepare

  * verifies that master node can be upgraded (there is enough resources
    for that) and prepares it for upgrade

  * creates backup of /boot partition and LVM snapshots for others

  * stops services that shouldn't run during upgrade

* fuel-distupgrade update

  * creates mos7.0-base repo

  * configures yum repositories correctly

  * replaces packages and updates master node

* fuel-distupgrade commit

  * makes changes persistent after successfull updgrade

* fuel-distupgrade rollback

  * reverts changes back is upgrade failed

* fuel-distupgrade finalize

  * finlize upgrade process after either 'commit' or 'rollback'


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

Both variants require a lot of manual work, and every security update made
by any way will differ from previous one.


--------------
Upgrade impact
--------------

This feature affects the upgrade process of the Fuel Master node. It must be
reflected in corresponding updates to fuel-upgrade code for versions where the
feature will be supported (at least version 7.0), since the fuel-upgrade already
does manage repositories in its own way.

**Updating packages on master node**

As was mentioned before, the following command should be used to manipulate
packages on host system:

::

  $ sudo yum --disablerepo=* --enablerepo=mos7.0-base --enablerepo=base \
  > --enablerepo=extras --enablerepo=updates <yum arguments>

For example, to update glibc:

::

  $ sudo yum --disablerepo=* --enablerepo=mos7.0-base --enablerepo=base \
  > --enablerepo=extras --enablerepo=updates update glibc


---------------
Security impact
---------------

The proposed solution allows to fix security / bugs the fastest way. It also
reduces our technical debt and should remove significant amount of work from
support teams.


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

* CI snapshotting should be improved to support several CentOS releases.

* A placeholder for published repositories is required on our mirror.


--------------------
Documentation impact
--------------------

This feature should be documented because it's intended to performed on
customer's side without support stuff.


--------------
Implementation
--------------

TBD


Assignee(s)
===========

Primary assignee:
  teselkin-d

Other contributors:
  isuzdal

Mandatory design review:
  kozhukalov
  gelbuhos


Work Items
==========

* Infra team to update snapshotting - snapshot names should include CentOS
  release number as part of it's name.

* Infra team to create a placeholder for repositories to be published.

* CI / Infra team to create a job that publishes snapshot under a fixed
  name (using the placeholder above), and prevents those packages from deletion
  when snapshot becomes too old.

* MOS Linux team to implement 'fuel-distupgrade' as part of 'fuel-upgrade' tool.


Dependencies
============

TBD


------------
Testing, QA
------------

* QA framework shold be improved to support master node upgrade scenario as
  part of our standard tests (BVT / smoke / SWARM).

* A set of tests that allows us to make a decision that snapshot is
  'good enough' to be published should be created.

* Periodic job that runs a set of tests mentioned above should be created.


Acceptance criteria
===================

Please specify clearly defined acceptance criteria for proposed changes.


----------
References
----------

[0] https://review.openstack.org/#/c/274118/
