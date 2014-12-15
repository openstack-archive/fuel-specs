..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Make all L23network resources provider-based
============================================

Related links:

* https://blueprints.launchpad.net/fuel/+spec/l23network-refactror-to-provider-based-resources
* https://docs.google.com/a/mirantis.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4

Problem description
===================

For network configuration FUEL use L23network puppet module. It uses for
Openvswitch, native linux L2 and L3 network settings, because this module
provide operation system agnostic interface. Main goals of this blueprint --
provide not only OS agnostic, but provider-agnostic interface. For implement it
all network resources should be provider-based.
At this moment only Openvswitch part made as set of provider-based resources.

I propose refactor this module for achive following aims:

* unify, and make provider-agnostic configuration options for all network
  resources (not only Openvswitch)
* make l23network resources pluggable by provider-based puppet way. As demo, we
  can made Contrail or OpenDaylight plugin.
* improve possibility of combine different provider to the one composite network
  scheme.

Proposed change
===============

L23network initial process
--------------------------
Initial setup of L23network. Use_* and install_* parameters allow deployer to
block some functionality and installing packets. It may need for highly
customized configurations.

.. code-block:: puppet

  class { 'l23network':
      use_ovs            => false,
      install_ovs        => false,
      use_lnx            => true,
      install_brctl      => true,
      install_vlan_tools => true,
      install_bond_tools => true,
      install_eth_tools  => true,
      vendor_specific    => {},
  }

I propose, by default, to install all available packages and enable all base
functionality. But it may be a cause for discussion.

Non-empty vendor-specific field leads to execute pre- and post-setup hooks. This
need for plugin making. For example, pre-setup class may configure
additional repos and/or do anything else for preparing node to use
vendor-specific solution.

In the L23network each resource contains vendor-specific field. This hash, empty
by default, required by plugin-writers. It allows them don't change custom type
code for adding additional parameters. Due inheriting and extending puppet type
(not provider!) is a non-trivial task.

L2::Bridge
----------

Interface:

.. code-block:: puppet

    l23network::l2::bridge { 'br1':
      ensure          => present,
      stp             => true,
      stp_properties  => {
          system_id     => '',
          priority      => '',
          hello_time    => '',
          max_age       => '',
          forward_delay => '',
      },
      bpdu_forward    => true,
      vendor_specific => {},
      external_ids    => {},
      provider        => lnx,
    }

Internals:

Puppet definition l23network::l2::bridge contains:

* converter from hierarchical stp_properties hash to flat stp_* parameters
* call pre-, post- and middle- plugin hooks (if defined)
* call custom puppet type (l2_store_config) to confogure bridge at (re)boot.
* call custom puppet type (l2_bridge) to configure bridge in runtime
* make auto-require and auto-before for corresponded resources af it need.

L2::Port
--------
Juts a port. All parameters will be specifyed later.

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
      mtu       => undef,  # will be calculated automatically if it's possible. Ignored for OVS by design
      vlan_ids  => [0,0],  # vlan IDs for each jack
      provider  => lnx     # (or ovs)
    }

For OVS provider this resource will be implemented as native "patch" interface
type. For LNX -- as veth pair, where interfaces inserted to corresponded bridges
as tagged or not ports.


L2::Tunnel
----------
It's a special type of port, looks like L2::Patch resource.
Designed for connect bridges on different nodes for build one L2
virtual network segment.

.. code-block:: puppet

    l23network::l2::tunnel { 'tun-to-node2':
      peer      => ".....",
      bridge    => 'br1',
      port      => 'br1-xxx1',
      vlan_id   => 0,
      mtu       => undef, # will be calculated automatically if it's possible.
      type      => gre,   # (or vxlan)
      provider  => lnx
    }

Will be supported following types of TUNs:

* Point-to-point GRE TUN
* Point-to-point VXLAN TUN
* Multicast group based VXLAN


L3::Ifconfig
------------
This resource should only configure IP addresses, gateways, etc... All L2
funcionality from this resource will be moded to corresponded provider of
following resource.


Pluggability and multiple OS support
------------------------------------
Each L23network plugin represents as standalone puppet module with strong class
naming rules. For example, for provider XXX plugin should looks like:

.. code:: text

  l23network_xxx
  + lib
  | + puppet
  |   + provider
  |     + l23_store_config               # this providers should be
  |     | + xxx_centos6.rb               # inherited from
  |     | + xxx_centos7.rb               # l23_store_config_base,
  |     | + xxx_ubuntu.rb                # l23_store_config_centos,
  |     | + xxx_another-supported-os.rb  # l23_store_config_ubuntu
  |     + l2_bridge
  |     | + xxx.rb
  |     + l2_bond
  |     | + xxx.rb
  |     + l2_port
  |       + xxx.rb
  |     ...
  + manifests
  | + l2
  | | + bridge_pre.pp
  | | + bridge_middle.pp
  | | + bridge_post.pp
  | | ...
  | + init.pp
  | + params.pp
  + spec
    + will be better if anything was here :)


L23network contains set od custom facts. One of them 'l23_os' should be used in
all L23network puppet resources, because different versions of operation systems
in some cases should be interpreted as different OSes. For example -- centos6
and centos7 are very different distributives by approach to configuration
process.
Each resource has top-level object -- ordinary puppet definition, it contains:

* vendor-specific field -- his hash, empty by default,
  required only for plugins. It allows them don't change custom type
  code for adding non-standart parameters. Due inheriting and extending puppet
  type (not provider!) is a non-trivial task.
* converter for some hierarchical properties hash to flat.
* call plugin hook (if defined) *l23_network_$provider::l2::$resource_pre* with
  same parameters as top-level define.
* call custom puppet type (*l2_store_config*) with corresponded provider to
  configure resource at (re)boot.
  This resource should contains combined provider for each OS for each resource
  type.
* call plugin hook (if defined) *l23_network_$provider::l2::$resource_middle*
* call custom puppet type (*l2_$resource*) with corresponded provider to
  configure resource in runtime
* call plugin hook (if defined) *l23_network_$provider::l2::$resource_post*

Example of call plugin hook:

.. code:: puppet

  $res_define = "l23network_${provider}::l2::bridge_pre"
  if defined ($resource_define) {
    res_title = "${provider}_bridge_pre"
    pram_hash = {
      ensure          => present,
      stp             => true,
      stp_properties  => {
          .....
      },
      bpdu_forward    => true,
      vendor_specific => {},
      external_ids    => {},
      provider        => lnx,
    }
    res_data = {}
    res_data[$res_title] = $param_hash
    create_resources($res_define, $res_data)
  }


This call maked by puppet stdlib create_resource() function.



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

* make low-level L2 network resources provider-based

  * bridge
  * port
  * bond
  * patch

* make support for GRE/vxlan tunneling
* make L3 network resources provider-based
* make 2nd version of network_scheme (remove huge of shit-code)
* add plugability to the init call
* support frequencely used SDN as plugin


Dependencies
============

* adrien/filemapper
* puppetlabs/stdlib
* may be adrien/boolean for comfortable pass boolean values to types.
* may be camptocamp/kmod for managing kernel modules.
* may be kernel23/iproute2 for policy-routing


Testing
=======

We will need to improve devops to support emulating multiple L2 domains so that
systems tests can be run using this topology.

Also will be better implement test cases for periodically run ones on
bare-metal lab.


Documentation Impact
====================

This refactoring should not bring huge changes to the current documentation,
because network_scheme interface will not contains lot of changes. But this
refactoring bring pluggability.
L23network plugin how-to should be written and published.


References
==========

* Transformations. How it work:
  https://docs.google.com/a/mirantis.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4
