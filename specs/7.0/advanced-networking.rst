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
orchestrator as is. It meets our DSL format and has to be shown in UI in
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

Relationships between entities:

"network roles" to "tasks" mapping should be set in tasks descriptions.
Network roles descriptions will be gathered into release attributes as tasks
descriptions are gathered.
When environment is created network roles descriptions are copied into cluster
attributes together with ones loaded from plugins. So, cluster has its own set
of network roles based on corresponding set of tasks.
Cluster's node roles and tasks are traversed to gather information on how
network roles are connected with node roles. This info is required for UI as
it knows nothing about tasks. This info is saved into network roles
descriptions in cluster's attributes.

Set of network roles for particular node depends on environment configuration
and deployment tasks relevant for the node, i.e. it is the same for all nodes
in given environment which have the same set of node roles.
Set of network roles is unique for every node network group in cluster.
It depends on node set in particular node network group at the moment.
These sets (network roles to node, network roles to node network group) are
not saved anywhere. They are calculated on API request if it is required for UI
(TBD: as an option, UI itself could calculate these dependencies).
But the set of network roles assigned to particular network is saved in
"network" entity in DB. Nailgun must ensure network roles are not duplicated on
different networks within one node and within one node network group.

"network" entity contains the parameters: cidr, gateway, ip ranges, vlan id,
topology. Each "network" may have all the parameters defined. Some of these
parameters can be omitted by user for particular node network group.
List of obligatory parameters for every "network role" should be defined in
"network role" network properties. Corresponding list for any particular
"network" will depend on set of "network roles" mapped to that "network".

When node network groups of particular environment are created/removed networks
are affected. Networks which were connected to node network groups that are
no longer in environment are removed. Networks for node network groups that
were added into environment are created. No default network roles to networks
mapping is done for new node network group as it contains no nodes while being
added into cluster (so, no network roles are required).

Networks metadata which is now stored in release (
networks_metadata.nova_network and networks_metadata.neutron) is not required
for 7.0 environments. Only default admin-pxe network will have some metadata
(limitations). Other networks are created by user and their properties fully
depend on user (i.e. API) input. More precisely, network properties are partly
set via API directly and partly depend on network roles which are assigned
to them.

Nailgun DB tables changes:

rename "nodegroups" to "node_network_groups"
rename "network_groups" to "networks"

Change "networks" table:
- change node_network_groups (change to M:M relationship w node_network_groups)
- add network_roles (JSON - list of network roles names)
- add short_name (string - will be used as corresponding endpoint name)
- add meta_dsl (JSON - new meta described using our DSL)

"networking_configs" table is not in use for 7.0 environments as all settings
are moved to network roles metadata.

Add table "node_network_groups_to_networks" to serve
node_network_groups to networks M:M relationship.


REST API impact
---------------

Add "/clusters/x/network_configuration/networks/" url
to configure networks' parameters, add/delete networks, assign network roles.

Admin-pxe networks will be managed using the same handlers
("/clusters/x/network_configuration/networks/") - nothing is changed here for
clients but there are changes in nailgun as networks to node_network_groups
mapping become M:M.

Old environments (6.1 and older) should be accessible via both new and old
API handlers. But support of old environments via new API handlers may be
postponed to 2nd stage.
New environments should be accessible via both new and old API handlers.


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
In addition, user will be able to create/delete networks.


Performance Impact
------------------

No Library performance impact is expected.
There will be some performance impact for Nailgun as additional traversing of
deployment tasks and copying/creation of objects will be required within a
number of API calls (cluster create, node network group create, node add).
It should not affect user experience noticeably.
UI performance impact is to be estimated.


Other deployer impact
---------------------

N/A


Developer impact
----------------

N/A


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
   a. Switch to ML2 and multiple network roles (partly hardcoded, no UI
      support, no support of user-defined network roles to networks mapping).
      (Estimate: 0.5-1w)
   b. Refactoring and versioning of network manager.
      (Estimate: 1-1.5w)
   c. Change DB schema (add new functionality) and fix network manager, API and
      serialization for orchestrator (to support old func in new DB schema).
      Ensure it does not break current workflow and interacts with Library
      properly (take multi-cl-l2 API into account?).
      (Estimate: 1-1.5w + QA time)
   d. Add new network manager, API and serialization for orchestrator. Ensure
      it interacts with UI and Library parts properly.
      (Estimate: 2-3w + QA time)
   e. Provide an ability to work with 'old' environments via new API.
      (Estimate: 1-1.5w + QA time)
   f. Networking parameters checker update.
      (Estimate: 1w)
   g. Validation for new API handlers.
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

