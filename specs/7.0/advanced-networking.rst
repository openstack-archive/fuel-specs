..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Advanced/Flexible networking support in Fuel
============================================

https://blueprints.launchpad.net/fuel/+spec/granular-network-functions

Fuel will be able to provide more flexible networking configurations.
Services will not be tied to networks 1:1. User will be able to create
any number of networks and map them to services (i.e. network roles).
Network roles set for particular node will depend on node roles set (more
exactly, deployment tasks set) and configuration of environment.

It is required to support both "new" and "old" networking strategies
in API/RPC. We need to support "old" one for environments based on earlier
releases.

Nova-Network is not supported for new environments, it is supported for old
ones only.


Problem description
===================

Fuel 6.x has a very straightforward networking configuration procedure.
It's required for environment to use 4-5 networks depending on environment
configuration. Every service uses its own (predefined) network. Furthermore,
most networks are configured on all environment nodes no matter are they
required or not (with the exception of Public network for Fuel 5.1 and later).

There is a bunch of tickets that refer to different user stories:
https://bugs.launchpad.net/fuel/+bug/1272349 (fixed as special case)
https://bugs.launchpad.net/fuel/+bug/1285059 (fixed as special case)
https://bugs.launchpad.net/fuel/+bug/1341026
https://bugs.launchpad.net/fuel/+bug/1355764
https://bugs.launchpad.net/fuel/+bug/1365368
https://bugs.launchpad.net/fuel/+bug/1403440
https://bugs.launchpad.net/fuel/+bug/1415552
https://blueprints.launchpad.net/fuel/+spec/fuel-storage-networks (partly)
https://blueprints.launchpad.net/fuel/+spec/separate-public-floating (partly)


Proposed change
===============

1. Network role is separated from network. Network roles set for every node
will depend on node roles (more exactly, on tasks planned for particular
node roles) and environment's configuration. Network roles are assigned
to networks (M:1), networks are assigned to interfaces (M:1).
Release attributes (fixture) will contain default networking configuration
(or several configurations).

2. Networks can be arbitrary created/deleted by user (limitations: at least
one network must exist for environment, 'admin' network cannot be deleted)
via API (and CLI/UI). Parameters of a particular network can be changed
for each node network group in the environment independently.

3. Different network roles may have different requirements for parameters of
underlying network, networks may have different requirements for parameters of
corresponding network interface (e.g. 'admin' network cannot be placed on
LACP bond interface, 'vlan/private' network role doesn't require L3 setup,
networks with 'public' and 'management' roles should have VIPs).
Such requirements must be described in network flags of particular
network roles. Some flags are to be defined for networks too
(e.g. 'admin' network should not be confused with other ones).

4. Network roles description is located near the tasks description (say,
in separate file nearby, e.g. 'network_roles.yaml'). It can be located in
plugins the same way. Task description has section [network_roles] where
the list of names of network roles required is declared. Network roles
description is loaded the same way as for tasks, into release attributes.
Network role description includes id (name), network properties and metadata.
Id is a string that uniquely identifies the network role.
Network properties are properties required for underlying network such as
CIDR, gateway, VIP(s), topology.
Metadata is a data which is not processed by nailgun and passed into
orchestrator as is. It meets out DSL format and has to be shown in UI in
Network Settings tab. User can see/edit/save its contents.
User can change network roles within particular environment via API.

5. Each node network group may have its own network roles to networks mapping.
Networks are tied to node network group now. So, each node network group has
its own set of networks. This way, network roles to networks mapping can be
individually set for every node network group. When environment is created
one node network group is created in it. It has some networks and some
network roles mapped to them by default. When user creates new
node network group via API, the set of networks is copied from default
node network group to new one. There is no network roles which correspond to a
new node network group by default as no nodes are in there.

6. It will be not mandatory to map all networks to interfaces on every node
(on Interfaces mapping tab). Appropriate warning messages should be provided.
So, it will be not obligatory to use all networks on all nodes. User will be
able to select where to use or not to use particular networks (with some
limitations, e.g. networks with 'admin' and 'management' roles must be mapped).

