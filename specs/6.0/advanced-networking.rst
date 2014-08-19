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
HA environment). Such requirements must be described in network flags of
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
network (L2/L3 parameters) for every node network group.

10. Assignment of VIP for network managed by dhcp. It is about 'admin' network
now. When some network role that requires VIP is mapped there, IP address
should be reserved via dnsmasq. This can be done as a separate task or as a
predeployment hook.

11. Make additional setup of dnsmasq on master node when node network groups
are configured. User should do that by hands now. Doing this automatically
will improve user experience while working with node network groups.

12. It will be not mandatory to map all networks to interfaces on every node
(on Interfaces mapping tab). Appropriate warning messages should be provided.
So, it will be not obligatory to use all networks on all nodes. User will be
able to select where to use or not to use particular networks.

13. More granular network roles are proposed:
https://docs.google.com/a/mirantis.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4/edit#
https://review.openstack.org/#/c/142475/

14. Use network schema for Nova-Network as it is done for Neutron now. This one
is required for enabling support of new features for Nova-Network environments.
Otherwise, new features will be supported for Neutron-enabled deployments only.


Alternatives
------------

This feature is a composition of several smaller enhancements. Some of them
can be implemented separately. E.g. network schema for Nova-Network, automatic
setup of dnsmasq (VIP assignment, node network groups management).

