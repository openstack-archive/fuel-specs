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
Slave nodes can't be restored after fail. Including but not limited to
MongoDB failures, Galera failures, update failures, upgrade failures, etc.


Proposed change
===============

Reinstallation feature includes multiple changes which should be implemented.


* Partition Preservation (will be implemented separately)
  (https://blueprints.launchpad.net/fuel/+spec/partition-preservation).

* Node renaming (https://blueprints.launchpad.net/fuel/+spec/node-naming).

* MongoDB recovery in case of failure (assumed should be fixed in 7.0).

* Swift ring sync during redeploy (assumed should be fixed in 7.0).


  Reinstallation process:

  1) Nailgun shouldn't serialize recovered contriller as primary

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

API part will not change. Reinstallation process will use standart
API calls - provision and deploy

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

:Primary Assignee: Ivan Ponomarev

Work Items
----------

#. Nailgun shouldn't serialize recovered contriller as primary
   Nailgun should be able reinstall slave node and using the same name
   to return slave node back to the cluster.


Dependencies
============

No strict dependencies

Testing
=======

Scenarios to automate

Reinstall single compute
1. Checkout previous repository version
2. Do reinstallation of the compute
3. Run Network check
4. Run OSTF tests set

Reinstall single controller
1. Checkout previous repository version
2. Do reinstallation of the controller
3. Run Network check
4. Run OSTF tests set

Reinstallation of full cluster
1. Checkout previous repository version
2. Do reinstallation of whole cluster
3. Run Network check
4. Run OSTF tests set


Documentation Impact
====================

Reinstallation documentation will be added to the User Guide section

References
==========

