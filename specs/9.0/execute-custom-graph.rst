..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Ability To Execute Custom Deployment Graph
==========================================


https://blueprints.launchpad.net/fuel/+spec/custom-graph-execution

This blueprint introduces new feature allowing
a user to execute particular deployment graph
with ability to merge it with existing
deployment graphs of upstream master release.
This would allow a user to implement complex orchestrated
workflows such bugfixes application, reference architecture
altering or even upgrades.


-------------------
Problem description
-------------------

As a deployment engineer I would prefer to have an opportunity
to apply one-shot fixes or workflows which require complex orchestration
such as 'detach DB on the fly and move it to another cluster of nodes' or
even upgrades, while the most common case is application of bugfixes
which require more than simple packages installation.

----------------
Proposed changes
----------------

The proposed change assumes that each deployed cluster has 3 classes of
deployment graphs with the following hierarchy (the lower one is of more
importance):

* Release-default Graph

* Cluster-specific Graph

* Graphs introduced by plugins (effective merge of these graphs)

The feature essentially extends model of graphs being used to allow
typisation of graphs being used during deployment. Custom graph may be of
any particular type and will be stored in the database with this type.
Default deployment graphs will have type 'default'. Thus, this feature
assumes FULL BACKWARD compatibility with existing methods of calculation
of pre-serialized deployment graph representation.


Graph serialization is performed by the following technique. Each deployment
run executes deployment of particular **type** ('default' by default).

Nailgun module introduced by this feature which is responsible for graph
merge fetches graphs of each class for corresponding type of deployment
and merges them by merging all task IDs where low-level attributes override
the higher ones.

Example:

.. |darr| unicode:: 0x2193

Default deployment

Release **default** graph - derived from tasks.yaml of fuel-library

  |darr|

Cluster **default** graph (empty by default)
with cluster-specific tasks specified by the user

  |darr|

Plugins **default** graphs (deployment tasks from plugins)


UseCase1

Release **usecase1** graph - empty for now but can be derived
from tasks.yaml of fuel-library or be delivered by MUs

  |darr|

Cluster **usecase1** graph (empty by default)
with cluster-specific tasks specified by the user

  |darr|

Plugins **usecase1** graphs
can be specified by plugin developers

All the changes are going to be related to Nailgun and python-fuelclient
parts.

Web UI
======

None so far

Nailgun
=======

Main changes are going to happen within the pieces that construct preserialized
graphs which essentially resemble a list of dictionaries of deployment tasks.

There will be 3 sources of data:

* Default release graph derived from /etc/puppet/modules

* Cluster-specific graph uploaded by user

* Plugins graph which is a function of plugin and cluster metadata merger

Data model
----------

5 new models are going to be added:

* DeploymentGraph
  A model that contains a list of IDs of deployment graphs

  * id           = Graph ID

  * verbose_name = User readable name of graph

* ReleaseDeploymentGraphs
  This one is going to store couplings between releases and particular
  deployment graphs

  * id

  * type - Graph type

  * deployment_graph_id - Graph ID from DeploymentGraph table

  * release_id - Release ID

* PluginDeploymentGraph
  This one is going to store couplings between releases and particular
  plugin deployment graphs

  * id

  * type - Graph type

  * deployment_graph_id - Graph ID from DeploymentGraph table

  * plugin_id - Plugin ID

* ClusterDeploymentGraph
  This one is going to store info on particular cluster deployment graphs

  * id

  * type - Graph type

  * deployment_graph_id - Graph ID from DeploymentGraph table

  * cluster_id - Cluster ID

* DeploymentGraphTasks
  This model actually represents a list of tasks with their metadata
  and which graph they are connected to

    * id - Task id. not identical to id of task in the yaml file

    * deployment_graph_id - Id of the graph the task belongs to

    * task_name - Task name. Identical to 'id' field of the task in the
      yaml file. Unique within every graph.

    * version, test_post, test_pre, type, groups, tasks, roles,
      reexecute_on, refresh_on, required_for, requires, cross_depended_by,
      cross_depends, parameters - corresponding fields of the deployment tasks

    * _custom - custom task fields provided by the user that do not fall
      into the list above

