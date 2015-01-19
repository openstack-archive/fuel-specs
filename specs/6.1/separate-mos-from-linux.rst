..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
Separate MOS from Linux repos
=============================

https://blueprints.launchpad.net/fuel/+spec/separate-mos-from-linux

Problem description
===================

* As a Cloud Operator I should be able to run OS updates as well as MOS updates
  during Product Life cycle

* As a Cloud Operator I would like to see what packages provided by MOS and
  what packages provided by OS Provider

* As a Cloud Operator I would like to have OS support contract as well as MOS
  support

* As a Cloud Operator I would like to get security updates as fast as possible
  independantly from OS Provider as well as from MOS

* As a Cloud Operator I should be able to see sources of OS and MOS packages

* As a Cloud Operator I should be able to see debug symbols of OS and MOS
  packages

* As a Developer, I would like to have the same approach for making changes to
  Fuel components and their dependencies.

To provide highest quality MOS should separate lifecycle OS and Cloud lifecycle
management. Meanwhile OS Updates shouldn't break MOS functionality and vice
versa.

Proposed change
===============

Types of software packages
--------------------------

This specification introduces a clear separation between a base OS (an RHEL or
Debian based Linux distribution), and an OpenStack distribution (MOS). All
software packages deployed by Fuel a divided into following categories based on
their relation to the specific base OS and OpenStack distribution being
deployed:

#. Upstream package: a package from a base OS is reused directly, without MOS
   specific modifications.

#. Modified package: a package from a base OS has MOS specific modifications,
   verbatim version from the base OS cannot be used as is.

#. Upgraded package: a variant of modified package, where MOS specific
   modifications include an upgrade to a more recent software version.

#. Downgraded package: a variant of modified package, where MOS specific
   modifications include a downgrade to an older software version.

#. Regressed upstream package: a package from a base OS was reused without MOS
   specific modifications, until a new upstream version introduced a
   regression. A modified package has to be used temporarily until the
   regression is fixed in a more recent version from upstream OS.

#. MOS specific package: a package is specific to MOS and does not exist in the
   base OS.

Different releases of MOS can put the same software package in different
categories.

Distributing MOS packages
-------------------------

Released MOS packages will be distributed as part of a Fuel ISO image. Upstream
packages, as well as any other IP protected by respective OS vendors, will not
be the included in Fuel ISO images. Regular updates to the MOS OpenStack
distribution will be delivered through online MOS mirrors.

MOS mirrors structure
---------------------

MOS mirrors should be organized in the same way as base OS mirrors. MOS mirrors
should follow industrial standards. The structure of a mirror should be done in
the same way as base OS mirrors.

Every supported OS will have own set of repositories containing MOS packages
per release (mos6.1, mos7.0 etc.) These repositories must contain only packages
with MOS specific modifications, and no upstream packages from the
corresponding base OS.

Mirror should be publicly and globally available and distributed. User should
be able to create and maintain local mirrors for use in environments without
direct Internet access.

Top level MOS mirror structure
------------------------------

::

  /
  +--+centos
  |  |
  |  +--+6
  |  |  |
  |  |  +--+mos6.0
  |  |  |
  |  |  +--+mos6.1
  |  |
  |  +--+7
  |     |
  |     +--+mos7.0
  |     |
  |     +--+mos7.1
  |
  +--+ubuntu
     |
     +--+dists
     |
     +--+pool
     |
     +--+...

Debian based mirror structure
-----------------------------

MOS mirror should include several repositories (updates, security, proposed)
built in the same way as a base OS mirror (Debian). Repository sections are
organized in the same way (main, restricted) according to package licenses
(non-free). The meaning of components for Debian mirror resembles the meaning
of components of the base OS distribution mirror.

