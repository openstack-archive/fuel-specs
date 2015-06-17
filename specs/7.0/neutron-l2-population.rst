======================================
Neutron L2 population plugin
======================================

https://blueprints.launchpad.net/fuel/+spec/neutron-l2-population

This blueprint describes Neutron L2 population plugin which can improve
performance of tunneling protocols. The L2 Population driver enables
broadcast, multicast, and unicast traffic to scale out on large overlay
networks.

Problem description
===================

Destination MAC addresses aren’t initially known by the agents,
so multicast or broadcast traffic is flooded out tunnels to all other compute
nodes. Also currently if a node isn’t hosting any ports in a specific network
it will receive broadcast traffic designated to that network.
This is not an effective approach from network perfomance point of view,
because Neutron service has full knowledge of the topology and can propagate
the forwarding information among agents using a common RPC API.

Proposed change
===============

Neutron supports L2 population since Havana.
When using the ML2 plugin with tunnels, the l2pop mechanism driver uses RPC
notifications to send updates in topology (ports) to all layer 2 agents.
So agents can use this information instead of getting it via broadcast traffic.

In order to use the feature it should be enabled during clusters deployment
using Puppet manifests. If testing results will not show any regression when
this feature is enabled, it's also proposed to enable it in Fuel by default.

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

Turning on L2 population during upgrade from previous releases can destroy all
existing tunnels.

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

* Amount of broadcast traffic in Neutron private networks will be decreased
* Network scalability and performance will grow.

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

* l2_population option should be enabled in neutron module when tunnelling is
  used (GRE/VXLAN)
* l2population will be added to mechanism_drivers and passed to neutron module

Backward compatibility
----------------------

None

Work Items
-------------

* Update Puppet manifests to enable L2 popualtion

Assignee(s)
-----------

Sergey Kolekonov

Dependencies
============

None

Documentation Impact
====================

New Neutron services behavior after enabling L2 poulation option should be
reflected in documentation to correctly debug possible problems.

References
==========

None

Testing
=======

* All existing Tempest/Rally tests should pass
* Check that if broadcast traffic is initiated from a virtual machine in
  network1 only a compute nodes which hosts virtual machines from network1 will
  receive the traffic
