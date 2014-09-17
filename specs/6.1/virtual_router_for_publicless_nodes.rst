..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Virtual router for pulic-less nodes
===================================

https://blueprints.launchpad.net/fuel/+spec/virtual-router-for-env-nodes

Problem description
===================

Not each node in the env should be connected to the public network. But some
services on this node may require access to the external (public) services
(i.e. DNS, NTP).

Currently, in 5.1, as default gateway for each of this nodes specified a master
node. This solution does not correspond HA principals.

Actually, this problem closely intersects with `issue of DNS and NTP independency
<https://blueprints.launchpad.net/fuel/+spec/external-dns-ntp-support>`_, and I
propose implement both solutions in the same tack.

Proposed change
===============

Create virtual router namespace on the each controller nodes. Assign pair of
Public/Management VIP (only for HA deployments), managed by Pacemaker.
Connection states between namespaces on controllers should be synchronized by
conntrackd. All incoming traffic from management network should be NATed through
Virtual Router Public VIP.

In those namespaces, also, should be located DNS and NTP servers (see
`corresponded blueprint
<https://blueprints.launchpad.net/fuel/+spec/external-dns-ntp-support>`_
for more information).

This way allow us achieve maximum reliability even if corresponded customer
provided services goes down.



Alternatives
------------

* Leave this issue as is.

  * pros:

    * No efforts will be spend.

  * cons:

    * Master node is not obligatory part of cluster and may disappear at any
      moment.
    * Master node is not reserved. It is a SPOF for each HA-deployed env.


* Allow to customer define default gateway from his own infrestructure.

  * pros:

    * Minimal efforts from fuel-library team.

  * cons:

    * Huge changes in the Network checker part of Nailgun.
    * Increase number of networks on public-less nodes.
    * We should implement some additional mechanics for network connectivity
      to the customer's network. I.e. implement 80% functionalyty, that was
      removed as unnided, while fixing
      `LP#1272349 <https://bugs.launchpad.net/fuel/+bug/1272349>`_.
    * We can not be shure, that customer-provided services enough reliable.



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

UI impact
---------

UI should allow user to change data, described in  "Data model impact" section.

Upgrade impact
--------------

While upgrage we should upgrade rpm/deb packets and restart corresponded services.

Security impact
---------------

no impacts

Notifications impact
--------------------

no impacts

Performance Impact
------------------

Implementation this moves DNS and NTP servers maximum close to the requester.
Time of reaction to the client requests should be decreased.

Other end user impact
---------------------

End user gets some addition options, that not obligatory for changes. Deployed
env can work properly with default values.

Documentation Impact
--------------------

In the documentation should be described possibility of change values from "Data
model impact" section.





Implementation details
======================

On each controller proposed create network namespace. This network namespace will
be connected to the management and public bridges. This feature impacts only
Neutron-based configuration, because we just create additional network interfaces
by openvswitch. Mechanick, that used for "haproxy" network namespace (by two veth
pairs and proxyarp mechanicks) not allowed here, because we need pure routing
procedures.

::

                                   br-ex                                           br-ex
  +----------------------------------O---+        +----------------------------------O---+
  | Controller-I                    ^ ^  |        | Controller-II                   ^ ^  |
  |                                 | |  |        |                                 | |  |
  |      +------------------------+ | |  |        |      +------------------------+ | |  |
  |      |   HAproxy namespace    | | |  |        |      |   HAproxy namespace    | | |  |
  |  +---O VIP.mgmt               O-+ |  |        |  +---O                VIP.pub O-+ |  |
  |  |   +------------------------+   |  |        |  |   +------------------------+   |  |
  |  |                                |  |        |  |                                |  |
  |  |   +------------------------+   |  |        |  |   +------------------------+   |  |
  |  |   |   V.router namespace   |   |  |        |  |   |   V.router namespace   |   |  |
  |  | +-O VIP.rou    VIP.pub.rou O---+  |        |  | +-O                        O---+  |
  |  | | +------------------------+      |        |  | | +------------------------+      |
  |  | |      \                          |        |  | |                     /           |
  |  | |       \                         |        |  | |                    /            |
  |  v v        \                        |        |  v v                   /             |
  +---O----------------------------------+        +---O----------------------------------+
    br-mgmt       \                                 br-mgmt              /
                   \                                                    /
                    \                                                  /
                     \                  *----------*                  /
                      +----------------* conntrackd *----------------+
                                        *----------*


