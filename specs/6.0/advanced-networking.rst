..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Advanced networking feature
==========================================

https://blueprints.launchpad.net/fuel/+spec/advanced-networking

Fuel will be able to provide more flexible networking configurations.
Services will not be tied to networks 1:1. User will be able to create
any number of networks and map them to services (i.e. network roles).
Network roles set for particular node will depend on node roles set and
configuration of environment.


Problem description
===================

Fuel 5.0 has a very straightforward networking configuration procedure.
It's required for cluster to use 4-5 networks depending on cluster
configuration. Every service uses its own network. Furthermore, all networks
are configured on all cluster nodes no matter are they required or not.

There is a bunch of tickets that refer to different user stories:
https://bugs.launchpad.net/fuel/+bug/1272349
https://bugs.launchpad.net/fuel/+bug/1285059
https://bugs.launchpad.net/fuel/+bug/1341026
https://bugs.launchpad.net/fuel/+bug/1355764
https://blueprints.launchpad.net/fuel/+spec/fuel-storage-networks (partly)
https://blueprints.launchpad.net/fuel/+spec/separate-public-floating (partly)
https://bugs.launchpad.net/fuel/+bug/1322553


Proposed change
===============

1. Network role is separated from network. Network roles set for every node
will depend on node’s role and cluster configuration. Network roles can be
assigned to networks (M:1), networks to interfaces (M:1). There will be
a number of networks presets in fixture as we have now. Networks flags will
be connected to networks roles not to networks.

2. Networks can be arbitrary created/deleted by user (at least one network
must exist for cluster) via API (and CLI/UI). Parameters of a particular
network can be changed for each nodes’ group in cluster independently.

3. Different network roles may have different requirements for parameters of
underlying network or corresponding network interface (e.g. network with
‘admin’ network role cannot be placed on bond interface, ‘mesh’ network role
doesn’t require L3 setup, network with ‘public’ role should have VIP on
HA cluster). Such requirements must be described in network flags of
particular network roles. We may need to define some flags for networks too
(TBD).

4. There are two types of network roles proposed: mandatory (fixed mapping to
node roles, defined globally, described in fixture) and user-defined (option).


Alternatives
------------

This feature is a composition of several smaller enhancements. Some of them
can be implemented separately. E.g. network addition/removal for particular
nodes' groups, user-defined network roles.

Another way is implementation of particular user-stories. We use this approach
(e.g. with https://bugs.launchpad.net/fuel/+bug/1272349) when necessary
but such fixes lead to degradation of design consistency and
code support experience.

Options to make networking configuration more flexible (optional) - TBD:
1. It is not mandatory to map all networks to interfaces on every node
(on Interfaces mapping tab). Appropriate warning messages should be provided.
2. User can enable/disable the presence of particular network in particular
node group OR particular network can be added/removed for selected
node groups (on Networking configuration tab).
3. User-defined network roles can be added/removed via API, which refer to
particular cluster and node roles within it.


Data model impact
-----------------

Relationships between entities will be changed:

“network roles” set is depended on cluster configuration and nodes roles,
it is the same for all nodes with the same set of node roles. “network roles”
to “node roles” mapping is static and should be set in fixture.
This mapping for mandatory network roles cannot be changed via API.
User-defined network roles can be introduced (TBD, see Alternatives).

“network role” -> “network” mapping can be changed freely by user.
It is 1:1 by default, i.e. it reproduces default networking configuration
that is available without advanced networking feature - TBD.

Every network can have all the parameters defined: cidr, gateway, ip ranges,
vlan id. Some of these parameters can be omitted by user.

node [1:M] interface [1:M] network
cluster [1:M] network role [M:1] network
node group [1:M] network

Entities uniqueness:

1. “network roles” to “node roles” mapping is global (for mandatory
network roles) It is set in fixture.
2. “network roles” to “networks” mapping is unique within a cluster
(option - node group).
3. mandatory “network roles” set is unique globally.
4. user-defined “network roles” set is unique within a cluster (mandatory
“network roles” must be auto-created for every new cluster in this case).
5. “networks” set (their quantity and names) is unique within a cluster
but parameters of every network are unique within a node group
(networks are auto-created for every new node group).

Nailgun DB tables changes:

rename ‘node_roles’ to ‘nodes_to_node_roles’
rename ‘roles’ to ‘node_roles’

Add “network_roles” table:
- id
- name (constant for mandatory network roles, variable for user-defined
    network roles)
- node_role_id (FK to node_roles)
- meta (current network flags)
- release_id (FK to releases)
- cluster_id (FK to clusters)
- node_group_id (FK to node_groups, TBD)

Change “network_groups” table (rename to ‘networks’):
- id
- name (user-defined)
- release_id (FK to releases)
- cluster_id (FK to clusters)
- node_group_id (FK to node_groups)
- cidr
- gateway
- dns_list (TBD)
- ip_ranges
- vlan_start
- node_id (M:M, optional)


REST API impact
---------------

Add “/clusters/x/network_configuration/network_roles/“ url
to get/set “network role” -> “network” mapping (and add/delete networks roles
in future).

Add “/clusters/x/network_configuration/networks/” url
to add/delete networks and configure networks' parameters.

Use old network handlers to get/set common cluster networking parameters.

Network flags (https://etherpad.openstack.org/p/nailgun-network-group-flags)
are set for networks roles now (some of network flags become obsolete - TBD).
We may need to define some flags for networks too - TBD.


Upgrade impact
--------------

Migration of schema and data must be provided to support previously created
environments and creation of environments with older releases. It should
include migration of existing releases, clusters and their nodes data.


Security impact
---------------

No additional security modifications needed.


Notifications impact
--------------------

N/A.


Other end user impact
---------------------

Significant changes are expected in UI with regard to networking configuration
experience. User will be allowed to perform two kinds of mapping instead
of one: network roles to networks mapping, networks to intefaces mapping.
In addition, user will be able to create/delete networks and user-defined
network roles (option). Selection from a number of default network schemes
can be provided via wizard (option).


Performance Impact
------------------

No Nailgun/Library performance impact is expected.
UI performance impact is to be estimated.


Other deployer impact
---------------------

Andrew Woodward, please provide info on that.


Developer impact
----------------

Additional logic can be introduced to determine most relevant networking
configurations on the base of cluster configuration provided by user - TBD.


Implementation
==============

Assignee(s)
-----------

Feature Lead: Alexey Kasatkin

Mandatory Design Reviewers: Dmitry Borodaenko, Andrey Danin

Developers: Alexey Kasatkin, Vitaly Kramskikh, Andrew Woodward

QA: Igor Shishkin


Work Items
----------

* Nailgun implementation - basic items (introduction of network role,
  DB changes)
* Nailgun implementation - basic items (API changes, defaults changes)
* Nailgun implementation - optional items (items listed in Alternatives and
  Developer impact)
* UI design in detail
* UI implementation


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/multiple-cluster-networks


Testing
=======

* Additional unit/integration tests for Nailgun.
* Additional functional tests for UI.
* Additional System tests against a standalone test environment with altered
  network roles to networks mapping, networks to interfaces mapping,
  with minimal number of networks per cluster (one in most cases).

* Some part of old tests of all types will become irrelevant and
  are to be redesigned.


Documentation Impact
====================

The documentation should describe new networking architecture of Fuel,
changes and new features in networking configuration process in UI.
Test cases are to be described in detail in separate document.


References
==========

https://blueprints.launchpad.net/fuel/+spec/advanced-networking
