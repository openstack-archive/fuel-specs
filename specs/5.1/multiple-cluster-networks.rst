..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================
Multiple L2 networks
====================

https://blueprints.launchpad.net/fuel/+spec/multiple-cluster-networks

Problem description
===================

Currently Fuel only supports one set of networks (admin, public, management,
storage) for each cluster. The consequence of this is that a cluster will be a
single L2 domain. Forcing the use of a single L2 domain presents scalability
problems. Any time a large number of nodes is to be deployed it is important to
split the nodes into separate L2 domains to avoid broadcast storms.

Proposed change
===============
Fuel will need to be extended in the following ways:

1. We will introduce the concept of a node group to Nailgun. Node groups will
   be an arbitrary grouping of nodes in the current cluster.

   a) Networks will be associated with node groups instead of clusters.
   b) Nodes will associate automatically with Node groups if the Node's
      discovered address is from a Node Group's fuelweb_admin network
   c) A Node group will associate with a cluster when a node is added to it
   d) A node will serialize its network information based on its relationship
      to networks in its Node Group
   e) A node must be associated with a Node Group or it is de facto in
      an error state (as we can’t serialize any network data for it)
2. Deployed nodes will need to have routes to all other nodes and their
   networks.
3. Fuel DHCP discovery networks will be managed by adding or removing
   fuelweb_admin NetworkGroups to NodeGroups
4. New constraints when deploying a cluster with multiple Node Groups

   a) all controllers should be a member of the same Node Group (while
      controllers can technically be in separate Node Groups, this is not
      practical because this breaks the haproxy vip from working)
   b) can only deploy using a network manager that is configured with a
      tunneling protocol (like Neutron GRE)

Alternatives
------------

Leave it as-is. This will limit our ability to deploy large-scale environments.

Data model impact
-----------------

Networks are currently tied to a cluster. In order to support multiple networks
per cluster we will add the concept of a node group. Networks will be attached
to a node group, nodes will be assigned to a node group, and node groups will
belong to a cluster.

The network_groups table will need to allow a display name for each network and
the current name column will be changed to ‘type’. The current names are
used explicitly when validating and serializing the network configuration.
Keeping them as a “network type” (which is what they really are) will allow
validation and serialization to continue functioning while allowing the user
to specify meaningful names.

Network groups will no longer be tied to a cluster, but to a node group
instead.

A new table, node_groups will be created. Each node and network will reference
one of these groups.


REST API impact
---------------

New API handlers will need to be created to allow creation and modification of
networks. Node-related APIs will be updated to work with node groups.

We will add a new API handler for creating, updating and deleting node groups.
New handlers for the task of managing network groups and IP address ranges will
be created. The node API handler will be updated to allow the assignment of
nodes to a node group.

Security impact
---------------

None

Notifications impact
--------------------

Nodes can be assigned to a group automatically based on which admin network it
recieves an address from. The user can be notified in the UI of this
auto-association.

Other end user impact
---------------------

None

Performance Impact
------------------

Performance of nailgun should not be impacted.

Other deployer impact
---------------------

A separate DHCP range will need to be configured for each admin network. The
correct dnsmasq configurations can be generated automatically by nailgun.

Dnsmasq supports a config directive to include config files from a directory.
Upon creation of an admin network Nailgun can create a file with the
approriate DHCP configuration.

Developer impact
----------------

None


Implementation
==============


Assignee(s)
-----------

Primary assignee:
    Ryan Moe (rmoe@mirantis.com)

Work Items
----------

None

Dependencies
============

None

Testing
=======

We will need to improve devops to support emulating multiple L2 domains so that
systems tests can be run using this topology.

Documentation Impact
====================

The concept of node groups and how networks are assigned to nodes will need
to be documented.

References
==========

https://review.openstack.org/#/c/83204/