Deployment graph model lifecycle
--------------------------------

It is possible to `create`, `update`, `delete` deployment graph and establish
relations from deployment graph to the Release, Cluster and Plugin records.

Creation
^^^^^^^^

Graph `type` and related model `id` + `type` is required to create graph.
Graph `tasks` and graph `name` is optional.

There could be only one graph of given `type` related to the external model. So
any graph could be addressed by external model ID and graph `type`.

Clusters is supposed to be default relation target for the custom graphs.

Default graph type is `default` and this type will be used in all operations
if no type is specified.

Update
^^^^^^

Graph `name` (verbose name, not `type`) and graph tasks could be updated.

During update Nailgun fetches existing tasks from DB, making diff against
new tasks and performs create/delete operations based on `task_name` field to
reduce DB load.

Tasks is atomic, when task content is not changed, task is preserving its
database surrogate is.
When any field of task is changed, task will be re-created.

TBD: task update preserving database ID (by task_name)?

Deletion
^^^^^^^^

Tasks is related as many-to-one to the deployment graph and will be cascade
deleted when graph is removed.

Graph external relation is cascade deleted when external model is removed or
graph is removed.

TBD: two approaches to graph deletion is possible:

1. Every graph is related only to one external model, when parent model is
removed, this graph is removed automatically.

2. Graph is related to the one or more models and should be deleted when
all external relations is removed. So the orphan graphs cleanup on nailgun
models deletion or changes events or via cron-job-like garbage collection
script is required.

REST API
--------

An API handler should be introduce to support:

* list existing graphs for specified cluster

* upload graph from yaml file by graph type and class
  for specified cluster (only for cluster graph)

* download existing graph or merge of some existing graphs
  to yaml file by graph type and class for specified cluster

* delete existing graph by graph type and class
  from specified cluster (only for cluster graph)

* execute existing graph with graph type
  on the subset of nodes or whole cluster

Graph information JSON format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

  {
    "type": "graph_type",
    "name": "Verbose Graph Name",
    "tasks": {
      "id": "my-task",
      "type": "puppet",
      "parameters": {
        ...
      }
    }
  }

Operations with graph by graph ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Metainformation about graphs (list of graphs with names and relations)
  `GET /graphs/`

(TBD: do we need graph creation without attachment to model?)

* Create graph
  `POST /graphs/`

* Get Information about specific graph
  `{'name': 'name', 'relations': '[...]', 'tasks': '[...]'}`

  `GET /graphs/<graph-id>`

* Update graph
  `PUT /graphs/<graph-id>`

* Delete graph
  `DELETE /graphs/<graph-id>`

(TBD: Why not to use handler above to operate tasks? Do we need granular
tasks operations?)

* Get tasks
  `GET /graphs/<graph-id>/tasks`

* Update tasks
  `PUT /graphs/<graph-id>/tasks`

* Get task by DB ID
  `GET /graphs/<graph-id>/tasks/<task-id>`

(TBD: is PUT required? Task is supposed to be atomic and every update should be
create operation if task content differ or leave task intact if it is the same
do we need granular tasks operations at all?)

* Update task by DB ID
  `PUT /graphs/<graph-id>/tasks/<task-id>`

* Delete task by DB ID
  `DELETE /graphs/<graph-id>/tasks/<task-id>`

Operations with graph via different models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Get all graphs for release
  `GET /releases/<release_id>/deployment_graphs/`

* Create graph related to Release
  `POST /releases/<release_id>/deployment_graphs/`

* Operate specific type for Release
  `GET/PUT/DELETE /releases/<release_id>/deployment_graphs/<graph_type>/`


* Get all graphs for Cluster
  `GET /clusters/<cluster_id>/deployment_graphs/`

* Get merged tasks for the environment

  Existing `GET /clusters/<cluster_id>/deployment_tasks/`
  Should be extended with `type` parameter

* Create graph related to Cluster
  `POST /clusters/<cluster_id>/deployment_graphs/`

* Operate specific type related to Cluster
  `GET/PUT/DELETE /clusters/<cluster_id>/deployment_graphs/<graph_type>/`

