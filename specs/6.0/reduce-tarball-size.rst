..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
Reduce upgrade tarball's size
=============================

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

* Fuel-OSCI has to prepare special repos which will contain only
  packages that are changed regarding to some previous release.

* The Fuel Upgrade script has to be able to add new "OpenStack releases"
  with one, two or more repos.

Alternatives
------------

We can distribute just a set of changed packages instead of a small repo.
In that case we will need to create a new repo on fly during fuel upgrade
procedure. Creating repos on fly is not trivial procedure and may fail
time to time due to outside factors.

Data model impact
-----------------

None

REST API impact
---------------

None

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

An unpack time of tarball should be reduced.

Other deployer impact
---------------------

* slave nodes may have more than one repo in the system.

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

Work Items
----------

* add multi-repo support to both Astute and Nailgun;
* change uan pgrade tarball format to contain diff-based repos;
* add support of diff-based repos to fuel-upgrade script.


Dependencies
============

None


Testing
=======

Existing Fuel Upgrade / OpenStack patching tests are enough since it's about
improvements, not about entirely new feature.

But next tests may be added:

* tests that there're more than one repo on slaves;
* tests that an upgrade tarball contains only changed packages, not all.


Documentation Impact
====================

None


References
==========

* #fuel-dev on freenode
