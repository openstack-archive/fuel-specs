..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Task Based Deployment With Astute
==========================================


https://blueprints.launchpad.net/fuel/+spec/task-based-deployment-astute

* Intro

  This blueprint is a suggestion to improve our deployment orchestration
  to make it possible to improve deployment time and decrease our technical
  and architectural debt by an order of magnitude.


--------------------
Problem description
--------------------
  So far we have had a really neat but half-completed orchestration engine since 6.1
  This engine allowed us to split gigantic puppet catalogue into pieces and run tasks
  one by one allowing users to introduce tasks within plugins thus making Fuel much
  more flexible. Unfortunately, due to lack of resources we had to postpone complete
  implementation of an orchestrator that can orchestrate tasks instead of roles. This
  leads to performance issues of the deployment significantly affecting deployment time.
  While in fact it could be almost O(1+n/limit), it is almost O(n*m) where *n* is number of roles,
  *m* is number of nodes and *limit* is configurable limit of parallel deployment of nodes.
  This became especially harmful when we introduced role-as-a-plugin feature [0] as role
  dependencies make deployment take up to 4-6 hours, simply waiting for roles to be completed
  without actual dependencies between them.

  This makes our deployment go 80 minutes for a basic BVT use case, while it could have taken
  30 minutes with parallelized deployment. This blueprint suggests a change that should once
  and forever remove such roadblocks from Fuel.

  This would allow us to drastically improve things:

  * Shrink CI time to 30 minutes

  * Make our infra gating swift for packages

  * Provide developers with very quick feedback

  * Allow us to unlock settings tabs to do simple redeployment after settings change (partial lifecycle management)

  * Make Fuel look even more awesome


----------------
Proposed changes
----------------

We propose to enable this feature by applying the following changes:

* Make roles just a Nailgun entity, not known to Astute

* Make Nailgun generate a graph of tasks for execution based not on roles, but on tasks

* Make Astute traverse the graph according to dependencies

* Introduce new version of tasks.yaml format allowing depl. engineer to set cross-node dependencies

* Introduce 'anchor' type of task which does not require any type of execution

* Refactor Fuel Library to introduce cross-node dependencies and anchors

* Adjust FUEL CLI correspondingly

* Allow a user to disable task-based deployment in case he does not want this feature or faces any
  issues with it

Web UI
======


Nailgun
=======

Nailgun should be configurable whether to have task-based-deployment enabled or not.
Task-based deployment for the cluster should be enabled only when all the tasks
used are compatible with this change and task-based-deployment is enabled.

Data model
----------

REST API
--------

There could be slight changes for REST API, e.g. ability to ask Nailgun
to prefetch additional tasks into deployment. Let's call it '--fetch-deps'.
It should be disabled by default, but should allow a user to specify
whether he wants to add additional required tasks into the graph.

For example, our current behaviour is to run the deployment and disregard
whether there are dependencies missing. But it would be a good UX improvement
if we just allowed an advanced switch to add these dependencies into deployment
graph.

E.g.  **fuel nodes --node 2,3 --deploy --fetch-deps** for secondary controllers
would prefetch tasks from the primary controller or **fuel nodes --node 1 netconfig --fetch-deps**
would add netconfig and other tasks for the node, so that it does not fail, but succeeed.

Tasks YAML format Change
------------------------

* Introduce additional syntax for a requirement for a task.

It should be extended in the following way:

Tasks Format Versioning
~~~~~~~~~~~~~~~~~~~~~~~
version: 1.0.0|2.0.0|null

Null version is equal to version 1 and to legacy task and
deployment graph format.
Task-based deployment can be run only when ALL tasks in
the graph have version set to '2'


Tasks Cross Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

This field allows for a setting dependencies of tasks
between the nodes. This means that task on node B
can depend on task on node A, while independent
tasks can be executed in parallel on the nodes.

.. code-block:: yaml

  cross-depended-by|cross-depends
    - name: <task-name-regexp>
    [role: <role-name-regexp>]
    [policy:  <any|all>]
   default values:
   role-name-regexp: .*
   policy: all

Task Strategy
~~~~~~~~~~~~~

This field is going to be a replacement for parallelization
of deployment groups.
It should be parsed by astute as a prerequisite for task execution
to identify whether a particular task can be executed. For example,
we spin up no more than N tasks of this type.

.. code-block:: yaml

  strategy:
    type: parallel|one-by-one
    amount: <integer>
  
* Add an 'anchor' task type that has no target and is used for tasks sync,
  is being actually executed on the master node with 'return true' behaviour
  and is being used identically to Puppet anchor resource type as a simple
  synchronization point

Orchestration
=============

Astute should be extended with a set of methods that respect the following:

* Dependencies between the tasks provided by Nailgun

* Concurrency policies for tasks (e.g. no more than 6 replication slaves for
  Galera at a time)

* One task per node at a time.

There will be a set of new tasks states introduced:

* Success - Tasks has been successfully executed
* Error - Task has failed
* In Progress - Task is being executed
* Waiting - Task does not have dependencies satisfied yet
* Pending - Task has all the dependencies met, but not all of the pre-requisites are met
  (e.g. concurrency policy)
