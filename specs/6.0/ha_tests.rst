 
==========================================
HA tests improvements
==========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/ha-test-improvements



Problem description
===================

Need to add new HA tests and modify the existing one


Proposed change
===============

We need to clarify the list of new tests and new checks and then implement it in
system tests

Alternatives
------------

No alternatives

Data model impact
-----------------

No impact

REST API impact
---------------

No impact

Upgrade impact
--------------

No impact

Security impact
---------------

No impact

Notifications impact
--------------------

No impact

Other end user impact
---------------------

No impact

Performance Impact
------------------

No impact

Other deployer impact
---------------------

No impact

Developer impact
----------------

Implementation
==============

Assignee(s)
-----------

Can be implemented by fuel-qa team in parallel

Work Items
----------

1. Shut down public vip two times
(link to bug https://bugs.launchpad.net/fuel/+bug/1311749)

Steps:
1. Deploy HA cluster with Nova-network, 3 controllers, 2 compute
2. Find node with public vip
3. Shut down eth with public vip
4. Check vip is recovered
5. Find node on which vip is recovered
6. Shut down eth with public vip one more time
7. Check vip is recovered
8. Run OSTF
9. Do the same for management vip

2. Galera does not reassemble on galera quorum loss
(link to bug https://bugs.launchpad.net/fuel/+bug/1350545) 

Steps:
1. Deploy HA cluster with Nova-network, 3 controllers, 2 compute
2. Shut down one controller
3. Kill mysqld on second controller
4. Start first controller
5. Check galera reassembles
6. Run OSTF

3. Corrupt root file system on primary controller

Steps:
1. Deploy HA cluster with Nova-network, 3 controllers, 2 compute
2. Corrupt root file system on primary controller
3. Run OSTF

4. Block corosync traffic
(link to bug https://bugs.launchpad.net/fuel/+bug/1354520)

Steps:
1. Deploy HA cluster with Nova-network, 3 controllers, 2 compute
2. Login to rabbit master node
3. Block corosync traffic
 iptables -I INPUT -p udp --dport 5405 -m state --state NEW,ESTABLISHED,RELATED -j DROP
4. Wait 10 min and unblock it
 iptables -D INPUT -p udp --dport 5405 -m state --state NEW,ESTABLISHED,RELATED -j DROP
5. Check rabbitmqctl cluster_status at rabbit master node
6. Run OSTF HA tests

5. HA scalability for mongo

Steps:
1. Deploy HA cluster with Nova-network, 1 controller and 3 mongo nodes
2. Add 2 controller nodes and re-deploy cluster
3. Run OSTF
4. Add 2 mongo nodes and re-deploy cluster
5. Run OSTF

6. Lock DB access on primary controller

Steps:
1. Deploy HA cluster with Nova-network, 3 controllers, 2 compute
2. Lock DB access on primary controller
3. Run OSTF

7. Need to test HA failover on clusters with bonding

8. HA load testing with rally
(May be not a part of this blueprint)

9. Need to test HA Neutron cluster under high load and simultaneous removing of virtual router prots
(related link http://lists.openstack.org/pipermail/openstack-operators/2014-September/005165.html)


Dependencies
============



Testing
=======



Documentation Impact
====================



References
==========


