=========================================
Support FWaaS Neutron feature in MOS/FUEL
=========================================

https://blueprints.launchpad.net/fuel/+spec/support-fwaas-in-mos

Problem description
===================

Firewall as a service is a very popular and useful feature, which OpenStack
customers often use in prodcution. So we should have this functionality in
Mirantis OpenStack.

Proposed change
===============

Implement FUEL plugin which should configure FWaaS functionality in Neutron
and Horizon.

Alternatives
------------

It also might be implemented as a part of FUEL core, but we decided to make
it as a plugin for several reasons. First of all, in Kilo community
decided to separate VPNaaS and other aaS services into their own project(repo),
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

* Implement FUEL plugin
* Prepare simple test environment
* Prepare CI/CD with testing on test bed
* Write Documentation and User Guide

Dependencies
============

None

Testing
=======

* Test this plugin on all FUEL deployment modes
* Test FWaaS functionality as well:
  https://wiki.openstack.org/wiki/Quantum/FWaaS/Testing

Documentation Impact
====================

This feature should be documented. The planing guide will be updated.

References
==========

* https://wiki.openstack.org/wiki/Neutron/FWaaS
* https://wiki.openstack.org/wiki/Neutron/FWaaS/HowToInstall
* https://wiki.openstack.org/wiki/Quantum/FWaaS/Testing
