===========================================
Support for maintenance mode on controllers
===========================================

https://blueprints.launchpad.net/fuel/+spec/controller-maintenance-mode

Support for maintenance mode on controllers

Problem description
===================


:First:

  there is no unified way to obtain needed state across all operation systems
  (OS) used within fuel. There are different ways for each of them:

  * for Ubuntu it is recovery mode
  * for Centos 6 it is single mode with modification
  * for Centos 7 it is rescue runlevel.

  So we have to use different algorithms which depend on OS. Common for all
  mentioned operating systems single mode does not provide network access and
  has different behavior.

:Second:

  when we stop services or use switching runlevels for obtaining maintenance
  mode (MM), very often we have “garbage things” (zombie processes, locks,
  memory leaks,  etc). It doesn’t let to do service staff properly.

:Third:

  dependency and interaction between services. If we want to stop some  service
  manually, we have to keep in mind all its dependencies and take care of them
  as well.

:Fourth:

  similar mode in other OS, for example “Windows safe mode”, has mechanism
  for automatic enforcing MM mode, if we have unexpected emergency reboot. So
  we need the same, but because we usually don't have access to console in one
  hand and in other hand automatic enforce of MM should accept some
  “emergency” reboots.

:Fifth:

  some services have own “maintenance mode” such as corosync which let us
  do the same things. But they may do it in a different way than required by
  us,  they may be absent in current cloud configuration.

:Sixth:

  HA services may look node in MM like node in “fail state” because
  services on it don’t stop own work properly.

Proposed change
===============

Proposed features
-----------------

* Solution should be compatible with Ubuntu and CentOS, and have unified OS
  independent interface.

* Ability to enter maintenance mode manually.

* Ability to enter maintenance mode automatically when operating system keeps
  rebooting unexpectedly. If we have more than REBOOT_COUNT “unclean”
  reboots MM will be enforced. “unclean” means unexpected reboot by
  COUNTER_RESET_TIME sec from boot.

* Maintenance mode should stop all services except really crucial ones like
  networking, ssh, etc.

* Add ability to boot node in maintenance mode.

* There should be configuration parameter to switch off MM functionality.

* Allow schedule command which will be execute after switching into MM.

* Allow specify custom command which will be execute before switching into and
  from MM.

Implementation model
---------------------

General overview
+++++++++++++++++

We will create common procedure and unified interface for all operating system
which are used by fuel. It let us enforce MM state and return into operational
mode in a unified way for all operating systems. Under the hood it will be
based on boot scripts and mechanisms which are specific for each operating
system. It is possible that we will introduce some changes to these mechanisms
to obtain proper set of services running in MM.

This procedure is not a service of openstack, but unification of recovery
procedures across all OSs. It will give us the same user interface across all
used systems.

Interface description
+++++++++++++++++++++

It is suggested to create “umm” utility which will enforce maintenance mode
on the system and resume normal operation.

**Usage:**

::

  umm status                               - check mm status

  umm on [command to execute in mm mode]   - enforce MM mode [and execute
                                             command when MM is reached]

  umm off [reboot]                         - continue boot process [or reboot]
                                             into operational mode.

  umm enable                               - enable mm functionality

  umm disable                              - disable mm functionality


Architectural design
+++++++++++++++++++++++

To avoid “garbage things” described in the second problem, maintenance mode
will be obtained only by reboot and subsequent pausing of the boot process on
apropriate state and resuming it when we want switch back into operational
state.

It lets us:

* be sure that only needed processes work on the node

* don’t process start and stop dependencies manually

* expect that all services will be properly notified and all roles will be
  transferred to other nodes. So in case HA  configuration - cluster will still
  work properly if we have enough working controllers.

For that we will modify boot-shutdown mechanism and create state in which only
network, ssh daemon and services which are needed for them are run.

We will modify current boot process for automatically enforce MM if system has
some “unexpected” reboot during established time.

Delivery details
++++++++++++++++

Individual packet will be built for each operating system. This packet will
provide unified umm utility plus specific implementation for each OS. Then, we
will modify puppet manifests to install this package by default.



Alternatives
------------

Corosync MM

OS native recovery tools - for example friendly-recovery Ubuntu package

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

Assignee(s)
-----------

:Primary assignee: Peter Zhurba

:QA: Veronika Krayneva

:Documentation: Peter Zhurba, Dmitry Klenov

:Reviewer: Vladimir Kuklin

Work Items
----------

1. Create common interface for all operating systems.

2. Create Ubuntu solution. Modification upstart configs and grub loader.

3. Create Centos solution. Modification initscript configs and grub loader.

4. Create Centos solution. Modification SystemD configs and grub loader.

5. Modify controller deploying procedure.

Dependencies
============

None

Testing
=======

Boot in maintenance mode on one node
------------------------------------

Preconditions
+++++++++++++

All actions are performed on the same controller. Once finished with these
actions, move on to another controller

Actions
+++++++

1. Enter maintenance mode

2. Wait when maintenance mode is reached

3. Leave maintenance mode

Expected result
+++++++++++++++

1. Maintenance mode is enabled

2. Maintenance mode started successfully

3. All services start successfully when maintenance mode is switched off


Auto maintenance mode on one node
---------------------------------

Preconditions
+++++++++++++

All actions are performed on the same controller. Once finished with all
actions, move on to another controller

Actions
+++++++

1. X or more unexpected reboots per Y min

2. Wait when maintenance mode starts

3. Disable maintenance mode

4. X or more unexpected reboots per Y min


Expected result
+++++++++++++++

1. Reboot finished successfully

2. Maintenance mode started successfully

3. MM is disabled

4. After MM is disabled, MM shouldn't be reached after unexpected reboot


Documentation Impact
====================

::

  Operations Guide      -> “Maintenance Mode” will be added.

  Terminology Reference -> “Maintenance Mode” will be added.

References
==========

- https://blueprints.launchpad.net/fuel/+spec/controller-maintenance-mode
