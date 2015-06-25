..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================================================
Allow Fuel to deploy multi-rack environments, based on dynamic routing
======================================================================

For a customer, we need to provide ability to deploy Open Stack environment
to multiple rack, which contains only one (at least) L3 network per rack. No
L2 segmentation should be used. Dynamic routing protocols (OSPF, BGP or RIP)
should be used for announce IP addresses form non-base network to
provider/customer infrastructure.


Problem description
===================

Since fuel 6.0 end user has ability to deploy emvironment with multiple node
groups. For access from one node group to another for each network exists
additional static routes. This reference architecture has following limitation:

* There is no ability to share VIP and floating addresses between node groups.
* If already deployed cluster will extended by one or more node groups all nodes
  should be re-deployed for add routes to an extra node groups.
* Network address space can't be shared between node groups without usage shared
  L2 ethernet segment.

Proposed change
===============

Deploy Open Stack, using at least one L3 network per rack. This network will
call "base network" below.
Use dynamic routing solutions (OSPF, BGP or RIP) for anounce non-base network
resources to the network infrastructure.

For implement this functionality we should re-design some of Fuel components.
Existing multiple node groups solution, that independed from datacenter
infrastructure, will be extended up to this case.

 .. image:: ../../images/8.0/multirack/Multi_rack_ospf.png
    :width: 50 %

This big feaature logically splited to three stages. Each next stage extends
functionality of previous:

* Stage #1. One base network per rack. Each node send OSPF announces about
  virtual and floating IPs.
* Stage #2. More than one base network per rack. Each node send and receive
  OSPF announces.
* Stage #3. Add ability to use BGP or RIP instead OSPF for announcing.

Predictable limitation
----------------------

* Only TUN segmentation type may be used for Neutron.
* End user's data center should provide network infrastructure, which able:

  * receive OSPF anounces and redistribute ones to an neighbor's node racks.
  * privide access to internet for nodes, which required it (i.e. master node,
    controller nodes)

Implementation details
----------------------

Network checker
^^^^^^^^^^^^^^^
Should be able check connectivity between nodes, placed into different racks


Dynamic routing
^^^^^^^^^^^^^^^
For dynamic routing functionality we should install and configure something
ospfd (quagga, bird, etc...) on each node.


VIPs and Haproxy
^^^^^^^^^^^^^^^^
*Currently:* VIPs jumping between controller nodes by Pacemaker

*Planned:* VIPs will be assigned in its own network namespace on each
controller and will be announced by ospfd for anycast usage.


External (public) network
^^^^^^^^^^^^^^^^^^^^^^^^^
*Curently:* At least each controller node has connection to public
network. Public network used only for following purposes:

* access to public Openstack API and Horizon from "external world"
* abilily of North -- South network connectivity for VM instances by floating
  IP usage
* access from cluster nodes to "external world"

*Planned:* Remove "external" network use case. Access from cluster nodes to
the external world should be provided by datacenter infrastructure. For use
floating IP and Haproxy will be used anounce of VIPs and floating IPs by OSPF.


V-router
^^^^^^^^
*Currently:* Controller make NAT for traffic to external world from nodes,
which has no external network attached.

*Planned:* V-router functionality should be disabled. NAT should be provided
by datacenter infrastructure. This limitation should be, because alternative
way is make source routing on TOR-switches for dilevery "external" traffic to
controllers.


Corosync & Pacemaker
^^^^^^^^^^^^^^^^^^^^
If the multi-rack deployment used, Corosync should use only 'udpu' manner for
sync states, because datacenter infrastructure doesn't guarantee to route
multicast traffic between racks.


Neutron
^^^^^^^
*Currently:* Neutron has special OVS bridge (br-floating) for assignment
floating IP addresses. This bridge connected (L2) to the External (public)
network. Neutron creates network namespaces, gateway ports in this bridge and
"moved" this ports to namespaces. Assigns floating and gateway IP addresses to
this ports.

*Planned:* Special OVS bridge (br-floating) will be present on each node, but
not be connected on L2 with something. Instead this connectivity node, contains
L3-agent, will anounce local static routes to theese IPs.

 .. image:: ../../images/8.0/multirack/neutron_fips_differences.svg
    :width: 50 %


Alternatives
------------

Use external, provided by end user or provider infrastructure, balancer for
handle VIP and floating addresses between racks. Create abstract messaging
system for announcing address place change. Handle of address change events is
out of scope cluster, deployed by fuel.


Data model impact
-----------------

...in progress...


REST API impact
---------------

...in progress...


UI impact
--------------

...in progress...



Upgrade impact
--------------

...in progress...


Security impact
---------------

...in progress...



Notifications impact
--------------------

N/A.


Other end user impact
---------------------

N/A.


Performance Impact
------------------

No Nailgun/Library/UI performance impact is expected.


Other deployer impact
---------------------

N/A


Developer impact
----------------

N/A


Implementation
==============

Assignee(s)
-----------

Feature Lead: ???

Mandatory Design Reviewers: Andrew Woodward, Chris Clason

Developers: Aleksey Kasatkin, Ivan Kliuk, Sergey Vasilenko, Vitaly Kramskikh

QA: Anastasiia Urlapova


Work Items
----------

Stage #1 (just one L3 network per rack with OSPF used)

* Nailgun: Provide required network_scheme and network_metadata hashes.
* Nailgun/UI: Provide functional for store required OSPF configuration options.
* Master-node: Provide ability for pass PXE/DHCP and external traffic over
  one NIC with one L3 network.
* Library: prepare manifests for using new data structures
* Nailgun: provide changes in API.

Stage #2 (each node should has ability use multiple L3 networks)

* xxx


Dependencies
============

Partially depends on 'flexible networking' feature.


Testing, QA
===========

* Support cluster nodes placement.
* Support new network topology
* Ability to configure VMs for emulate TOR-switches.
* Some part of old tests of all types will become irrelevant and
  are to be redesigned.

Acceptance Criteria
-------------------

* There is no need to select networking backend when environment
  is being created (in wizard).
* Any or both of VLAN and TUN backends can be set up for the environment.


Documentation Impact
====================

The documentation should describe new networking architecture of Fuel,
changes and new features in networking configuration process in UI.


References
==========

