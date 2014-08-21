============================
Multiple L3 agent in Neutron
============================

https://blueprints.launchpad.net/fuel/+spec/fuel-multiple-l3-agents

In FUEL 5.1 and before HA network solution based on one neutron-l3-agent,
switchable between controllers.

This blueprint describes way for using multiple L3 agents instead single.
It need for network scalability and neutron performance improvement.

Problem description
===================

When we create virtual router in Neutron, it scheduled to the L3-agent (to one
of alive if we have several ones, by random select). After this, Neutron server
do not monitor life cycle for agent, that served this router. If the L3-agent
service stop or node, contains this agent, not running -- Neutron server do not
reschedule this router to another L3-agent.  have no HA network solution.


Proposed change
===============

I suggest divide implementation of this feature to twa stages. On the first
stage we should convert existing rescheduling script to the neutron agent,
managed by pacemaker.

Neutron-rescheduling-agent, will monitor life-cycle of each registered
neutron-agent, reschedule routers from dead L3 agents to alive, reschedule
networks from dead dhcp-agents to alive.

Rescheduling agent should do:

* periodically connect to the Neutron API and monitor life cycle of L3 and
  DHCP agents
* recognize "die" status of agent
* re-schedule routers/networks
* activate fdb-clean procedure if need
* destroy agents, that present in die status long time
* (stage #2): Using AMQP for connecting to the Neutron server for monitoring
  life cycle of agents

Alternatives
------------

In the Juno release in the Neutron will be a solution DVR L3 agent. But it's looks like alternative router solution. This solution served only VMs with floating IP addresses and don't change behavior for VM's without FIP. Also this solution don't change behavior for DHCP agents.

In the K... release of Neutron will be a solution based on VRRP. But this solution don't cover situation where both of vrrp nodes go down. This solution also need external re-scheduling mechanism.

Data model impact
-----------------

None

REST API impact
---------------

None

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

* Time delays while neutron agents go out should be reduced.
* Network scalability will grow.
* Load on a separate controller should be reduced.
* Customer will get possibility for adding any counts of nodes with started
  neutron agents and network scalability will grow.

Other deployer impact
---------------------

None

Developer impact
----------------

None

References
==========

None
