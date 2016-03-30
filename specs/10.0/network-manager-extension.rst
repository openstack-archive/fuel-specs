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

All current network manager code (everything in network/\*), models, tasks,
objects, and serializers will be moved into an extension
[#nailgun_extensions]_. The network manager extension will be responsible for
returning the correct NetworkManager instance. ``Cluster.get_network_manager``
will just have pass the current cluster instance to the extension. Network
manager currently has a de facto public interface (defined as methods which
are called from outside of NetworkManager and tests) which consists of the
following methods:

		* ``_get_interface_by_network_name``
		* ``_get_pxe_iface_name``
		* ``_update_attrs``
		* ``assign_given_vips_for_net_groups``
		* ``assign_networks_by_default``
		* ``assign_networks_by_template``
		* ``assign_vips_for_net_groups_for_api``
		* ``assign_vips_for_net_groups``
		* ``check_ips_belong_to_ranges``
		* ``clear_assigned_networks``
		* ``clear_bond_configuration``
		* ``create_admin_network_group``
		* ``create_network_groups_and_config``
		* ``create_network_groups``
		* ``ensure_gateways_present_in_default_node_group``
		* ``find_nic_assoc_with_ng``
		* ``generate_vlan_ids_list``
		* ``get_admin_interface``
		* ``get_admin_ip_for_node``
		* ``get_admin_networks``
		* ``get_assigned_ips_by_network_id``
		* ``get_assigned_vips``
		* ``get_free_ips``
		* ``get_iface_properties``
		* ``get_ip_by_network_name``
		* ``get_lnx_bond_properties``
		* ``get_network_by_netname``
		* ``get_network_config_create_data``
		* ``get_networks_not_on_node``
		* ``get_node_groups_info``
		* ``get_node_network_mapping``
		* ``get_node_networks_with_ips``
		* ``get_node_networks``
		* ``get_ovs_bond_properties``
		* ``get_prohibited_admin_bond_modes``
		* ``get_zabbix_url``
		* ``is_cidr_intersection``
		* ``is_range_intersection``
		* ``is_same_network``
		* ``prepare_for_deployment``
		* ``prepare_for_provisioning``
		* ``update_interfaces_info``
		* ``update_restricted_networks``
		* ``update``


Analysis will be done in order to reduce the number of public methods. For
example, some methods are more appropriate in an object
(``get_lnx_bond_properties`` should be in ``objects.Bond``) or can be replaced
with queries to an object collection where they are called. This will be done
to reduce the burden of implementing alternative network manager extensions.
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
    * NovaNetworkConfig

Any relationship between core and extension models will be removed.
Relationships between core models and extension models will not be allowed.

Many relationships and properties can be converted into object methods in the
appropriate object.

    * Node.nic_interface and Node.bond_interfaces can be retrieved using
      objects.NICCollection.filter() and objects.BondCollection.filter()
      respectively.
    * The Cluster.network_groups property can be implemented in terms of
      objects.NetworkGroupCollection.filter().
    * Cluster.network_config can be removed. A NetworkConfig object can be
      provided by the extension. Anything that relies on this property belongs
      in the network manager extension.


REST API
--------

No new APIs will be added at this time. Existing network-related APIs will be
moved into the extension. These APIs are:

.. list-table::
    :header-rows: 1

    * - URL
      - Handler
    * - /api/v1/clusters/:cluster_id>network_configuration/ips/:ip_addr_id/vips/
      - ClusterVIPHandler
    * - /api/v1/clusters/:cluster_id>network_configuration/ips/vips/
      - ClusterVIPCollectionHandler
    * - /api/v1/networks/
      - NetworkGroupCollectionHandler
    * - /api/v1/networks/:id/
      - NetworkGroupHandler
    * - /api/v1/clusters/:cluster_id/network_configuration/neutron/
      - NeutronNetworkConfigurationHandler
    * - /api/v1/clusters/:cluster_id/network_configuration/neutron/verify/
      - NeutronNetworkConfigurationVerifyHandler
    * - /api/v1/clusters/:cluster_id/network_configuration/nova_network/
      - NovaNetworkConfigurationHandler
    * - /api/v1/clusters/:cluster_id/network_configuration/nova_network/verify/
      - NovaNetworkConfigurationVerifyHandler
    * - /api/v1/clusters/:cluster_id/network_configuration/template/
      - TemplateNetworkConfigurationHandler
    * - /api/v1/clusters/:cluster_id/network_configuration/deployed/
      - NetworkAttributesDeployedHandler


Orchestration
=============

The following methods exist in NetworkManager solely for use in orchestrator
serializers.

    * ``get_iface_properties``
    * ``get_node_networks``
    * ``get_node_networks_with_ips``
    * ``get_node_network_mapping``

These methods can be moved from NetworkManager into one or more data pipelines
[#data_pipelines]_ in the extension.

RPC Protocol
------------

Extension API handlers need to be able to deal with deferred tasks. Currently
it is expected that a task's receiver will be a method of the NailgunReceiver
class. RPCConsumer should take a list of receiver classes and check each of
them for the appropriate method. This list of receiver methods could be
determined by finding all modules in e.g. a nailgun.rpc.receivers group.

The following tasks will be moved into the extension:

    * ``VerifyNetworksTask``
    * ``UpdateDnsmasqTask``

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
    * Move constants into extension.
    * Move network manager tests into extension.
    * Create data pipelines for deployment and provisioning serialization.
    * Reduce number of public methods provided by NetworkManager


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

Nothing in Nailgun's core should depend on objects, models, serializers or
anything else provided by the network manager extension.

----------
References
----------

.. [#nailgun_extensions] https://specs.openstack.org/openstack/fuel-specs/specs/9.0/stevedore-extensions-discovery.html
.. [#data_pipelines] https://specs.openstack.org/openstack/fuel-specs/specs/9.0/data-pipeline.html
