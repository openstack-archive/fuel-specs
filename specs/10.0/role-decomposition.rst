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

Task placement will be determined based on new unit - `tag`. Each release or
plugin role may contain(or not, in this case role name will be considered as
a tag name) specific set of tags. Task definitions will contain a list of tags
which will be used to match them to nodes.
This requires a new task resolver on nailgun side and work on decoupling of
tasks on fuel-library side.

Web UI
======

None

Nailgun
=======

A new tags based resolver which supports tags should be introduced. Tags are
simple entities what should be used for tasks resolution(in opposite to old
role driven resolution approach) only. User is not able to operate with node's
tags directly, but, he should create new role containing tags what he is
interested in and assign created role to the node.
``primary-tags`` field should be introduced for node model to store primary
set of tags for the node.
Tags will be fetched from roles metadata during serialization process and
will not be stored for each node directly(we have no `tags` field in node db
model).
It should be possible to create roles for clusters and it will be possible
to have so-called roles for release and cluster created with this release.
The idea is that cluster roles have a higher priority than release roles and
it means that only cluster role will be used if we have so-called cluster
and release roles.
 
Data model
----------

An additional field named ``tags`` will be added to release metadata to
provide ability to specify set of tags for release roles.
`Tag` should have only one field:
- `has_primary` property

Example:

  .. code-block:: yaml

    roles_metadata:
      controller:
        name: "Controller"
        tags:
          - controller
          - mysql
    tags_metadata:
      controller:
        name: "controller"
        has_primary: true
      mysql:
        name: "mysql"
        has_primary: true


New JSON fields ``volumes_metadata`` and ``roles_metadata`` should be
introduced for cluster model.

New JSON field ``tags_metadata`` should be introduced for cluster, release,
plugin models.

``primary_roles`` column should be renamed to ``primary_tags`` for node model.

REST API
--------

Nailgun API should be extended to support role's creation for clusters to
make cluster's specific roles not visible for other clusters and avoid
mishmash.

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

Fuel Client should be extended to support role's creation for clusters.

Plugins
=======

As plugins have ability to define its own roles it will be possible to specify
tags for any particular role introduced by a plugin. I would mention that it's
possible, but, not obligatory to specify tags for role(in this case role
name will be used for tasks resolution).

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
- controller

Fuel-library tasks part should be re-written for corresponding components to
support new approach with tags.
All tasks related only to specific tag should be marked with this tag(
field `role` or `groups` should be replaced with `tags`).

The version of library tasks where `role` field has been replaced with `tags`
shall be bumped.

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

We should consider changes in tag's assignment between minor releases.
For example, it may be embedded into db migration process.

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

User will be able to create roles with specific set of tags.
Initially, user has only default set of roles and its tags. If he wants,
for example, create detached role with 'mysql', he should create new cluster
role containing only 'mysql' tag.
User is able to modify roles(and its set of tags) in any moment except of
deployment process.

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

Describe how to create custom roles(with custom set of tag).

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  * Viacheslav Valyavskiy <vvalyavskiy@mirantis.com>

Other contributors:
  * Mikhail Zhnichkov <mzhnichkov@mirantis.com>

Mandatory design review:
  * Vladimir Kuklin <vkuklin@mirantis.com>
  * Stanislaw Bogatkin <sbogatkin@mirantis.com>

Work Items
==========

 #. Introduce operations with roles for cluster(API, DB)
 #. New tags based resolver in nailgun
 #. Extend fuel-client to support operations with roles
    for cluster
 #. Role/Tag decomposition in Fuel-library
 #. Update composition data access methods in fuel-library
 #. Decouple Neutron component in fuel-library

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

User is able to deploy services currently tied to the controller (e.g.
Keystone, Neutron, Mysql) on separate nodes via CLI(Web UI have a
nice to have priority).

----------
References
----------

None
