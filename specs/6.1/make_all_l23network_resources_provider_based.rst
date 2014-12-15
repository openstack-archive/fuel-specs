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

For network configuration, Fuel uses L23network puppet module. It is used for
Openvswitch, native linux L2 and L3 network settings, because this module
provides operation system agnostic interface.
The main goal of this blueprint is to provide not only operation system
agnostic, but provider-agnostic interface. To implement
it, all network resources should be provider-based.
At this moment, only Openvswitch part is made as a set of
provider-based resources.

I propose to refactor this module for achieve the following aims:

* unify, and make provider-agnostic configuration options for all network
  resources (not for Openvswitch only)

* make l23network resources pluggable by a provider-based puppet way.
  As a demo, we can made Contrail or OpenDaylight plug-in.

* improve possibility of combining different provider to the one composite
  network scheme.

Proposed change
===============

L23network initial process
--------------------------

Initial setup of L23network. The <use_*> and <install_*> parameters
allow deployer to
block some functionality and packets installation. It may be
required for highly
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

I propose, to install all available packages and enable all base
functionality by default: it requires further discussion.

Non-empty vendor-specific field leads to execute pre- and post-setup hooks.
This is required for plug-in-making. For example, pre-setup class may configure
additional repos and/or do anything else to prepare node to use a
vendor-specific solution.

In the L23network, each resource contains vendor-specific field.
This hash,
empty by default, is required by plug-in-writers. It allows them not to change
custom type code to add extra parameters. Due to inheriting and
extending puppet type (not the provider one), is a non-trivial task.

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

Puppet definition l23network::l2::bridge contains the following:

* converter from hierarchical stp_properties hash to flat stp_* parameters.

* call pre-, post- and middle- plug-in hooks (if defined).

* call custom puppet type (l2_store_config) to configure bridge at (re)boot.

* call custom puppet type (l2_bridge) to configure bridge in runtime.

* make auto-require and auto-before for corresponding resources if needed.

L2::Port
--------

It is just a port. All parameters will be specified later.

L2::Bond
--------

It is a special type of port, designed for bonding two or more interfaces.


L2::Patch
---------

It is a special type of port, designed to connect bridges
inside one physical host to one
L2 virtual network segment.

.. code-block:: puppet

    l23network::l2::patch { 'br1-to-br2':
      bridges   => ['br1', 'br2'],
      ports     => ['br1-xxx1', 'br2-xxx2'],  # patchcord jack's names
      mtu       => undef,  # will be calculated automatically if it's possible.
                           # Ignored for OVS by design
      vlan_ids  => [0,0],  # vlan IDs for each jack
      provider  => lnx     # (or ovs)
    }

For OVS provider, this resource will be implemented as a
native "patch" interface
type. For LNX as a veth pair, where interfaces are inserted to the
corresponding
bridges as (un)tagged ports.


L2::Tunnel
----------

It is a special type of port, that looks like L2::Patch resource.
It is designed to connect bridges on different nodes to build one L2
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

This resource should only configure IP, for example, addresses and gateways.
All L2 funcionality from this resource will be moded to the corresponding
provider of the following resource.


Pluggability and multiple OS support
------------------------------------

Each L23network plug-in represents a standalone puppet module with the strong
class naming rules. For example, for provider named xxx plug-in will look
as follows:

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
    + will be better if anything is here :)


L23network contains a set of custom facts. One of them, 'l23_os' should be used
in all L23network puppet resources, because different versions of operation
systems in some cases should be interpreted as different operations systems.
For example, centos6 and centos7 are very different distributives in terms of
configuration process.
Each resource has top-level object: ordinary puppet definition that contains
the
following:

* vendor-specific field - its hash, empty by default,
  required only for plug-ins. It allows them not to change custom type
  code for adding non-standart parameters. Due to inheriting and extending
  puppet
  type (not the provider one), is a non-trivial task.

* converter for some hierarchical properties hash to flat.

* call plug-in hook (if defined) *l23_network_$provider::l2::$resource_pre*
  with the same parameters as defined at the top-level.

* call custom puppet type (*l2_store_config*) with the corresponding
  provider to
  configure resource at (re)boot.
  This resource should contain combined provider for each operations system
  for each resource type.

* call plug-in hook (if defined) *l23_network_$provider::l2::$resource_middle*.

* call custom puppet type (*l2_$resource*) with the corresponding
  provider to
  configure resource in runtime.

* call plug-in hook (if defined)
  *l23_network_$provider::l2::$resource_post*.

Here is an example of call plug-in hook:

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


This call is made by puppet stdlib create_resource() function.



Alternatives
------------

Leave it as-is. This will limit our ability to deploy and
configure some specific
vendor-based solutions, that are incompatible with Openvswitch.


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

List of supported operation systems will be extended.
New operation systems can be added by a plug-in.

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
* convert interface file to set of files one per interface for Debian OS
  family at init stage
* add pluggability to the init call
* support frequently used SDN as a plug-in


Dependencies
============

* adrien/filemapper
* puppetlabs/stdlib
* may be adrien/boolean for comfortable pass boolean values to types.
* may be camptocamp/kmod for managing kernel modules.
* may be kernel23/iproute2 for policy-routing


Testing
=======

We will have to improve devops to support multiple L2 domains emulation so
that system tests could be run using this topology.

Also it would be nice to implement test cases to run them
periodically on a bare-metal lab.


Documentation Impact
====================

This refactoring should not bring huge changes to the current documentation,
because network_scheme interface will not contain lot of changes. But this
refactoring brings pluggability.
L23network plug-in how-to should be written and published.


References
==========

* Transformations. How it works:
  https://docs.google.com/a/mirantis.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4