* Must not introduce regression into NodeGroups feature implemented to support
  multi-racks deployments, but it can replace it with new implementation if
  it fits the upcoming multi-rack story. Deployment engineers should
  be able to deploy multi-rack envs with additional work to setup routing,
  but with no required changes to the core networking module of Nailgun.

* User is able to create/delete networks and setup L2/L3 parameters for them.
  Design will support One logical network for environment at a minimum.
  But there are restrictions (in 7.0 implementation at least) which may prevent
  collocation of all network roles to single network. All restrictions will be
  described in metadata and could be easily adjusted when everything is ready.

* Names of the networks are set by user (with some possible limitations).

* User is able to map network roles to networks almost freely (This mapping is
  node network group -wide, so user is able to set mapping for all nodes in
  group in one turn. Only relevant network roles will actually be mapped for
  each particular node.). Some restrictions on network roles collocation may
  exist though. Such restrictions will be described in network roles metadata.

* There is a default network roles to networks mapping which is provided by
  backend (it can be provided as fixture).

* Network roles description is located near the tasks description (say, in
  separate file nearby). It can be located in plugins the same way.
  Propogation of network roles from plugins is searate task which is in scope
  of "network role s a plugin" story. Task description has section
  [network_roles] where the list of names of network roles required is
  declared. Network roles description is loaded the same way as for tasks,
  into release attributes.

* Tasks are traversed when environment is created to gather info on network
  roles to node roles mapping. That info is saved (into cluster attributes,
  TBD) for quick access. Current set of network roles for particular
  node network group is calculated every time node is added/removed or
  environment settings are changed. Current set of network roles for node is
  calculated during data serialization for orchestrator or when info on node's
  network roles is to be shown in UI (if we need this info in UI at all).

* Network roles set for every particular node depends on node roles (more
  exactly, on tasks for particular node roles) and environment's configuration.
  I.e., network roles required by particular node roles (by tasks which are
  executed for that node role), such as Ceph, should appear on
  roles-to-networks mapping configuration only if node role is placed to the
  Node. This should, in fact, eliminate the checkbox "configure public network
  on compute nodes" - as compute role won't have a need for public network
  role. Availability of particular network roles depends on environment
  settings also. Example: if "Use Neutron in DVR mode" is enabled on settings
  tab, then floating network role has to be allocated on every server which has
  role "compute".

* Validation of provided networking scheme and parameters is done on backend
  (probably on UI and by network verification tool also).

* It's not obligatory to map all networks of particular node to node's
  interfaces. If network is not associated with any network roles it can be
  left unmapped. It will not be set up on the node then.

* Admin-PXE network has some limitations: Admin-PXE role is always mapped
  to it, no any other role can be mapped to it, it cannot be deleted or moved.
  Admin network is inviolable while it is shared between environments. It may
  have some bond limitations as well (not to allow PXE over certain bond
  configs). Limitations are introduced at the request of library team. It is
  not a design limitation though. All of the limitations will be described in
  metadata and can be adjusted. Limitations can be removed completely after
  appropriate testing of the final implementation.

* There should be an ability to define multiple IP subnets for floating IP
  usage. Floating IP ranges should be considered as separate Neutron related
  metadata, as it's purely configuration data for Neutron, and it's tighten to
  particular network role configuration, not to the underlay Fuel provides for
  OpenStack. (This task is nice-to-have priority.)

* Network role can require (via its metadata) one or more IP addresses assigned
  from the network it is assigned to.

* Backend should provide API which supports the following operations:
  create/modify/remove logical networks, modify network roles (as a part of
  cluster attributes), modify network roles to networks mapping.


Documentation Impact
====================

The documentation should describe new networking architecture of Fuel,
changes and new features in networking configuration process in UI.


References
==========

https://blueprints.launchpad.net/fuel/+spec/granular-network-functions
