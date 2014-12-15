..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Make all L23network resources provider-based
============================================

Related links:

* https://blueprints.launchpad.net/fuel/+spec/l23network-refactror-to-provider-based-resources
* https://docs.google.com/a/mirantis.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4/edit#heading=h.n2krytstn2p

Problem description
===================

L23network puppet module using in FUEL for managing network configuration for
Openvswitch, native linux L2 network stack and L3 network parameters for NICs.
At this moment only Openvswitch part made as provider based.

I propose refactor this module for achive following aims:

* unify, and make provider-agnostic configuration options for all network
  resources (not only Openvswitch)
* make l23network resources pluggable by provider-based puppet way. As demo, we
  can made Contrail or OpenDaylight plugin.
* improve possibility of combine different provider to the one composite network
  scheme.

Proposed change
===============

L2::Bridge
----------

L2::Port
--------


L2::Bond
--------
It's a special type of port. Designed for bonding two or more interfaces.


L2::Patch
---------
It's a special type of port.
Designed for connect bridges inside one physical host to one
L2 virtual network segment.

.. code-block:: puppet

    l23network::l2::patch { 'br1-to-br2':
      bridges   => ['br1', 'br2'],
      ports     => ['br1-xxx1', 'br2-xxx2'],  # patchcord jack's names
      vlan_ids  => [0,0],  # vlan IDs for each jack
      provider  => lnx  # (or ovs)
    }

For OVS provider this resource will be implemented as native "patch" interface
type. For LNX -- as veth pair, where interfaces inserted to corresponded bridges
as tagged or not ports.


L2::Tunnel
----------
It's a special type of port.
Designed for connect bridges on different nodes to one L2
virtual network segment. It looks like L2::Patch resource.

.. code-block:: puppet

    l23network::l2::tunnel { 'tun-to-node2':
      peer      => ".....",
      bridge    => 'br1',
      port      => 'br1-xxx1',
      vlan_ids  => 0,
      type      => gre,  # (or vxlan)
      provider  => lnx
    }

Will be supported following types of TUNs:

* Point-to-point GRE TUN
* Point-to-point VXLAN TUN
* Multicast group based VXLAN



L3::Ifconfig
------------



Alternatives
------------

Leave it as-is. This will limit our ability to deploy configure some specific
vendor-based solutions, that incompotible with open vSwitsh.


Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Backward compatibility will achived by API versioning.

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

None

Other deployer impact
---------------------

List of supporting operation systems will be extended.
New OSes can be added by plugin.

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  * Sergey Vasilenko (xenolog) <svasilenko@mirantis.com>

Other contributors:
  * Stanislaw Bogatkin (sbogatkin) <sbogatkin@mirantis.com>
  * Dmitry Ilyin (idv1985) <dilyin@mirantis.com>
  * Andrey Danin (adanin) <adanin@mirantis.com>

Work Items
----------

* Make low-level L2 network resources provider-based
* Make support for GRE/vxlan tunneling
* Make L3 network resources provider-based
* Support frequencely used SDN as plugin


Dependencies
============

None


Testing
=======

We will need to improve devops to support emulating multiple L2 domains so that
systems tests can be run using this topology.

Also will be better implement test cases for periodically run ones on
bare-metal lab.


Documentation Impact
====================

Current documentation will has not lage changes, because network_scheme
interface shouldn't be changed. But this refactoring give us pluggability.
L23network plugin how-to should be written/published.


References
==========

* Transformations. How it work:
  https://docs.google.com/a/mirantis.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4/edit#heading=h.n2krytstn2p
