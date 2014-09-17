..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================
Virtual router for public-less nodes
====================================

https://blueprints.launchpad.net/fuel/+spec/virtual-router-for-env-nodes

Problem description
===================

Only certain nodes should have a physical interface on the public network.
But some services on these nodes may require access to the external (public)
services (i.e. DNS, NTP).

Currently, in 5.1, the default gateway for all nodes is specified as the Fuel
Master node. This solution does not satisfy HA principals.

Actually, this problem closely intersects with `DNS and NTP blueprint
<https://blueprints.launchpad.net/fuel/+spec/external-dns-ntp-support>`_,
and I propose implement both solutions in the same task.

Proposed change
===============

Create virtual router namespace on the each controller nodes. Assign pair of
Public/Management VIP (only for HA deployments), managed by Pacemaker.
Connection states between namespaces on controllers should be synchronized by
conntrackd. All incoming traffic from management network should be routed
through VR management VIP and then NATed through VR public VIP.

Virtual Router Public VIP.

In those namespaces, also, should be located DNS and NTP servers (see
`corresponded blueprint
<https://blueprints.launchpad.net/fuel/+spec/external-dns-ntp-support>`_
for more information).

This way allow us to achieve maximum reliability even if the customer's own
provided service goes down.


Alternatives
------------

* Leave this issue as is.

  * pros:

    * No efforts will be spent.

  * cons:

    * Master node is not obligatory part of cluster and may disappear at any
      moment.
    * Master node is not reserved. It is a SPOF for each HA-deployed env.


* Allow to customer define default gateway from his own infrastructure.

  * pros:

    * Minimal efforts from fuel-library team.

  * cons:

    * Huge changes in the Network checker part of Nailgun.
    * Increase number of networks on public-less nodes.
    * We should implement some additional mechanics for network connectivity
      to the customer's network. I.e. implement 80% functionality, that was
      removed as unnecessary, while fixing
      `LP#1272349 <https://bugs.launchpad.net/fuel/+bug/1272349>`_.
    * We can not be sure, that customer-provided services reliable enough.



Data model impact
-----------------

In the Nailgun database should be appeared fields for

* DNS-servers
* NTP-servers
* Public VIP for virtual router
* Management VIP for virtual router

REST API impact
---------------

In the REST API should be serializers for data fields from "Data model impact"
section. Nailgun should, also, generate one Public and one Management VIP.

Developer impact
----------------

Nailgun should generate and reserve one Public and one Management VIP.

UI impact
---------

UI should allow user to change data, described in "Data model impact" section.

Upgrade impact
--------------

While upgrage we should upgrade rpm/deb packets, restart corresponded services
and change default routes.

Security impact
---------------

no impacts

Notifications impact
--------------------

no impacts

Performance Impact
------------------

Implementation of this approach moves DNS and NTP servers as close as possible
to the clients. Time of reaction to the client requests should be decreased.

Other end user impact
---------------------

End user gets some addition options, that not obligatory for changes. Deployed
env can work properly with default values.

Other deployer impact
---------------------

None

Implementation
==============

On each controller proposed create network namespace. This network namespace
will be connected to the management and public bridges. This feature impacts
only Neutron-based configuration, because we just create additional network
interfaces by openvswitch.

  Approach, that was used for "haproxy" network namespace (by two veth
  pairs and proxy_arp) is not allowed here, because of we need pure routing
  procedure.

I propose to divide work on this blueprint to some independent stages. Each
stage, except first, may be developed as concurrent tasks and don't depends
from another.

Stage #1 -- cooking virtual routers inside controllers
------------------------------------------------------

::

                                 br-ex                                   br-ex
  +-------------------------------OOO--+  +------------------------------OOO--+
  | Controller-I                  ^ ^  |  | Controller-II                ^ ^  |
  |                               | |  |  |                              | |  |
  |      +----------------------+ | |  |  |      +---------------------+ | |  |
  |      |   HAproxy namespace  | | |  |  |      |  HAproxy namespace  | | |  |
  |  +---O VIP.mgmt             O-+ |  |  |  +---O             VIP.pub O-+ |  |
  |  |   +----------------------+   |  |  |  |   +---------------------+   |  |
  |  |                              |  |  |  |                             |  |
  |  |   +----------------------+   |  |  |  |   +---------------------+   |  |
  |  |   |   V.router namespace |   |  |  |  |   |  V.router namespace |   |  |
  |  | +-O VIP.rou    VIP.pub.r O---+  |  |  | +-O                     O---+  |
  |  | | +----------------------+      |  |  | | +---------------------+      |
  |  | |      \                        |  |  | |                    /         |
  |  | |       \                       |  |  | |                   /          |
  |  v v        \                      |  |  v v                  /           |
  +--OOO-------------------------------+  +--OOO------------------------------+
    br-mgmt       \                         br-mgmt             /
                   \                                           /
                    \                                         /
                     \                *----------*           /
                      +--------------* conntrackd *---------+
                                      *----------*

Virtual router should be created by command set like this::

# ip netns add vrouter
# ip netns exec vrouter ip link set up dev lo
# ip netns exec vrouter sysctl -w net.ipv4.ip_forward=1
# ip netns exec vrouter ip route replace via %%DEFAULT_GATEWAY%%
# ovs-vsctl add-port br-mgmt vr-mgmt -- set Interface vr-mgmt type=internal
# ovs-vsctl add-port br-ex vr-ex -- set Interface vr-ex type=internal
# ip link set dev vr-mgmt netns vrouter
# ip link set dev vr-ex netns vrouter
# ip netns exec vrouter ip addr add %%VROUTER_EXT_VIP%% dev vr-ex
# ip netns exec vrouter ip addr add %%VROUTER_MGMT_VIP%% dev vr-mgmt
# ip netns exec vrouter ip link set up dev vr-mgmt
# ip netns exec vrouter ip link set up dev vr-ex
# ip netns exec vrouter iptables -t nat -A POSTROUTING -o vr-ex -j MASQUERADE

For functionality services, inside namespace, when VIPs located on another
node.

I propose create additional interface, NAT, low priority routing. As it does
for haproxy namespace.


Stage #2 -- configuring DNSMASQ and NTPD inside these namespaces
----------------------------------------------------------------

See
`corresponded blueprint
<https://blueprints.launchpad.net/fuel/+spec/external-dns-ntp-support>`_
for more information.


Stage #3 -- reserving connection states by VRRPD/CARP
-----------------------------------------------------

will be written

Assignee(s)
-----------

Primary assignee:
  omolchanov

Work Items
----------

#. Write puppet manifest to provide new namespace with new VIPs

#. Rewrite existing OCF ns_IPaddr2 to provide ability connecting
   to bridge

#. Add changes to nailgun

Dependencies
============
* https://blueprints.launchpad.net/fuel/+spec/refactor-l23-linux-bridges

Testing
=======
#. We need to build new fuel ISO and test if deployment work as expected.
#. We need to test that all nodes have access to internet using extenal router
   VIP.
#. We need to test that connection (wget download) won't be dropped after node
   that manages both VIPs fails.

Documentation Impact
====================
In the documentation should be described possibility of change values from
"Data model impact" section.

References
==========

[1] https://review.openstack.org/#/c/142475/
