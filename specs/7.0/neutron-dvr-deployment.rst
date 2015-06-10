..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================
Neutron DVR support
===================

https://blueprints.launchpad.net/fuel/+spec/neutron-dvr-deployment

Neutron Distributed Virtual Router implements the L3 Routers across the
compute nodes, so that tenants intra VM communication will occur without
hitting the controller node. (East-West Routing)

Also Neutron Distributed Virtual Router implements the Floating IP namespace
on every compute node where the VMs are located. In this case the VMs with
FloatingIPs can forward the traffic to the external network without reaching
the controller node. (North-South Routing)

Neutron Distributed Virtual Router provides the legacy SNAT behavior for
the default SNAT for all private VMs. SNAT service is not distributed,
it is centralized and the service node will host the service.


Problem description
===================

Currently Neutron L3 Routers are deployed on specific Nodes (controller nodes)
where all the compute traffic will flow through.

* Problem 1: Intra VM traffic flows through the controller node

  In this case even VMs traffic that belong to the same tenant on a different
  subnet has to hit the controller node to get routed between the subnets.
  This would affect performance and scalability.

* Problem 2: VMs with FloatingIP also receive and send packets through
  the controller node routers

  Today FloatingIP (DNAT) translation is done on the controller node and
  also the external network gateway port is available only at the controller.
  So any traffic that goes to the external network from the VM will
  have to go through the controller node. In this case the controller node
  becomes a single point of failure and also the traffic will heavily load
  the controller node. This would affect the performance and scalability.


Proposed change
===============

The proposal is to distribute L3 Routers across compute nodes when required
by VMs. This implies having external network access on each compute node.

In this case there will be enhanced L3 Agents running on each and every
compute node (This is not a new agent, this is an updated version of the
existing L3 Agent). Based on the configuration in the L3 Agent.ini file,
the enhanced L3 Agent will behave in legacy (centralized router) mode or as
a distributed router mode.

Also the FloatingIP will have a new namespace created on the specific
compute node where the VM is located (this is done by L3 agent itself).
Each Compute Node will have one new namespace for FloatingIP per external
network that will be shared among the tenants. Additional namespace and
external gateway port will also be created on each compute node for the
external traffic to flow through, in case there are VMs with floating ips
residing on this node. This port will consume additional IP address from
external network.

Default SNAT functionality will still be centralized and will be running on
controller nodes.

The Metadata agent will be distributed as well and will be hosted on all
compute nodes and the Metadata Proxy will be hosted on all the distributed
routers.

This implementation is specific to ML2 with OVS driver.
All three type of segmentation are supported: GRE, VXLAN, VLAN.

Constraints and Limitations
---------------------------

* No Distributed SNAT

  Neutron Distributed Virtual Router provides the legacy SNAT behavior for the
  default SNAT for all private VMs. SNAT service is not distributed,
  it is centralized and the service node will host the service.
  Thus current DVR architecture is not fully fault tolerant - outbound traffic
  for VMs without floating IPs is still going through one L3_agent node and
  is still prone to failures of a single node.

* Only with ML2-OVS/L2-pop

  DVR feature is supported only by ML2 plugin with OVS mechanism driver. If
  using tunnel segmentation (VXLAN, GRE) L2 population mechanism should be
  enabled as well.

* OVS and Kernel versions

  Proper operation of DVR requires OpenvSwitch 2.1 or newer and VXLAN requires
  kernel 3.13 or newer.

* No bare metal support

  Distributed routers rely on local l3 agent (resided on compute node) for
  address translation, so for bare metal instances only legacy routers should
  be used.

Deployment impact
-----------------

* Architecture changes

  * Neutron L3 and metadata agents will be deployed on all compute nodes and
    managed by Upstart. Agents deployment scheme on controller nodes is not
    changed.

  * All compute nodes require bridge to external network

