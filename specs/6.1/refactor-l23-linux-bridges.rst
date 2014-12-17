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

l23_store_config custom type
----------------------------

This resource implemented for changing part of config file by mappind
according to given key/value mapping

.. code-block:: puppet

    l23_store_config { "l2_$interafce":
        file   => "ifcfg-$interface",
        config => {
            DEVICE    => eth1,
            BRIDGE    => br1,
            ONBOOT    => yes,
        },
    }

Place of file location defined inside providerfor corresponded operation
system.

L2::Bridge
----------

Interface:

.. code-block:: puppet

    l23network::l2::bridge { 'br1':
      ensure          => present,
      external_ids    => "bridge-id=${name}",
      provider        => lnx,
    }

Internals:

Puppet definition l23network::l2::bridge contains:

* call custom puppet type (l23_store_config) to change network interface
  configuration file.
* call custom puppet type (l2_bridge) to configure bridge in runtime
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

* adrien/filemapper
* puppetlabs/stdlib


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
