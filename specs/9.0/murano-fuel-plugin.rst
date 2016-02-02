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
upgrade script.

For Fuel 9.0 Murano plugin should support Murano Mitaka deployment with
Glance Artifact repository and Cloud Foundry Service Broker API features.

Web UI
======

Murano and all its features will be moved from standart Fuel Web UI to
plugin UI settings.

Nailgun
=======

All code related to Murano will be removed from Fuel Nailgun.

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

Fuel won't install Murano, so all modular tasks for murano will moved
to plugin codebase.

------------
Alternatives
------------

As alternative, can be used manual configuration of Murano services, by using
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

Since Murano will be a plugin, user will need to install/activate Murano plugin in
Fuel. Without these steps Murano will be unavailable.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

After removing Murano from Fuel installation from box, it will be available only
via plugin, as a result we need to support this plugin according to current version
of Fuel. It means, that we need to keep Murano plugin in actual state with current
Fuel Astute tasks, UI related changes.

On a deployment process side there are no any actual important changes - all
current Murano's features, which already exist in Fuel, will be kept.

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

This feature requires additional CI tests for plugin repository. These CI jobs
should deploy simple Fuel environment with Murano plugin installed on each
commit to Murano plugin repository.

--------------------
Documentation impact
--------------------

It should be noted that Fuel won't be able to deploy Murano from the box
anymore. Murano can be used with Fuel only as plugin.


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

* Murano network and node role in Fuel: Murano network role won't be provided
  by Fuel, so it should be implemented in plugin. Also it should be possible
  to deploy standalone Murano and Murano on controller nodes. This requires to
  have specific Murano node role in plugin.

* Plugin Web UI: the same option from current Fuel Web UI will be moved to
  plugin Web UI.

* Upgrade script for plugin: this script should be able to update Murano plugin
  to newer version. Also it should be possible to upgrade Murano from plugin
  in Fuel 8.0 environment which is going to be upgraded to 9.0.

* Murano OSTF tests: they should be removed from OSTF container as well
  as Murano is removed from Fuel codebase.

* Murano tests in SWARM: all current tests should be rewritten to support
  Murano installation from plugin. Additional tests should be added to
  check current and new features from Murano Mitaka.

* CI tests for plugin repository: it should be possible to test each commit
  to Murano plugin repository. Simple Murano deployment test will be enough.

Dependencies
============

------------
Testing, QA
------------

* Current Murano tests in SWARM should be rewritten to support
  Murano deployment from plugin.

* Additional tests should be added to SWARM to cover Murano features
  like CFapi, GLARE.

* CI jobs should be implemented to tests each commit for Murano plugin
  repository. These jobs should check Murano deployment and base functionaly.

Acceptance criteria
===================

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
