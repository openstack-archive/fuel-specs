=========================================
Support FWaaS Neutron feature in MOS/FUEL
=========================================

https://blueprints.launchpad.net/fuel/+spec/support-fwaas-in-mos

FWaaS (FireWall-as-a-Service) is Neutron extension that introduces firewall
feature set.
Neutron FwaaS  provides a cloud-centric abstractions for a security feature
set spanning traditional L2/3 firewalls to richer application-aware
next-generation firewalls.
This plugin uses IPTables driver.

Problem description
===================

Firewall as a service is a very popular and useful feature, which OpenStack
customers often use in production. So we should have this functionality in
Mirantis OpenStack.

Proposed change
===============

Implement FUEL plugin which should configure FWaaS functionality in Neutron
and Horizon.

Alternatives
------------

It also might be implemented as a part of FUEL core, but we decided to make
it as a plugin for several reasons. First of all, in Kilo community
decided to separate FWaaS and other aaS services into their own project(repo),
so we would do it the same way. Another reason is that any new additional
functionality makes a project and test it more difficult, which is an
additional risk for the FUEL release.

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

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:

Feature Lead: Andrey Epifanov
Mandatory Design Reviewers: Stanislaw Bogatkin, Sergey Kolekonov,
Sergey Vasilenko
Developers: Andrey Epifanov
QA: Timur Nurlygayanov

Work Items
----------

* Implement FUEL plugin.
* Write documentation.
* Testing.

Dependencies
============

* FUEL 6.0 and higher

Testing
=======

* Prepare test plan.
* Test a deployment with activated plugin on all FUEL deployment modes.
* Test FWaaS functionality as well:
  https://wiki.openstack.org/wiki/Quantum/FWaaS/Testing
* Integration tests with other OpenStack components and Neutron plugins.

Documentation Impact
====================

* Deployment Guide (how to prepare an env for installation, how to install
  the plugin, how to deploy OpenStack env with the plugin)
* User Guide (which features the plugin provides, how to use them in the
  deployed OS env)
* Test Plan
* Test Report

References
==========

* https://wiki.openstack.org/wiki/Neutron/FWaaS
* https://wiki.openstack.org/wiki/Neutron/FWaaS/HowToInstall
* https://wiki.openstack.org/wiki/Quantum/FWaaS/Testing
