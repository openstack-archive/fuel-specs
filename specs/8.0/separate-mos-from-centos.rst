..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================
Separate MOS packages from CentOS ones
======================================

https://blueprints.launchpad.net/fuel/+spec/example

--------------------
Problem description
--------------------

* As a Cloud Operator I would like to provision CentOS 7 on environments

* As a Cloud Operator I would like to see what RPM packages are provided by
  Mirantis OpenStack and what RPM packages are provided by base distro

* As a Cloud Operator I would like to get security updates as fast as possible
  independantly for base distro as well as for Mirantis OpenStack

* As a Package Maintainer I would like to keep track of sources to all
  Mirantis OpenStack packages and minimize the number of modified ones as much
  as possible

----------------
Proposed changes
----------------

Web UI
======

* Once users have created an environment on CentOS they should be able to
  provide both CentOS and MOS RPM repos as well as additional repos on the
  "Setting" tab. By default, official CentOS repo for CentOS upstream and
  Fuel repo for MOS RPM packages should be used.

Nailgun
=======

Data model
----------

* Nailgun default settings for CentOS must include repository
  settings for CentOS and MOS repos listed in the "Web UI" chapter.

* These settings should reuse the existing model of editable attributes
  that allow to specify a set of repos and their options (i.e. priority)

REST API
--------

None

Orchestration
=============

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

* Fuel Puppet manifests have to be adjusted to support CentOS 7 deployments

------------
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

--------------
Upgrade impact
--------------

When Fuel master node is upgraded to a version that supports Linux distro
separation, package repositories for old versions of MOS deployed by previous
version of Fuel will keep using the old mirror structure. Package repositories
for the new versions of MOS will use the structure defined in the
mos-rpm-repos-iface_ specification.

.. _mos-rpm-repos-iface: https://github.com/stackforge/fuel-specs/blob/master/specs/7.0/mos-rpm-repos-iface.rst

---------------
Security impact
---------------

None

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

In case of offline installations, user will be required to create a copy of MOS
and base distro mirrors by using a script described in the
`separate_mos_from_linux`_ specification.

------------------
Performance impact
------------------

If packages are consumed from remote 3rd party servers, overall deployment
time may be increased. In case of offline installation, no deployment speed
degradation is expected.

-----------------
Deployment impact
-----------------

Changes described in this document allow to increase product flexibility,
by making possible to choose an operating system and install it independent
of MOS.

----------------
Developer impact
----------------

None

--------------------------------
Infrastructure/operations impact
--------------------------------

System tests for CentOS will be adjusted to reflect the new repositories scheme
for MOS packages and base OS packages.

--------------------
Documentation impact
--------------------

The documentation should cover:

* How to use the script for creating local base OS and MOS mirrors for
  deployment in an environment without direct Internet access.

--------------------
Expected OSCI impact
--------------------

* RPM packages built for OpenStack cluster will be stored separately
  as it is described by the mos-rpm-repos-iface_ specification.

-------------------------------
Package versioning requirements
-------------------------------

Package version string, as well as package metadata for a *MOS specific* or
*divergent* package must not include registered trademarks of base distro
vendors, and should include "mos" keyword.

-----------------------
RPM packages versioning
-----------------------

Package name constructs from::

    <name>-<version>-<release>

For example::

    python-iso8601-0.1.10-1.el7

Where:

- python-iso8601 - name
- 0.1.10 - version
- 1.el7 - release

All modifications should be made in release section.

**1** - first digits in *release* represents actual package revision/release
number and should be incremented in case of package update(spec modification,
patching etc).

Example::

    python-iso8601-0.1.10-1.el7 -> python-iso8601-0.1.10-2.el7

**el7** - represents distribution that was used during package building
process and generated by %{?dist} macro. For packages maintained by MOS  special
suffix must be add after %{?dist} macro which represents *MOS release* during
package build process.

