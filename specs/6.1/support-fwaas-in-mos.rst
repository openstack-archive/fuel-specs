=========================================
Support FWaaS Neutron feature in MOS/FUEL
=========================================

https://blueprints.launchpad.net/fuel/+spec/support-fwaas-in-mos

Problem description
===================

Firewall as a service is a very popular and useful feature, which OpenStack
customers often use in prodcution. So we have to have this functionality in
Mirantis OpenStack.

Proposed change
===============

Implement FUEL plugin which should configure FWaaS functionality in Neutron
and Horizon.

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

This feature whould be documented. The planing guide will be updated.

References
==========

* https://wiki.openstack.org/wiki/Neutron/FWaaS
* https://wiki.openstack.org/wiki/Neutron/FWaaS/HowToInstall
* https://wiki.openstack.org/wiki/Quantum/FWaaS/Testing
