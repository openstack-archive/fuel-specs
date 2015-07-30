..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Automation of prepare CI for product new release
================================================

.. https://blueprints.launchpad.net/fuel/+spec/<BLUE_PRINT_NAME>

Problem description
===================

On starting of work on every new release of product we need to recreate CI for
it and make some preparations. All of these specified on Devops release
checklist, that specified for each product release
(`6.1 <https://mirantis.jira.com/wiki/display/PRD/6.1+-+DevOps+release+checklist>`_,
`7.0 <https://mirantis.jira.com/wiki/display/PRD/7.0+-+DevOps+release+checklist>`_).

Currently most of operations are manual and as consequence:

* all scope of operations take a long time

* all the operations has some barriers of entry

* all manual operations are subject of the human-mastakes risk

As a Build Engineer, I want to reduce manual work on preparing CI for new
product release.

Current workflow description:

1. Get ready for HCF:

  #. Create jobs that clones all the needed packages from 7.0 repositories
     to newely created 8.0 repositories

  #. Create branches on projects for **8.0**;

2. On HCF

  #. Freeze 7.0 mirrors (disable automatic updates for 7.0 root symlink);

3. Just after HCF

  #. Create branch **stable/7.0** in repositories with OSCI scripts;

  #. Switch OSCI Jenkins jobs to branch **stable/7.0**;

  #. Switch to **stable/7.0** branch of fuel-qa in OSCI package testing jobs;

  #. Create **8.0** jobs at OSCI Jenkins.

Proposed change
===============

The idea is to automate all the operations, when it possible, and control them
via Jenkins, because Jenkins provide possibility of easy reproduction and
control by tasks. As a consequence it will be easy-reproducible,
easily-controlled, automated (as possible), fault tolerant process.

Following parts (by the items above) should be automated:

- **1.1.** Prepare Jenkins job, that creates change request to
  *fuel-infra/jenkins-jobs*, that propose jobs thats copyes
  existent packages (7.0) to repository for new release (8.0)

  Q: how to specify list of packages to copy?

  After that proposed change request should be reviewed and merged manually
  and folowing jobs should be updated via JJB.

- **1.2.** Prepare Jenkins Job, that creates branches on projects.

  List of repositories to create branches specified on the LP bug (like
  `this <https://bugs.launchpad.net/fuel/+bug/1450095>`_).

  Branches should be created according the list:

  - **8.0** for *packages/**
  - **openstack-ci/fuel-8.0/2015.2.0** for *openstack/**
  - **openstack-ci/fuel-8.0/2015.2.0** for *openstack-build/**


- **2.1.** Prepare Jenkins job that creates change request to
  *fuel-infra/jenkins-jobs*, that propose patch

  ::

    is-updates: true

  to **servers/openstack-ci/7.0/projects.yaml**

  After that proposed change request should be reviewed and merged manually
  and folowing jobs should be updated via JJB.

- **3.1.** Prepare Jenkins Job, that creates branches **stable/7.0** in
  repositories with OSCI scripts:

  - obs/perestroyka
  - ci-test-request
  - ci-status-client

- **3.2.** Prepare Jenkins job that creates change request to
  *fuel-infra/jenkins-jobs*, that propose to switch OSCI Jenkins jobs to
  branch **stable/7.0**.

  Skip *maintain* jobs at the **servers/openstack-ci/7.0/projects.yaml**

  After that proposed change request should be reviewed and merged manually
  and folowing jobs should be updated via JJB.

- **3.3.** Prepare Jenkins job that creates change request to
  *fuel-infra/jenkins-jobs*, that propose to switch to **stable/7.0** branch
  of fuel-qa scm in OSCI package testing jobs
  *servers/openstack-ci/7.0/macros.yaml*

  After that proposed change request should be reviewed and merged manually
  and folowing jobs should be updated via JJB.

- Create 8.0 jobs at OSCI Jenkins
- **3.4.** Prepare Jenkins job, that creates change request to
  *fuel-infra/jenkins-jobs*, that propose all new release jobs
  (8.0) at OSCI Jenkins using existent jobs (7.0) as a templates

  Copy all the jobs from **servers/openstack-ci/7.0/** to
  **servers/openstack-ci/8.0/** excluding *maintain* jobs.

  After that proposed change request should be reviewed and merged manually
  and folowing jobs should be updated via JJB.

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

None

Infrastructure impact
---------------------

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Maksim Rasskazov <mrasskazov@mirantis.com>

QA:
  <TBD>

Mandatory Design Reviewers:
  Roman Vyalov <rvyalov@mirantis.com>,
  Dmitrii Burmistrov <dburmistrov@mirantis.com>,
  Aleksandra Fedorova <afedorova@mirantis.com>

Work Items
----------

* Implement Jenkins job that creates new job based on specified template
* Implement Jenkins job that creates specified branches on specified projects
* Implement Jenkins multijob that implements complete pipeline

Dependencies
============

Testing
=======

Acceptance Criteria:

* Usage should be clean
* All the jobs should be implemented via JJB
* All the operations should be idempotent
* All the logs should be detail as possible and clean to read

Documentation Impact
====================

None

References
==========