(TBD: do we need merged plugins tasks for the environment?)


* Get all graphs for Plugin
  `GET /plugins/<cluster_id>/deployment_graphs/`

* Create graph related to Plugin
  `POST /plugins/<cluster_id>/deployment_graphs/`

* Operate specific type related to plugin
  `GET/PUT/DELETE /clusters/<plugin_id>/deployment_graphs/<graph_type>/`



Run custom graph
^^^^^^^^^^^^^^^^

Graph should be ran for given cluster with optional nodes list.
And it is not possible to run graph without cluster.

* Existing `PUT /cluster/<cluster_id>/deploy/`

  Should be extended with `type` parameter.

Fuel CLI
--------

Fuel CLI interface `graph` command should be extended:

Graph uploading
^^^^^^^^^^^^^^^

* fuel2 graph upload --env env_id [--type graph_type] --file tasks.yaml

(TBD: do we need CLI functionality for modification of plugin and release
graphs?)

* fuel2 graph upload --release release_id [--type graph_type] --file tasks.yaml
  (?)

* fuel2 graph upload --plugin plugin_id [--type graph_type] --file tasks.yaml
  (?)

`--type` is optional. ‘default’ graph type with confirmation should be used if
no type is defined.

Graph downloading
^^^^^^^^^^^^^^^^^

* fuel2 graph download --env env_id [--type graph_type]
  [--file tasks.yaml]

* fuel2 graph download --release release_id [--type graph_type]
  [--file tasks.yaml]

* fuel2 graph download --plugin plugin_id [--type graph_type]
  [--file tasks.yaml]

`--type` is optional and ‘default’ graph will be downloaded in no type is defined.
Graph execution

Graph execution
^^^^^^^^^^^^^^^

* fuel2 graph execute --env env_id [--type graph_type] [--node node_ids]

Graph execution available only for the environment.




* fuel graph list --env env_id

* fuel graph upload --env env_id --cluster --type graph_type --file tasks.yaml

* fuel graph download --env env_id --cluster --type graph_type --file
  cluster_graph.yaml

* fuel graph download --env env_id --plugins --type graph_type
  --file plugins_graph.yaml

* fuel graph download --env env_id --release --type graph_type
  --file release_graph.yaml

* fuel graph download --env env_id --cluster --release --type graph_type
  --file merged_cluster_and_release_graphs.yaml

* fuel graph download --env env_id --all --type graph_type --file
  merged_all_graphs.yaml

* fuel graph execute --env env_id --type graph_type [--node node_ids]

RPC Protocol
------------

None

Fuel Client
===========

Fuel client should be modified to support usage of one-shot or continuous
custom graphs, e.g. CRUD operations with the graph and triggering of
deployment of the particular graph *type* within the cluster

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

Use other solutions like Mistral or Solar, but their integration
might take more than months.

--------------
Upgrade impact
--------------

None, as this functionality will be available only for 9.0 clusters

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

Improvment of overall user experience and ability for a user to script
arbitrary deployment actions such maintenance of cluster, security updates
and even upgrades

------------------
Performance impact
------------------

Insignificant overhead while working with graph models

-----------------
Deployment impact
-----------------

Deployment could be customized since this feature is implemented
and each deployment task can be logged against particular cluster
it is being executed with

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

Possible increase of memory consumption on the Master node
by Nailgun and Postgres

--------------------
Documentation impact
--------------------

Client and API documentation should be extended

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  ikutukov

Other contributors:
  bgaifullin
  vsharshov

Mandatory design review:
  rustyrobot
  ikalnitsky


Work Items
==========

* Implement data models

* Modify tasks serializers to fetch data from these models and merge graphs
  on the fly

* Add REST API handlers

Dependencies
============

-----------
Testing, QA
-----------

Introduce functional testing for graph overrides and one-shot executions, e.g.
generate a graph, upload it, execute it.

Acceptance criteria
===================

As a user I should be able to inject a set of tasks into deployment graph
per-cluster or execute one-shot deployment of a particular deployment graph
without injecting it into default deployment flow.

----------
References
----------