::

  $(OS_MIRROR)                 $(MOS_MIRROR)
  +                            +
  |                            |
  +--+ubuntu                   +--+ubuntu
     |                            |
     +--+dists                    +--+dists
     |  |                         |  |
     |  +--+precise-backport      |  +--+mos6.1-proposed
     |  |                         |  |
     |  +--+precise-proposed      |  +--+mos6.1-security
     |  |                         |  |
     |  +--+precise-security      |  +--+mos6.1-updates
     |  |                         |  |
     |  +--+precise-updates       |  +--+mos6.1
     |  |                         |  |
     |  +--+precise               |  +--+mos7.0-proposed
     |  |                         |  |
     |  +--+trusty-backport       |  +--+mos7.0-security
     |  |                         |  |
     |  +--+trusty-proposed       |  +--+mos7.0-updates
     |  |                         |  |
     |  +--+trusty-security       |  +--+mos7.0
     |  |                         |
     |  +--+trusty-updates        +--+indices
     |  |                         |  |
     |  +--+trusty                |  +--+...
     |                            |
     +--+indices                  +--+pool
     |  |                         |  |
     |  +--+...                   |  +--+main
     |                            |  |  |
     +--+pool                     |  |  +--+a
     |  |                         |  |  |
     |  +--+main                  |  |  +--+...
     |  |                         |  |  |
     |  +--+multiverse            |  |  +--+z
     |  |                         |  |
     |  |--+restricted            |  |--+restricted
     |  |                         |     |
     +  |--+universe              |     +--+a
     |                            |     |
     |--+...                      |     +--+...
                                  |     |
                                  |     +--+z
                                  |
                                  +--+project
                                     |
                                     +--+mos-archive-keyring.gpg
                                     |
                                     +--+mos-archive-keyring.sig

RHEL based mirror structure
---------------------------

MOS mirror should include several repositories (os, updates, fasttrack)
built in the same way as a base OS mirror (RHEL).

::

  $(OS_MIRROR)                           $(MOS_MIRROR)
  +                                      +
  |                                      |
  +--+centos-6                           +--+centos-6
  |  |                                   |  |
  |  +--+...                             |  +--+mos6.1
  |                                      |  |
  +--+centos-7                           |  +--+mos7.0
     |                                   |     |
     +--+7                               |     +--+os
        |                                |     |  |
        +--+os                           |     |  +--+x86_64
        |  |                             |     |     |
        |  +--+x86_64                    |     |     +--+Packages
        |     |                          |     |     |  |
        |     +--+Packages               |     |     |  +--+*.rpm
        |     |  |                       |     |     |
        |     |  +--+*.rpm               |     |     +--+RPM-GPG-KEY-MOS7.0
        |     |                          |     |     |
        |     +--+RPM-GPG-KEY-CentOS-7   |     |     +--+repodata
        |     |                          |     |        |
        |     +--+repodata               |     |        +--+*.xml,*.gz
        |        |                       |     |
        |        +--+*.xml,*.gz          |     +--+updates
        |                                |        |
        +--+updates                      |        +--+x86_64
           |                             |           |
           +--+x86_64                    |           +--+Packages
              |                          |           |  |
              +--+Packages               |           |  +--+*.rpm
              |  |                       |           |
              |  +--+*.rpm               |           +--+repodata
              |                          |              |
              +--+repodata               |              +--+*.xml,*.gz
                 |                       |
                 +--+*.xml,*.gz          +--+centos-7
                                            |
                                            +--+mos7.1
                                            |
                                            +--+mos8.0

Development mirrors
-------------------

Build system should allow developers to build packages, these packages should
be placed to special mirror which can be specified in Nailgun to deliver these
packages to environment. Later, this functionality should be exposed to
community allowing Community engineer (nova, cinder) to put own git repository
and commit, build system should build packages and provide link which will be
specified in Nailgun.

Repositories priorities
-----------------------

Handling of multiple package repositories in Nailgun [1]_ will be extended to
allow setting of priorities during deployment.

For Debian, APT pinning [6]_ priorities for MOS repos must be set above 1000,
which causes a version of the package from the repo to be installed even if
this constitutes a downgrade of the package, and will prevent installation of
newer versions of the package from the upstream repo as long as any version of
the package is available from a MOS repo.

For CentOS, there's no special meaning of priorities except for a simple
majority. We are keeping the same priorities as for Debian just for
consistency.

The following default values will be used for setting yum repo and APT pinning
priorities via Fuel UI:

