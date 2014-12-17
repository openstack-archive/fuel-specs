..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================================
Add provider for native linux bridges to L23network
===================================================

Related links:

* https://blueprints.launchpad.net/fuel/+spec/refactor-l23-linux-bridges
* https://docs.google.com/a/mirantis.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4

Problem description
===================

For network configuration FUEL use L23network puppet module. In this module no
support for native linux bridges. Also support for native linux bonding
implemented as part of Ifconfig resource, not as puppet provider for Bond
resource.

This blueprint proposed following changes:

* implement provider for native linux bridging
* implement provider for changing configuration files for Centos and Ubuntu
* migrate from puppet template engine to FileMapper (l23_store_config custom
  type)

Proposed change
===============

L23network initial process
--------------------------
Initial setup of L23network. Use_* and install_* parameters allow deployer to
block some functionality and installing packets. It may need for highly
customized configurations.

.. code-block:: puppet

  class { 'l23network':
      use_ovs            => true,
      install_ovs        => true,
      use_lnx            => true,
      install_brctl      => true,
  }

I propose, by default, to install all available packages and enable all base
functionality. But it may be a cause for discussion.

L23_stored_config custom type
-----------------------------

This resource implemented for manage interfaces config files. Each possible
parameter should be described in type.
This resource allow us to forget ERB templates, because for some cases (i.e.
bridge + port with same name + ip address for this port) we should modificate
config file content triple.

.. code-block:: puppet

    l23_stored_config { 'br1':
      onboot   => true,
      method   => manual,
      mtu      => 1500,
      provider => lnx
    }

Place of config files location defined inside provider for corresponded
operation system (and provider -- in the future).

L2::Bridge
----------

This resource implemented for runtime configiration of bridge and call
l23_stored_config for store config.

.. code-block:: puppet

    l23network::l2::bridge { 'br1':
      ensure          => present,
      external_ids    => "bridge-id=${name}",
      provider        => lnx,
    }

Internals:

Puppet definition l23network::l2::bridge contains:

* call L23_stored_config to change persistent interface configuration.
* call L2_bridge to configure bridge in runtime
* make auto-require and auto-before for corresponded resources if it need.


L2::Port
--------
Resource for configuring port L2 options. Only L2 options. For configuring
L3 options -- use *L23network::l3::ifconfig* resource

.. code-block:: puppet

  l23network::l2::port { 'eth1.101':
    ensure    => present,
    bridge    => 'br1',  # port should be a member of given bridge. If no value
                         # given this property was unchanged, if given 'absent'
                         # port will be excluded from any bridges.
    mtu       => 9000,   # MTU value, unchanged if absent.
    onboot    => true,   # whether port has UP state after setup or node boot
    #ethtool   => {},
    provider  => lnx
  )

Alternative VLAN definition

.. code-block:: puppet

  l23network::l2::port { 'vlan77':
    vlan_id   => 77,
    vlan_dev  => eth1,
    provider  => lnx
  )

Internals:

Puppet definition l23network::l2::port contains:

* call L23_stored_config to change persistent interface configuration.
* call L2_port to configure port in runtime
* check for existing bridge, if it need.
* make auto-require and auto-before for corresponded resources if it need.


L2::Bond
--------
It's a special type of port. Designed for bonding two or more interfaces.


L3::Ifconfig
------------
Resource for configuring IP addresses on interface. Only L3 options.
For configuring L2 options -- use corresponded L2 resource.

.. code-block:: puppet

  l23network::l3::ifconfig { 'eth1.101':
    ensure           => present,
    ipaddr           => ['192.168.10.3/24', '10.20.30.40/25'],
    gateway          => 192.168.10.1,
    #gateway_metric  => 10,  # different Ifconfig resources should not has
                             # gateways with some metrics
  )


Alternatives
------------
Leave it as-is. Upgrade Open vSwitch to latest LTS and pray.


Data model impact
-----------------
None


REST API impact
---------------
None


Upgrade impact
--------------
None


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
None


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


Work Items
----------

* implement provider for change interface's config files.
* implement providers for native linux resources:

  * bridge
  * port
  * bond


Dependencies
============

* puppetlabs/stdlib
* adrien/filemapper
* adrien/boolean


Testing
=======

We will need to improve devops to support emulating multiple L2 domains so
that systems tests can be run using this topology.

Also will be better implement test cases for periodically run ones on
bare-metal lab.


Documentation Impact
====================

None

References
==========

* Transformations. How it work:
  https://docs.google.com/a/mirantis.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4
