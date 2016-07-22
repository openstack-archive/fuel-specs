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

Currently a role encompasses many tasks that cannot be separated from each
other. Deployers should have the flexibility to distribute services across
nodes in any combination they see fit.

----------------
Proposed changes
----------------

Task placement will be determined based on a node's tag. Task definitions
will contain a list of tags which will be used to match them to nodes.
This requires a new task resolver on nailgun side and work on decoupling of
tasks on fuel-library side.

Web UI
======

UI part should be extended to display set of tags for particular node.

Nailgun
=======

A new resolver which supports role's tags should be introduced.
Initially, role contains full set of tags produced by this role and some of
role's tags may be used for assignment to the specific node. So, for
example, if you assigned 'controller' role to the specific node, then
all its tags 'mysql', 'neutron', 'keystone', 'rabbitmq' will be assigned
to the node.
It should be possible to assign tag to the node even if this tag belongs
to role what is not assigned to current node. It means that we have no
strong restriction between roles and tags to allow user to decide what
set of tags is needed for particular role.
For example, controller role producing tags neutron and rabbitmq. If we have
node with `tagged` role, new resolver should collect tasks using this `tagged`
role(all tasks and groups with 'neutron' and 'rabbitmq' tags should be
collected).
If role producing set of tags and it was assigned to particular node, new
resolver should collect all tasks with `tagged` roles produced by this role.
Initially, role contains full set of tags produced by this role and then
user is able to configure specific set of tags for particular node(remove tag
from the node, assign tag to the node, etc.).
For example:

- 'controller' role is assigned to the node and user does not change tag's
  assignment - tasks with any of tags produced by 'controller' role should
  be applied on the node
- 'controller' role is assigned to the node and user removed all tags from the
  node except for 'rabbitmq' tag - only tasks with 'rabbitmq' tag should be
  applied on the node

Each of role tags will have the similar constraints like role producing this
tag:
- count of the nodes for tag's assignment
- `has_primary` property
- etc.

Pre-deployment checker should check that all role's tags have been assigned
to nodes and show info message to the user. Anyway, user will be able to
proceed without assigning of full set of tags.

Number of nodes with detached roles does not depend on number of pure
controller nodes. Anyway, even if we have only one node with `tagged` role
it will be configured in HA manner (pacemaker with one cluster node will be
brought up, etc.) to make it ready for scaling in the future.

Also, cross-dependency task's resolution should be introduced for tags.

Data model
----------

An additional field named ``tags`` will be added to roles_metadata in each
release. This list of tags will be used during task serialization.
New field ``tag`` should be introduced into node's data model.
Data about role assignment needs to be serialized as a cluster attribute cause
other nodes need to be able to look up another node's tag(s).

REST API
--------

Nailgun API should be extended to support assigning of `tags`.
Proposed workflow:

* user is able to assign role(providing set of tags) or tag to the particular
  node
* user is able to manipulate with tag's assignment via API

Available operations with tag via API:
* add new tag
* modify any tag
* list all tags
* delete tag
* assign set of tags to node
* remove tags from a node

Example of API request for assigning `tag` to node:
*  ${API_URL}/?node_id=${node_id}&tags=['neutron', 'mysql']

It should be allowed to create custom tags via API.

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

Additional work should be done in fuel client component for pretty output of
`tagged` roles and its manipulation.

Available operations with tag via CLI:
* add new tag
* modify any tag
* list all tags
* delete tag
* assign set of tags to node
* remove tags from a node

Plugins
=======

It's expected that changes in fuel-library and nailgun components
may lead to failing for some of fuel-plugins.

Mandatory plugins list:
- aic-fuel-plugin
- fuel-plugin-contrail
- LMA (ES, Influx, collector & alerting)
- zabbix-database
- zabbix-mon

Fuel Library
============

Blueprint's scope includes detaching of following components:
- Neutron (incl. L3 agents, LBaaS, etc)
- Keystone
- MySQL DB
- RabbitMQ

`tags` will be introduced for controller role:
- neutron
- keystone
- mysql
- rabbitmq

Fuel-library tasks part should be re-written for corresponding components to
support new approach with tags. New groups of the tasks for described
components should be added and stuck to the introduced `tags`.
Introduced group should provide list of the tasks what are needed for
deployment of particular component, also, it should contain field `tags` with
list of tags what group belong is.
Existing core tasks should not be modified to not brake existing deployment
workflow.

Example:

  keystone groups to be introduced:

  .. code-block:: yaml

    - id: keystone
      type: group
      tags: [keystone]
      tasks: [hiera, fuel_pkgs, globals]
      parameters:
        strategy:
          type: parallel

  .. code-block:: yaml

    - id: primary-keystone
      type: group
      tags: [primary-keystone]
      tasks: [hiera, fuel_pkgs, globals]
      parameters:
        strategy:
          type: one_by_one

As we have a lot of places in fuel-library code where we are collecting
set of ip address for particular component by node's role we should
re-write this data access methods to work with `tagged` roles and
provide fallback mechanism to support old style role based approach.

Initially, we are going to have one pacemaker cluster for all ``tagged``
nodes what need in it. For example, if we have 'node-1' with tag 'mysql' and
'node-2' with tag 'rabbitmq' then single pacemaker cluster with resources
'rabbitmq' and 'mysql' acting on corresponding nodes will be created.

There is no detached plugin for neutron. So, additional efforts should
be spent to collect mandatory tasks for neutron task group and test it.

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

User will be able to detach set of components described in the specification
from controller node.
User can change set of tags for any role using nailgun API and CLI for particular
environment or release.

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

Describe how to decompose roles using node tags.

It should be possible to move detached services to separate node after the
deployment process. We are not planning to prepare automated procedure for
cleaning services what are supposed to be detached from nodes where it was
placed initially. So, corresponding document should be prepared.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  * Viacheslav Valyavskiy <vvalyavskiy@mirantis.com>

Other contributors:
  * Ivan Ponomarev <iponomarev@mirantis.com>

Mandatory design review:
  * Vladimir Kuklin <vkuklin@mirantis.com>
  * Stanislaw Bogatkin <sbogatkin@mirantis.com>

Work Items
==========

 #. Introduce operations with tags via nailgun API
 #. New tags based resolver in nailgun
 #. Role/Tag decomposition in Fuel-library
 #. Update composition data access methods in fuel-library
 #. Decouple Neutron component
 #. Prepare documentation for cluster scaling
 #. Update mandatory fuel plugins

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

None
