..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================
3rd-party CI with MOS Integration tests
========================================

https://blueprints.launchpad.net/fuel/+spec/third-party-openstack-integration-ci

--------------------
Problem description
--------------------

We need to execute full integration test suite for OpenStack components
after the deployments with Fuel. This suite containts different test suites:

 * Tempest

 * Rally

 * 3rd-party SWARM-based test scenarios

We need to create separate repository for 3rd-party SWARM-based test
scenarios, repository for jenkins job templates and configure CI
for these tests.

We can't run all these tests in SWARM tests suite for many reasons:

 * Fuel SWARM tests has different mission. Fuel-qa repository already
   contains deployment tests for Fuel and doesn't contain separate tests
   for OpenStack verification. The goal of existing SWARM tests is to
   perform integration testing of Fuel components.

 * MOS QA engineers don't have core reviewer access in fuel-qa repository,
   but only MOS QA team is reponsible for OpenStack integration test suite
   and we need to have the full access to be able to change everithing which
   we need to change / fix / enable or disable.

 * Execution of OpenStack integration tests require to download code of
   different OpenStack componens from github and sometimes we need to use
   custom versions on fuel-qa and fuel-devops coponents in our jobs.
   We want to avoid such changes in fuel-qa repository.

----------------
Proposed changes
----------------

* Create github repository where we will be able to store 3rd-party
  automated integration test cases

* Create github repository where we will be able to store jenkins jobs
  templates for new CI

* Grand the core reviwer access to the following engineers:

    * tnurlygayanov
    * akuznetsova
    * kkuznetsova
    * vrovachev
    * vryzenkin
    * aurlapova
    * tleontovich
    * afedorova

* Configure Jenkins CI server to run new jobs

Web UI
======
None

Nailgun
=======

Data model
----------
None


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
None


------------
Alternatives
------------

We can create non-public github repository with automated tests
and setur separate CI server which will be under full controll of MOS QA team.
The impact of this alternative solution is than QA team should allocate
additional resources for infrastructure maintenance and configuration
and internal processes in thse repositories will be not clear and open for
everyone in OpenStack comunity.

--------------
Upgrade impact
--------------
None

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
None

------------------
Performance impact
------------------
None

-----------------
Deployment impact
-----------------
None

----------------
Developer impact
----------------
We will run all our integration test suites on daily and per-commit basis,
the feedback on the builds status will speedup and QA team will find and
describe deffects faster.

Per-commit jobs will allow to find critical isssues before the merge of
new code to stable branches. Developers will be able to find the detailed
logs of OpenStack integration tests for each commit and will be able to
identify the root of the issues.


---------------------
Infrastructure impact
---------------------
 * It will require to create two github repositories and setup new CI service.

 * It will require to take care about the infrastructure issues, user access,
   servers and network management.

 * It will require to help QA engineers with any inrastructure issues and
   questions.

--------------------
Documentation impact
--------------------
None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  tnurlygayanov, afedorova, dborodaenko

Other contributors:
  gduldin, kkuznetsova, akuznetsova, vryzhenkin, agalkin, vrovachev

Mandatory design review:
  tnurlygayanov


Work Items
==========

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============
None

------------
Testing, QA
------------
None

Acceptance criteria
===================
* Repository for jenkins jobs templates created and the following engineers
  have core reviewer access to this repository:

  * tnurlygayanov
  * akuznetsova
  * kkuznetsova
  * vrovachev
  * vryzenkin
  * aurlapova
  * tleontovich
  * afedorova

* Repository for 3rd-party integration tests created and the following
  engineers have core reviewer access to this repository:

  * tnurlygayanov
  * akuznetsova
  * kkuznetsova
  * vrovachev
  * vryzenkin
  * aurlapova
  * tleontovich
  * afedorova

* Separate Jenkins service is available and configured to use jenkins job
  builder templates

* Syntax checks configured for repository with 3rd-party integration tests

----------
References
----------
None
