..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
MOS Node Reinstallation
==========================================

https://blueprints.launchpad.net/fuel/+spec/mos-node-reinstallation

Node reinstallation allows fully/partially recover failed nodes
using the standard fuel processes 'provision' and 'deploy'.
Full reinstallation - purge all data from reinstalled node
Partial reinstallation - some data can be preserved OS will be
reinstalled.
In case when only system should be reinstalled from scratch
(partially) Partition Preservation feature should be enabled.

(https://blueprints.launchpad.net/fuel/+spec/partition-preservation)

Problem description
===================

Currently fuel does not fully support functioning node reinstallation.
Slave nodes can't be restored if error raised after fail.


Proposed change
===============

Reinstallation feature includes multiple changes which should be implemented.


* Partition Preservation (will be implemented separately)
  (https://blueprints.launchpad.net/fuel/+spec/partition-preservation).

* Node renaming (https://blueprints.launchpad.net/fuel/+spec/node-naming).

* MongoDB recovery in case of failure (assumed should be fixed in 7.0).

* Swift ring sync during redeploy (assumed should be fixed in 7.0).


  Reinstallation process:

  1) In the situation when node fail primary controller role should
     be moved to the online node.

  2) Partition preservation manipulation should be prepared
     before node will be reprovisioned.

  3) The last step is provision and deploy.


Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

Nailgun api part can be scale if new entity (replace,redeploy, etc)
will be useful and fits into product scope.

API changes will be in partition preservation
(https://blueprints.launchpad.net/fuel/+spec/partition-preservation).

Node renaming
(https://blueprints.launchpad.net/fuel/+spec/node-naming).


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

Reinstallation process using partition preservation should improve
deployment stage. Swift, Mysql, Mongodb services synchronization
time should be shorter.
In case compute node should be reinstalled using partition
preservation method VM images migration not required.

None

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

Nailgun part should be scale. Nailgun should be able to transfer
primary controller role to the online node.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Ivan Ponomarev - ivanzipfer


Work Items
----------

#. Scale nailgun part. Nailgun should be able to transfer
   primary controller.
   Nailgun should be able reinstall slave node and using the same name
   return slave node back to the cluster.

#. Nailgun api can be scale with additional commands
   (reinstall,redeploy, etc)



Dependencies
============

No strict dependencies

Testing
=======

Reinstall single compute on HW with partition preservation:

1) Enable partition preservation in disks settings (disks.yaml)
   of the compute
2) Do reinstallation of the compute
3) Run OSTF tests set
4) Run Network check
5) Check data on partitions
6) Check availability preserved VM's

Reinstall single controller on HW with partition preservation

1) Enable partition preservation in disks settings (disks.yaml)
   of the controller
2) Do reinstallation of the controller
3) Run OSTF tests set
4) Run Network check
5) Check data on partitions
6) Check services data that have been preserved
   Services should normally works using preserved data


Documentation Impact
====================

Reinstallation documentation will be added to the User Guide section

References
==========

