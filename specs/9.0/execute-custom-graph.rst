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


--------------------
Problem description
--------------------

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


Upgrade

Release **upgrade** graph - empty for now but can be derived
from tasks.yaml of fuel-library or be delivered by MUs

  |darr|

Cluster **upgrade** graph (empty by default)
with cluster-specific tasks specified by the user

  |darr|

Plugins **upgrade** graphs
can be specified by plugin developers


One-shot

Release **one-shot** graph - empty

  |darr|

Cluster **one-shot** graph specified by the user
to cover the specific use case

  |darr|

Plugins **one-shot** graphs - empty


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

* Plugins graph which is a function of plugin metadata merger

Data model
----------

5 new models are goint to be added:

* DeploymentGraph
  A model that contains a list of IDs of deployment graphs

* ReleaseDeploymentGraph
  This one is going to store couplings between releases and particular
  deployment graphs

* PluginDeploymentGraph
  This one is going to store couplings between releases and particular
  plugin deployment graphs

* ClusterDeploymentGraph
  This one is going to store couplings between releases and particular
  cluster deployment graphs

* ClusterPluginDeploymentGraph
  This one will contain a graph which is a result of merge of the graphs
  for a particular cluster

* DeploymentGraphTasks
  This model actually represents a list of tasks with their metadata
  and which graph they are connected to

REST API
--------

An API handler to support graphs upload/list/update/deletion/execution
should be introduced.

Fuel CLI
--------

Fuel CLI interface `graph` command should be extended:

* fuel graph list --env env_id

* fuel graph upload --env env_id --type graph_type --file tasks.yaml

* fuel graph download --env env_id --type graph_type --file output.yaml

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

Improval of overall user experience and ability for a user to script
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

------------
Testing, QA
------------

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
