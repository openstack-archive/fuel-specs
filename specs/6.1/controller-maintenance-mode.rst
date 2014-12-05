===========================================
Support for maintenance mode on controllers
===========================================

https://blueprints.launchpad.net/fuel/+spec/controller-maintenance-mode

Support for maintenance mode on controllers

Problem description
===================

Currently there is no functionality built into controller which gives user
ability to safely undertake repairs in operating system, its services etc.
These activities can influence running Openstack environment thus all Openstack
services should be stopped.

Proposed change
===============

Required features
-----------------

* Solution should be compatible with Ubuntu and CentOS.
* Ability to enter maintenace mode manually.
* Ability to enter maintenace mode automatically when operating system keeps
  rebooting unexpectedily.
* Maintenace mode should stop all services except really crucial ones like 
  netowrking, ssh, etc.
* Maintenace mode should start previously stopped services.
* Add ability to boot node maintenance mode.

Alternatives
------------

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

* Potentially proposed changes could introduce additional tool to manage
  maintenance mode.

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

Work Items
----------

Dependencies
============

None

Testing
=======

Documentation Impact
====================

We need to prepare additional section describing this implementation in
main MOS documentation.

References
==========

- https://blueprints.launchpad.net/fuel/+spec/controller-maintenance-mode