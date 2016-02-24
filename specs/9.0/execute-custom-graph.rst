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

The proposed change assumes that each deployed cluster has 3 deployment
graphs with the following hierarchy:

* Release-default Graph

* Graphs introduced by plugins (effective merge of these graphs)

* Cluster-specific Graph

The lower one overrides the higher ones. A user can always alter deployment
of the cluster by specifying which graph he wants to run particular deployment
with.

All the changes are going to be related to Nailgun and python-fuelclient parts.

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

An API handler to support graphs upload/list/update/deletion
should be introduced.

RPC Protocol
------------

None

Fuel Client
===========

Fuel client should be modified to support usage of one-shot or continuous
custom graphs, e.g. CRUD operations with the graph and triggering of
deployment of the particular cluster

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

Improval of overall user experience

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

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

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

As a user I should be able to inject a set of tasks into deployment graph per-cluster
or execute one-shot deployment of a particular deployment graph without injecting
it into default deployment flow.

----------
References
----------