7. 2-nd stage. Assignment of VIP for network managed by dhcp. It is about
admin-pxe network now. When some network role that requires VIP is mapped
there, IP address should be reserved via dnsmasq. This can be done as a
separate deployment task or as a predeployment hook. Admin-pxe network is not
allowed to hold non-admin network roles while it is shared between environments
though.

8. 2-nd stage. Provide an ability to share network (L2/L3 parameters) between
several node network groups. As for now, each particular node network group
have its own L2/L3 parameters for every network. It is 1:1 mapping. It will be
possible to share arbitrary networks (use shared L2/L3 parameters) between
several node network groups. It will be possible to use completely arbitrary
mapping via API (may be CLI as well) and UI will support two options: share
particular network among all node network groups within environment or create
separate network (L2/L3 parameters) for every node network group.


Alternatives
------------

This feature can be treated as a composition of several smaller changes. Some
of them can be implemented separately. E.g. separation of network and network
role (the basic part of this whole ticket), automatic setup of dnsmasq (for
VIP assignment), share network (L2/L3 parameters) between several node network
groups. Although, all those stories are connected and smaller changes enhance
user experience related to the main story - separation of network and network
role.

Another way is implementation of particular user-stories. We use this approach
(e.g. with https://bugs.launchpad.net/fuel/+bug/1272349) when necessary
but such fixes lead to degradation of design consistency and code support
experience.


Data model impact
-----------------

Relationships between entities will be changed:

"network roles" set for particular node depends on environment configuration
and deployment tasks relevant for the node, i.e. it is the same for all nodes
in given environment which have the same set of node roles. "network roles" to
"tasks" mapping should be set in tasks descriptions. Network roles descriptions
will be gathered into release attributes as tasks descriptions are gathered.
When environment is created network roles descriptions are copied into cluster
attributes together with ones loaded from plugins. So, cluster has its own set
of network roles based on corresponding set of tasks. Although, set of
network roles is unique for every node network group in cluster. It depends on
node set in particular node network group at the moment. This set itself is not
saved anywhere. It is calculated on API request. But the set of network roles
assigned to particular network is saved in "network" entity in DB.


"network" entity contains L2, L3 parameters: cidr, gateway, ip ranges, vlan id,
topology.

Each "network" can have all the parameters defined: cidr, gateway, ip ranges,
vlan id. Some of these parameters can be omitted by user for particular
node network group. List of obligatory parameters for every "network role"
should be defined in "network role" metadata (in fixture). Corresponding list
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

1. "network roles" set is unique within a release, it is set in release
attributes (fixture). "release" owns "network roles".
2. "network groups" set is unique within an environment, network groups are
managed via API. "cluster" owns "network groups".
3. "networks" set is unique within a node network group (one network can be
bound to one or several node network groups), networks are managed via API.
"cluster" owns non-admin "networks". admin "networks" are global.
4. "node network group" set is global, node network groups are managed via API.
5. "node roles" to "network roles" mapping is unique within a release,
it is set in release attributes (fixture).
6. "network roles" to "network groups" mapping is unique within an environment,
it is set via API.
7. "network groups" to "networks" mapping is unique within an environment,
it is set when "network" is created (i.e. when cluster is created or when new
"network group" is created or when node from new "node network group" is added
into cluster) and cannot be changed via API directly.
8. "networks" to "node network groups" mapping is unique within an environment
(admin "networks" to "node network groups" mapping is global), it cannot be
changed via API in the 1-st stage.
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
- node_roles (M:M relationship w node_roles)
- release_id (FK to releases)
- network_group_id (FK to network_groups)
- meta (network flags)

Change "network_groups" table:
- id
- name
- cluster_id (FK to clusters)
- meta (network flags)

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

Add table "nodes_to_networks" to serve nodes to networks M:M relationship.
Add table "nodes_roles_to_network_roles" to serve
nodes_roles to network_roles M:M relationship.
Add table "node_network_groups_to_networks" to serve
node_network_groups to networks M:M relationship.

REST API impact
---------------

Add "/clusters/x/network_configuration/network_roles/" url
to get network_roles and their properties,
to get/set "network role" -> "network group" mapping.
This url is optional, TBD.

Add "/clusters/x/network_configuration/network_groups/" url
to add/delete/modify network groups and
to get/set "network role" -> "network group" mapping.

Add "/clusters/x/network_configuration/networks/" url
to configure networks' parameters and add/delete networks.

Add "/clusters/x/network_configuration/configuration" url
to get/set common environment networking parameters (e.g. neutron parameters).

2-nd stage: Modify "/nodegroups/x/" handler to add an ability
to get/set "network" -> "node network group" mapping.

Manage admin networks with the same handlers
("/clusters/x/network_configuration/networks/")
or create dedicated ones? Admin networks are out of clusters actually but can
be treated as in-cluster networks.
Is support of old API required?


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

Feature Lead: Aleksey Kasatkin

Mandatory Design Reviewers: Andrew Woodward, Chris Clason, Sergey Vasilenko

Developers: Aleksey Kasatkin, Vitaly Kramskikh, Sergey Vasilenko,
            Andrew Woodward, Ivan Kliuk

QA: Igor Shishkin


Work Items
----------

1-st stage (7.0 release).

* Nailgun:
   a. Refactoring and versioning of network manager.
      (Estimate: 1.5-2w)
   b. Change DB schema (add new func) and fix network manager, API and
      serialization for orchestrator (to support old func in new DB schema).
      Ensure it does not break current workflow and interacts with Library
      properly (take multi-cl-l2 API into account?).
      (Estimate: 2-3w + QA time)
   c. Add new network manager, API and serialization for orchestrator. Ensure
      it interacts with UI and Library parts properly.
      (Estimate: 2-3w + QA time)
   d. Provide an ability to work with 'old' environments via new API.
      (Estimate: 1-1.5w + QA time)
   e. Networking parameters checker update.
      (Estimate: 1w)
   f. Validation for new API handlers.
      (Estimate: 0.5-1w)

* Network verification tool:
   a. Update and extend verification according to new configuration management.
      Under consideration. Update of nailgun part maybe enough.

* UI:
   a. Networks and network roles management
   b. Change format for networks parameters
      (Estimate: 8w in total?)

* Library:
   a. Decoupling of networks and roles in manifests.
      (Estimate: ?)

* CLI:
   a. Add new functionality (network roles, new networks mapping)
      (Estimate: 2w in total)

2-nd stage is preliminarily planned to 7.1 release.


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

* User is able to create/delete networks and setup L2/L3 parameters for them
  (minimum number of networks is one).

* Names of the networks are set by user (with some possible limitations).

* Network roles set for every particular node depends on node roles and
  environment's setup.

* User is able to map network roles to networks almost freely (This mapping is
  environment-wide, so user is able to set mapping for all nodes in one turn.
  Only relevant network roles will actually be mapped for each particular
  node.).

* There is a default network roles to networks mapping which is provided by
  backend (it should work for simple environments, with our VB scripts).

* Validation of provided networking scheme and parameters is done on backend
  (probably on UI and by network verification tool also).

* It's not obligatory to setup all networks of particular node and map them to
  node's interfaces. Some networks may remain unmapped if they are not needed
  on particular node.

* Network roles description (with their mapping to node roles) and default
  networks' configuration is defined in release attributes (fixture).

* Admin-PXE network have some limitations: Admin-PXE role is always mapped to
  it, it cannot be deleted, it cannot be added to bonds of some types (TBD).

* There should be an ability to define multiple IP subnets for floating IP
  ranges.

* 2-nd stage: CLI/API only: There is an ability to share network between
  several node (network) groups or to use separate L2/L3 parameters for each
  node (network) group. Mapping of networks to node (network) groups
  via CLI/API can be completely arbitrary.

* 2-nd stage: There is a special case when network managed by dhcp needs VIPs
  to be assigned. IP addresses should be reserved via dnsmasq. This can be done
  as a separate task or as a predeployment hook.


Documentation Impact
====================

The documentation should describe new networking architecture of Fuel,
changes and new features in networking configuration process in UI.


References
==========

https://blueprints.launchpad.net/fuel/+spec/granular-network-functions
