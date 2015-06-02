..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Reduce time to publish packages
===============================

https://blueprints.launchpad.net/fuel/+spec/granular-update-mirrors

Problem description
===================

* As a Package Maintainer, I want my package updates to be published to
  official package repositories immediately after my code changes are merged
  in git to reduce the time it takes to publish packages

At the moment, packages are built and tested in simple and deploy tests as
part of patch set validation, then pushed to staging mirrors, then staging
mirrors are validated using BVT system tests using most recent stable build of
Fuel, then staging mirrors are published. There are no logs 

Proposed change
===============

We must complete all package validation (including BVT) before package change
patch set is merged, and then publish packages to the mirrors immediately after
review is merged.

Each package built via Gerrit change request will undergo the following tests:

* basic syntax test (rpmlint and lintian, for RPM and DEB packages,
  respectively)
* basic package health test (install, run basic shell script, uninstall)
* full system test based on the following scenario:
  - RPM package: ha_nova_vlan
  - DEB package: ha_neutron_ceph

All tests will be running in parallel. In case if basic package health test
for a given patch set is failed, the respective full system test must be
aborted to prevent the waste of a CI system resources.

Full logs for a system test run must be available in the OSCI Jenkins as a job
artifact.

On merge event in Gerrit, rebuilt package will be pushed to a respective
stable repository on an internal OSCI mirror, and right after that, this
repository will be synced to the external OSCI mirrors without any further
verification. RPM and DEB mirrors are synced independently, list of synced
packages must be included as an artifact to an appropriate OSCI Jenkins job.

Alternatives
------------

Keeping the time lag of several hours between approving a code or specification
change and updated package becoming available for customers is not acceptable.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

None

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

None

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

Due to more complex scenarios used in deploy tests configuration, time to
complete all CI jobs for a single commit will increase approx. by 60%-120%.
A speed of publishing of packages, decreased from hours to minutes, should
compensate this inconvenience, though.

Infrastructure impact
---------------------

* Changes in system tests will require additional servers to be used as OSCI
  Jenkins slaves.

* Logs of a system tests will be stored on the OSCI Jenkins Master, therefore
  we will need to increase the storage capacity for this server (at least 1 TB
  is required).

* Changes described in this document will only apply to 7.0+ CI environments,
  no backporting for older releases is planned.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Vitaly Parakhin <vparakhin@mirantis.com>

DevOps:
  <TBD>

QA:
  <TBD>

Work Items
----------

* Implement OSCI Jenkins job for syncing of CentOS mirrors [1]_
* Implement OSCI Jenkins job for syncing of Ubuntu mirror [1]_
* Create OSCI Jenkins jobs for new package tests
* Setup new OSCI Jenkins slaves for package test jobs [2]_
* Switch package tests to new jobs
* Eliminate the staging mirrors phase in the MOS 7.0 Product CI
* Replace all packages sources of MOS 7.0 components in Gerrit with fully
  unpacked source code (get rid of orig.tar.gz etc)

Dependencies
============

None

Testing
=======

Acceptance Criteria:

* Each package source code and build script change patch set is validated with
  the same level of test coverage that is currently used for package staging
  mirrors.
* All validation is done on patch sets before the change is merged; once the
  change is merged, package is propagated to official package repositories
  without additional validation.
* There are no binary packages in any of the MOS 7.0 package repositories that
  were not built by the new build system from master or 7.0 specific branches
  in git repositories with build scripts and fully unpacked source code (no
  orig.tar.gz files in git).
* Individual package and test jobs can be retriggered one at a time.

Documentation Impact
====================

None

References
==========

.. [1] `Refactor rsync scripts <https://trello.com/c/BlQjHISB/209-refactor-safe-rsync-scripts>`_
.. [2] `OSCI to public <https://blueprints.launchpad.net/fuel/+spec/osci-to-public>`_