Example::

    python-iso8601-0.1.10-1.el7 -> python-iso8601-0.1.10-1.el7~mos8.0.1

**Options/tags should be modified by CI/Build:**

Below provided example with options from python-iso8601.spec file::

    Name:           python-iso8601
    Version:        0.1.10
    Release:        1%{?dist}

CI/Build system should modify *Version:* and *Release:* values before build
process to ensure that package version and release represents truth:

- *Version:* for **OpenStack projects** must be substituted with last tag
  in code branch from where package will be built.
- *Release:* value should be preserved and concatenated with MOS specific
  attributes.

Example::

    was:    Release:        1%{?dist}
    became: Release:        1%{?dist}~mosX.X.X

This modification leads to transformations as follows::

    python-iso8601-0.1.10-1.el7 -> python-iso8601-0.1.10-1.el7~mos8.0.1

**Subsequent version:**

This number represents amount of commits into code since last tag change in
current code branch and must be added after **mosX.X**.

Example::

    python-heat-2015.2-1.el7~mos8.0.123 -> python-heat-2015.2-1.el7~mos8.0.124

**Structure of release part for packages maintained by Mirantis:**

python-iso8601-0.1.10-1.%{?dist}~mos8.0.1
Where:

- ~ separator from base Linux distro version
- mosX.X - X.X represents major and minor version of MOS release.
- 3rd X - represents commits number since last tag/branch update in code.

For example we have python-iso8601 package with code version = *0.1.10*

- package release = *1*,
- %{?dist} = Linux distro name(el7),
- MOS release = *mos8.0*,
- commits number into code within code version 0.1.10 = *1*.

Only packages from security-updates repository should have security update
number at the very end!

Regular packages should only have commits number for the very last
value in version string.

--------
Backport
--------

If package needs to be backported by any reason - name and version must be
kept. Modification required for *release* part, initial revision of a package
also should be preserved. Any further modifications of package will be
represented in commits number which follows after *mosX.X*. By default this
value will be always set to 1 and will be increased in case of package modification.

Example::

    python-iso8601-0.1.10-1.el7 -> python-iso8601-0.1.10-1.el7~mos8.0.1
    python-iso8601-0.1.10-1.el7~mos8.0.1 -> python-iso8601-0.1.10-1.el7~mos8.0.2

--------------
Package update
--------------

If required to update package SPEC file or add patch or make any other
modifications not related to code version update, package revision / release
number must be increased. If a major change (new version of the software being
packaged) occurs, the version number is changed to reflect the new software
version, and the release number is reset to 1. In case of packages maintained
by MOS this is **valid for OpenStack** projects.

For **non OpenStack** projects, like dependencies and back-ported packages all
updates will be represented in commits number part of release. After code
version update Commits number value resets to 1 and will be increased in cases
of further modifications of a package.

Update of dependencies within one code version(*non OpenStack*)::

    python-iso8601-0.1.10-1.el7~mos8.0.1 -> python-iso8601-0.1.10-1.el7~mos8.0.2

Update of dependencies in case of code version update(*non OpenStack*)::

    python-iso8601-0.1.10-1.el7~mos8.0.1 -> python-iso8601-0.1.11-1.el7~mos8.0.1

Update of OpenStack project - SPEC changed::

    python-heat-2015.2-1.el7~mos8.0.123 -> python-heat-2015.2-2.el7~mos8.0.123

Update of OpenStack project - code tag/branch changed::

    python-heat-2015.2-1.el7~mos8.0.123 -> python-heat-2015.3-1.el7~mos8.0.1

----------------------------------------------
Versioning of packages in post-release updates
----------------------------------------------

**Updates:**

Since MOS reaches GA status, ie officially released, all updated packages will
be published into separate *updates* repository. Updated package will have
higher commit number value in the release part then package from stable
repository.

