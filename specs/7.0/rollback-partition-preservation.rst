==================================================
Support for partition preservation during rollback
==================================================

https://blueprints.launchpad.net/fuel/+spec/rollback-partition-preservation

Support for partition preservation during rollback

Problem description
===================

:First:

Currently Fuel performs full re-provisioning while performing rollback which
implies data deletion. For instance, it doesn't preserve virtual machine
image files, compute node log files, database files. That said it loses
valuable data during rollback.
So operator has to manually backup valuable data before rollback.

Proposed change
===============

The idea is to preserve certain partitions on the nodes during rollback while
fully reformat others. For instance, keep partition /var/lib/nova/instances
intact but create filesystem on / (root) from the scratch.

Proposed features
-----------------

* Allow keeping certain partitions with valuable data on the nodes during
  rollback

* Allow choosing needed strategy (with or without partition preservation)
  through API

* Allow configuring a set of partitions to preserve via config file

Implementation model
--------------------

General overview
++++++++++++++++

In context of this blueprint Rollback feature will be modified in order to
keep data.

Note, this blueprint is all about modifying Fuel, not OpenStack.

Architectural design
++++++++++++++++++++

First off, here’s how partitioning in Fuel 6.x works right now. There are two
components - VolumeManager (on nailgun’s side) and Fuel agent (a process
inside bootstrap OS). Fuel agent is quite straightforward - it just executes
orders from VolumeManager. Fuel agent knows nothing about partitioning layout,
it doesn't contain any business logic. So it is VolumeManager which contains
that business logic.

The idea of Rollback Paritition Preservation is to keep data (vm images, logs,
db files, etc) during reprovisioning. So in terms of partitioning instead of
fully deleting partitions and creating a new partition table Fuel will
preserve data on some specific partitions (not all) while it still will
reformat others (like root partition).

Workflow will be as following:
1) a user requests rollback with --preserve-data flag set
2) Nailgun passes that command with parameters to VolumeManager

If --preserve-data is not set VolumeManager issues the same set of commands
as before. Otherwise

3) VolumeManager discovers (via astute.yaml) partition layout and other
   required information
4) Based on that info VolumeManager issues such set of commands to Fuel agent
5) So that Fuel Agent results with reformatting root parition on target node
   but it keeps /var/lib/nova/instances (and other needed partitions provided
   by VolumeManager).

The decision which partitions to keep (/var/lib/nova/instances, /var/log, etc)
is taken in VolumeManager. The list of partitions to preserve will be
configurable via config (most likely via astute.yaml). Fuel will be delivered
with predefined list which would contain such data as (but not limited to):
- /var/lib/nova/instances
- /var/log
- /var/lib/mysql


Delivery details
++++++++++++++++

In context of this blueprint VolumeManager will be modified significantly in
order to issue an updated set of commands to Fuel agent. Also, Fuel agent will
be potentially changed, but those changes will be minor. In addition to
VolumeManager and Fuel agent there will be small changes in nailgun in order
to pass --preserve-data flag from the interface (CLI) to VolumeManager during
rollback.

Alternatives
------------

The alternative approach would be copying valuable data back and forth before
and after the rollback. But that would drastically increase time needed for
rollback.

REST API impact
---------------

As this blueprint is all about adding new configurable behaviour to rollback
feature - it introduces parameter --preserve-partitions to REST API call
which performs rollback with default value as False.

Data model impact
-----------------

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

This blueprint itself is about boosting speed of rollback operation

Plugin impact
-------------

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

:Primary Assignee: Evgeniy Afonichev

:QA: Veronika Krayneva

:Documentation: Peter Zhurba, Dmitry Klenov

:Reviewer: Vladimir Kuklin, Vladimir Kozhukalov

Work Items
----------

1. Pass --preserve-partitions parameter from FUEL client to Nailgun
   (VolumeManager)

2. Adapt VolumeManager to take --partition-preservation flag during deploy and
   generate appropriate partition layout for Fuel agent

3. Adapt fuel-agent/manager taking into account preserved partitions


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/mos-rollback

Testing
=======

TBD

Documentation Impact
====================

Rollback section which is planned to be added in 'Rollback' story will be
improved with information about Partition Preservation options.

References
==========

https://blueprints.launchpad.net/fuel/+spec/mos-rollback
https://blueprints.launchpad.net/fuel/+spec/rollback-partition-preservation
