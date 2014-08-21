=============================
Multiple L3 agents in Neutron
=============================

https://blueprints.launchpad.net/fuel/+spec/fuel-multiple-l3-agents

In FUEL 5.1 and before HA network solution was based on one neutron-l3-agent,
which was switchable between controllers.

This blueprint describes a way of using multiple L3 and DHCP agents instead of
single. It is required for network scalability and neutron performance 
improvements.

Problem description
===================

When we created virtual router in Neutron, it was scheduled to the L3-agent
(to one of alive if we had multiple agents using random selection).
Before Juno Neutron server didn't monitor life cycle of agent serving
this router. If the L3-agent service stopped on a node containing this agent or
connectivity was lost, Neutron server didn't reschedule this router to
another L3-agent. So there was no HA network solution.

Proposed change
===============

In Juno multiple solutions for this problem were introduced.
The easiest solution is to use the internal Neutron routers rescheduling
mechanism. In that case Neutron server automatically monitors L3 agents
lifecycle. If agent is marked as dead, all routers associated to the dead agent
will be safely moved by Neutron server to an alive agent on another node and
auxiliary resources created by the dead agent, such as additional interfaces
and iptables rules, will be removed.
There are some cases when auxiliary resources will be kept on the dead node and
potentially affect connection to instances. For example, when L3 agent is alive
but lost connection to a message broker. To avoid such problems additional
monitoring and clean up mechanism should be added. It must be easily usable
by Pacemaker. Current rescheduling script must be modified to match the
proposed changes.

This feature allows to have permanent and stable connection to instances
even in case of failure of one or more L3 agents. Also it allows to
effectively distribute routers between all available agents to improve
network performance.

For DHCP agent multiple-agent mode implemented as experimental feature
and disabled by default.

Alternatives
------------

In the Juno release DVR L3 agent is introduced. It looks like alternative
router solution. This solution serves only VMs with floating IP addresses and
doesn't change behavior for VMs without FIP.
Also this solution doesn't change behavior of DHCP agents.

There's another solution based on VRRP.
The problem is that this solution doesn't cover situation where both vrrp nodes
are down. This solution also needs external re-scheduling mechanism.

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

* Time delays when neutron agents go down will decrease.
* Network scalability will grow.
* Load on a separate controller will be decreased.
* Customers will get a possibility to add any number of nodes with started
  neutron agents and network scalability will grow.

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

* In astute.yaml we have following options:

  * quantum_settings/L3/multiple_dhcp_agents (default=false)
  * quantum_settings/L3/dhcp_agents_per_network (default=3)
  * quantum_settings/L3/multiple_l3_agents (default=true)

* OCF scripts for L3 and DHCP agents got "multiple_agents" option, that allows
  run agents in non-singletone mode
* cluster::neutron::l3 and cluster::neutron::dhcp classes got "multiple_agents"
  option, that allows  configure agents for running in multiple-agent mode
* cluster::neutron::dhcp got "agents_per_net" option (by default = 3), that
  describe amount of dhcp-agents for serve each network. This default
  justifyed by performance reasons.

Backward compatibility
----------------------

Using "multiple_agents" option for OCF scripts we can manipulate behavior
of L3 and DHCP agents. Moreover, for using old-style behavior of L3/DHCP
agents we should decrease clone size for corresponded Pacemaker
resources to "1".

Work Items
-------------

- Update Puppet manifests to enable multiple L3 agents
- Add necessary patches to Neutron for additional agents monitoring
- Edit the rescheduling script and Pacemaker OCF script
  to support multiple agents behavior

Assignee(s)
-----------

Sergey Vasilenko
Eugene Nikanorov
Oleg Bondarev
Sergey Kolekonov

Dependencies
============

None

Documentation Impact
====================

New Neutron-server behavior in case of dead L3 agents should be reflected in
documentation to correctly debug possible problems.


References
==========

None

Testing
=======

- Deploy HA cluster
- All instances must be constantly available via floating ips and have Internet
  access even in case of whole controller failure or particular cases such as
  message broker failures