Another way is implementation of particular user-stories. We use this approach
(e.g. with https://bugs.launchpad.net/fuel/+bug/1272349) when necessary
but such fixes lead to degradation of design consistency and
code support experience.


Data model impact
-----------------

Relationships between entities will be changed:

"network roles" set for particular node depends on environment configuration
and node roles, it is the same for all nodes in given environment
with the same set of node roles. "network roles" to "node roles" mapping
should be set in fixture. This mapping cannot be changed via API. User-defined
network roles can be introduced via fixure.

"network" entity contains L2, L3 parameters: cidr, gateway, ip ranges, vlan id.
"network group" entity contains only network's name, its mapping to
"network roles" and list of "networks". All "network" entities with the same
mapping to "network roles" (and having one user-defined name) are combined to
one "network group".

"network role" to "network group" mapping will be 1:1 (and set of networks
will be the same as in Fuel 6.0) for Nova-Network until network schema for
Nova-Network will be implemented.

Each "network" can have all the parameters defined: cidr, gateway, ip ranges,
vlan id. Some of these parameters can be omitted by user for particular
node network group. List of obligatory parameters for every "network role"
should be defined in "network role" meta info in fixture. Corresponding list
for any particular "network" will depend on set of "network roles" mapped to
that "network".

Each environment should have its own (auto created) Admin network group to have
an ability to map network roles to Admin networks. Particular set of Admin
networks in this group will depend on current set of nodes in environment.
It is true for all other networks. So, set of networks for given network group
is changed together with changing of nodes set.

When node network group set of particular environment is changed (while nodes
are added or removed) networks set is also changed. Networks which are
connected to node network groups that are no longer in environment are removed.
Networks for node network groups that were added into environment are created
if corresponding network group has "1 to 1" mapping mode (networks should be
created by UI or by Nailgun - TBD).

Entities uniqueness and methods of definition:

1. "network roles" set is unique within a release, it is set in fixture.
"release" owns "network roles".
2. "network groups" set is unique within an environment, network groups are
managed via API. "cluster" owns "network groups".
3. "networks" set is unique within a node network group (one network can be
bound to one or several node network groups), networks are managed via API.
"cluster" owns non-admin "networks". admin "networks" are global.
4. "node network group" set is global, node network groups are managed via API.
5. "node roles" to "network roles" mapping is unique within a release,
it is set in fixture.
6. "network roles" to "network groups" mapping is unique within an environment,
it is set via API.
7. "network groups" to "networks" mapping is unique within an environment,
it is set when "network" is created (via API) and cannot be changed later.
8. "networks" to "node network groups" mapping is unique within an environment
(admin "networks" to "node network groups" mapping is global),
it is set via API.
9. "nodes" to "node network groups" mapping is global, it is set by nailgun
initially, can be changed via API.
10. there is no explicit "clusters" to "node network groups" mapping, it is got
by nailgun on the base of "nodes" to "node network groups" mapping.

Nailgun DB tables changes:

rename "node_roles" to "nodes_to_node_roles"
rename "roles" to "node_roles"
rename "nodegroups" to "node_network_groups"

Add "network_roles" table:
- id
- name
- node_role_id (FK to node_roles)
- meta (network flags)
- release_id (FK to releases)
- network_groups_id (FK to network_groups)

Change "network_groups" table:
- id
- name
- release_id (FK to releases)
- cluster_id (FK to clusters)

Add "networks" table:
- id
- cluster_id (FK to clusters)
- network_group_id (FK to network_groups)
- node_network_groups (M:M relationship w node_network_groups)
- cidr
- gateway
- ip_ranges
- vlan_start
- nodes (M:M relationship w 'nodes')
- meta (network flags)

Change "node_network_groups" table:
- id
- name
- nodes (1:M relationship w nodes)
- networks (M:M relationship w networks)

Add table "nodes_to_networks" to serve nodes-to-networks M:M relationship.
Add table "node_network_groups_to_networks" to serve
node_network_groups-to-networks M:M relationship.


REST API impact
---------------

Add "/clusters/x/network_configuration/network_roles/" url
to get/set "network role" -> "network" mapping.

Add "/clusters/x/network_configuration/networks/" url
to add/delete networks and configure networks' parameters.

Add "/clusters/x/network_configuration/configuration url
to get/set common environment networking parameters.


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
of one: network roles to networks mapping, networks to interfaces mapping.
In addition, user will be able to create/delete networks. Selection from a
number of default network schemes can be provided via wizard (option).
Node network group are managed from root menu not from environment as they
are independent from environments now.


Performance Impact
------------------

No Nailgun/Library performance impact is expected.
UI performance impact is to be estimated.


Other deployer impact
---------------------

N/A


Developer impact
----------------

Additional logic can be introduced to determine most relevant networking
configurations on the base of environment configuration provided by user - TBD.


Implementation
==============

Assignee(s)
-----------

Feature Lead: Alexey Kasatkin

Mandatory Design Reviewers: Dmitry Borodaenko, Andrey Danin

Developers: Alexey Kasatkin, Vitaly Kramskikh, Sergey Vasilenko, Andrew Woodward

QA: Igor Shishkin


Work Items
----------

* Nailgun:
   a. Change DB schema and serialization for orchestrator.
      Ensure it does not break current API (take multi-cl-l2 API into account?)
      (Estimate: 2-3w)
   b. Change API. Ensure it interacts with UI and Library parts properly.
      (Estimate: 1-1.5w)
   c. Make support of L23 combination (ovs/linux-br/etc.).
      (Estimate: 1-1.5w)
   d. Make support of vip assignment for networks managed by dhcp.
      (Estimate: 1w)
   e. Setup of dnsmasq on master node when node network groups are configured.
      (Estimate: 1w)
   f. Make support of network schema for Nova-Network.
      (Estimate: 1w+qa)

   priorities: a,b - must (0), c - must (1), d,e - should, f - nice to have

* UI:
   a. Node network groups management
   b. Networks and network roles management
   c. Change format for networks parameters

   priorities: a,b,c - must
   (Estimate: 8w in total)

* Library:
   a. Refactoring of network roles.
   spec: https://review.openstack.org/#/c/142475/
   b. ovs/linux-br/etc. combination.
   (Estimate: 1w+bonds)
   c. Make support of vip assignment for networks managed by dhcp.
   d. Setup of dnsmasq on master node when node network groups are configured.
   e. Use network schema for Nova-Network.
   (Estimate: 2w+)

   priorities: a,b - must, c,d - should, e - nice to have

* CLI:
   a. Change Multiple Cluster Networks functionality (node network groups
   are outside cluster).
   b. Add new functionality (network roles, new networks mapping)

   priorities: a,b - must
   (Estimate: 2w in total)


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/multiple-cluster-networks


Testing
=======

* Additional unit/integration tests for Nailgun.
* Additional functional tests for UI.
* Additional System tests against a standalone test environment with altered
  network roles to networks mapping, networks to interfaces mapping,
  with minimal number of networks per environment (one in most cases).

* Some part of old tests of all types will become irrelevant and
  are to be redesigned.

Acceptance Criteria
-------------------

* Each node has one interface. All network roles are assigned to one network
  (no bonding). Networks to interfaces is 1:1.

* Each node has two or more interfaces.
  First (Private) network is for management (including HA for controllers),
  overlay, storage and Fuel admin network roles. Second (Public) network is
  for floating/Public address space. Networks to interfaces is 1:1.

* Controllers have three interfaces: First (Mgmt) network is for management
  (including HA for controllers) and Fuel admin network roles. Second
  (Private) is for overlay and storage network roles. Third (Public) is for
  floating/Public address space. Other nodes have two interfaces: First (Mgmt)
  network is for management and Fuel admin network roles. Second (Private) is
  for overlay and storage. Networks to interfaces is 1:1.


Documentation Impact
====================

The documentation should describe new networking architecture of Fuel,
changes and new features in networking configuration process in UI.
Test cases are to be described in detail in separate document.


References
==========

https://blueprints.launchpad.net/fuel/+spec/advanced-networking
