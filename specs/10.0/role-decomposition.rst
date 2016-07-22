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

Task placement will be determined based on a node's tag. Task definitions
will contain a list of labels which will be used to match them to nodes.
This requires a new task resolver.

Web UI
======

Human readable names should be displayed instead ugly controller::* name
convention.
For example, we can just display only second part of `tagged` role:

- controller::rabbitmq -> rabbitmq
- controller::neutron  -> neutron
- controller::mysql    -> mysql
- controller::keystone -> keystone

Nailgun
=======

A new resolver which supports role's tags should be introduced.
Initially role contains full set of tags produced by this role. For example,
controller role producing tags neutron and rabbimq. If we have no tags
assigned to particular node, new resolver should collect tasks using
`controller::*` regular expression. If we have one of role's tags assigned,
new resolver should collect tasks using remaining tags - `controller::neutron`
or `controller::rabbitmq`. This appoach allows us to detach tasks from
controller role.

Controller scope of tags example:
- controller::* (all controller tasks should be assigned for current node)
- controller::rabbitmq (only rabbitmq task should be assigned on this node)

Each of role tags will have the similar constraints like role producing this
tag:
- count of the nodes
- `has_primary` property
- etc.

Pre-deployment checker should check that all role's tags have been assigned
to nodes.

Data model
----------

An additional field named ``tags`` will be added to roles_metadata in each
release. This list of tags will be used during task serialization. The
tags for a node's role will be added to the any tags assigned explicitly
by the user.

REST API
--------

Nailgun role assigning API should be extended to support assigning of `tagged`
roles:
 ${API_URL}/?node_id=${node_id}&roles=[controller::neutron, controller::mysql]


Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

It's expected that changes in fuel-libray and nailgun components
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

Following set of `tagged` roles will be introduced:
- controller::neutron 
- controller::keystone
- controller::mysql
- controller::rabbitmq

Fuel-library tasks part should be re-written for corresponding components to
support new approach with namespaces. New groups of the tasks for described
components should be added and sticked to the introduced `tagged` roles.
Introduced group should provide list of the tasks what are needed for
deployment of particular component.
Existing core tasks related to the component should be re-assigned to the
one of introduced groups.

Example:

  keystone group to be introduced:

  .. code-block:: yaml

    - id: keystone
      type: group
      role: [controller::keystone]
      tasks: [hiera, fuel_pkgs, globals]
      parameters:
        strategy:
          type: parallel

  keystone task:
  
  .. code-block:: yaml

    - id: keystone
      type: puppet
      groups: [controller]

  will be changed to:

  .. code-block:: yaml

    - id: keystone
      type: puppet
      groups: [keystone]

Primary roles also should be introduced for proposed `tagged` roles.

  keystone group to be introduced:

  .. code-block:: yaml

    - id: primary-keystone
      type: group
      role: [controller::keystone]
      tasks: [hiera, fuel_pkgs, globals]
      parameters:
        strategy:
          type: one_by_one

  keystone task:
  
  .. code-block:: yaml

    - id: primary-keystone
      type: puppet
      groups: [primary-controller]

  will be changed to:

  .. code-block:: yaml

    - id: primary-keystone
      type: puppet
      groups: [primary-keystone]


As we have a lot of places in fuel-library code where we are collecting
set of ip address for particular component by node's role we should
re-write this data access methods to work with `tagged` roles and
provide fallback mechanism to support old style role based approach.

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

Describe how to decompose roles using node labels.

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