Example::

    python-iso8601-0.1.10-1.el7~mos8.0.200 -> python-iso8601-0.1.11-1.el7~mos8.0.201
    python-heat-2015.2-1.el7~mos8.0.200 -> python-heat-2015.2-1.el7~mos8.0.201

**Security updates:**

Security updates will also be published in a separate repositiry and based on
package from *updates* repository. Additional subsequent version will be add to
the version of a package which *represents security update* number following
by *s* prefix.

Example::

    python-iso8601-0.1.10-1.el7~mos8.0.201 -> python-iso8601-0.1.11-1.el7~mos8.0.201.s1
    python-heat-2015.2-1.el7~mos8.0.201 -> python-heat-2015.2-1.el7~mos8.0.201.s1

**Work with branches within updates:**

Banches example:

- openstack-ci/fuel-8.0/stable - freezes after GA
- openstack-ci/fuel-8.0/updates - branch for maintenance updates between main
  releases
- openstack-ci/fuel-8.0/security-updates - branch for security updates

Any changes into *updates* branch must be passed through all tests.
Any changes into *security-updates* branch should include CVE security fixes
and sould be based on the last stable commit from *updates* or *stable* branch in
case of absence of published updates.

Example for python-iso8601 0.1.10 package:

Stable branch::

    project: python-iso8601
    branch: openstack-ci/fuel-8.0/stable
    number of commits: 1
    tag: 0.1.10

After GA, *stable* branch should be frozen and do not accept any changes.
All further work is moving into "updates" branch, this means all next
maintenance updates will be published from this branch.

Updates branch::

    project: python-iso8601
    branch: openstack-ci/fuel-8.0/updates
    number of commits: 2
    tag: 0.1.10

In case of critical vulnerabilities found for project, updates with security
patches will be committed into *security-updates*, published into
security-updates package repositories and also pushed into *updates* branches
to keep these changes.

Security updates branch::

    project: python-iso8601
    branch: openstack-ci/fuel-8.0/security-updates
    number of commits: 2
    security update tag: s1
    tag: 0.1.10

Transformations within ongoing MOS releases as for dependecies as for
OpenStack projects::

   mos8.0:                  python-iso8601-0.1.10-1~mos8.0.1
   mos8.0:                  python-heat-2015.2-1.el7~mos8.0.1
   mos8.0-updates:          python-iso8601-0.1.10-1~mos8.0.2
   mos8.0-updates:          python-heat-2015.2-1.el7~mos8.0.2
   mos8.0-security-updates: python-iso8601-0.1.10-1~mos8.0.2.s1
   mos8.0-security-updates: python-heat-2015.2-1.el7~mos8.0.2.s1
   mos8.1:                  python-iso8601-0.1.10-1~mos8.1.1
   mos8.1:                  python-heat-2015.2-1.el7~mos8.1.1

------------------------------
Prioritization of repositories
------------------------------

From out of the box *YUM* package manager has no ability to use repository
priorities. This functionality is accessible via yum plugin named
**yum-plugin-priorities** and accessible from Base repository. Also this
makes us able to use priorities for *Holdback* repositories.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vitaly Parakhin <vparakhin@mirantis.com>

QA assignee:
   TBD

Other contributors:
  TBD

Mandatory design review:
  TBD

Work Items
==========

* Determine the source of each package on MOS RPM mirror

* Build MOS Packages for CentOS 7

* Modify make system to allow to build ISO with CentOS 7

* Add support of RPM repositories to the local mirrors creation script


Dependencies
============

.. _separate_mos_from_linux: https://github.com/stackforge/fuel-specs/blob/master/specs/6.1/separate-mos-from-linux.rst

------------
Testing, QA
------------

TBD

Acceptance criteria
===================

* ISO with CentOS 7 passes all BVT & Swarm system tests
* All main CentOS clusters configurations can be successfully deployed
* Local mirrors creation script can create local copies of MOS and
  base OS repositories and can add them to Nailgun

----------
References
----------

TBD
