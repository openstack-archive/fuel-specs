..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================
Reliable Pacemaker Galera Resource Agent Script
===============================================

https://blueprints.launchpad.net/fuel/+spec/reliable-galera-ocf-script

This document is intended to capture the problems and requirements for
Pacemaker OCF “Resource Agent” (hereafter RA) for better MySQL Cluster
management.

Problem description
===================

Here are the issues in current implementation of Cluster management:

* Adding New Node to the cluster

  - Donor is locked while rsync/mysqldump is running during State Snapshot
    Transfer (SST)
  - Haproxy doesn’t detect whether node is out of sync during SST
  - Current implementation uses mysqldump as State Snapshot Transfer (SST)
    which blocks "Donor" during the `process
    <http://galeracluster.com/documentation-webpages/nodeprovisioning.html
    #comparison-of-state-snapshot-transfer-methods>`_.
  - Pacemaker/Corosync gets de-synced on new controller addition. It happens 
    due to puppet adds new member to "gscomm://" while old settings remains on
    the other existing controller nodes. Currently, it requires *crm resource 
    cleanup <>* for the hanged resource on the remained controller nodes.

* Reboot Whole cluster (Power outages scenario)

  - OCF script doesn’t determine the latest DB version and always relies on
    “primary controller” as a donor.

* Single Node reboot

  - Haproxy doesn’t detect whether node is out of sync during Incremental
    Transfer State (IST)

* Advanced features

  - Currently puppet manifests use *cs_shadow* as a method for cluster 
    management. It's not possible to use *crm_attribute* to store attributes 
    in configuration as *cs_shadow* will revert values back

Proposed change
===============
* Cluster Bootstrap

  - Use Percona’s implementation of init script which allows to bootstrap
    cluster even when wsrep_cluster_address has all nodes specified.

* Adding New Node to the cluster
  
  - Use **xtrabackup-v2** as a default method for SST
  - Use Percona's HAProxy `clustercheck script 
    <https://github.com/olafz/percona-clustercheck/blob/master/clustercheck>`_

* Reboot Whole cluster (Power Outage scenario)

  - RA script introduce timeout where pacemaker waits for 60-120 seconds until
    it can see more nodes to start looking for latest GTID if/when all nodes
    are down
  - After 60-120 seconds RA script must start the process of Primary Component 
    election which is the node with the latest GTID.
    and join cluster. This timeout can be specified as cluster attribute and
    can be changed by administrator.
  - Node with the latest GTID will became Galera Primary Controller (PC)
    During IST, HAProxy will fail over to another active master. Second node 
    will use PC as backup (requires **xtrabackup-v2**, otherwise both will be 
    down during IST)
  - If the node bootstrapped after timeout it will discard its configuration. 
    This usually happenes when it's stuck performing *fsck*.

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

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

During normal operations the perfomance will be the same. On new node 
addition the perfomance will be improved as "xtrabackup" won't lock donor and 
faster than mysqldump SST method

Other deployer impact
---------------------

None

Developer impact
----------------

None


Implementation
==============

None

Assignee(s)
-----------

Primary assignee:
  Sergii Golovatiuk (sgolovatiuk@mirantis.com)

Work Items
----------

None

Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/ha-pacemaker-improvements

Testing
=======

All set of destructive tests: Reboot single node, reboot whole cluster, add a
new node from Fuel UI

Documentation Impact
====================

None

References
==========

None
