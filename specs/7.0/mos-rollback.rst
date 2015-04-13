..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
MOS Rollback
==========================================

https://blueprints.launchpad.net/fuel/+spec/mos-rollback

Snapshot based documentation allows to checkout between versions using
checkpoint process and to recover node to the previous state using
provision and deploy stage.
Also this method includes database and virtual machine
images partition preservation.
(https://blueprints.launchpad.net/fuel/+spec/rollback-partition-preservation)

Problem description
===================

A detailed description of the problem:

Currently fuel does not support any rollback solution.
Slave nodes can't be restored if error raised after patching


Proposed change
===============

Rollback feature includes multiple changes should be implemented

* Making snapshot repositories

* Partition Preservation (will be realized separatelly)

* Node renaming (https://blueprints.launchpad.net/fuel/+spec/reset-count-from-one)

* MongoDB recovery in case of failure (assumed should be fixed in 7.0)

* Swift ring sync during redeploy (assumed should be fixed in 7.0)


  Rollback process

  1) All repos should be cloned to the docker container on master node
  2) Docker container checks repo updates and makes new checkpoint when update appears
  3) 'dockerctl' should be improved to checkout between snapshots
  4) The last step is provision and deploy failed node using previous snapshot release


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

* A tool to mirror and version yum and apt repositories

   Yum repos Pacrat solution

   Apt repos Aptly solution

* Using git-annex for binary version

  All addititonal solutions still can be realized

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

Fuel UI should be improved to support case when end user need to checkout
to previous checkpoint

Performance Impact
------------------

A little more network in case when repository will be cached
on Fuel node

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

Part of fuel-web will be improved to support node renaming and sending
additional partition preservation information

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Ivan Ponomarev - ivanzipfer

Partition preservation part
  Evgeniy Afonichev

Work Items
----------

#. All repos should be cloned to the docker container on master node
#. Docker container checks repo updates and makes new checkpoint when update appears
#. 'dockerctl' should be improved to checkout between snapshots
#. The last step is provision and deploy failed node using previous snapshot release


Dependencies
============

No strict dependencies

Testing
=======

It's necessary to improve devops to support
Node renaming and Partition preservation feature


Documentation Impact
====================

User Guide section - add new section -
Rollback documentation

References
==========

