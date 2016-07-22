..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Role decomposition
==========================================

https://blueprints.launchpad.net/fuel/+spec/role-decomposition


--------------------
Problem description
--------------------

Currently the controller role encompasses many tasks that cannot be separated
from a controller node. Deployers should have the flexibility to distrubute
services across nodes in any combination they see fit.


----------------
Proposed changes
----------------

Task placement will be determined based on a node's label. Task definitions
will contain a list of labels which will be used to match them to nodes.
This requires a new task resolver.

Web UI
======

None

Nailgun
=======

A new resolver which matches node labels to tegs will be added.
Tag - should exist in tasks which describes any roles.
Whole scope of this tasks should exist for one environment
and can be assign for one node or split to another.
Controller scope of Tags Example:

- controller:* (all tags should be assigned for current node)
- controller:rabbitmq (only rabbitmq task should be assigned on this node)

Validator - should be able to check that all tasks described for Tag
and assigned to cluster.

Data model
----------

An additional field named ``labels`` will be added to roles_metadata in each
Release. This list of labels will be used during task serialization. The
labels for a node's role will be added to the any labels assigned explicitly
by the user.


REST API
--------
None

Orchestration
=============


RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

All tasks will need to have one or more labels assigned to them. There will
be some tasks that require decomposition.

At least next tasks should be de-composed:

1. Neutron (incl. L3 agents, LBaaS, etc)
2. Keystone
3. MySQL DB
4. RabbitMQ

Re-compose neutron components:

1. neutron-server
2. neutron agent
3. neutron-dhcp-agent
4. neutron-l3-agent

Tags shoul be added to tasks in yaml files

------------
Alternatives
------------

None

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

None

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Describe how to decompose roles using node labels.

--------------
Implementation
--------------

Assignee(s)
===========


Primary assignee:
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

 #. Tags/task based node assignment.
 #. Role/Service decomposition:
     Update fuel-library tasks to support role decomposition
 #. Update composition data access methods in fuel-library:
     Fuel-library should not rely on node roles when collecting set of
     IP addresses for a particular service (neutron, rabbitmq, etc.)
     It should be based on a node label instead.
 #. Decouple Neutron component:
     Allow different Neutron components (server, l3-agent, dhcp-agent) to
     be installed on separate nodes.
 #. Prepare documentation for cluster scaling
    It should be possible to move some of critical
    services(rabbit, keystone, neutron, mysql) to separate node after the
    deployment process. We are not planning to prepare automated procedure
    for cleaning services what are supposed to be detached from nodes where
    it was place initially.
 #. Update mandatory fuel plugins
    It's expected that changes in fuel-libray and nailgun components
    may lead to failing for some of fuel-plugins.



Dependencies
============

None

------------
Testing, QA
------------

Introduce tests for various combinations of controller decomposition.

Acceptance criteria
===================

User is able to deploy services currently tied to the controller (e.g. Keystone,
Neutron, MySQL) on separate nodes.

----------
References
----------

.. [0] https://review.openstack.org/#/c/341678/
