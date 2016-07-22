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
Initially, when we assign role to the node, full set of tags produced by this
role will be assigned to the node automatically and then user is able to
configure assignment of tags for the node(remove tag from the node,
assign tag to a node, etc.) via API/CLI/UI. For example, if you assign
'controller' role to the specific node, then all its tags 'mysql', 'neutron',
'keystone', 'rabbitmq' will be assigned to the node.
Tags may be assigned or removed from a node regardless of the defaults
inherited by role assignment. It means that we have no strong restriction
between roles and tags to allow user to decide what set of tags is needed
for particular role.
For example, controller role producing tags neutron and rabbitmq. So, new
resolver should collect tasks using these `tags` (all tasks and groups with
'neutron' and 'rabbitmq' tags should be collected).

For example:

- 'controller' role is assigned to the node and user does not change tag's
  assignment - tasks with any of tags produced by 'controller' role should
  be applied on the node
- 'controller' role is assigned to the node and user removed all tags from the
  node except for 'rabbitmq' tag - only tasks with 'rabbitmq' tag should be
  applied on the node

We have decided to introduce extension's support for automatic tag's
assignment(when we are assigning role what's providing tags).
Callback, to the nailgun's extensions will be performed when user assign
role to the node. So, developer will be able to embed his own piece of logic
into assignment group of tags to the node.

For example extension may produce following tag's assignment for the controller
role:

  .. code-block:: yaml

    - node_id: 1
      node_roles: [controller]
      tags: [cluster:2, mysql:1]
    - node_id: 2
      node_roles: [controller]
      tags: [cluster:1, mysql:2]


New task's processing workflow:

- if task has `tags` field - task should be resolved by tags(resolver should
  check intersection between node's tags and task's tags)
- if task has no `tags` field - resolver should resolve task by role as
  it works previously
- if group of tasks has `tags` field - tasks what are storing in this group
  ('tasks' field) should be appended to task's list for execution on node with
  corresponding `tags` (should be checked intersection between node's tags and
  task's tags)

Tags should be added to existing core tasks what are supposed to be detached
from controller. 'controller-common' tag should be introduced to represent
remaining set of tasks(this set does not include detached `tags`) to allow
user to leave this remaining part of tasks only for specific nodes.

  .. code:: python

    resolver = tags_resolver if task.get('tags') else role_resolver
    resolver.resolve(node, task)


Advantage: we are not messing up resolving by tags and roles.
Disadvantage: we should mark ALL controller-common tasks(remaining part of
tasks what was not bound to any tag) with 'controller-common' tag to exclude
it from task's serialization for `tags`.

Example:

We have following set of tasks:

  .. code-block:: yaml

    - id: mysql
      role: [controller]
      tags: [mysql]
    - id: haproxy 
      role: [controller]
      tags: [controller-common]
    - id: globals
      role: ['/.*/']

And following set of nodes:

  .. code-block:: yaml

    - id: node-1
      roles: [controller]
      tags: [mysql]

Task 'haproxy' should be marked with 'controller-common' tag to not be applied
for nodes with other tags(for example 'mysql').

Plugin's tasks will be processed in old way(by role) if plugin's tasks have no
`tags` field.

Serialization logic should be extended to support 'primary' tags assignment.

Pre-deployment checker should check that all pre-defined tags have been
assigned to nodes and show info message to the user. Anyway, user will be
able to proceed without assigning of full set of tags.

Number of nodes with detached roles does not depend on number of pure
controller nodes. Anyway, even if we have only one node with assigned `tag`
it will be configured in HA manner (pacemaker with one cluster node will be
brought up, etc.) to make it ready for scaling in the future.

Cross-dependency task's resolution should be introduced for tags.

It should be possible to change set of tags for a node after the deployment to
make moving of components from old node to new one easier.

Data model
----------

An additional field named ``tags`` will be added to release metadata to
provide ability to specify set of core tags for release.
`Tag` should have the similar properties with role:
- `has_primary` property(is obligatory now)
- etc.

Example:

  .. code-block:: yaml

    roles_metadata:
      controller:
        name: "Controller"
        tags:
          - controller-common
          - mysql
    tags_metadata:
      controller-common:
        name: "controller-common"
        has_primary: true
      mysql:
        name: "mysql"
        has_primary: true


This list of tags will be used during task serialization.
New field ``tags`` should be introduced into node's data model.
Data about role assignment needs to be serialized as a cluster attribute
because other nodes need to be able to look up another node's tag(s).
User should be able to introduce his own tags for releases and clusters.

REST API
--------

Nailgun API should be extended to support assigning of `tags`.
Proposed workflow:

* user should assign some of roles to the node(set of tags provided by assigned
  role will be added to node's tags automatically)
* user is able to manipulate with tag's assignment via API:
    - user is able to manipulate with predefined set of tags(assign, unassign)
    - user should have an ability to create his own tags and assign them

Note: User is not able to remove any of predefined tags.

Available operations with tag via API:
* create new tag(for cluster or release)
* delete user-defined tags(for cluster or release)
* modify user-defined tags metadata
* list all tags(for cluster or release)
* assign tag to the node
* unassign tag from the node

Example of API request for `tag` creation for the cluster:
*  ${API_URL}/?cluster_id=1&tag_name='swift'&role='swift'&meta=${tag_metadata}

Note: If user-defined tag will be introduced for the cluster tags will be
available only for this cluster.

Example of API request for `tag` creation for the release:
*  ${API_URL}/?release_id=1&tag_name='swift'&role='swift'&meta=${tag_metadata}

Note: If user-defined tag will be introduced for the release tags will be
available in all cluster created with this release.

Example of API request for assigning `tag` to node:
*  ${API_URL}/?node_id=${node_id}&tags=['neutron', 'mysql']

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

Additional work should be done in fuel client component for pretty output of
`tags` and its manipulation.

Available operations with tag via CLI:
* create new tag(for cluster or release)
* delete user-definded tags(for cluster or release)
* modify user-defined tags metadata
* list all tags(for cluster or release)
* assign tag to the node
* unassign tag from the node

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
- controller-common

Fuel-library tasks part should be re-written for corresponding components to
support new approach with tags.
All tasks related only to specific tag should be marked with this tag(
additional field `tags`).

Example:

  keystone task to be changed:

  .. code-block:: yaml

    - id: keystone
      type: puppet
      groups: [controller]

  .. code-block:: yaml

    - id: keystone
      type: puppet
      groups: [controller]
      tags: [keystone]

As we have a lot of places in fuel-library code where we are collecting
set of ip address for particular component by node's role we should
re-write this data access methods to work with `tags` and
provide fallback mechanism to support old style role based approach.

Initially, we are going to have one pacemaker cluster for all nodes
with assigned `tags` what need in it. For example, if we have 'node-1'
with tag 'mysql' and 'node-2' with tag 'rabbitmq' then single pacemaker
cluster with resources 'rabbitmq' and 'mysql' acting on corresponding
nodes will be created.

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
If user don't assign some of mandatory tags(tags what are declared in release
information) warning message should be provided to user.

Workflow:
- user assigning role to the node
- user is able to configure set of tags for this node

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

* Create new test cases for the new operations with tags
* Extend fuel-qa test suite with new API tests for the operations with tags

Acceptance criteria
===================

User is able to deploy services currently tied to the controller (e.g. Keystone,
Neutron, Mysql) on separate nodes via API(Web UI and CLI have a nice to have
priority).

----------
References
----------

None