* Fuel Library related changes

  * Update Neutron Puppet module to support DVR-related options (L3 agent mode,
    L2 population, distributed router option)

  * Update Cloud Networking related Puppet modules to deploy Neutron L3 and
    metadata agents on compute nodes with appropriate configuration

  * update Horizon related Puppet modules to add an ability to enable Neutron
    DVR options

* Fuel Web related changes

  * When Neutron DVR is enabled, a network scheme with external bridges on all
    compute nodes should be generated

Alternatives
------------

None

Data model impact
-----------------

"distributed" flag will be added to the router object data model.
This will enable the agent to take necessary action based on the router model.

REST API impact
---------------

Users with admin rights will be able to set "distributed" attribute on
router create and update API calls. IOW admins will be able to create both
distributed and legacy routers. This attribute will not be visible to
regular users.

Upgrade impact
--------------

The upgrade path from legacy to distributed router is supported. It's a 3
step process:

* neutron router-update router1 --admin_state_up=False

* neutron router-update router1 --distributed=True

* neutron router-update router1 --admin_state_up=True

distributed->legacy upgrade is not officially supported in Kilo but it may
work, just needs to be tested.

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

Inter VM traffic between the tenant subnets doesn't need to reach the router
in the controller node to get routed and will be routed locally from the
compute node. This would increase the performance substantially.

Also the Floating IP traffic for a VM from a Compute Node will directly hit
the external network from the compute node, instead of going through the router
on the controller node.

Dataplane testing results from 25 bare metal nodes env show significant
performance improvement for both East-West and North-South (with floating IPs)
scenarios.

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Infrastructure impact
---------------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  obondarev

Other contributors:
  skolekonov

Work Items
----------

* Patch fuel-lib to enable DVR by default

  * this will enable DVR testing at early stage

* Scale testing

  * Rally scenarios

  * Shaker scenarios

  * debug

  * bug fixing/backport from upstream

* Patch fuel-web to add ability to enable/disable DVR

  * disable DVR by default

Dependencies
============

This will likely depend on enabling l2-population for tunneling which is a
separate effort. However we will not wait but enable l2 pop as part of DVR
effort if needed.

Testing
=======

Manual Acceptance Tests
-----------------------

* On an environment with DVR enabled check that created router has
  “distributed “ attribute set to True via Horizon or CLI

* Boot a VM on a subnet connected to DVR router. Check external connectivity.

* Assign Floating IP to the VM. Check external connectivity. Ensure VM is
  reachable from external network.

* Boot a second VM on a different subnet connected to the same router. Ensure
  inter-subnet connectivity (both VM can reach each other)

Scale
-----

* Environment with DVR enabled should pass all tests currently run on Scale
  Lab with no significant performance degradation

* No additional Rally scenarios are needed to test specifics of DVR.

HA/Destructive Tests
--------------------

All existing HA/destructive tests should pass on env with DVR enabled.
Additional scenarios should include:

* East-West HA Test

  * Have several VM from different subnets running on different compute nodes.
    The subnets should be connected to each other and to an external network by
    a DVR router

  * Shutdown all controllers of the environment

  * Inter-subnet connectivity should be preserved: VMs from different
    subnets/compute nodes should still be able to reach each other

  * No dataplane downtime is expected

* North-South HA Test

  * Have a VM with Floating IP running on a subnet connected to an external
    network by a DVR router

  * Shutdown all controllers of the environment.

  * External connectivity should be preserved: VMs should still be able to
    reach external network

  * No dataplane downtime is expected

Data Plane Tests with Shaker
----------------------------
Shaker scenarios should be run on a bare-metal environment with DVR enabled.
Significant increase in performance is expected for east-west and north-south
(with Floating IPs) topologies. Some of the results were already obtained
(see "Performance Impact" section of the this doc)

Documentation Impact
====================

Ability to enable DVR support in Neutron should be documented in
Fuel Deployment Guide.

References
==========

None
