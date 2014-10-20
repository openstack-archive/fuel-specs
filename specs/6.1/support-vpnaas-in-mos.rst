=============================================
Fuel plugin for VPNaaS Neutron feature in MOS
=============================================

https://blueprints.launchpad.net/fuel/+spec/support-vpnaas-in-mos

Problem description
===================

Today multi-cloud integration is a popular topic, because very
often we have more than one cloud and want to have some interaction
between tenants from the different clouds for some reason, like HA for
our services on the VMs. And of course the most popular use case to have a
VPN tunnel from your private network to the private network in your public
cloud.
For this purpose in OpenStack Neutron was implemented VPNaaS, which we
need to support in MOS and Fuel.


Proposed change
===============

Implement a FUEL plugin which should deploy VPN service and configure VPNaaS
functionality in Neutron and Horizon.

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

* openswan package

Testing
=======

* Test deployment of this plugin on all FUEL deployment modes
* Test VPN connection with test VPN point

Documentation Impact
====================

This feature whould be documented. The planing guide will be updated.

References
==========

* https://wiki.openstack.org/wiki/Neutron/VPNaaS
* https://wiki.openstack.org/wiki/Neutron/VPNaaS/HowToInstall
* http://docwiki.cisco.com/wiki/OpenStack:Havana:VPNaaS