* Upstream OS repositories (including base, updates, security) - no priority
* Extra repositories specified by customer - no priority
* MOS base, updates, and security repositories - 1050
* MOS holdback repository - 1100

To handle a case when customer needs to override MOS packages, there must be
an option to specify extra repository priority explicitly when adding it via
Fuel CLI.

Package versioning requirements
-------------------------------

Package version string of any package with MOS specific modifications,
including MOS specific packages, must include 'mos' keyword, and must not
include registered trademarks of any base OS vendors.

Every new revision of a modified, upgraded, downgraded, or MOS specific package
targeted at a MOS release (including corresponding maintenance releases and
update channels) must have a package version greater than or equal to the
version of the same package in all previous releases of MOS, their maintenance
release and update channels, as well as the versions of the same package
previously published in the update channel for this MOS release.

For example, there must be no package version downgrades in the following MOS
release progression (where 6.1.1 matches the state of 6.1-updates at the time
of 6.1.1 maintenance release):

    6.0 -> 6.0.1 -> 6.1 -> 6.1.1 -> 6.1-updates -> 7.0

Every new revision of a regressed upstream package must have a package version
greater than previous revisions of the same package that were published to the
holdback repository for that MOS release.

Package version of an upgraded package must be constructed in a way that would
allow an upstream package with the same software version to supercede the
upgraded package in MOS when it is published by the upstream OS. This will
simplify phasing out modified packages in favor of upstream packages between
major MOS releases, but, due to repo priorities defined above, will not lead to
new upstream packages superceding upgraded packages available from MOS repos
when applying updates.

Debian package versioning
-------------------------

Versioning requirements defined in this section apply to all packages with MOS
specific changes: modified, upgraded, downgraded, regressed, or MOS specific
packages.

Debian revision [7]_ of a MOS package should always start with a "0mos" prefix,
followed by a MOS build version.

When a new software version of a package is targeted for a future major release
of MOS (i.e. a release in a release series that had no GA releases yet), MOS
build version must start with 1, and increased sequentially for every new build
of the same software version until the targeted release reaches General
Availability. For example: 1.2.3-0mos1, 1.2.3-0mos2.

When a new build of the same software version is targeted for an update channel
or a maintenance release of a GA release, a second number, starting with 1,
must be added to the MOS build version after a dot, while the first number must
remain the MOS build version released with the GA release. For example, if
1.2.3-0mos2 was released in the GA release, subsequent updates for the same
release series will be 1.2.3-0mos2.1, 1.2.3-0mos2.2.

When a new software version of a MOS package is introduced in an update or a
maintenance release, first number in the MOS build version must be set to 0.
For example, if 1.2.3-0mos2 was released in the GA release, version 1.2.4 will
be packaged as 1.2.4-0mos0.1.

In modified, downgraded, and MOS specific packages, the upstream version of a
package must exactly match the software version, without no suffixes.

In upgraded packages, the upstream version must consist of the software version
followed by "~mos" and the targeted MOS release series. For example, if base OS
contains version 1.2.3 and version 1.2.4 is required in MOS 6.1, MOS package
version will be 1.2.4~mos6.1-0mos1.

In regressed packages, same "~mosx.y" suffix must be appended to the upstream
version. For example, if base OS package version 1.2.3-0ubuntu1 introduces a
regression in MOS 6.1, the replacement package versions will be
1.2.3~mos6.1-0mos1, 1.2.3~mos6.1-0mos2 when introduced before GA, or
1.2.3~mos6.1-0mos0.1, 1.2.3~mos6.1-0mos0.2 when introduced in updates channel
or maintenance release.

Debian package metadata
-----------------------

All deb packages that are not deployed directly from an upstream OS must have
the following metadata:

#. Latest entry in the debian/changelog must contain:

   - reference to the targeted MOS release series (e.g. mos6.1)

   - reference to the organization that produced the package (Mirantis)

   - commits (full git commit sha1) in the source code repository and specs
     repository that the package was built from

#. Maintainer in debian/control must be MOS Team

