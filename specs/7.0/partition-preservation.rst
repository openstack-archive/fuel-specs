==================================================
Support for partition preservation during rollback
==================================================

https://blueprints.launchpad.net/fuel/+spec/rollback-partition-preservation

Support for partition preservation

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

* Allow choosing needed strategy (what partition should be preserved)
  through API

* Allow configuring a set of partitions to preserve using disk.yaml

Implementation model
--------------------

General overview
++++++++++++++++

In context of this blueprint Rollback feature will be modified
in order to keep data.
On data preservation following use cases were identified:
1) keep Ceph data
2) keep Swift data
3) keep Nova instances cache
4) keep DB/logs/other custom partition types (Ericsson specific ATM)

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

Preserved partition must located as separate mountpoints
Mountpont should be add to the openstack.yaml
in case when specific mountpoint doesn't exist

Workflow will be as following:

1) Keep this function low-level, tied to settings of the node
2) Add 'keep' or similar boolean flag to node disks settings
   in Nailgun API (i.e. disks.yaml):

   ``fuel node --node 1 --disk --download``
   ::

     cat node_1/disks.yaml

     - extra:
       - disk/by-id/scsi-SATA_QEMU_HARDDISK_QM00001
       - disk/by-id/ata-QEMU_HARDDISK_QM00001
       id: disk/by-path/pci-0000:00:01.1-scsi-0:0:0:0
       name: sda
       size: 101836
       volumes:
       - name: os
         size: 101836
         keep: true

   then upload modified disk.yaml

   ``fuel node --node 1 --disk --upload``
3) Cobbler pmanager.py to handle 'keep' flag so if it is True for
   a partition then the partition will not be deleted or formatted
4) Mcollective agent initiate (erase_node.rb module in Mcollective)
   to disable erasing partitions with 'keep: True' when node is
   deleted from environment
5) Investigate state of art to implement this feature in master/6.1
   release with IBP as a default provisioning mechanism, as opposite
   to Cobbler kickstart-based approach
6) Regarding with new fuel provisioning method fuel agent should be
   modified to preserve(#4 #5 should be skiped)

Delivery details
++++++++++++++++

In context of this blueprint VolumeManager will be modified significantly in
order to issue an updated set of API. Also, Fuel agent will
be potentially changed, but those changes will be minor. In addition to
VolumeManager and Fuel agent there will be small changes in nailgun in order
to pass skip flag (disk.yam) to VolumeManager.

Alternatives
------------

The alternative approach would be copying valuable data back and forth before
and after the rollback. But that would drastically increase time needed for
rollback.

REST API impact
---------------

As this blueprint is all about adding new configurable behaviour to rollback
feature - it introduces parameter to disk.yaml to REST API
which performs default value as False.

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

This blueprint itself is about boosting speed of rollback and migration operations

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

:Primary Assignee: Ivan Ponomarev

:QA: Veronika Krayneva

:Documentation: Peter Zhurba, Dmitry Klenov

:Reviewer: Vladimir Kuklin, Vladimir Kozhukalov

Work Items
----------

1. Pass preserve partitions parameter from disk.yaml Nailgun
   (VolumeManager)

2. Adapt VolumeManager to take partition preservation flag and
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
