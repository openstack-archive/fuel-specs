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

Since Fuel 5.1 an upgrade tarball may contain few OpenStack bundles and
each OpenStack bundle includes a self-sufficient repo. The "self-sufficient"
here means that the repo contains not only OpenStack packages, but system.

The system packages are rarely changed so in most cases we can distribute
within OpenStack bundle a small repo which contains only those packages
that were changed regarding to some base previous release.

To achieve this goal we need to resolve next points:

* The Nailgun has to be able to send one, two or more repos to Astute
  and Astute has to be able to handle this.

* A Jenkins job should be added to create a diff-based repo. A diff-based
  repo should be updated if and only if a base repo has been successfully
  rebuilt. The Jenkins job should be able to receive a base (parent)
  repo/mirror as a job parameter.

* A diff-based repo should contain only packages that are changed regarding
  to some base release. For example, Fuel 6.0 upgrade tarball will ship
  with a repo which contains only changed packages regarding to Fuel 5.1.

* The Fuel Upgrade script has to be able to add new "OpenStack releases"
  with one, two or more repos.

Information about base repo should be added through `openstack.yaml`. It
can be injected automatically during build process.

There should be only one upgrade chain::

    5.1 -> 6.0 -> 6.1

in other words there should be situation when we get 6.0 without upgrading
to ``5.1``. For example, next upgrade chain is invalid and should not be
existed::

    5.0.1 -> 6.0 -> 6.1


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
        "repo_name": "repo_path"
    }

and could contain several repos.

The changes that was described above is already implemented in both
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

Other contributors:

* Fuel OSCI
* Fuel DevOps

Work Items
----------

* Add multi-repo support to Astute.
* Add multi-repo support to Nailgun.
* Add Jenkins job for creating a diff-based mirror.
* Add Jenkins job for creating an upgrade tarball with diff-based repos.
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
