..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
MOS Node Reinstallation
==========================================

https://blueprints.launchpad.net/fuel/+spec/mos-node-reinstallation

Node reinstallation allow to fully/partially recover failed node
using the standard fuel processes provision and deploy
In case when only system should be reinstalled from
scratch (partially) Partition Preservation feature should be enabled

(https://blueprints.launchpad.net/fuel/+spec/partition-preservation)

Problem description
===================

Currently fuel does not fully functioning node reinstallation.
Slave nodes can't be restored if error raised after fail


Proposed change
===============

Reinstallation feature includes multiple changes which should be implemented


* Partition Preservation (will be implemented separately)
  (https://blueprints.launchpad.net/fuel/+spec/rollback-partition-preservation)

* Node renaming (https://blueprints.launchpad.net/fuel/+spec/node-naming)

* MongoDB recovery in case of failure (assumed should be fixed in 7.0)

* Swift ring sync during redeploy (assumed should be fixed in 7.0)


  Reinstallation process

  1) In the situation when node fail primary controller role should
     be moved to the online node

  2) Manipulation like partition preservation should be prepared
     before node will be reprovisioned

  3) The last step is provision and deploy


Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

Nailgun api part can be scale if new entity (replace,redeploy, etc)
will be useful and fits into product scope

API changes will be in partition preservation
(https://blueprints.launchpad.net/fuel/+spec/partition-preservation)

Node renaming
(https://blueprints.launchpad.net/fuel/+spec/node-naming)


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
should be shorter
In case compute node should be reinstallation using partition
preservation method. VM images migration not required

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
primary controller role to the online node

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Ivan Ponomarev - ivanzipfer


Work Items
----------

#. Scale nailgun part. Nailgun should be able to transfer
   primary controller

#. Nailgun api can be scale with additional commands
   (reinstall,redeploy, etc)



Dependencies
============

No strict dependencies

Testing
=======

It's necessary to improve devops to support
Node renaming and Partition preservation feature


Documentation Impact
====================

Reinstallation documentation will be added to the User Guide section

References
==========