Example of a valid debian/changelog entry::

  python-keystoneclient (2014.2.3-0mos1) mos6.1; urgency=low

    * Source commit: 17f8fb6d8d3b9d48f5a4206079c18e84b73bf36b
    * Build commit: 8bf699819c9d30e2d34e14e76917f94daea4c67f

   -- MOS Team <mos@mirantis.com>  Sat, 21 Mar 2015 15:08:01 -0700

Package lifecycle management
----------------------------

To deliver high quality of product MOS teams should push package updates during
Product lifecycle.

Packaging lifecycle should follow the MOS product lifecycle (Feature Freeze,
Soft Code Freeze, Hard Code Freeze).

Package flow should be specified from building package, passing SRU or
FastTrack Channels (mos6.1-proposed as a sample), acceptance testing, security
testing before it will appear in "updates" in MOS mirror.

Continous integration testing against Upstream
----------------------------------------------

As a part of a product lifecycle there should be periodical system tests that
verify functionality of MOS against:

- the current state of Upstream mirror (base system plus released updates),
  to check stability of current release
- the current state of the Stable Release Updates Channel [2]_ or FastTrack
  Channel [3]_ , to check if package candidates in "proposed" channel introduce
  any regressions

In order to facilitate QA testing, we should create a full dependencies graph
for MOS packages, add missing requirements from appropriate requirements.txt
files, and use this list for system tests.

Handling of system test results
-------------------------------

If the system test against SRU Channel [2]_ or FastTrack Channel [3]_ reveals
one or several packages that break MOS functionality, MOS teams must provide
one of the following solutions:

- solve the issue on the product side by releasing fixed MOS packages through
  the "updates" channel
- raise a debate with Upstream SRU reviewing team regarding problem packages
- (if none of the above helps) put working version of a problem package to
  the holdback repository

Also, any package that failed the system test, must be reflected on the
release status page.

Holdback repository
-------------------

Holdback repository is a measure aimed to ensure the highest quality of MOS
product. If there is an Upstream package that breaks the product, and this
problem cannot be fixed in a timely manner, MOS team publishes the package
proven stable to the "mosXX-holdback" channel. This repository should be
automatically configured on all installations with highest priority.

The case when OS Upstream vendor releases fixed version of a problem package,
must be covered by MOS system tests.

Ideally, Upstream updates shouldn't break the functionality of Product. The
number of packages in "mosXX-holdback" should be zero. Even if package is put
in repository, MOS team should contact OS Upstream to report the regression.
Package Update should be discarded before it appears in Update channel. If
package is supposed to appear in Update channel, MOS team should update
"mosXX-holdback" channel before that.

Testing in this channel should be done against every package as next release
may fix the regression that might occur. Once regression is fixed in upstream
the package should be removed from "mosXX-holdback" repository.

Release status page
-------------------

To ensure that MOS customers have full info on the release stability, all
packages that produce system test failures must be also reported in several
different ways:

- via web: via status page on the https://fuel-infra.org/ website
- on deployed nodes: via hook that updates MOTD using the above website
- on deployed nodes: via apt pre-hook that checks the status via the above
  website, and warns customer in case if "apt-get update" command is issued

Packages building module
------------------------

Fuel DEB packages build routine will be dropped. Fuel DEB packages will be
consumed from the MOS mirror directly on master node. [1]_

Control files for Fuel DEB packages will be moved to the public MOS Gerrit
instance.

Explicit list of Fuel DEB packages is below:

* fencing-agent
* nailgun-mcagents
* nailgun-net-check
* nailgun-agent
* python-tasklib

Docker containers building module
---------------------------------

All Dockerfile configs will be adjusted to include both upstream and MOS
repositories.

ISO assembly module
-------------------

ISO assembly module will be adjusted to exclude all parts mentioned above.

Offline installations
---------------------

There's various reasoning behind having a local mirrors of Upstream OS,
from security considerations, to making deployments faster and more reliable.
To support such installation cases we will implement the Linux console
script that mirrors the public Upstream and MOS mirrors to a given location,
allowing to put these local sources as input for the appropriate menu entry
of Fuel "Settings" tab on UI, or specify directly via Fuel CLI.
In case of deb-based Upstream OS, MOS requires packages from multiple
sections of a given distribution (main, universe, multiverse, restricted),
so the helper script will mirror all packages from components specified above.
Requirements:

