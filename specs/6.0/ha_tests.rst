 
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
7. Check rabbit status with MOS script

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

Steps:
1. Deploy HA cluster with Neutron Vlan, 3 controllers, 2 compute, eth1-eth4 interfaces are bonded in active backup mode
2. Destroy primary controller
3. Check pacemaker status
4. Run OSTF
5. Check rabbit status with MOS script

8. HA load testing with rally
(May be not a part of this blueprint)

9. Need to test HA Neutron cluster under high load and simultaneous removing of virtual router ports
(related link http://lists.openstack.org/pipermail/openstack-operators/2014-September/005165.html)

10. Cinder Neutron Plugin

Steps:
1. Deploy HA cluster with Neutron GRE, 3 controllers, 2 compute, cinder-neutron plugin enabled
2. Run network verification
3. Run OSTF

11. Rmq failover test for compute service

Steps:
1. Deploy HA cluster with Nova-network, 3 controllers, 2 compute with cinder roles
2. Disable one compute node with
nova-manage service disable --host=<compute_node_name> --service=nova-compute
3. On controller node under test (which compute node under test is connected to via rmq port 5673) repeat spawn / destroy instance requests continuosly (sleep 60) while the test is running
4. Add iptables block rule from compute IP to controller IP:5673 (take care for conntrack as well)
iptables -I INPUT 1 -s compute_IP -p tcp --dport 5673 -m state --state NEW,ESTABLISHED,RELATED -j DROP
5. Wait 3 min for compute node under test should be marked as down in the nova service-list
6. Wait for another 3 min for it to be brought up back
7. Check for the compute node under test queue - it should be zero messages in it
8. Check if the instance could be spawned at the node

12. Check monit on compute nodes

Steps:
1. Deploy HA cluster with Nova-network, 3 controllers, 2 compute
2. Ssh to every compute node
3. Kill nova-compute service
4. Check that service was restarted by monit

13. Check pacemaker restarts heat-engine in case of losing amqp connection

Steps:
1. Deploy HA cluster with Nova-network, 3 controllers, 2 compute
2. SSH to controller with running heat-engine
3. Check heat-engine status
4. Block heat-engine amqp connections
5. Check if heat-engine was moved to another controller or stopped on current controller
6. If moved - ssh to node with running heat-engine
6.1 Check heat-engine is running
6.2 Check heat-engine has some amqp connections
7. If stopped - check heat-engine process is running with new pid
7.1 Unblock heat-engine amqp connections
7.2 Check amqp connection re-appears for heat-engine


14. Neutron agent rescheduling

Steps:
1. Deploy HA cluster with Neutron GRE, 3 controllers, 2 compute
2. Check the neutron-agents list consitency (no duplicates, alive statuses, etc)
3. On host with l3 agent create one more router
4. Check there are 2 namespaces
5. Destroy controller with l3 agent
6. Check it was moved to another controller, check all routers and namespaces were moved
7. Check metadata agent was also moved, there is process in router namespace that listen
to 8775 port

15. DHCP agent rescheduling

Steps:
1. Deploy HA cluster with Neutron GRE, 3 controllers, 2 compute
2. Destroy controller with dhcp agent
3. Check it was moved to another controller
4. Check metadata agent was also moved, there is process in router namespace that listen
to 8775 port

Dependencies
============



Testing
=======



Documentation Impact
====================



References
==========


