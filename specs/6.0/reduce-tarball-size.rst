..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================================
Reduce an openstack release size inside upgrade tarball
=======================================================

https://blueprints.launchpad.net/fuel/+spec/reduce-tarball-size

Let's reduce size of our fuel upgrade tarball, since it's huge and
uncomfortable for distribution.


Problem description
===================

We need to reduce upgrade tarball's size in order to simplify distribution
workflow, boost up downloading/unpacking speed and reduce used space
on master node's file system.


Proposed change
===============

Terms
-----

*openstack bundle*
  An OpenStack bundle is a set of artifacts which together constitute
  an openstack release in terms of Nailgun. The bundle contains next
  artifacts:

  - puppet modules and manifests
  - ubuntu and centos repos
  - openstack.yaml

*full repo*
  A full repo is a self-sufficient repo which contains all packages
  that are required for both master node and openstack deployment.

*diff-based repo*
  A diff-based repo is a kind of repo that contains only those packages
  that were changed regarding to some previous repo. Please note,
  that a previous repo may be either full or diff-based one.

*base repo*
  A base repo term is used only in context of diff-based repos, when
  we want to point the repo on which a diff-based repo based.

Changes
-------

Since Fuel 5.1 an upgrade tarball may contain few OpenStack bundles and
each OpenStack bundle includes a self-sufficient repo. The "self-sufficient"
here means that the repo contains not only OpenStack packages, but system.

The system packages are rarely changed so in most cases we can distribute
within OpenStack bundle a small repo which contains only those packages
that were changed regarding to some base previous release.

The changes have to be detected by packages' checksum, since we can't rely
on package versions due to the following issue -
`LP1376694 <https://bugs.launchpad.net/fuel/+bug/1376694>`_.

To achieve this goal we need to resolve next points:

* A build system should have a ``make mirror_diff`` goal to create
  a diff-based mirror between current mirror and some previous one.
  As it was mentioned in previous paragraph, a diff-based mirror should
  be created by comparing packages' checksums from both mirrors.

* A build system should have a ``make openstack_bundle`` goal to
  create an artifact which contains a *release* in terms of Nailgun.
  See "Terms" section for details.

* A Jenkins job should be added to create a diff-based repo. The job should
  be triggered if a staged mirror has been updated and should provide
  a diff-based mirror as an artifact for further usage.

* A diff-based mirror should become *stable*, when an appropriate
  full mirror get *stable*. In other words, a diff-based should
  always keep sync with a full one, so we always know it has
  the same version of packages as a full one.

* Each Jenkins Job which creates both ISO and upgrade tarball should
  also provide an *openstack bundle* as artifact for further usage
  from another jobs.

* The Jenkins Job which builds ISO/tarball for current version (6.0)
  should be able to include additional *openstack bundles* in order
  to deliver more than one openstack release.

* The Fuel Upgrade script has to be able to add new "OpenStack releases"
  with one, two or more repos. In other words, the script should detect
  whether we're dealing with a diff-based repo and if so to add a path
  to base repo too.

Information about base repo should be added through `openstack.yaml`. It
can be injected automatically during build process or can be done by
Fuel Upgrade script.

There should be only one major upgrade chain. For example::

    5.1 -> 6.0
    5.1.1 -> 6.0

In other words, there shouldn't be a situation when we upgrade to ``6.0``
from ``5.0.x`` series.


Alternatives
------------

We can distribute just a set of changed packages instead of a small repo.
In that case we will need to create a new repo on fly during fuel upgrade
procedure. Creating repos on fly is not trivial procedure and may fail
time to time due to outside factors.

Data model impact
-----------------

A deployment info (a one that Nailgun sends to Astute and Astute saves it
as `astute.yaml`) should have a ``repo_metadata`` field, which is a JSON
object (or Python dictionary).

The ``repo_metadata`` has next structure::

    "repo_metadata": {
        "repo_name_1": "repo_path_1",
        "repo_name_2": "repo_path_2",
    }

and will be converted into following yum's repo file::

    [repo_name_1]
    name=repo_name_1
    baseurl=repo_path_1
    gpgcheck=0

    [repo_name_2]
    name=repo_name_2
    baseurl=repo_path_2
    gpgcheck=0

The changes that was described above are already implemented in both
Nailgun and Astute, and therefore should be kept as is.

REST API impact
---------------

Master node IP is not a constant value, so maybe we need to support some
sort of ``{master_ip}`` replacement in release handlers. Alternatively,
it could be done by an upgrade script.

Upgrade impact
--------------

The Fuel Upgrade script has to be able to add new "OpenStack releases"
with one, two or more repos.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

* Unpacking time of tarball should be reduced.
* Downloading time of tarball should be reduced.

Other deployer impact
---------------------

* Slave nodes may have more than one repo in the system.

Developer impact
----------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Igor Kalnitsky <ikalnitsky@mirantis.com>
* Sergey Kulanov <skulanov@mirantis.com>

Other contributors:

* Fuel OSCI
* Fuel DevOps

Work Items
----------

* Add ``make mirror_diff`` goal to build system.
* Add ``make openstack_bundle`` goal to build system.
* Add Jenkins Job for creating a diff-based mirror.
* Configure existing Jenkins Jobs for providing an *openstack bundle*
  as artifact.
* Configure existing Jenkins Jobs to use additional *openstack bundles*
  if needed.
* Add support of diff-based repos to fuel-upgrade script.


Dependencies
============

None


Testing
=======

Existing Fuel Upgrade / OpenStack patching tests are enough since it's about
improvements, not about entirely new feature.

But next tests may be added:

* Test that there're more than one repo on slaves.
* Test that an upgrade tarball contains only changed packages, not all.
* Test that a diff-based release passes the same tests as the full release.


Documentation Impact
====================

The documentation about release management should be added and it should
resolve next questions:

* Which components includes a release?
* Where are the components stored?
* How releases reuse packages from older releases.


References
==========

* #fuel-dev on freenode