* input Upstream OS mirror URL
* input MOS mirror URL
* ability to run as cronjob to update Upstream OS and MOS mirrors

Alternatives
------------

There is no alternative to the repositories separation approach due to
considerations related to distribution policies of major OS vendors.
Regarding the helper script to download Upstream OS repositories, there
could be a different approach implemented, by downloading only particular
packages that required by MOS. However, we consider that providing a full
upstream repository would make customer experience a bit better, especially
in cases when additional upstream packages that are not a part of MOS need
to be installed).

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

When Fuel master node is upgraded to a version that supports Linux distro
separation, package repositories for old versions of MOS deployed by previous
version of Fuel will keep using the old mirror structure. Package repositories
for the new versions of MOS will use the structure defined in this
specification.

Also see support-ubuntu-trusty [5]_ on the upgrade impact of switching the base
Ubuntu version from 12.04 (precise) to 14.04 (trusty).

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

In case of offline installations, user will be required to create a
copy of MOS/Upstream mirrors by using a script described in this
document.

Performance Impact
------------------

If packages are consumed from remote 3rd party servers, overall deployment
time may be increased. In case of offline installation, no deployment speed
degradation is expected.

Other deployer impact
---------------------

Changes described in this document allow to increase product flexibility,
by making possible to choose an operating system and install it independent
of MOS.

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Vitaly Parakhin <vparakhin@mirantis.com>
  Dmitry Burmistrov (make build system with updates and security updates)
  DevOPS (organize mirror, organize status page)

QA:
  Artem Panchenko <apanchenko@mirantis.com>
  Denis Dmitriev <ddmitriev@mirantis.com>

Mandatory Design Reviewers:
  Sergii Golovatiuk <sgolovatiuk@mirantis.com>
  Tomasz Napierala <tnapierala@mirantis.com>
  Vladimir Kuklin <vkuklin@mirantis.com>
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>
  Roman Vyalov <rvyalov@mirantis.com>

Work Items
----------

* Create local OS mirrors for CI purposes
* Change Fuel make system to exclude DEB packages from ISO
* Create MOS mirror with the same structure as OS vendor
* Deb package build process should be changed. All packages should be put in
  MOS mirror
* Create CI Jobs to test against OS vendor SRU [2]_
* Create status page to notify customers in case of problems with OS updates.
   - Create apt hooks to notify the customer in case of "apt-get upgrade"
* Adapt system tests of Ubuntu for the new repositories workflow
* Implement script for creating of local Upstream and MOS mirrors on master
  node.

Dependencies
============

None

Testing
=======

As this document introduces structural changes to the ISO composition and
MOS mirrors layout, testing procedure must reflect the updated workflow
for deploying Ubuntu environments described in this blueprint. [1]_

* Test if master node can be bootstrapped
* Test if CentOS cluster can be deployed
* Test if Ubuntu cluster can be deployed

Documentation Impact
====================

The documentation should cover:

* The description of the new MOS package lifecycle, including mirrors structure
  and package versioning and metadata conventions.

* How to use the script for creating local base OS and MOS mirrors for
  deployment in an environment without direct Internet access.

References
==========

.. [1] `Consume External Ubuntu <https://blueprints.launchpad.net/openstack/?searchtext=consume-external-ubuntu>`_
.. [2] `Ubuntu SRU procedure <https://wiki.ubuntu.com/StableReleaseUpdates#Examples>`_
.. [3] `CentOS FastTrack Channel <http://mirror.centos.org/centos/7/fasttrack/Readme.txt>`_
.. [4] `Building target images with Ubuntu on master node <https://blueprints.launchpad.net/fuel/+spec/ibp-build-ubuntu-images>`_
.. [5] `Support Ubuntu 14.04 (Trusty) <https://blueprints.launchpad.net/fuel/+spec/support-ubuntu-trusty>`_
.. [6] `apt_preferences(5) <http://manpages.debian.org/man/5/apt_preferences>`_
.. [7] `Debian Policy 5.6.12 (Version) <https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-Version>`_
