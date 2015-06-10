..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================
Sync OpenStack puppet modules from upstream
===========================================

https://blueprints.launchpad.net/fuel/+spec/upgrade-openstack-puppet-modules

This blueprint is about how we are going to sync upstream OpenStack puppet
modules and their dependencies into fuel-library.

Problem description
===================

Current versions of Fuel-library OpenStack and some base modules is Juno-based
and these versions are not appropriate to deploy OpenStack Kilo release
and OpenStack from trunk. Our puppet code has increasing code divergence with
upstream. To better support of current OpenStack release we should keep our
puppets synced this upstream. Also there are a lot of local to Fuel fixes
for issues in puppet modules which should be contributed to upstream.


Proposed change
===============

In order to achieve better stability in Fuel and benefit the community,
we need to merge our Puppet modules from upstream. This process involves
merging core OpenStack components and their dependencies first, then
updating Fuel specific components/HA architecture second according
to changes in first step.

One of the ways to support deployment of current
OpenStack release is to have puppet modules synced to the latest stable
versions. The idea is to have current stable release of OpenStack puppet
modules and then work with upstream master to minimize difference.
This requires contribution of Fuel specific changes to upstream.
Final goal is to use and support upstream modules for Fuel deployment.

Moving from outdated manifests to the newest stable versions has several
important advantages:

*   Latest releases of puppet modules support all OpenStack component
    functionality, including new options, features, configurations and
    deployment schemes.

*   Using latests puppet modules decreases the code diverge between
    upstream sources and forked modules and partially addresses
    the technical dept accumulated from the latest sync iteration
    based on the versions 4.1.x mostly.

*   Having small difference between upstream and fuel-library OpenStack
    modules lets make easier transitions between Fuel releases.

*   Fuel specific changes is going to be revised and that makes easier
    the process of contributing them to upstream.


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

Other deployer impact
---------------------

Deployers will get full functionality of latest stable puppet module.
This will allow to use features and options implemented in upstream
for current OpenStack release without objectionable workarounds
in modular classes.

Developer impact
----------------

None

Implementation
==============

Implementation is going to be fairly simple. We are going to use latest
stable version (tag) of each module. For OpenStack modules we are focused
on version 5.0.0.

Each module will be tested according to the following testing flow:

* Testing node should have puppet-3.4 installed

* Run base noop tests for module

* Replace old module in fuel-library and run fuel-library noop tests

* Adapt usage of new puppet module in fuel-library. This will require
  updates in modular puppet scripts and in 'openstack' module.

* Rake rspec testing

* Test real deployment

Then this module should be sent on review according following workflow:

1. First patch contains only module sync changes. Fuel CI will be disabled
   for such patches.

2. Next patch is adaptation of this module to the fuel deployment scheme:
   this patch should contain changes in module like:

   * cherry-pick of some commits from master branch of module

   * some custom updates in module

   * fixes for issues in 'modular' and 'openstack' classes

   * custom changes which were merged after previous sync as adaptation
     should be processed using following workflow:

     - changes which are merged in upstream or outdated should be revised
     - changes which are not present in upstream should be merged
       as adaptation part. Also such changes if they are not Fuel specific
       should be send on review to upstream

Workflow for new OpenStack modules (e.g. openstacklib):

   * Create two fuel-infra repositories for these new puppet modules:
     - repository 'module_name' will contain source code of puppet module
       with branches according to Fuel releases, for example:
       '7.0' branch for Fuel 7.0.
       Code for this branches should be synced according to the flow:
          1. Master branch will be synced automatically.
          2. Another branches will be synced manually from appropriate tag
             for current Fuel release:
                e.g. openstacklib: branch 7.0 - tag 5.0.0
     - repository 'module_name-build' will contain spec files for building
       deb and rpm packages for this module. The same branching strategy:
       '7.0' branch is for Fuel 7.0.
   * These packages should be included in common mirrors for packages
     and should be present in each ISO
   * Create deployment task for installing these packages. This task should
     run right after fuel-pkgs task.

Pros:
   * These modules will be kept up to date with every Fuel release
   * Issues in such modules should be fixed in upstream. It's good point
     for contribution


Every task for module preparation will be tracked in Trello board:
https://trello.com/b/epRiNHz6/mos-puppets

Assignee(s)
-----------

Primary assignee:
  Ivan Berezovskiy

Other contributors:
  Alexey Deryugin
  Bartłomiej Piotrowski
  Denis Egorenko
  Maxim Yatsenko
  Sergey Kolekonov
  Sergii Golovatiuk
  Vasyl Saienko

Reviewers:
  Aleksandr Didenko
  Bogdan Dobrelya
  Dmitry Ilyin
  Sergey Vasilenko
  Sergii Golovatiuk
  Vladimir Kuklin

QA:
  Fuel QA Team

Work Items
----------

Trello board for the feature is here:
https://trello.com/b/epRiNHz6/mos-puppets

Implementation plan
-------------------

Step #1:
  Upgrade base puppet modules:

  * stdlib
  * ssh
  * concat
  * mysql
  * xinetd

Step #2:
  Modules which should be removed:

  * puppetmaster
  * qpid

Step #3:
  Add new modules:

  * galera
  * opesntacklib

Step #4:
  Upgrade OpenStack modules:

  * keystone
  * nova
  * neutron
  * glance
  * heat
  * ceilometer
  * cinder
  * swift
  * sahara
  * mongodb
  * murano
  * horizon

Step #5:
  Merge following modules into 'cluster' module:

  * ceilometer_ha
  * heat_ha

Step #6:
  Integrate 'ironic' module:

  * blueprint: https://blueprints.launchpad.net/fuel/+spec/fuel-integrate-ironic

Dependencies
============

None

Testing
=======

Feature is considered completed as soon as there is no deployment tests
failing. This feature should be mostly considered as task for puppet modules
upgrade, thus not affecting functionality of the deployed cloud at all.

Documentation Impact
====================

Process of development is not going to be drastically changed.
Documentation should have notes that puppet modules was updated accorting
to the latest appropriate version for Openstack Kilo release.

References
==========

1. Blueprint https://blueprints.launchpad.net/fuel/+spec/upgrade-openstack-puppet-modules
2. Trello board https://trello.com/b/epRiNHz6/mos-puppets
3. Etherpad https://etherpad.openstack.org/p/fuel_puppet_modules_upgrade
