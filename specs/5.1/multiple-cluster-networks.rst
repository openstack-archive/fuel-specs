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
problems.

Proposed change
===============

Allow the creation of multiple instances of each network type for each cluster.

Alternatives
------------

Leave it as-is. This will limit our ability to deploy large-scale environments.

Data model impact
-----------------

Networks are currently tied to a cluster. In order to support multiple networks
per cluster we will add the concept of a node group. Networks will be attached
to a node group, nodes will be assigned to a node group, and node groups will
belong to a cluster.

REST API impact
---------------

New API handlers will need to be created to allow creation and modification of
networks. Node-related APIs will be updated to work with node groups.

Security impact
---------------

None

Notifications impact
--------------------

Nodes can be assigned to a group automatically based on which admin network it
recieves an address from. The user can be notified of this auto-association.

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

None

Documentation Impact
====================

The concept of node groups and how networks are assigned to nodes will need
to be documented.

References
==========

https://review.openstack.org/#/c/83204/
