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

An additional option will be added to astute.yaml and then passed to Puppet
manifests to enable this feature. If testing results will not show any
regression when this feature is enabled, it's also proposed to enable it
in Fuel by default.

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

With L2pop mechanism driver enabled extra notifications are generated
for every port create/update/delete.

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

* L2 population option will be added to Fuel Web UI
  This option must be enabled if Neutron DVR is enabled
* l2_population option should be enabled in neutron module when tunnelling is
  used (GRE/VXLAN) and L2 population feature is enabled in astute.yaml
* l2population will be added to mechanism_drivers and passed to neutron module
  when L2 population feature is enabled in astute.yaml

   .. code-block:: python

    ---------------------
    quantum_settings:
      l2_population: true
    ---------------------

Backward compatibility
----------------------

None

Work Items
-------------

* Update Puppet manifests to enable L2 popualtion

Assignee(s)
-----------

Primary assignee:
  Sergey Kolekonov

Other contributors:
  Anna Babich (QA)

Mandatory design reviewer:
  Sergey Vasilenko

Dependencies
============

None

Documentation Impact
====================

* New Neutron services behavior after enabling L2 poulation option should be
  reflected in documentation to correctly debug possible problems.
* New Fuel Web UI option for Neutron L2 population should be described


References
==========

None

Testing
=======

* All existing Tempest/Rally tests should pass
* Check that if broadcast traffic is initiated from a virtual machine in
  network1 only a compute nodes which hosts virtual machines from network1 will
  receive the traffic

Acceptance criteria
-------------------

* Deploy an environment with at least two compute nodes
  and GRE/VXLAN segmentation
* Create two Neutron private networks
* Start two VMs using two previously created networks and make sure that
  the VMs were scheduled to different compute nodes
* Emulate broadcast traffic on the first VM using arping utulity (for example)
* Capture incoming traffic on the compute node with the second VM: there should
  be no broadcast traffic initiated by the first VM as there're no VMs from the
  same private network with the first VM on this compute node
