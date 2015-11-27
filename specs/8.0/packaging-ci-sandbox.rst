..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================
Packaging CI sandbox
====================

https://blueprints.launchpad.net/fuel/+spec/packaging-ci-sandbox

Packaging CI is our most complicated CI system. We need to have solution
which allow us to test changes before we will implement it on main systems.

--------------------
Problem description
--------------------

Packaging CI uses many different systems and services:

* puppet master - used to deploy rest of the systems
* gerrit server - git server and source of code for tests, it is also used as
  a source of events for zuul
* zuul server - gating system, it decide what is executed on CI
* jenkins master - used to manage job execution on slave servers
* slave for package building - used to build packages
* slave for publisher - used to sign and publish packages on repository
* slave for repository - package repository
* slave for install test - used to test packages installation
* slave for deployment test - used to test openstack deployment

We need a solution which allow us to work with changes in any part of those
systems. We need to have possibility to:

* make changes in puppet manifests/hiera and check what will happened after
  system update or full redeploy
* allow to make changes in jenkins jobs and test it
* allow to make changes in zuul configuration and test gating process
* allow to add new repositories, jenkins jobs, change workflow and test it

We also need a documentation for packaging CI which will help with
understanding test processes.

Actual version of packaging CI sandbox was installed manually and need to be
recreated in reproducible way.

----------------
Proposed changes
----------------

Create documentation on https://docs.fuel-infra.org with descriptions of steps
required for sandbox installation. It should contains:

* list of systems used in packaging CI and their requirements
* list of repositories used by systems with descriptions, at least:

  * `fuel-infra/jenkins-jobs
    <https://github.com/fuel-infra/jenkins-jobs>`_ - source of jenkins jobs
  * `fuel-infra/puppet-manifests
    <https://github.com/fuel-infra/puppet-manifests>`_ - source of manifests
  * `infra/ci-test-request
    <ssh://review.fuel-infra.org:29418/infra/ci-test-request>`_ - scripts used
    for install tests
  * `fuel-infra/zuul-layouts
    <ssh://review.fuel-infra.org:29418/fuel-infra/zuul-layouts>`_ - scripts
    used to build zuul configuration
  * `openstack/fuel-mirror
    <https://github.com/openstack/fuel-mirror/tree/master/perestroika>`_ -
    perestroika scripts

* procedure for puppet master installation
* gerrit installation with configuration which allow to clone other
  repositories
* jenkins master installation
* jenkins slaves installation
* zuul installation
* description with configuration steps required to connect all services into
  one system
* description with steps required for clone existed packaging CI with other
  users, keys, domain names, etc, all on separate environments which could
  be easily changed without worry about original environment
* description for test workflows, it should explain all main steps of test

Created systems and documentations should allow to build fully functional CI
sandbox as a part of existed infrastructure. It should also allow to create
standalone version of sandbox builded from scratch. This approach allow to:

* reuse existed infrastructure, in many cases we don't need to create
  dedicated systems
* build fully functional packaging CI from scratch
* full verification for all CI elements, we can check recovery procedures

Create changes in jenkins-jobs repository with scripts used for building
standalone test CI from scratch and scripts used for CI clone. System
assumptions:

* reuse scripts from mos-infra/lab
* create CI systems as a local LXC containers or KVM machines
* allow to full redeploy CI systems with our local changes

Web UI
======

None

Nailgun
=======

None

Data model
----------

None

REST API
--------

None

Orchestration
=============

None

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

None

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

TODO

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

Infra developers will be able to test changes in packaging flow before merge.

---------------------
Infrastructure impact
---------------------

Existed systems which will be used in sandbox:

* test gerrit server (review-tst01.vm.mirantis.net) - devops system
* test zuul server (zuul02-sandbox.infra.mirantis.net) - will be redeployed
* test jenkins master (osci-buildtest.infra.mirantis.net) - will be redeployed
* test slave for publisher/repository (publisher01-tst.infra.mirantis.net) -
  will be redeployed
* test slave for package build (perestroika-slave04.infra.mirantis.net) - will
  be redeployed

New systems:

* test puppet master (1G RAM, 1-2CPU, 20-40GB HDD) - VM with acceess for
  CI team
* test slave for install/deployment test (32G RAM, 8 CPU, 1TB HDD) - optional
  hardware server, if possible actual slave for package build will extended to
  use also for this role

--------------------
Documentation impact
--------------------

There will be update for https://docs.fuel-infra.org with description of
installation process for packaging CI.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  akaszuba

Other contributors:
  None

Mandatory design review:
  afedorova


Work Items
==========

* Collect informations about existed systems
* Create test environment with all services and create draft description with
  requirements and steps needed to install it
* Reproduce CI processes, jobs, workflows in test environment (it is a way to
  collect all required dependencies, configurations etc), create documentation
  draft with description for this processes
* Create PoC system and show demo how to install own sandbox
* Collect all feedback and update documentation to final version
* Create new packaging CI sandbox as a part of existed systems

Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/fuel-ci-basic-installation

------------
Testing, QA
------------

None

Acceptance criteria
===================

* There is a documentation with all required steps needed to install CI sandbox
  as a part of existed infrastructure and as a new standalone solution
* There are a scripts used for installation of sandbox standalone version

----------
References
----------

Git repositories used by packaging CI:

* https://github.com/fuel-infra/jenkins-jobs
* https://github.com/fuel-infra/puppet-manifests
* ssh://review.fuel-infra.org:29418/infra/ci-test-request
* ssh://review.fuel-infra.org:29418/fuel-infra/zuul-layouts
* https://github.com/openstack/fuel-mirror/tree/master/perestroika
