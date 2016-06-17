..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Deployment task execution history in Fuel UI
============================================

https://blueprints.launchpad.net/fuel/+spec/ui-deployment-history

Show deployment execution graphs for all deployments in the Cluster page in
Fuel UI. This would allow End User to perform maintenance of a cluster with
an ability to do troubleshooting and audit of things happening in the cluster.


--------------------
Problem description
--------------------

Currently, it is almost impossible for Fuel UI user to see and understand
details of the deployment execution processes happened to his cluster.
User has no information about running processes on nodes during deployment,
the tasks sequence and statuses, just a total result of successful or failed
environment deployment.
It makes maintenance and troubleshooting of a cluster difficult and prolonged
in Fuel UI.


This change proposes to show all the information about particular deployments
ever executed for each particular cluster and it's nodes.


----------------
Proposed changes
----------------


Web UI
======

#. Deployment progress bar on a cluster Dashboard should be clickable if
   'deployment' task is running in the cluster. By click on the progress bar,
   a graph with the deployment data should appear.

#. If a cluster was already deployed, then the cluster page should
   include a new 'Deployment History' tab that displays graphs of all
   finished cluster deployments.
   Use should be able to choose a particular deployment on the tab (each
   deployment in the list has its own id and the start time unique attributes)
   and get the process details and see graphs for all the deployed nodes.

Deployment graph is a set of timelines and each timeline represents a sequence
of deployment tasks for each deployed cluster node.
An additional timeline shows execution of tasks on the master node.

Each task is an area on a node timeline, which should reflect the following
data about the task:

* name
* the start time
* the end time
* status

A task area should be clickable and display a pop-up with all other task
properties, which come from API.

Timelines should be scalable and support zooming for better UX.

[TBD] Node deployment process can be finished with success or error result.
Deployment graph should display an error message of the failed task.

A timeline does not include tasks with 'skipped' status because they don't
participate in the deployment.
The same for tasks with 'pending' status. They are not presented in a timeline
because they are not started yet.

[TBD] Do we want to display a total duration timer for a deployment timeline?

Deployment timeline should have a control to switch to a table representation.
It is a set of tables (a table per deployed node), that display a list of
deployment tasks on a particular node. The table columns are:

* name
* the start time
* the end time
* status
* [TBD] message (in case of failed task?)
* additional information (all other task attributes)

The list of tasks should be sorted by the start time attribute in a table.

All tasks, including skipped and pending, should be shown in a table view.

History of a particular cluster deployment comes from
`GET /api/transactions/<deployment_id>/deployment_history/` response.
The response is a list of objects that describe deployment tasks in
the following format (only attributes used in Fuel UI are described):

.. code-block:: json

  {
    "task_name": "upload_configuration",
    "node_id": "master",
    "status": "pending",
    "time_start": null,
    "time_end": null,
    ...,
    "requires": ["pre_deployment_start"],
    "required_for": ["pre_deployment_end"],
    "custom": {},
    "type": "upload_file",
    "refresh_on": ["*"],
    "parameters": {
      "path": "/etc/openstack/config.yml",
      "timeout": 180,
      "data":{
        "yaql_exp": "$.toYaml()"
      }
    },
    "version": "2.1.0",
    "role": ["master", "/.*/"],
    "roles": ["master", "/.*/"],
  }

where

* `task_name` is a name of a deployment task
* `node_id` is id of node where a task executed OR 'master' string, that means
  a task is executed on the master node
* `status` is a status of a task and has one of the following values:
  'pending' (default), 'ready', 'running', 'error', or 'skipped'
* `time_start` is a timestamp when a task was started (Null if a task is not
  started yet)
* `time_end` is a timestamp when a task was finished (Null if a task is not
  started or not finished yet)

`task_name` attribute can also have `null` value. Such tasks represent
synchronization processes on nodes and refer to Virtual Sync Node. Fuel UI
should not display a timeline for this node, timelines of cluster nodes or
the master node should be shown only.

Ids of all cluster deployments come from the response of
`GET /api/transactions?cluster_id=<cluster_id>&tasks_names=deployment` API
call.

`GET /api/transactions/?cluster_id=<cluster_id>&tasks_names=deployment&
statuses=running` API call should be used on the cluster Dashboard to get id
of the running deployment.


Nailgun
=======


Data model
----------

No changes required.


REST API
--------

#. Need to add filtering of results by task names or/and statuses for
   `GET /api/transactions/` method. The following API calls should be 
   supported:

   * `GET /api/transactions/?cluster_id=<cluster_id>&tasks_names=deployment`
   * `GET /api/transactions/?cluster_id=<cluster_id>&tasks_names=deployment&
     statuses=running`

#. Each item in `GET /api/transactions/` response should contain `time_start`
   attribute, that will be used in Fuel UI to distinguish cluster deployments
   by their 'id' and 'time_start' attributes.
   TransactionCollection class should be modified accordingly.


Orchestration
=============


RPC Protocol
------------

No changes required.


Fuel Client
===========

[TBD] Should filtering of transaction collection by task names or/and statuses
be added to fuel-client?


Plugins
=======

No changes required.


Fuel Library
============

No changes required.


------------
Alternatives
------------

None.


--------------
Upgrade impact
--------------

None.


---------------
Security impact
---------------

None.


--------------------
Notifications impact
--------------------

None.


---------------
End user impact
---------------

Ability to easier troubleshoot and perform maintenance of a cluster.


------------------
Performance impact
------------------

None.


-----------------
Deployment impact
-----------------

None.


----------------
Developer impact
----------------

None.


---------------------
Infrastructure impact
---------------------

None.


--------------------
Documentation impact
--------------------

Fuel UI user guide should be updated to include information about the feature.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  jkirnosova

Other contributors:
  bdudko

Mandatory design review:
  vkramskikh
  ashtokolov


Work Items
==========

* Display a deployment graph of a current deployment on the Dashboard tab.
* Display history graphs of all finished cluster deployments in a new
  Deployment History tab.
* Support both display modes for a deployment graph: a timeline view and
  a table view.
* Add filters for a table representation of a deployment history (filters
  by node, task name, task status).


Dependencies
============

None.


------------
Testing, QA
------------

* Manual testing.
* UI functional tests should cover the changes.

Acceptance criteria
===================

Fuel UI user should be able to run several deployments for a cluster and see
the deployment tasks history in the cluster page, including real-time
information about a current deployment.


----------
References
----------

* Store Deployment Tasks Execution History in DB
  https://blueprints.launchpad.net/fuel/+spec/store-deployment-tasks-history
