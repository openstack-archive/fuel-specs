..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================
Network Manager Extension
=========================

https://blueprints.launchpad.net/fuel/+spec/network-manager-extension

--------------------
Problem description
--------------------

In an effort to further modularize Fuel network manager will be moved to an
extension. Network manager as an extension will allow alternative
implementations in the future. This will help to create well-defined interfaces
between components in Nailgun.

----------------
Proposed changes
----------------

All current network manager code, models, and objects will be moved into an
extension [#nailgun_extensions]_. Network manager (and its subclasses)
currently have a de facto public interface (defined as methods which are called
from outside of NetworkManager and tests) which consists of the following
methods:

        * prepare_for_deployment
        * prepare_for_provisioning
        * assign_vips_for_net_groups
        * get_assigned_vips
        * assign_given_vips_for_net_groups
        * assign_vips_for_net_groups_for_api
        * get_free_ips
        * _get_pxe_iface_name
        * clear_assigned_networks
        * clear_bond_configuration
        * assign_networks_by_default
        * get_network_by_netname
        * _update_attrs
        * update_interfaces_info
        * get_admin_ip_for_node
        * get_admin_interface
        * _get_interface_by_network_name
        * get_ip_by_network_name
        * get_zabbix_url
        * is_same_network
        * is_cidr_intersection
        * is_range_intersection
        * create_admin_network_group
        * update_restricted_networks
        * create_network_groups
        * ensure_gateways_present_in_default_node_group
        * update
        * create_network_groups_and_config
        * get_network_config_create_data
        * get_networks_not_on_node
        * get_lnx_bond_properties
        * get_iface_properties
        * find_nic_assoc_with_ng
        * get_prohibited_admin_bond_modes
        * get_assigned_ips_by_network_id
        * get_admin_networks
        * check_ips_belong_to_ranges
        * get_node_networks
        * assign_vips_for_net_groups_for_api
        * assign_vips_for_net_groups
        * get_node_groups_info
        * generate_vlan_ids_list
        * get_ovs_bond_properties
        * get_node_networks_with_ips
        * get_node_network_mapping
        * assign_networks_by_template

Analysis will be done in order to reduce the number of public methods. For
example, some methods are more appropriate in an object
(get_lnx_bond_properties should be in objects.Bond) or can be replaced with
queries to an object collection where they are called. This will be done to
reduce the burden of implementing alternative network manager extensions.
Requiring extensions to implement 45 methods is excessive.


Web UI
======

No changes required.


Nailgun
=======


Data model
----------

The following Objects (and their related collection) will similarly be moved
from Nailgun core to the extension:

    * Bond
    * IPAddr
    * IPAddrRange
    * NetworkGroup
    * NIC

The following database models related to networking will be moved from
Nailgun core to the extension. The extension will manage future migrations.

    * IPAddr
    * IPAddrRange
    * NetworkBondAssignment
    * NetworkGroup
    * NetworkNICAssignment
    * NetworkingConfig
    * NeutronConfig
    * NodeBondInterface
    * NodeNICInterface


REST API
--------

No new APIs will be added at this time. Existing network-related APIs will be
moved into the extension. These APIs are

    * ClusterVIPHandler
    * NetworkConfigurationVerifyHandler
    * NetworkGroupHandler
    * NeutronNetworkConfigurationHandler
    * NeutronNetworkConfigurationVerifyHandler
    * NovaNetworkConfigurationHandler
    * NovaNetworkConfigurationVerifyHandler
    * TemplateNetworkConfigurationHandler


Orchestration
=============


RPC Protocol
------------

Extension API handlers need to be able to deal with deferred tasks. Currently
it is expected that a task's receiver will be a method of the NailgunReceiver
class. RPCConsumer should take a list of receiver classes and check each of
them for the appropriate method. This list of receiver methods could be
determined by finding all modules in e.g. a nailgun.rpc.receivers group.

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

Do nothing.

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

None

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

None

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

Future changes to network manager, or its related models or objects will have
to be made in the extension.

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Ryan Moe <rmoe@mirantis.com>

Other contributors:
  <launchpad-id or None>

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

    * Move database models to extension.
    * Move API handlers, validators, serializers to extension.
    * Move objects and serializers to extension.
    * Create data pipelines for deployment and provisioning serialization.


Dependencies
============

None

------------
Testing, QA
------------

As this is strictly refactoring work existing test coverage will be sufficient
for verifying these changes.

Acceptance criteria
===================

None

----------
References
----------

.. [#nailgun_extensions] https://blueprints.launchpad.net/fuel/+spec/stevedore-extensions-discovery
