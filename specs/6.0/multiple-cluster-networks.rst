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
the current name column will be changed to 'type'. The current names are
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

The network configuration handler will be modified to allow per-node group
network configuration. If a node group is not specified then the cluster's
default group will be used.

We will add a new API handler for creating, updating and deleting node groups.
The node API handler will be updated to allow the assignment of nodes to a
node group. Upon creation of a node group a set of networks will be generated
the way we do for clusters currently.

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

Network verification as it stands now will not work with multiple L2 domains.
More research will be needed to determine how easily it can be made to support
that.

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

Upgrade impact
--------------

Schema and data migrations will be provided to support previously created
environments.

Implementation
==============


Assignee(s)
-----------

Primary assignee:
    Ryan Moe (rmoe@mirantis.com)

Work Items
----------

* Modify database models and create migrations for old environments
* Add API handlers for configuring node groups
* Add support to Fuel CLI for managing node groups
* Update Puppet manifests to configure the required routes

Dependencies
============

None

Testing
=======

We will need to improve devops to support emulating multiple L2 domains so that
systems tests can be run using this topology.

Testing for non-multiple cluster networks will continue to function as it
currently does. No modifications to the current process are necessary to test
a single cluster network deployment. For multiple cluster network deployments
the testing is outlined below.

Manual testing
--------------
Manual testing can be accomplished by the following steps:
#. Spin up two environments with devops and fuel-main::

 # All networks must be routed. Isolated networks (default for management and
 storage networks) will not work.
 export FORWARD_DEFAULT=route
 export ADMIN_FORWARD=nat
 export ENV_NAME=alpha
 nosetests fuelweb_test.tests.base_test_case:SetupEnvironment.setup_master
 export ENV_NAME=beta
 nosetests fuelweb_test.tests.base_test_case:SetupEnvironment.setup_master
 # You don't need to let beta install the fuel master node

#. Kill the default dnsmasq and the one for beta (Specifing no DHCP to the
nosetests or network in devops will still not allow dhcp-helper / dhcrelay to
function. A dnsmasq instance is created by libvirt for every network
regardless)::

 ps axu | awk '/dnsmasq\/beta_admin.conf/{system("kill "$2)} \
   /dnsmasq\/default.conf/{system("kill "$2)}'

#. Start a dhcp-helper or dhcrelay (Update -S to match the IP of the
alpha-admin, Update -i to include the virtual interface of the beta_admin
network)::

 dhcp-helper -s 10.110.0.2 -i virbr6

#. Add DHCP network to cobbler as below.
#. bootstrap nodes in alpha, and beta, both sets of nodes should discover.
#. Add a second NetworkNodeGroup to the fuel node.

DHCP
----
For each fuelweb_admin network you will additionally need to add DHCP networks
into ``/etc/cobbler/dnsmasq.template`` (in future revisions this will be
handled automatically).::

 dhcp-range=alpha,10.110.1.68,10.110.1.127,255.255.255.192
 dhcp-option=net:alpha,option:router,10.110.1.65
 dhcp-boot=net:alpha,pxelinux.0,boothost,10.110.0.2

the ``alpha`` is the name of the network in dnsmasq, this must be unique
in the dnsmasq config.

The second line, ``dhcp-option`` router should be the that segments network.

The third line, ``dhcp-boot`` boothost should point to the fuel server.

DHCP requests can be forwarded to the fuel server either by the network switch
via dhcp-helper (bootp) or via a relay client such as dhclient or dhcp-helper

Automated Testing
-----------------
Improvements will need to be made into devops so that it can run the steps for
the manual process. Work will also need to be done so that the cobbler
dnsmasq can be automatically updated when a new fuel-admin network is
created.

Documentation Impact
====================

The concept of node groups and how networks are assigned to nodes will need
to be documented.

The planning guide will be updated with an overview of the network layout
required for this feature.

References
==========

https://review.openstack.org/#/c/99179/
