=============================================
Juno. How we can improve Openstack networking
=============================================

Introduction
------------
It is obvious, that with the arrival of the next version Openstack we expect get
some improvements. With arrival Juno relese to the Neutron arrive 2 improvements,
that helps us make virtual networking in MOS better:

A. network `rescheduling patch <https://review.openstack.org/#/c/110893>`_

B. DVR (Distributed Virtual Router)

C. HA L3-agent (based on VRRP)

   * `blueprint <https://blueprints.launchpad.net/neutron/+spec/l3-high-availability>`_
   * `feature description <http://assafmuller.com/2014/08/16/layer-3-high-availability/>`_

D. since Havana we have some options, that allow us having multiple DHCP agent
   for serving one network.

Terminology
-----------
Network node
    Node (Controller or additional node), that contains running DHCP, L3 and
    Metadata agents.
Controller node
    Node, that contains openstack API, schedulers and another control processes
    of Openstack components


Patch "A" (Solution "A")
------------------------
This patch should allow us:

* change current rescheduling mechanizm to the Neutron native.
* having multiple parallel working L3-agents for increase scalability.
* minimize out of service time while rescheduling.
  Now this time can't less 30-40 sec. After this patch I expect 3-5 sec.

If we remove hard dependency Network node from Controller, and
dedicate Network node as common role (it also will be useful for "granular
deployment" task), we can recommend to customers following env scheme::

                   +------------+
                  /              \
             +-> * Public network * <-+
             |    \              /    |
             |     +------------+     |
             |                        |
             |ex.                     |ex.
        +----*-------+        +-------*----+       +------------+
        |            |-+      |            |-+     |            |-+
        | Controller | |      | dedicated  | |     |  Compute   | |
        |      nodes | |      |  Network   | |     |     nodes  | |
        | (opt.+     | |      |     nodes  | |     |            | |
        |   network) | |      |            | |     |            | |
        |            | |      |            | |     |            | |
        +------*-----+ |      +------*-----+ |     +------*-----+ |
          +----|-------+        +----|-------+       +----|-------+
               |                     |                    |
               |                     |                    |
               +---------------------+--------------------+
                          Private (or mesh) network

**Note:** Since 5.1 compute node not needed external (public) interface. This
interface appear on Compute, Cinder, Ceph nodes only if specified its necessity.

Unfortanly, native rescheduling made only for router functionallity. Because for
DHCP-agents we should using our custom old method of rescheduling.
Or try use solution "D" -- year ago I tested it and found some problem when
guest OS served by many DHCP servers.

I propose following roadmap for implementing this feature:

* (fuel-library team) **Making "Network node" role as dedicated role.** This
  role should be deployed as part of controller, or as a independed role.
* (UI/Nailgun team) **Support "Network node" role.**
  While controller adding, "Network node" role should adding
  automatically. If env already contains two or more nodes with role "Network
  node", this role may be deleted from any node. While we adding "Network node"
  role to the node, Nailgun should check existence of public (br-ex) interface
  on this node.
* (fuel-library team) **Disable our custom rescheduling mechanics for
  L3-agent.** Instead this we will use Neutron native rescheduling.
* (fuel-library team) **Implement multiple DHCP-agent for virtual networks.**
* (fuel-library team) Remove (or modify) out custom mechanics for rescheduling
  DHCP-agents.



Patch "B" (Solution "B")
------------------------
DVR -- Distributed Virtual router. Allow pass Floating IP (**and only
floating**) traffic through public interface on Compute node. Non floating IP
traffic continues to pass through Controllers (or additional network nodes, if
we implements this feature).

Shure, DVR feature required public interface on Compute node. Therefore this
solution not suitable for customers, which requires maximal isolate env nodes
from outside world (e.g. isolate Compute nodes).

DVR -- is a controversial solution. This solution has some limitations. E.g. DVR
doesn’t work with VLAN segmentation, only with tunneling and L2population. Also
DVR incompotible with L3-HA feature.

I can't recommend this solution as default way for virtual networking in MOS due
its limitations. But it's a good addition solution, that may be implemented as yet
another virtual networking use case. This solution, for example, perfect for
clouds, where dominated floating traffic and no strict security requirements.

Implementation of DVR feature described in the
`blueprint <https://blueprints.launchpad.net/fuel/+spec/neutron-dvr-deployment>`_.

Patch "C" (Solution "C")
------------------------
This solution is a continuation of multiple L3 ageent feature. It allows serve
one tenant network by a few L3-agents in active-standby mode. In combination with
additional network node this solution should forcely improve HA in virtual
networking. Using VRRP should disable out of service time.
Moreover this patch should allow us propose to customers virt.network scheme
with regionally spaced network nodes::

                                  +--------------+
                                 /                \
          +-------------------> * Floating network * <---------------------+
          |                      \                /                        |
          |                       +--------------+                         |
          |          |                                         |           |
          |          .                                         .           |
          |ex.       |                                         |           |ex.
  +-------*----+     .   +------------+     +------------+     .   +-------*----+
  |            |-+   |   |            |-+   |            |-+   |   |            |-+
  | dedicated  | |   .   | Controller | |   |  Compute   | |   .   | dedicated  | |
  |  Network   | |   |   |      nodes | |   |     nodes  | |   |   |  Network   | |
  |     nodes  | |   .   |            | |   |            | |   .   |     nodes  | |
  |            | |   |   |            | |   |            | |   |   |            | |
  | DC-I       | |   .   |            | |   |            | |   .   | DC-II      | |
  +------*-----+ |   |   +------*-----+ |   +------*-----+ |   |   +------*-----+ |
    +----|-------+   .     +----|-------+     +----|-------+   .     +----|-------+
         |           |          |                  |           |          |
         |           .          |                  |           .          |
         +----------------------+------------------+----------------------+
                     .       Private (or mesh) network         .
                     |                                         |
                     .                                         .
    Datacenter I     |                                         |    Datacenter II


With minimal effort we can implement this solution as default for the all MOS-HA
installations.
