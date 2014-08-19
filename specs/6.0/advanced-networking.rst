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

It is required to support both "new" and "old" networking strategies
in API/RPC. We need to support "old" one for environments based on earlier
releases.

MVP implementation will support new features at least for Neutron-enabled
deployments.


Problem description
===================

Fuel 6.0 has a very straightforward networking configuration procedure.
It's required for environment to use 4-5 networks depending on environment
configuration. Every service uses its own (predefined) network. Furthermore,
all networks are configured on all environment nodes no matter are they
required or not (with the exception of Public network for Fuel 5.1 and later).

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
will depend on node role and environment's configuration. Network roles are
assigned to networks (M:1), networks are assigned to interfaces (M:1).
Fixture will contain both network roles description (with their mapping to
node roles) and default networks configuration (or several configurations).

2. Node network groups (former node groups) are moved out from environment.
Node network groups will be created and managed independently from
environments. Nodes should be distributed among node network groups before
being added to environments.

3. Networks can be arbitrary created/deleted by user (limitations: at least
one network must exist for environment, 'admin' network cannot be deleted)
via API (and CLI/UI). Parameters of a particular network can be changed
for each node network group in the environment independently.

4. Different network roles may have different requirements for parameters of
underlying network or corresponding network interface (e.g. network with
'admin' network role cannot be placed on bond interface, 'mesh' network role
doesn't require L3 setup, network with 'public' role should have VIP on
HA cluster). Such requirements must be described in network flags of
particular network roles. Some flags are to be defined for networks too
(e.g. 'admin' network should not be confused with other ones).

5. There are two types of network roles proposed: mandatory (fixed mapping to
node roles, described in fixture) and user-defined (optional, can be added
to fixture manually).

6. Additional 'network group' entity is introduced. It describes
environment-wide network's parameters (name, mapping to network role, etc.).
L2/L3 parameters are node network group-wide and they are stored in 'network'
entity. So, real objects mapping is a bit more complex than it is written in
1st chapter: network roles are assigned to network groups (M:1), network groups
are assigned to networks (1:M), networks are assigned to interfaces (M:1).
Network group contains several networks (1:M), node network group contains
several networks (1:M), environment contains several network groups (1:M).
DB relations are not the same (see Data model impact).

7. Provide an ability to use mixture of different L23 providers within one
environment. OVS is the only supported solution in API/CLI/UI currently.
It is highly desirable to have an ability to use Linux bridges/contrail/etc.
providers independently or in mixture. Apparently, it will not be possible to
have arbitrary mixture out of the box though, specific cases should be covered
using specialized plugins.

8. Get rid of separate nova-network and neutron urls. We use unified objects,
objects interconnection and data processing procedures (with minor differences
which are reflected in NetworkManager code mostly) for both providers so it
seems reasonable to use unified API urls and handlers. Old handlers should stay
as is. It is not the first priority task though.

9. Provide an ability to share network (L2/L3 parameters) between several
node network groups. As for now, each particular node network group have its
own L2/L3 parameters for every network. It is 1:1 mapping. It will be possible
to share arbitrary networks (use shared L2/L3 parameters) between several
node network groups. It will be possible to use completely arbitrary mapping
via API (may be CLI as well) and UI will support two options: share particular
network among all node network groups within environment or create separate
network object for every node network group.


. Use network schema for Nova-Network as it is done for Neutron now. This one
is required for enabling support of new features for Nova-Network environments.
Otherwise, new features will be supported for Neutron-enabled deployments only.


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
3. User-defined network roles can be added/removed via fixture.


Data model impact
-----------------

Relationships between entities will be changed:

"network roles" set is depended on cluster configuration and nodes roles,
it is the same for all nodes with the same set of node roles. "network roles"
to "node roles" mapping is static and should be set in fixture.
This mapping for mandatory network roles cannot be changed via API.
User-defined network roles can be introduced (TBD, see Alternatives).

"network group" entity contains only networks' names and some user-defined
flags may be. "network" entity contains L2, L3 parameters: cidr, gateway,
ip ranges, vlan id.

"network role" -> "network group" mapping can be changed by user.
It is 1:1 by default, i.e. it reproduces default networking configuration
that is available without advanced networking feature - TBD.

Every "network" can have all the parameters defined: cidr, gateway, ip ranges,
vlan id. Some of these parameters can be omitted by user for particular
node group. All the network parameters can be left unconfigured for particular
node group when there are no nodes in the group use this network.

node [1:M] interface [1:M] network
cluster [1:M] network role [M:1] network group
node group [1:M] network

Entities uniqueness:

1. "network roles" to "node roles" mapping is global (for mandatory
network roles) It is set in fixture.
2. "network roles" to "network groups" mapping is unique within a cluster.
3. "network roles" set is unique globally.
4. "network groups" set is unique within a cluster but parameters of every
"network" are unique within a node group (networks are auto-created for every
new node group).

Nailgun DB tables changes:

rename 'node_roles' to 'nodes_to_node_roles'
rename 'roles' to 'node_roles'

Add "network_roles" table:
- id
- name (constant for mandatory network roles, variable for user-defined
network roles)
- node_role_id (FK to node_roles)
- meta (current network flags)
- release_id (FK to releases)
- cluster_id (FK to clusters)
- network_groups_id (FK to network_groups)

Change "network_groups" table:
- id
- name (user-defined)
- release_id (FK to releases)
- cluster_id (FK to clusters)
- meta (network flags if any, TBD)

Add "networks" table:
- id
- cluster_id (FK to clusters)
- node_group_id (FK to node_groups)
- cidr
- gateway
- dns_list (TBD)
- ip_ranges
- vlan_start
- node_id (M:M)

Add table 'nodes_to_networks' to serve nodes-to-networks M:M relationship.


REST API impact
---------------

Add "/clusters/x/network_configuration/neutron/network_roles/" url
to get/set "network role" -> "network" mapping.

Add "/clusters/x/network_configuration/neutron/networks/" url
to add/delete networks and configure networks' parameters.

Add "/clusters/x/network_configuration/neutron/configuration url
to get/set common cluster networking parameters.

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
In addition, user will be able to create/delete networks. Selection from a
number of default network schemes can be provided via wizard (option).


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

Acceptance Criteria
-------------------

* Each node has one interface. All network roles are assigned to one network
  (no bonding). Networks to interfaces is 1:1.

* Each node has two or more interfaces (two NICs or one NIC and one bond).
  First (Private) network is for management (including HA for controllers),
  overlay, storage and Fuel admin network roles. Second (Public) network is
  for floating/Public address space. Optionally the second network can be on
  a bond. Networks to interfaces is 1:1.

* Controllers have three interfaces: First (Mgmt) network is for management
  (including HA for controllers) and Fuel admin network roles. Second
  (Private) is for overlay and storage network roles. Third (Public) is for
  floating/Public address space. Other nodes have two interfaces: First (Mgmt)
  network is for management and Fuel admin network roles. Second (Private) is
  for overlay and storage. Networks to interfaces is 1:1. Second
  interface can be a bond (with Private network).


Documentation Impact
====================

The documentation should describe new networking architecture of Fuel,
changes and new features in networking configuration process in UI.
Test cases are to be described in detail in separate document.


References
==========

https://blueprints.launchpad.net/fuel/+spec/advanced-networking
