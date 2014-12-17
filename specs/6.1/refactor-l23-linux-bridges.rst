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

For network configuration Fuel uses L23network puppet module. In this module
there is no support for native linux bridges. Also support for native linux
bonding implemented as part of Ifconfig resource, not as puppet provider for
Bond resource.

This blueprint proposed following changes:

* implement provider for native linux bridging
* implement provider for changing configuration files for Centos and Ubuntu
* migrate from puppet template engine to FileMapper (l23_store_config custom
  type)

Proposed change
===============

L23network initial process
--------------------------
Initial setup of L23network. Use_* and install_* parameters allow Cloud
deployer to block some functionality and installing packets. It may need for
highly customized configurations.

.. code-block:: puppet

  class { 'l23network':
      use_ovs            => true,
      install_ovs        => true,
      use_lnx            => true,
      install_brctl      => true,
  }

This bluprint proposes, by default, to install all available packages and
enable all basic functionality. But it may be a case for discussion.

L23_stored_config custom type
-----------------------------

This resource is implemented to manage interface config files. Each possible
parameter should be described in resource type.

This resource allows to forget about ERB templates, because in some cases
(i.e.  bridge + port with same name + ip address for this port) we should
modificate config file content three times.

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

  l23network::l2::port { 'eth1':
    mtu       => 9000,   # MTU value, unchanged if absent.
    onboot    => true,   # whether port has UP state after setup or node boot
    #ethtool   => {},
    provider  => lnx
  }

  l23network::l2::port { 'eth1.101':
    ensure    => present,
    bridge    => 'br1',  # port should be a member of given bridge. If no value
                         # given this property was unchanged, if given 'absent'
                         # port will be excluded from any bridges.
    onboot    => true,
    #ethtool   => {},
    provider  => lnx
  }

Alternative VLAN definition

.. code-block:: puppet

  l23network::l2::port { 'vlan77':
    vlan_id   => 77,
    vlan_dev  => eth1,
    provider  => lnx
  }

Internals:

Puppet definition l23network::l2::port contains:

* call L23_stored_config to change persistent interface configuration.
* call L2_port to configure port in runtime
* check for existing bridge, if required.
* make auto-require and auto-before for corresponded resources if required.


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
                             # gateways with same metrics
  }


Network Scheme
--------------
Network scheme is a YAML-based definition of network topology for host.
Network scheme is a versionized data structure. Varsion may be:

* **1.0** -- FUEL 6.0 and lower.
* **1.1** -- FUEL 6.1.* -- intermidial variant of format.
* **2.0** -- Future version of declarative format for pluggable L23network.

Network Scheme parsing and implementing by following way:


.. code-block:: puppet

  $fuel_settings = parseyaml($astute_settings_yaml)

  prepare_network_config($::fuel_settings['network_scheme'])
  $sdn = generate_network_config()
  notify {"SDN: ${sdn}": }

  class {'l23network':
    use_ovs => false,
    use_lnx => false
  }

Example of typical network scheme:

.. code-block:: yaml

  ---
  network_scheme:
    version: "1.0"
    provider: lnx
    interfaces:
      eth1:
        mtu: 7777
    transformations:
      - action: add-br
        name: br1
      - action: add-port
        name: eth1
        bridge: br1
      - action: add-br
        name: br-mgmt
      - action: add-port
        name: eth1.101
        bridge: br-mgmt
      - action: add-br
        name: br-ex
      - action: add-port
        name: eth1.102
        bridge: br-ex
      - action: add-br
        name: br-storage
      - action: add-port
        name: eth1.103
        bridge: br-storage
      - action: add-br
        name: br-prv
        provider: ovs
      - action: add-port
        name: test-ovs-prv
        bridge: br-prv
        provider: ovs
  #   - action: add-patch
  #     bridges:
  #       - br-prv
  #       - br1
    endpoints:
      br-mgmt:
        IP:
          - 192.168.101.3/24
        gateway: 192.168.101.1
        gateway-metric: 100
        routes:
          - net: 192.168.210.0/24
            via: 192.168.101.1
            metric: 10
          - net: 192.168.211.0/24
            via: 192.168.101.1
          - net: 192.168.212.0/24
            via: 192.168.101.1
      br-ex:
        gateway: 192.168.102.1
        IP:
          - 192.168.102.3/24
      br-storage:
        IP:
          - 192.168.103.3/24
      br-prv:
        IP: none
    roles:
      management: br-mgmt
      private: br-prv
      fw-admin: br1
      ex: br-ex
      storage: br-storage


Alternatives
------------
Leave it as-is. Upgrade Open vSwitch to latest LTS and hope that bonding was
fixed.

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
that systems tests can be run using this topology. For more advancing testing
it's required OVS support by devops

Also will be better implement test cases for periodically run ones on
bare-metal lab.


Documentation Impact
====================

The Documentation should be updated to explain the topologies and scenarios
for Cloud Operators

References
==========

* Transformations. How it work:
  https://docs.google.com/a/mirantis.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4
