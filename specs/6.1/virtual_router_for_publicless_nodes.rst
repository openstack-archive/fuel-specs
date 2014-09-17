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

Make virtual router namespace on the controller nodes, managed by Pacemaker.
Connection states between namespaces on controllers should be synchronized by
conntrackd. In that namespaces, also, should be located DNS and NTP servers (see
`corresponded blueprint
<https://blueprints.launchpad.net/fuel/+spec/external-dns-ntp-support>`_
for more information).

This way allow us achieve maximum reliability even if customer provided services
goes down.

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
    * We should implement some additional mechanics for network connectivity
      to the customer's network.
    * We can not be shure, that customer-provided services enough reliable.

