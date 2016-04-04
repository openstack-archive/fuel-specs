..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Community CI for openstack/rpm-packaigng
==========================================

Since Mirantis started its participate in the upstream packaging activities we
need to be able to test work made as by community as by our engineers.


--------------------
Problem description
--------------------

To be sure that RPM specs are correct and it is possible to build  RPM package
using this specs we need to build and test RPM package(s) for each pathset to
project openstack/rpm-packaging.


----------------
Proposed changes
----------------

For each pathset Zuul prepares parameters and triggers a job building and
testing package(s).

Job steps:

#. Get projects/tools required to build packages:

    * Get source code for current pathset using parameters GERRIT_PROJECT and
      GERRIT_REFSPEC (mapped by Zuul from its own parameters) containing info
      about current patchset
    * Get current source code of package builder:
      https://github.com/dburm/docker-builder
    * Get script and configuration for overriding default build parameters:
      https://review.fuel-infra.org/packaging/openstack-rpm-ci

#. Get from Git list of changed files in current commit/patchset
#. Prepare build environment:

    * Setup and activate Python virtualenv
    * Install to virtualenv tool *pymod2pkg*
    * Install to virtualenv requirements for projects/tools from first step

#. For each changed file:

    * If changed file is Jinja2 template (.spec.j2), then render RPM spec file
      using renderspec (installed on previous step as requirement of project
      openstack/rpm-packaging) and pymod2pkg
    * Prepare package building parameters using overrides if any
    * Copy exising in project tree source files
    * Download non-existing files assuming that source tag contains URL
    * Get tests contents if needed
    * Build package(s)
    * Create artifact to be used by publisher and tests

#. For each build artifact trigger publishing job
#. For each build artifact trigger install-test job


------------
Alternatives
------------

Instead of Zuul we can use Gerrit trigger plugin for Jenkins.


----------------
Developer impact
----------------

Zuul will post report for each pathset containing status and URL of the job,
and developers can see build logs and artifacts using during package
building/publishing/testing. Built packages will be placed at
`http://packages.fuel-infra.org/review/RPM-<CR_NUM>/`


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
 `Aleksander Evseev <https://launchpad.net/~aevseev-h>`_


Work Items
==========

* Prepare script and configuration for overriding package building parameters
* Prepare Jenkins jobs
* Prepare Zuul layout


Dependencies
============

* Overrides for package building parameters:
  https://review.fuel-infra.org/packaging/openstack-rpm-ci
* Docker-builder: https://github.com/dburm/docker-builder
* *Perestroika*:
  https://github.com/openstack/fuel-mirror/tree/master/perestroika
* Mirantis packaging specs (for install-test):
  `https://review.fuel-infra.org/p/openstack-build/<package>-build`
* *pymod2pkg*: https://github.com/openstack/pymod2pkg
* *renderspec*: https://github.com/openstack/renderspec


Acceptance criteria
===================

* CI reacts on commits to rpm-packaging and launch jobs/tests
* Results of jobs are published and accessible publicly
