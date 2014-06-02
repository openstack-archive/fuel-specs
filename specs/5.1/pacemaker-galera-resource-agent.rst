..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================
Reliable Pacemaker Galera Resource Agent Script
===============================================

https://blueprints.launchpad.net/fuel/+spec/reliable-galera-ocf-script

This document is intended to capture the problems and requirements for
Pacemaker OCF “Resource Agent” (hereafter RA) to improve Galera Cluster
management under Pacemaker Resource Manager


Problem description
===================

* Reboot Whole cluster (Power outages scenario)

  - RA script doesn’t determine the latest Galera GTID version. It always
    relies on “primary controller” as a donor. Under some circumstances
    Pacemaker cannot assemble Galera cluster.

* Reboot any node from cluster

* Add a new node to active cluster

* Advanced features

  - Currently puppet manifests use *cs_shadow* as a method for cluster
    management. It's not possible to use *crm_attribute* to store attributes in
    configuration as *cs_shadow* will revert values back

Proposed change
===============

* Write a new RA script for Galera with the following requirements

  - RA script allows to bootstrap cluster even when wsrep_cluster_address has
    all nodes specified.
  - RA script introduces timeout where pacemaker waits for 60-120 seconds until
    all nodes specified in CIB became online after reboot or outage.
  - After 60-120 seconds RA script must start the process of Primary Component
    election which is the node with the latest GTID. This timeout is specified
    as node attribute and can be changed by administrator. If all nodes
    specified in CIB are UP the election process will be started immediately.
  - RA script dertemines Galera GTID state and set it as node attribute. RA gets
    GTID from **mysqld --wsrep-recover** or SQL query
    **SHOW STATUS LIKE ‚wsrep_local_state_uuid**
  - The node with the latest GTID will become Galera Primary Controller. It
    will be started with empty gcomm:// string. All other nodes will join to
    Galera Primary controller to synchronize their state.
  - If the node bootstrapped after timeout it will discard its configuration.
    This usually happenes when it's stuck performing *fsck*.
  - When new a node is added to cluster it will join cluster normally.

* Remove cs_shadow

  - Remove cs_shadow from manifests to allow to store node attributes

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

Assignee(s)
-----------

Primary assignee:
  Sergii Golovatiuk (sgolovatiuk@mirantis.com)

Work Items
----------

- Write Galera OCF script
- Perform all set of destructive tests


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/ha-pacemaker-improvements

Testing
=======

All set of destructive tests: Reboot single node, reboot whole cluster, add a
new node from Fuel UI

Documentation Impact
====================

The documentation should indicate how to increase/decrease Bootstrap timeout.

References
==========

None
