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

* As a Cloud Operator I would like to see what packages are provided by MOS and
  what packages provided by OS Provider

* As a Cloud Operator I would like to have OS support contract as well as MOS
  support

* As a Cloud Operator I would like to get security updates as fast as possible
  independantly from OS Provider as well as from MOS

* As a Cloud Operator I should be able to see sources of OS and MOS packages

* As a Cloud Operator I should be able to see debug symbols of OS and MOS
  packages

* As a Fuel Developer, I would like to have the same approach for making
  changes to Fuel components and their dependencies.

To provide highest quality MOS should separate lifecycle OS and Cloud lifecycle
management. Meanwhile OS Updates shouldn't break MOS functionality and vice
versa.

Proposed change
===============

Types of software packages
--------------------------

This specification introduces a clear separation between base distro (Red Hat
or Debian based Linux OSes), and an OpenStack distribution (MOS). All software
packages deployed by Fuel are divided into following categories based on their
relation to the specific base distro and OpenStack distribution being deployed:

#. Upstream Package: a package from base distro is reused from distro
   repositories directly, without MOS specific modifications.

#. MOS Specific Package: a package which is specific to MOS and does not exist
   in base distro.

#. Forked package: a package from base distro which has MOS specific
   modifications and put to MOS repository.

#. Upgraded package: a variant of a forked package, where MOS specific
   modifications include an upgrade to a more recent software version which
   doesn't exist in base distro.

#. Holdback package: Upstream Package which was used from base distro
   repositories until a new upstream version introduced a regression. It was
   forked and put to special repository until the regression is fixed in a more
   recent version from base distro.

.. note:: Downgraded packages with upstream version lower than the version
          available in the base distro are not allowed.

Different releases of MOS can put the same software package in different
categories.

When possible, MOS specific modifications should be avoided, so that as many of
MOS dependencies as possible are satisfied by upstream packages from base
distro.

When possible, MOS patches should be contributed back to base distro to
minimize deviation between Upstream Package and Forked Package.

Distributing MOS packages
-------------------------

Released MOS packages will be distributed as part of Fuel ISO image. Upstream
packages, as well as any other IP protected by respective OS vendors, will not
be the included in Fuel ISO images. Regular updates to the MOS OpenStack
distribution will be delivered through online MOS mirrors.

MOS mirrors structure
---------------------

MOS mirrors should be organized in the same way as base distro mirrors. MOS mirrors
should follow industry standards. The structure of a mirror should be done in
the same way as base distro mirrors.

Every supported OS will have own set of repositories containing MOS packages
per release (mos6.1, mos7.0 etc.) These repositories must contain only packages
with MOS specific modifications, and no upstream packages from the
corresponding base distro.

Mirror should be publicly and globally available and distributed. User should
be able to create and maintain local copies of base distro and MOS mirrors. This
will allow user to use repositories in completely isolated environments or
create own freezed mirrors to pass extended validation before package update
roll-out across production environment.

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
built in the same way as base OS mirror (Debian or Ubuntu). Repository sections
are organized in the same way (main, restricted) according to package licenses
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

Red Hat based mirror structure
------------------------------

MOS mirror should include several repositories (os, updates, fasttrack) built
in the same way as base distro mirror (Red Hat or CentOS).

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

Repositories priorities
-----------------------

Handling multiple package repositories in Nailgun [1]_ will be expanded to
allow user to set priorities during deployment.

Default repository priorities are arranged so that packages from MOS
repositories are preferred over packages from base distro. On Debian based
systems, the force-downgrade APT pinning priorities are used for MOS
repositories to make sure that, when a package is available in a MOS repo, it
is always preferred over the package from base distro, even if the version in
MOS repo is lower.

Fuel developer repositories
---------------------------

Build system should allow developers to build packages. These packages should
be placed into special repository which can be specified in Nailgun [1]_ to
deliver these packages to an environment. In terms of Debian pinning of these
repositories should be higher base distro and MOS repositories. In terms of
CentOS repository priority value must be lower than base distro and MOS
repositories.

Later, this functionality should be exposed to the community allowing any
community engineer (e.g. nova, cinder) to specify their own git refspec
(repository and commit). The build system should be able to build packages and
provide a link which can be passed through Nailgun.

Holdback repository
-------------------

Holdback repository is a measure aimed to ensure the highest quality of MOS
product. If there is an Upstream package that breaks the product, and this
problem cannot be fixed in a timely manner, MOS team publishes the package
proven stable to the "mosXX-holdback" channel. This repository should be
automatically configured on all installations with highest priority.

The case when base distro vendor releases fixed version of a problem package,
must be covered by MOS system tests.

Ideally, Upstream updates shouldn't break the functionality of Product. The
number of packages in "mosXX-holdback" should be zero. Even if package is put
in repository, MOS team should contact base distro vendor to report the
regression. Package Update should be discarded before it appears in Update
channel. If package is supposed to appear in Update channel, MOS team should
update "mosXX-holdback" channel before that.

