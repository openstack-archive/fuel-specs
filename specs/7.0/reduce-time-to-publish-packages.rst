..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Reduce time to publish packages
===============================

https://blueprints.launchpad.net/fuel/+spec/reduce-time-to-publish-packages

Problem description
===================

* As a Package Maintainer, I want my package updates to be published to
  official package repositories immediately after my code changes are merged
  in git

#. At the moment, all changes to the MOS packages repositories are tested on
   a set of simple functional and integration tests so that they will not be
   merged into the stable package repository unless it passes all of the
   configured tests. Merged packages are then pushed to staging mirrors, then
   staging mirrors are validated using BVT system tests using most recent
   stable build of Fuel, then staging mirrors are published. Published mirrors
   are used to build yet another ISO image which is validated again via BVT
   system tests. Then the resulting mirror and ISO are passed to the swarm
   tests. This results in a long chain of processes maintained by different
   teams, and thus creates quite a long feedback loop.

#. Different test pipelines for different types of commits made to MOS
   repositories and StackForge repositories create inconsistency in test
   coverage between artifacts created from these sources.

#. Duplication of artifacts of the same type created in different test
   pipelines creates waste of computing capacity of CI infrastructure.

Proposed change
===============

We must complete all package validation (including system tests) before
package change patch set is merged, and then publish packages to the mirrors
immediately after review is merged.

Proposed flow for change requests to MOS packages code and/or spec is below:

* Change request is proposed for code review to Gerrit
* Change request parameters (repository name, branch, change ID) are passed
  to the Jenkins job that fetches sources and specs from Gerrit and pushes
  sources and specs to the build system in a respective format (SRPM for
  RPM packages, and unpacked sources for DEB packages)
* Package (or packages) is built from resulting sources and specs by the
  build system and placed into a test repository. Test repository location
  is created as a Jenkins job artifact
* Test repository is run through automated functional and integration tests
* Change request is peer-reviewed
* Change request is accepted or rejected by core team
* Change request is rebased and run through pre-merge automated checks
* Change request is merged or rejected
* Merge event from Gerrit is picked up by Jenkins job that places built
  packages to the internal repository and signes them (for RPM - a package
  itself, for DEB - repository metadata)
* Repository with rebuilt package is propagated to the external MOS mirrors
  by the means of Jenkins job that uses transactional syncronization

Test repository format
----------------------
Test repository with packages should be passed to the system tests as
parameter using the following conventions:

#. *RPM packages.* Plain RPM repository accessible by HTTP.
#. *DEB packages.* Single-component APT repository accessible by HTTP,
   with distribution name that equals to the current upstream OS codename.

Automated functional and integration tests
------------------------------------------
Each package built into a test repository will undergo the following tests:

#. *Basic syntax test* (rpmlint and lintian, for RPM and DEB packages,
   respectively)
#. *Basic package health test.* Uses plain VM with respective OS type that
   contains only the minimal set of packages. Package install, run basic
   shell script, and uninstall tests are performed.
#. *Full system test.* All packages are tested using the same
   scenarios that are used in current BVT tests on the Product CI. In
   order to keep the actual test run as short and reliable as
   possible, the VM snapshots for Fuel master node and cluster nodes
   are prepared ahead of time and kept on slave servers ready for
   immediate use. The process of preparing the VM snapshots ahead of
   time reduces the network traffic and influence of an external
   depencencies during the run.  The job that prepares the VM
   snapshots is executed on a daily basis or, alternatively, triggered
   on ISO update, depending on the frequency if ISO updates.

Depending on the package flavor, there are different artifacts that could be
supplied to the integration test job.

   #. RPM and DEB packages for clusters. Test repository is added to the
      Nailgun with highest priority (in terms of a respective package
      manager).

   #. Fuel Master host OS packages. Rebuilding of a Fuel ISO with an extra test
      repository and redeployment of Fuel Master node must precede the system
      test.

   #. Fuel bootstrap packages. Rebuilding of bootstrap package and
      installing it on the Fuel Master node created from snapshot prepared
      ahead precedes the system test.

   #. Fuel Docker container packages. Rebuilding of Fuel Docker containers
      late-package and installing it on the Fuel Master node created from
      snapshot prepared ahead precedes the system test.

All tests will be running in parallel. In case if basic package health test
for a given patch set is failed, the respective full system test must be
aborted to prevent the waste of a CI system resources.

Full logs for a system test run must be available in the Jenkins as a job
artifact. In order to support debugging of system test issues, snapshots of
VMs created during the test run are stored on Jenkins slaves for 20 days.

In order to support enhanced debug cases, there should be an ability to
replicate all the test parameters, including job artifacts, on a
Custom CI.

After merge event in Gerrit, package built on a gate will be pushed to a
respective stable repository on an internal OSCI mirror and signed in
terms of a respective package manager. Right after that, this
resulting repository will be synced to the external OSCI mirrors
without any further verification. RPM and DEB mirrors are synced
independently, list of synced packages must be included as an artifact
to an appropriate Jenkins job.

Testing of concurrent requests
------------------------------
To ensure that no regressions are introduced by merging of concurrent
requests, on merge event, every outstanding request must be speculatively
retested against the tip of the package code and specs branches exactly
as it is going to be merged.

To optimize handling of merge queue we are going to use Zuul as a
gating tool. [3]_

Auxiliary jobs
--------------
The following auxiliary jobs must be supported on the Jenkins as the
part of this spec:

* Job to prepare environment for system tests on the Jenkins slave servers
* Jobs to support debug sessions workflow
* Job to clean expired VM snapshots on Jenkins slaves

Alternatives
------------

As an alternative to Zuul we considered managing pre-merge checks via
set of custom scripts, but it appears that we need a lot of Zuul
functionality and in long-term we will benefit from reusing the
existent tooling, which is supported by wide community including
OpenStack Infra team.

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
A speed of publishing of packages decreased from hours to minutes, should
compensate this inconvenience, though.

Infrastructure impact
---------------------

* Changes in system tests will require additional servers to be used as
  Jenkins slaves.

* Logs of a system tests will be stored on the Jenkins Master, therefore
  we will need to increase the storage capacity for this server (at least 1 TB
  is required). Alternatively, this requirement could be addressed by the
  centralized diagnostic snapshot storage feature.

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

* Setup new Jenkins instance for packaging and tests
* Setup Zuul and Gearman instance and attach it to Jenkins
* Setup new Jenkins slaves for system test jobs [2]_
* Implement Jenkins job for transactional syncing of mirrors [1]_
* Implement Jenkins job that retriggers CI for outstanding requests on
  merge of a concurrent request
* Adapt system test Jenkins job to support different types of artifacts
* Switch packaging and tests for MOS 7.0 to new Jenkins
* Eliminate the staging mirrors phase on the MOS 7.0 Product CI
* Replace all packages sources of MOS 7.0 components in Gerrit with fully
  unpacked source code (get rid of orig.tar.gz etc)

Dependencies
============

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
.. [3] `Zuul -- Project Gating <http://docs.openstack.org/infra/zuul/gating.html>`_
