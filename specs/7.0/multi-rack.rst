..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Allow Fuel to deploy multi-rack environments
============================================

For a customer, we need to provide ability to deploy Open Stack environment
to multiple rack, which contains only one (at least) L3 network per rack. No
L2 segmentation should be used.

This blueprint observes architecture changes without deep details. For more
concrete description should be created more specific blueprints.


Problem description
===================

Fuel 6.1 and earlier has a separated networks for pass public, private,
storage, messaging, etc... traffic. These networks separated by using 802.1q
VLANs. This approach didn't allowed for datacenters which provide only L3
separation of racks.

Proposed change
===============

Deploy Open Stack, using at least one L3 network per rack. Change solutions,
which required L2 network segmentation to another, which not required. Use
dynamic routing solutions (at least OSPF), which provided by data center
infrastructure.

For implement this functionality we should re-design some of Fuel components.


Implementation details
----------------------

Network checker
^^^^^^^^^^^^^^^
Should be able check connectivity between nodes from different racks

OSPF
^^^^
For dinamic routing functionality we should install and configure quagga/ospfd
before configure most of Fuel and Openstack components on each node.


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
In multi-rack case Corosync should use only 'udpu' manner for sync ring build,
because datacenter infrastructure doesn't guarantee routinging multicast
traffic between racks.


Neutron
^^^^^^^
*Currently:* Neutron has special OVS bridge (br-floating) for assignment
floating IP addresses. This bridge connected (L2) to the External (public)
network. Neutron creates network namespaces, gateway ports in this bridge and
"moved" this ports to namespaces. Assigns floating and gateway IP addresses to
this ports.

*Planned:* Special OVS bridge (br-floating) will be present on each node, but
not be connected by L2 to anywhere. Instead this connectivity node, contains
L3-agent, will anounce local static routes to theese IPs.

 .. image:: ../../images/7.0/multirack/neutron_fips_differences.svg
    :width: 50 %


External balancer for VIPs
^^^^^^^^^^^^^^^^^^^^^^^^^^
*(stage #2)*

Datacenter infrastructure can provide external traffic balancer / firewall
functionality for non-direct access to cluster from outside world. Nailgun/UI
should able define additional IP addresses for haproxy instances. This
addresses will be used by external balancer for access to each haproxy
instance not through VIPs. In this case VIPs leaves only internal use.


Alternatives
------------

Build L2-separated networks by using native linux VxLAN over L3 network,
provided by data center infrastructure. Use L2-separated networks as in
"ordinary" deployment cases.


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


Testing
=======

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