Testing in this channel should be done against every package as next release
may fix the regression that might occur. Once regression is fixed in upstream
the package should be removed from "mosXX-holdback" repository.

Package versioning requirements
-------------------------------

Package version string of any package with MOS specific modifications,
including MOS specific packages, must include 'mos' keyword, and must not
include registered trademarks of any base distro vendors.

Every new revision of a forked, MOS specific, or upgraded package targeted to a
MOS release (including corresponding update repository) must have a package
version greater than or equal to the versions of the same package in all
previous releases of MOS (base, update, security repositories), as well as
versions of the same package previously published in any repos for this MOS
release.

For example, there must be no package version downgrades in the following MOS
release progression (where 6.1.1 matches the state of update repository at the
time of 6.1.1 maintenance release):

    6.0 <= 6.0.1 <= 6.1 <= 6.1.1 <= 6.1.2 <= 7.0

Every new revision of a holdback package must have a package version greater
than previous revisions of the same package that were published to the holdback
repository for that MOS release.

Package version of a forked or upgraded package must be constructed in a way
that would allow an upstream package with the same software version to
supercede the upgraded package in MOS when it is published by the upstream OS.
This will simplify phasing out forked packages in favor of upstream packages
between major MOS releases, but, due to repo priorities defined above, will not
lead to new upstream packages superceding upgraded packages available from MOS
repos when applying updates.

When the same package version is ported from one MOS release to another without
modifications (i.e. same upstream version and same set of patches), new package
version should include full package version from the original MOS release.

Debian package versioning
-------------------------

Versioning requirements defined in this section apply to all software packages
in all MOS repositories for Debian based distros. The standard terms defined in
Debian Policy [7]_ are used to describe package version components: epoch,
upstream version, Debian revision.

Upstream version of a package should exactly match the software version,
without suffixes. Introducing epoch or increasing epoch relative to base distro
should be avoided.

Debian revision of a MOS package should use the following format:

.. example:: <revision>~mos<subrevision>

In MOS specific packages, revision must always be 0. In forked, upgraded, and
holdback packages, revision should match the revision of a base distro package
the MOS package is based on. Subrevision numbering starts from 1.

.. example:: qemu-2.1.0-1 becomes qemu-2.1.0-1~mos1
             ohai-6.14.0-2ubuntu1 becomes ohai-6.14.0-2~mos1

Subsequent revisions of a package using the same upstream version and based on
the same base distro package should increment the subrevision.

.. example:: ohai-6.14.0-2~mos2, ohai-6.14.0-2~mos3

Subsequent revision of a package that introduces a new upstream version or new
base distro package revision should reset the subrevision back to 1.

.. example:: ohai-6.14.0-3ubuntu1 becomes ohai-6.14.0-3~mos1

FIXME: end of Dmitry's edits

Revision of Forked Packages should start from 1. It cannot be started from 0 as
it means that package shouldn't be forked and can be consumed from base distro
repository.

.. example:: qemu-2.1.0-2mos1+1

It can be read as qemu package with version 2.1.0 was forked from Ubuntu with
revision 1 and has 1 MOS modification to package metadata or has a patch to
qemu software.

Revison of MOS Specific package should start from 0.

.. example:: python-tasklib-0.0.1-0mos+0

It can be read as python-tasklib with version 0.0.1 doesn't exist in base
distro and was not updates since creation.

Revision of Upgraded Package may start from 0+0. In this case it means that
package was forked from base distro repository though there were no
modifications to package. Only software version was bumped and doesn't exist in
Upstream repositories. Zero in mos build version indicates that package was
forked from Upstream though upstream package contains lower software version.
When MOS changes are still required mos build version should start from 1

.. example:: openvswitch-2.3.11-0mos0+0

it can be read as openvswitch was forked from upstream but lower version (mos0).
The package version was bumped to 2.3.11 and doesn't contain any MOS changes.

Backporting packages
--------------------

In case where package backport is required from upper upstream version it
follows standard forking procedure.

For instance we need newer openvswitch which
doesn't exist in Ubuntu 14.04 though it exists in Ubuntu 15.04.

In case when we need to backport package from upper MOS release to update or
maintenance release ~{release_version} should be added as both packages will be
present in the same mirror.

For example, if base MOS repository contains version 1.2.3-0mos+1 and version
1.2.4 is required in MOS 6.1, and this pacckage is present in 7.0 as
1.2.4-1mos+1. Package will be backported and package version will be
1.2.4-1mos+1~mos61+0

When a new build of the backported package is targeted to update repository or
a maintenance release of a GA release, the MOS build version should be expanded
to include the original MOS build version, the targeted release series, and a
secondary build number, starting with 1. All three components must be separated
with a plus sign. For example, if 1.2.3-0mos+2 was released in the 7.0 GA
release, and was backported to 6.1 subsequent updates for the same release
series will be 1.2.3-0mos+2~mos6.1+1.

