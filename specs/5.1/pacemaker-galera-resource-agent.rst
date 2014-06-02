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

* Cluster Bootstrap

  - Init script for MySQL Galera doesn’t have special function which makes
    the bootstrap process difficult with predefined configuration with all
    nodes.

* Adding New Node to the cluster

  - Donor is locked while rsync/mysqldump is running during State Snapshot
    Transfer (SST)
  - Haproxy doesn’t detect whether node is out of sync during SST
  - Current implementation uses mysqldump as State Snapshot Transfer (SST)
    which blocks "Donor" during the `process
    <http://galeracluster.com/documentation-webpages/nodeprovisioning.html
    #comparison-of-state-snapshot-transfer-methods>`_.

* Reboot Whole cluster (Power outages scenario)

  - OCF script doesn’t determine the latest DB version and always relies on
    “primary controller” as a donor.

* Single Node reboot

  - Haproxy doesn’t detect whether node is out of sync during Incremental
    Transfer State (IST)

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
    and join cluster
  - Node with the latest GTID will became Galera Primary Controller (PC)
    During IST, HAProxy will fail back to backup. Second node will use PC as
    backup (requires **xtrabackup-v2**, otherwise both will be down during IST).
  - If the node bootstrapped after timeout it will discard its configuration 

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

None

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

None

Work Items
----------

None

Dependencies
============

None

Testing
=======

None

Documentation Impact
====================

None

References
==========

None
