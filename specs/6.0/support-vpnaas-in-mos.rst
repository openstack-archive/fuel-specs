..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Support of VPNaaS Neutron feature in MOS/FUEL
==========================================

https://blueprints.launchpad.net/fuel/+spec/support-vpnaas-in-mos


Problem description
===================

Today multi-cloud integration is a popular topic, because very
often we have more than one cloud and want to have some interaction
between tenants from the different clouds for some reason, like HA for
our services on the VMs.
For this purpose in OpenStack Neutron was implemented VPNaaS, which we
need to support in MOS and Fuel.


Proposed change
===============

Fuel will need to be extended in the following ways:

1. Add into Fuel-UI experimantal option for the deployment VPNaaS.
2. Add ability to deploy and control VPN agent instead of L3 agent.

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

* Add config option USE_VPNaaS (default: False)

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  aepifanov


Work Items
----------

* Add to Fuel ability to deploy VPN agent
* Update UI and manifests for availability to use VPNaaS
* Modify OCF scripts for the supporting VPN agents

Dependencies
============

* openswan package

Testing
=======

None

Documentation Impact
====================


This feature whould be documented. The planing guide will be updated.


References
==========

* https://wiki.openstack.org/wiki/Neutron/VPNaaS
* https://wiki.openstack.org/wiki/Neutron/VPNaaS/HowToInstall
* http://docwiki.cisco.com/wiki/OpenStack:Havana:VPNaaS