* Failed Dependencies - Task is ok by itself, but one of its parents is in Error, so it cannot be executed

Astute will form a view of tasks for execution for each particular node and synchronously monitor
a set of tasks that are being executed with periodic check. Whenever a node is free for execution,
Astute starts iterating through tasks and triggers a method that finds if task can be started. In this case
we just trigger a task and go to another node. Otherwise we try with another task.

Whenever there are only tasks with Error/Failed_Deps/Success for a node, we calculate node status and mark node as 'ready' if all tasks
are successful or 'error' otherwise.

Astute will also support generation of deployment graph dot file and (tentatively) its visualization in svg format.

Astute will also check for loops in the graph and fail immediately in case of any found with corresponding error message

RPC Protocol
------------

RPC Protocol change is the following:

Nailgun sends a message for execution in new format with deployment hash embedded into it.
Astute identifies that it should use new deployment/orchestration engine, generates the graph
for further execution and passes it to graph execution engine.

Nailgun will send a three-level hash to Astute of the following format that will be parsed by
astute and generated as a graph. There will also be an additional field in deploy_resp specifying
which deployment engine to use - old role-based or task-based

.. code-block:: yaml

  deployment_engine: <engine_name>
  nodes:
    - node: <node-id>
      - task: <task-name>
        parameters:
          - <task-parameter1>: <val1>
          - <task-parameter2>: <val2>

Fuel Client
===========

Fuel client needs to be fixed to generate single deployment info files instead of two for each role
Fuel client will require to be extended to send 'fetch-deps' option on the deployment of nodes.

Plugins
=======

This change does not affect plugins except for enabling pluggable roles/tasks
to be executed in more optimal way. This optimal way will be enabled only when
all tasks associated with the cluster are set into new version format and when
'task-based-deployment' flag is set to 'true'.

Fuel Library
============

Adjust Fuel Library tasks to use proper cross-node orchestration to avoid race
conditions.

* Remove references to *$role* attribute in hiera

  As role will become an obsolete abstraction on deployment level, some of the
  manifests will need to be adjusted to usage of *node_roles*

* Adjust tasks cross dependencies parallelizm to be controlled properly
  there are some tasks like **database** which are being deployed properly
  due to sequential character of their deployment groups. With new engine this
  paralellizm should be controlled by cross-dependencies. E.g. there should be
  2 types of tasks created:

.. code-block:: yaml

  id: primary-database
  ..
  id: database
    cross-depends: primary-database


------------
Alternatives
------------

There are almost no other alternatives except for integration of other orchestration engine.
This integration may require long time and will not get into 8.0 release.

--------------
Upgrade impact
--------------

There should be a migration introduced which sets pre-8.0 clusters to use old orchestration
engine.

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

Fuel client needs to be fixed to generate single deployment info files instead of two for each role


------------------
Performance impact
------------------

None.

-----------------
Deployment impact
-----------------

Deployment will take O(1) time ~ 30 minutes for the longest node deployment.
It will allow to enable redployment and some of LifeCycle management tasks which
can be implemented by simple redeployment.

----------------
Developer impact
----------------

Developers will require to understand that tasks that do not have explicit
cross-node dependencies will be deployed in parallel on different nodes.
They will need to introduce additional anchors and dependencies to avoid that.

Developers will have faster feedback from the deployment as it will take no more
than 30 minutes in comparison to good old couple of hours.

---------------------
Infrastructure impact
---------------------

None, except for improvement of hardware utilization by order of at least 4 times.

--------------------
Documentation impact
--------------------

Document the differences between new and old tasks format and how to pick one when needed.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Alexey Shtokolov (~ashtokolov)

Other contributors:
  Dmitry Ilyin (~idv1985)
  Vladimir Sharshov (~vsharshov)

Mandatory design review:
  Vladimir Kuklin (~vkuklin)
  Bogdan Dobrelia (~bogdando)
  Anastasia Urlapova (~aurlapova)
  Igor Kalnitsky (~ikalnitsky)



Work Items
==========

* Deduplicate roles in Nailgun before graph serialization

* Introduce graph traversal engine in Astute

* Introduce methods to check task execution availability in Astute

* Introduce support for 'old' and 'new' task format, so that new format can relate to tasks on the other nodes

* Add ability to set cluster 'deployment mode' in API and UI to run old version of 'non-optimal' deployment

* Fix FUEL CLI astute export

* Fix FUEL library relying on 'role' attribute in astute.yaml to switch to node_roles in hiera

* Rewrite tasks dependencies in Fuel Library to make things parallelized with the engine


Dependencies
============

------------
Testing, QA
------------

Nothing to change here, actually. As it just an internal deployment engine refactoring.

Acceptance criteria
===================

It should be possible to:

Deploy tasks with fuel based only on task context (node) and not a role.
Actual deployment of independent deployment tasks should run in parallel.
There should be a possibility to disable new engine whether any issues arise.

----------
References
----------

[0] https://blueprints.launchpad.net/fuel/+spec/role-as-a-plugin

