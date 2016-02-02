..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================
Murano as Fuel plugin
=====================

https://blueprints.launchpad.net/fuel/+spec/murano-fuel-plugin

--------------------
Problem description
--------------------

Now Murano is aligned with Fuel releases, and if user wants to get new
Murano features for its OpenStack environment deployed by Fuel user should
wait for new Fuel release, then upgrade whole cluster (all OpenStack
components). Main problem here that Fuel releases only every six month.

----------------
Proposed changes
----------------

Murano Fuel plugin can solve problem with getting new Murano features for
OpenStack environment deployed by Fuel. Murano as plugin for Fuel can be
continiously delivered and updated. Plugin will include Murano service packages
and upstream puppet-murano module for deployment, so support of new features
will come very fast.

User doesn't need to upgrade or reinstall whole Fuel cluster, he should
get only new Murano service packages and deployment manifests and run
upgrade script. This script will include backing up Murano database,
updating puppets for Murano and will be runned by Octane tool.

For Fuel 9.0 Murano as a plugin should support Murano Mitaka with identity
API v3 version for Murano services. Also there are two Murano features in
upstream: Glance Artifact repository and Cloud Foundry Service Broker API
features. These two feature can't work simultaneously. Hence will be added
possibility to choose only one of them.

Transition from Fuel default box to Fuel plugin deployment should follow next
way:

* We deprecate Murano deployment in Fuel 9.0, we leave an ability to deploy it
  keeping puppet manifests for Murano in fuel-library, keeping UI settings
  untill plugin will be prepared and tested;

* Fuel 9.0 should support same Murano deployment as it was supported in
  Fuel 8.0 without any new features;

* It will not be possible to install Murano plugin with Murano enabled from
  the box.

* All Murano codebase will be removed in Fuel 10.0 release.

Implementation of these transition steps means successfull transfer to Murano
plugin deployment.

Web UI
======

Murano will be deprecated on the Web UI: we will add deprecation message for
Murano and helper text, pointing to the plugin for at least one cycle.

Nailgun
=======

Nailgun tests for Murano will be removed, config in openstack.yaml fixture
will be kept. Whole Nailgun stuff will be removed in Fuel 10.0 release.

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

All related Murano manifests in fuel-library will be kept in Fuel 9.0, but
will be removed in Fuel 10.0 release.

------------
Alternatives
------------

As alternative, manual configuration of Murano services can be used, by using
Debian/UCA/RDO packages and upstream puppet manifests. But it this way
requires expertise in Murano configuration and puppet knowledge.

--------------
Upgrade impact
--------------

It should be possible to upgrade Fuel 8.0 environment with Murano to
Fuel 9.0 environment using Murano plugin manifests and service packages.

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

We will show warning on the Fuel Web UI that Murano deployment from box
is deprecated and it is recommended to use Fuel Murano plugin.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

When Fuel Murano deployment will be deprecated, Murano will be available
via plugin and from box for Fuel 9.0. All Murano related stuff will be removed
in Fuel 10.0 release.

On a deployment process side there are no any actual important changes - all
current Murano's features, which already exist in Fuel, will be kept. Murano
deployment from box will not support any new features.

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

This feature requires additional CI tests for plugin repository. These CI
jobs should deploy simple Fuel environment with Murano plugin installed on
each commit to Murano plugin repository.

--------------------
Documentation impact
--------------------

Murano can be used as built in Fuel and as plugin. It will be impossible
to deploy Murano as plugin in the same time with Murano from box.
It should be noted: Murano deployment as built in Fuel is deprecated.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Denis Egorenko

Other contributors:
  Ivan Berezovskiy
  Victor Ryzhenkin

Mandatory design review:
  Sergii Golovatiuk
  Serg Melikyan

QA engineer:
  Victor Ryzhenkin

Work Items
==========

* Murano service packages: murano, murano-dashboard, python-muranoclient and
  other Murano dependencies which are unique for it.

* Murano puppet module and modular tasks: upstream puppet-murano module
  should be used as a base for Murano deployment. In orchestration level we
  should have similar modular task as we have right now in Fuel.

* Murano network and node role in Fuel: Fuel Murano network role will be
  overridden by plugin. Also it should be possible to deploy standalone
  Murano and Murano on controller nodes. This requires to have specific
  Murano node role in plugin.

* Plugin Web UI: the same option from current Fuel Web UI will be moved to
  plugin Web UI.

* Upgrade script for plugin: this script should be able to update Murano
  plugin to newer version. Also it should be possible to upgrade Murano from
  Fuel 8.0 environment which is going to be upgraded to 9.0 with Murano
  from plugin.

* Murano OSTF tests: they should be removed from OSTF container as well
  as Murano is forbidden in Fuel base deployment.

* Murano tests in CI: these tests should verify base Murano plugin
  deployment on Fuel 9.0 and should run on every commit to Murano plugin
  repository.

Dependencies
============

------------
Testing, QA
------------

* Additional Murano tests for CI should be implemented to support
  Murano deployment from plugin.

* CI jobs should be implemented to tests each commit for Murano plugin
  repository. These jobs should check Murano deployment and base functionaly.

Acceptance criteria
===================

Murano should be deprecated in base Fuel installation.

Murano plugin should include following components for deployment:

* Web UI with ability to use all current Murano features.

* Plugin uses upstream murano-puppet module as base for deployment.

* Puppet manifests in plugin are idempotent.

* Plugin includes Murano service packages and its dependencies which are
  unique for Murano.

* End users are able to deploy Murano and its features:
  CFapi and GLARE at least.

----------
References
----------

1. LP Blueprint https://blueprints.launchpad.net/fuel/+spec/murano-fuel-plugin
