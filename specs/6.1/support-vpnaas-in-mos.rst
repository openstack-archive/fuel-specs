=============================================
Fuel plugin for VPNaaS Neutron feature in MOS
=============================================

https://blueprints.launchpad.net/fuel/+spec/support-vpnaas-in-mos

VPNaaS (VPN-as-a-Service) is a Neutron extension that introduces VPN feature
set.
VPNaaS provides multiple tunneling and security protocols with static routing.
For now this plugin uses OpenSwan, which is an opensource IPsec implementation
for Linux.

Problem description
===================

Today multi-cloud integration is a popular topic, because very
often we have more than one cloud and want to have some interaction
between tenants from the different clouds for some reason, like HA for
our services on the VMs. And of course the most popular use case to have a
VPN tunnel from your private network to the private network in your public
cloud.

Proposed change
===============

Implement a FUEL plugin which should deploy VPN service and configure VPNaaS
functionality in Neutron and Horizon.

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

* Implement FUEL plugin.
* Write Documentation.
* Testing.

Dependencies
============

* OpenSwan package.
* FUEL 6.0 and higher.

Testing
=======

* Prepare test plan.
* Test a deployment with activated plugin on all FUEL deployment modes.
* Test VPN connection with test VPN point.
* Integration tests with other OpenStack components and Neutron plugins.

Documentation Impact
====================

* Deployment Guide (how to prepare an env for installation, how to install
  the plugin, how to deploy OpenStack env with the plugin).
* User Guide (which features the plugin provides, how to use them in the
  deployed OS env).
* Test Plan.
* Test Report.

References
==========

* https://wiki.openstack.org/wiki/Neutron/VPNaaS
* https://wiki.openstack.org/wiki/Neutron/VPNaaS/HowToInstall
* http://docwiki.cisco.com/wiki/OpenStack:Havana:VPNaaS

