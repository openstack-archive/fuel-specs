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

At the moment, all changes to the MOS packages repositories are tested on
a set of simple functional and integration tests so that they will not be
merged into the stable package repository unless it passes all of the
configured tests. Merged packages are then pushed to staging mirrors, then
staging mirrors are validated using BVT system tests using most recent
stable build of Fuel, then staging mirrors are published.

Proposed change
===============

We must complete all package validation (including BVT) before package change
patch set is merged, and then publish packages to the mirrors immediately after
review is merged.

Proposed flow for change requests to MOS packages code and/or spec is below:

* Change request is submitted for code review to Gerrit
* Package is built from resulting sources and specs and placed into a test
  repository
* Test repository is run through automated functional and integration tests
* Change request is peer-reviewed
* Change request is accepted or rejected by core team
* Change request is run through pre-merge automated checks
* Change request is merged or rejected
* Package is built from resulting sources and specs, placed to the internal
  repository and signed (for RPM - a package itself, for DEB - repository
  metadata)
* Repository with rebuilt package is propagated to the external MOS mirrors

Test repositories
-----------------
<should structure be described in build system spec?>

Automated functional and integration tests
------------------------------------------

Each package built into a test repository will undergo the following tests:

#. *Basic syntax test* (rpmlint and lintian, for RPM and DEB packages,
   respectively)
#. *Basic package health test.* Uses plain VM with respective OS type that
   contains only the minimal set of packages. Package install, run basic
   shell script and uninstall tests are performed.
#. *Full system test (BVT analog).* Modification of a Fuel package may require
   rebuilding of various product artifacts. Depending on the package flavor,
   there are different test pipelines the test repository will follow.

   #. RPM and DEB packages for clusters. Test is performed against the
      stable Fuel ISO from Product Jenkins by the means of deploy of a
      cluster with adding of a test repository with highest priority (in
      terms of a respective package manager). In order to keep the actual
      test run as short and reliable as possible, the VM snapshots for
      Fuel master node and cluster nodes are prepared ahead of time and
      kept on slave servers ready for immediate use. The process of
      preparing the VM snapshots ahead of time reduces the network
      traffic and influence of an external depencencies during the run.
      The job that prepares the VM snapshots should be executed on a daily
      basis. 

   #. Fuel Master packages. Rebuilding of a Fuel ISO with an extra test
      repository and redeployment of Fuel Master node must precede the system
      test.

   #. Fuel bootstrap packages. Rebuilding of bootstrap package and
      installing it on the Fuel Master node created from snapshot prepared
      ahead precedes the system test.

   #. Fuel Docker container packages. Rebuilding of Fuel Docker containers
      package and installing it on the Fuel Master node created from
      snapshot prepared ahead precedes the system test.

All tests will be running in parallel. In case if basic package health test
for a given patch set is failed, the respective full system test must be
aborted to prevent the waste of a CI system resources.

Full logs for a system test run must be available in the OSCI Jenkins as a job
artifact. In order to support debugging of system test issues, snapshots of
VMs created during the test run are stored on Jenkins slaves for 20 days.

On merge event in Gerrit, rebuilt package will be pushed to a respective
stable repository on an internal OSCI mirror, and right after that, this
repository will be synced to the external OSCI mirrors without any further
verification. RPM and DEB mirrors are synced independently, list of synced
packages must be included as an artifact to an appropriate OSCI Jenkins job.

Auxiliary jobs
--------------
The following auxiliary jobs must be implemented as the part of this spec:

* Jobs to support debug sessions workflow
* Jobs to clean expired VM snapshots on Jenkins slaves

Alternatives
------------

None

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
  Andrey Nikitin <anikitin@mirantis.com>
  Dmitry Kaiharodtsev <dkaiharodsev@mirantis.com>

QA:
  <TBD>

Mandatory Design Reviewers:
  Roman Vyalov <rvyalov@mirantis.com>
  Aleksandra Fedorova <afedorova@mirantis.com>

Work Items
----------

* Implement OSCI Jenkins job for syncing of CentOS mirrors [1]_
* Implement OSCI Jenkins job for syncing of Ubuntu mirror [1]_
* Create OSCI Jenkins jobs for new package tests
* Setup new OSCI Jenkins slaves for package test jobs [2]_
* Switch package tests for MOS 7.0 to new jobs
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
