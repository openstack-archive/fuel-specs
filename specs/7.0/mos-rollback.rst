..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
MOS Rollback
==========================================

https://blueprints.launchpad.net/fuel/+spec/mos-rollback

Snapshot based rollback implementation allows to checkout between versions using
checkpoint process and to recover node to the previous state using
provision and deploy stage.
Also this method includes database and virtual machine
images partition preservation.
(https://blueprints.launchpad.net/fuel/+spec/rollback-partition-preservation)

Problem description
===================

Currently fuel does not support any rollback solution.
Slave nodes can't be restored if error raised after patching


Proposed change
===============

Rollback feature includes multiple changes which should be implemented

* Making snapshot  repositories

* Partition Preservation (will be implemented separatelly) (https://blueprints.launchpad.net/fuel/+spec/rollback-partition-preservation)

* Node renaming (https://blueprints.launchpad.net/fuel/+spec/reset-count-from-one)

* MongoDB recovery in case of failure (assumed should be fixed in 7.0)

* Swift ring sync during redeploy (assumed should be fixed in 7.0)


  Rollback process

  1) All repos should be cloned on the to the customer side and managed by aptly or pacrat package tools
  2) The script checks repo updates and makes new checkpoint using package tool
     when update appears
  3) script should has posibility to simply checkout between snapshots
  4) The last step is the standart API calls - provision and deploy
     which should be applied to failed node using previous
     snapshot release


::


|                      +-------------+
|                      | MOS channel |                +------------+
|                      +-----+-------+                |controller 1|
|                            | Sync repos             |            |
|                            |               +--------+checkpoint 3|
|                            | Each update   |        |            |
|     nova                   v new checkpoint|        |Status FAIL |
|   Partition          +-----+----------+    |        +------------+
|  preservation        |  Fuel master   |    |
|                      +----------------+    |
| +--------------+     |-|Checkpoint 3  +----+
| | compute      |     |-|              |             +------------+
| |              |     |----------------+             |controller 2|
| | checkpoint 2 |     |----------------+             |            |
| |              |     |-|Checkpoint 2  +-------------+checkpoint 2|
| | Status OK    +-------|              +-----+       |            |
| |              |     |----------------+     |       |Status OK   |
| |/var/lib/nova/|     |----------------+     |       +------------+
| |image         |     ||Checkpoint 1   |     |
| +--------------+     ||               |     |       +------------+
|                      |----------------+     |       |controller 3|
|                      +----------------+     |       |            |
|                                             +-------+checkpoint 2|
|                                                     |            |
|                                                     |Status OK   |
|                                                     +------------+

Alternatives
------------

* Using docker to store and create snapshots

* Using git-annex git for binary version

  All additional solutions also can be realized

Data model impact
-----------------

None

REST API impact
---------------

API changes will be in partition preservation
(https://blueprints.launchpad.net/fuel/+spec/rollback-partition-preservation)

Node renaming
(https://blueprints.launchpad.net/fuel/+spec/reset-count-from-one)

Node

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

Primary assignee:
  Ivan Ponomarev - ivanzipfer


Work Items
----------

#. All repos should be cloned on the to the customer side and managed by aptly or pacrat package tools
#. The script checks repo updates and makes new checkpoint using package tool
     when update appears
#. script should has possibility to simply checkout between snapshots
#. The last step is the standard API calls - provision and deploy
     which should be applied to failed node using previous
     snapshot release


Dependencies
============

No strict dependencies

Testing
=======

It's necessary to improve devops to support
Node renaming and Partition preservation feature


Documentation Impact
====================

Rollback documentation will be added to the User Guide section

References
==========