In holdback packages, same "~mosx.y" suffix must be appended to the upstream
version. For example, if base OS package version 1.2.3-0ubuntu1 introduces a
regression in MOS 6.1, the replacement package versions will be
1.2.3-0mos1~mos6.1+1 introduced in holdback repositiry.

When package is backported from upper release to previous releases it should
follow standard backport procedure where package name and version will remain
but ~{release_version} is appended to the Debian revision.

For example: MOS 7.0 has a package openssl1.0.1a-1mos1+0 which we need to
backport to 6.1 and 6.0. In this case backport package versions will become as

openssl1.0.1a-1mos1+0~6.1
openssl1.0.1a-1mos1+0~6.0

Debian package metadata
-----------------------

All deb packages that are not deployed directly from an upstream OS must have
the following metadata:

#. Latest entry in the debian/changelog must contain:

   - reference to the targeted MOS release series (e.g. mos6.1)

   - reference to the organization that produced the package (Mirantis)

   - commits (full git commit sha1) in all source code repositories that the
     package was built from: build repository commit if both source code and
     build scripts are tracked in the same repository (git-buildpackage style),
     or both source and build repository commits if source code is tracked in a
     separate repository from build scripts

#. Maintainer in debian/control must be MOS Team

Example of a valid debian/changelog entry::

  python-keystoneclient (2014.2.3-0mos1) mos6.1; urgency=low

    * Source commit: 17f8fb6d8d3b9d48f5a4206079c18e84b73bf36b
    * Build commit: 8bf699819c9d30e2d34e14e76917f94daea4c67f

   -- MOS Team <mos@mirantis.com>  Sat, 21 Mar 2015 15:08:01 -0700

If the package is a backport from a different release of an upstream OS (e.g. a
backport of a newer software version from Ubuntu 14.10 to Ubuntu 14.04), the
exact package version the backport was based on must also be specified in the
debian/changelog entry, along with the URL where the source package for that
package version can be obtained from (in order of preference: git-buildpackage
or similar source code repository, deb package pool directory, direct dpkg
source (orig and debian) download links.

Package lifecycle management
----------------------------

To deliver high quality of product MOS teams should produce package updates
during Product lifecycle when it's required.

Packaging lifecycle should follow the MOS product lifecycle (Feature Freeze,
Soft Code Freeze, Hard Code Freeze, Release, Updates).

Package flow should be specified from building package, passing SRU or
FastTrack Channels (mos6.1-proposed as a sample), acceptance testing, security
testing before it will appear in "updates" in MOS mirror.

Continous integration testing against base distro updates
---------------------------------------------------------

As a part of a product lifecycle there should be periodical system tests that
verify functionality of MOS against:

- the current state of base distro mirror (base system plus released updates),
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
- raise a debate with base distro SRU reviewing team regarding problem packages
- (if none of the above helps) put working version of a problem package to
  the holdback repository

Also, any package that failed the system test, must be reflected on the
release status page.

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

There's various reasoning behind having a local mirrors of base distro,
from security considerations, to making deployments faster and more reliable.
To support such installation cases we will implement the Linux console
script that mirrors the public base distro and MOS mirrors to a given location,
allowing to put these local sources as input for the appropriate menu entry of
Fuel "Settings" tab on UI, or specify directly via Fuel CLI. In case of
deb-based base distro, MOS requires packages from multiple sections of a given
distribution (main, universe, multiverse, restricted), so the helper script
will mirror all packages from components specified above. Requirements:

* input base distro mirror URL
* input MOS mirror URL
* ability to run as cronjob to update base distro and MOS mirrors

Alternatives
------------

There is no alternative to the repositories separation approach due to
considerations related to distribution policies of major OS vendors.
Regarding the helper script to download base distro repositories, there
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

In case of offline installations, user will be required to create a copy of MOS
and base distro mirrors by using a script described in this document.

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
* Implement script for creating of local base distro and MOS mirrors on master
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

.. [1] `Consume External Ubuntu <https://blueprints.launchpad.net/fuel/+spec/consume-external-ubuntu>`_
.. [2] `Ubuntu SRU procedure <https://wiki.ubuntu.com/StableReleaseUpdates#Examples>`_
.. [3] `CentOS FastTrack Channel <http://mirror.centos.org/centos/7/fasttrack/Readme.txt>`_
.. [4] `Building target images with Ubuntu on master node <https://blueprints.launchpad.net/fuel/+spec/ibp-build-ubuntu-images>`_
.. [5] `Support Ubuntu 14.04 (Trusty) <https://blueprints.launchpad.net/fuel/+spec/support-ubuntu-trusty>`_
.. [6] `apt_preferences(5) <http://manpages.debian.org/man/5/apt_preferences>`_
.. [7] `Debian Policy 5.6.12 (Version) <https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-Version>`_
