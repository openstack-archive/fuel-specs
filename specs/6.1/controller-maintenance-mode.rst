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

1. Modify boot-shutdown procedure for create state in which run only
network,ssh daemon and services which are needed for them. This state is
called Maintenance Mode (MM).

It part depends on operation system.



2. Create mechanism which allow obtain this MM, return into working
state, check current status. It it should be unified command for all
supported OS in fuel.

Usage

  umm status                                - check mm status
  umm on [command to execute in mm mode]    - enforce MM mode. And execute
                                            command when it will be reached
  umm off                                   - continue boot into 
                                            operational mode


Required features
-----------------

* Solution should be compatible with Ubuntu and CentOS, and have unified
  os independent interface.
* Ability to enter maintenance mode manually.
* Ability to enter maintenance mode automatically when operating system keeps
  rebooting unexpectedly.
* Maintenance mode should stop all services except really crucial ones like
  networking, ssh, etc.
* Maintenance mode should start previously stopped services.
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
  Maintenance mode.

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
test

Assignee(s)
-----------

Primary assignee:

Work Items
----------

1. Create maintenance mode control utility specification.
2. Create Ubuntu solution. Modification upstart configs and grub loader
3. Create Centos solution. Modification systemD configs and grub loader
4. Modify controller deploying procedure.

Dependencies
============

None

Testing
=======

Documentation Impact
====================

We need to prepare additional section describing this implemetation in
main MOS documentation.

References
==========

- https://blueprints.launchpad.net/fuel/+spec/controller-maintenance-mode
