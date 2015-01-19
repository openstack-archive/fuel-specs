======================================
Multiple DHCP agents in Neutron
======================================

https://blueprints.launchpad.net/fuel/+spec/fuel-multiple-l3-agents

In FUEL 6.0 and before HA network solution was based on one DHCP agent,
which was switchable between controllers.

This blueprint describes a way of using multiple DHCP agents instead of
single. It is required for network scalability and neutron performance
improvements.

Problem description
===================

When we created virtual network in Neutron, it was scheduled to the DHCP-agent
(to one of alive if we had multiple agents using random selection).
In Fuel version 6.0 and before Neutron server didn't monitor life cycle
of agent serving the network. There was only one DHCP agent in a cluster and
if the DHCP-agent service stopped or connectivity with a node containing
the DHCP agent was lost, Neutron server didn't reschedule networks.
So HA network solution was based on the custom script which used API calls.
Also in case of large number of networks with DHCP server the only agent
was overloaded.

Proposed change
===============

Neutron supports multiple DHCP agents, which can be used in two ways.
At first, all created networks can be distributed between available
DHCP agents. Also each network can be served with more than one DHCP agent
simultaneously. These functions give us a possibility to build more efficient
and reliable HA solution. Neutron server automatically monitors DHCP agents
lifecycle. In case of failure of all DHCP agents serving the network it
will be unscheduled from the dead agents and scheduled to alive agents.
So external rescheduling solutions aren't needed anymore.

Multiple DHCP agents will be enabled for cluster and the number of agents
serving each network will be increased. The Pacemaker OCF script for
Neutron DHCP agents has all necessary functionality.

This feature allows to have faster and more reliable DHCP service for
instances. Also it allows to effectively distribute virtual networks between
all available agents to improve network performance on large environments.

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

* Time delays for answers from DHCP servers will decrease.
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

  * quantum_settings/L3/multiple_dhcp_agents (default=true)
  * quantum_settings/L3/dhcp_agents_per_network (default=3)

* cluster::neutron::dhcp classes got "multiple_agents"
  option enabled by default, which allows to configure agents for running in
  multiple-agent mode
* cluster::neutron::dhcp got "agents_per_net" option (by default = 3),
  which describes amount of dhcp-agents to serve each network.
  This default was set due to performance reasons.

Backward compatibility
----------------------

Using "multiple_agents" option for OCF script we can manipulate behavior
of DHCP agent. Moreover, for using old-style behavior of DHCP
agent we should decrease clone size for corresponded Pacemaker
resources to "1".

Work Items
-------------

- Update Puppet manifests to enable multiple DHCP agents
- Add necessary patches to Neutron for network rescheduling mechanism

Assignee(s)
-----------

Sergey Kolekonov
Eugene Nikanorov
Sergey Vasilenko

Dependencies
============

None

Documentation Impact
====================

New Neutron-server behavior in case of dead DHCP agents should be reflected in
documentation to correctly debug possible problems.


References
==========

None

Testing
=======

- Deploy HA cluster
- All instances must get IP addresses correctly via DHCP even in case of
  whole controller failure or particular cases such as message broker failures
