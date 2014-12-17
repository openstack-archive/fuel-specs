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
* make auto-require and auto-before for corresponded resources af it need.


L2::Port
--------
Just a port. All parameters will be specifyed later.


L2::Bond
--------
It's a special type of port. Designed for bonding two or more interfaces.


Alternatives
------------
Leave it as-is. Upgrade open vSwitsh to latest LTS and pray.


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
