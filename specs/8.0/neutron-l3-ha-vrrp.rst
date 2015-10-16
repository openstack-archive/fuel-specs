..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
Neutron L3 HA VRRP support
==========================

https://blueprints.launchpad.net/fuel/+spec/neutron-vrrp-deployment


The aim of this blueprint is to add High Availability Features on virtual
routers to Fuel. L3 HA VRRP support covers only access to VMs and access from
VMs to Internet.

L3 HA feature gives an opportunity to establish connection faster after L3
agent failover than router rescheduling.


--------------------
Problem description
--------------------

Currently we are able to spawn many l3 agents, however each l3 agent is a SPOF.
If an l3 agent fails, all virtual routers of this agent will be lost, and
consequently all VMs connected to these virtual routers will be isolated from
external networks and possibly from other tenant networks. Existing
rescheduling has one big issue - thousands of routers take hours to finish the
rescheduling and configuration process.


----------------
Proposed changes
----------------

The idea of this spec is to schedule a virtual router to at least two
l3 agents, but this limit could be increased by changing a parameter in the
neutron configuration file.

L3 HA starts a keepalived instance in every router namespace. The different
router instances talk to one another via a dedicated HA network, one per
tenant. This network is created under the blank tenant to hide it from the CLI
and GUI. The HA network is a  Neutron tenant network, same as every other
network, and uses the default segmentation technology. HA routers have an ‘HA’
device in their namespace: When a HA router is created, it is scheduled to a
number of network nodes, along with a port per network node, belonging to the
tenant’s HA network. keepalived traffic is forwarded through the HA device (As
specified in the keepalived.conf file used by the keepalived instance in the
router namespace).


Flows::

         +----+                          +----+
         |    |                          |    |
 +-------+ QG +------+           +-------+ QG +------+
 |       |    |      |           |       |    |      |
 |       +-+--+      |           |       +-+--+      |
 |     VIPs|         |           |         |VIPs     |
 |         |      +--+-+      +--+-+       |         |
 |         +      |    |      |    |       +         |
 |  KEEPALIVED+---+ HA +------+ HA +----+KEEPALIVED  |
 |         +      |    |      |    |       +         |
 |         |      +--+-+      +--+-+       |         |
 |     VIPs|         |           |         |VIPs     |
 |       +-+--+      |           |       +-+--+      |
 |       |    |      |           |       |    |      |
 +-------+ QR +------+           +-------+ QR +------+
         |    |                          |    |
         +----+                          +----+


Web UI
======

In section Neutron Advanced Configuration we need a checkbox for enabling L3
HA. This checkbox cannot be enabled if DVR is turned on.


Nailgun
=======

Additional option 'neutron_l3_ha' will be added into opentack.yaml.
It will marked as incompatible with Neutron DVR.

Data model
----------

None

REST API
--------

No FUEL REST API changes.


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

None

Plugins
=======

None


Fuel Library
============

The following options should be passed to neutron::server class in order to
enable L3 HA and disable legacy rescheduling:

* l3_ha = True
* max_l3_agents_per_router = 3
* min_l3_agents_per_router = 2
* allow_automatic_l3agent_failover = False


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

Upgrade from legacy to HA router was not added in Liberty, but will be
backported from upstream.

We can upgrade legacy router to HA router by 3 steps::

 neutron router-update router1 --admin_state_up=False
 neutron router-update router1 --ha True
 neutron router-update router1 --admin_state_up=True

It also will be possible to make HA router legacy router.


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None


------------------
Performance impact
------------------

HA L3 is based on Keepalived(VRRP protocol) which gives the following features:

* Works within tenant networks
* Failover independent from RPC layer
* Expected to be quicker than rescheduling
  (Rescheduling - 1 router - 5 sec, then linear growth with number of routers
  Rough failover time: single router - 7-8 sec, 30 routers - 10 sec)


-----------------
Deployment impact
-----------------

L3 HA feature uses service network called "HA network" for VRRP protocol
messages. This network is created for every tenant, so if there's a limited
number of tunnels (or VLANs) for Neutron private networks
it should be considered.

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Ability to enable L3 HA support in Neutron should be documented in Fuel
Deployment Guide.


--------------------
Expected OSCI impact
--------------------

keepalived must satisfy the following criteria: 1.2.13, >1.2.16
(done for Ubuntu 14.04, satisfied in CentOS 7)

--------------
Implementation
--------------

Assignee(s)
===========


Primary assignee:
  Ann Kamyshnikova <akamyshnikova>

Other contributors:
  Sergey Kolekonov <skolekonov> (DE) Kristina Kuznetsova <kkuznetsova> (QA)

Mandatory design review:
  Eugene Nikanorov <enikanorov> Oleg Bondarev <obondarev>
  Sergey Vasilenko <svasilenko>


Work Items
==========

* Patch fuel-library and nailgun to add option for enabling L3 HA
    * disable L3 HA by default
* Scale testing
* Rally scenarios
* Shaker scenarios
* checking compatibility with plugins
* debug
* bug fixing/backport from upstream
* Patch fuel-web to add ability to enable/disable L3 HA
    * disable L3 HA by default


Dependencies
============

Since this implementation relies on Keepalived, Keepalived has to be
installed on each l3 node. The required version of Keepalived is the version
1.2.10 in order to have the IPV6 support. Safe versions:1.2.13,>1.2.16


------------
Testing, QA
------------

Manual Acceptance Tests
=======================
Create HA router and check:
 * Existence of keepalived process
 * (from admin) HA network(subnet) should be created for current tenant.
 * List of agents hosting router should contain list of agents and their
   status - one active others standby.
 * Neutron router port list should contain list of HA ports

HA/Destructive Tests
====================
All existing HA/destructive tests should pass on env with L3 HA enabled.

Additional scenarios should include:
 * L3 agent ban: ping test
    * create router
    * set gateway for external network and add interface
    * boot an instance in private net
    * add floating ip to vm
    * check what agent is active
    * start ping vm via floating ip
    * ban active l3 agent
    * Less than 10 packages should be lost
    * Check that another agent become active

 * SSH session failover
    * The same first 5 steps as for "L3 agent ban: ping test"
    * Enter vm using ssh
    * From vm ping 8.8.8.8
    * Stop active agent.
    * After some time (less than 10 packages can be lost) ping will be
      continued and another agent become master.

 * Test on 50 networks and 50 routers
    * Create 50 networks, subnets and 50 routers, for each router add interface
      to subnet, for some (for each fifths, for example) set gateway to public
      network.
    * Boot vm in one of the networks and add floating ip on it.
    * Same last 5 steps as for "L3 agent ban: ping test"

 * Test with 20 vms
    * Create 2 private networks with subnets
    * Create router and set gateway for external network and add interfaces for
      private networks that was created on the previous step.
    * Boot 10 vm in each network.
    * For each pair using iperf check connectivity restoration (around 15% of
      loss) for ICMP and TCP/UDP traffic during L3 agent failover.

Scale
=====

Environment with L3 HA enabled should pass all tests currently run on Scale Lab
with no significant performance degradation. No additional Rally scenarios are
needed to test specifics of L3 HA.

Acceptance criteria
===================

Pass acceptance functional test - after active L3 agent fails, connection
establishes and less than 10 packages should be lost.

----------
References
----------

`Blueprint <https://blueprints.launchpad.net/fuel/+spec/neutron-vrrp-deployment>`_
