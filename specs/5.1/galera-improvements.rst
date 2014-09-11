..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
Improve Galera Cluster Management
=================================

https://blueprints.launchpad.net/fuel/+spec/galera-improvements [1]_

Problem description
===================

Galera Cluster implementation has some issues when a new controller is added to
the cluster. This case usually happens during cluster deployment or new member
addition.

Here are the issues in current implementation of Galera Cluster Management:

  - Current implementation uses mysqldump as State Snapshot Transfer (SST)
    which blocks "Donor" during the `process
    <http://galeracluster.com/documentation-webpages/nodeprovisioning.html
    #comparison-of-state-snapshot-transfer-methods>`_. Donor is locked while
    mysqldump is running during State Snapshot Transfer (SST). Due to this
    it's not possible to deploy Fuel Controllers in parallel, as Primary
    Controller can perform SST with one controller only. All other controllers
    won't be able to synchronize their state with Primary Controller.
  - Haproxy doesn’t detect whether controlleris out of sync during SST/IST.
    It's not a problem during the deployment, but it may be a significant
    problem on new controller addition.

Proposed change
===============

  - Add MySQL 5.6.16 with galera 0.25 module to Fuel
  - Use Percona's HAProxy `clustercheck script
    <https://github.com/olafz/percona-clustercheck/blob/master/clustercheck>`_
    to verify Galera status
  - Refactor MySQL settings (wsrep.conf), include new Galera settings, remove
    default settings from config


Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Security impact
---------------

Port 49000 will be opened. Anyone will be able to obtain the status of Galera
Cluster.

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

During normal operations the perfomance will be the same. On new controller
addition the perfomance will be improved as "xtrabackup" won't lock donor and
faster than mysqldump SST method.
innodb_doublewrite, innodb_thread_concurrency, innodb_write_io_threads were
added to improve performance of InnoDB engine.

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
  sgolovatiuk@mirantis.com

Work Items
----------

None

Dependencies
============

None

Testing
=======

Destructive tests are required.
Manual testing and log verification are required.

Documentation Impact
====================

Describe clustercheck script functionality
HAProxy statistic for MySQL cluster

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/galera-improvements
