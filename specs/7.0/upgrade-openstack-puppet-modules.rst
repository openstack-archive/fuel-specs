..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================
Sync OpenStack puppet modules from upstream
==========================================

https://blueprints.launchpad.net/fuel/+spec/upgrade-openstack-puppet-modules

This blueprint is about how we are going to sync upstream OpenStack puppet
modules and their dependencies into fuel-library.

Problem description
===================

In order to achieve better stability in Fuel and benefit the community,
we need to merge our Puppet modules from upstream. This process involves
merging core OpenStack components first, then supporting components/HA
architecture second.

Proposed change
===============

Current versions of Fuel-library OpenStack and some base modules is very old
and these versions are not appropriate to deploy OpenStack Kilo release
and OpenStack from trunk. The best way to support deployment of current
OpenStack release is to have puppet modules synced to the latest stable
versions. The idea is to have current stable release of OpenStack puppet
modules and backport from upstream master the most important changes for
successful Fuel deployment.

Moving from outdated manifests to the newest stable versions has several
important advantages:

*   Latest releases of puppet modules support all OpenStack component
    functionality, including new options, features, configurations and
    deployment schemes.

*   Using latests puppet modules helps to save time for configuring
    OpenStack components. Those parts of configuration which are implemented
    and hardcoded now in intermediate 'openstack' class can be used and
    passed directly from modular class to corresponding module.

*   Latest version of puppet modules allows to make easier the process
    of backporting patches from upstream to Fuel-library.

*   Having small difference between upstream and fuel-library OpenStack
    modules lets make easier transitions between Fuel releases.


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

     - changes which are merged in upstream or outdated should be removed
     - changes which are not present in upstream should be merged
       as adaptation part. Also such changes if they are not Fuel specific
       could be send on review to upstream

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
  Modules which should be deleted:

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
