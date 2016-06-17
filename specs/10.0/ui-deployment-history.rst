..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Deployment task execution history in Fuel UI
============================================

https://blueprints.launchpad.net/fuel/+spec/ui-deployment-history

Show deployment execution graphs for all cluster deployments in Fuel UI.
This would allow End User to perform maintenance of a cluster with
an ability to do troubleshooting and audit of things happening to the cluster.


--------------------
Problem description
--------------------

Currently, it is almost impossible for Fuel UI user to see and understand
details of the deployment execution processes happened to cluster.
User has no information about running processes on nodes during deployment,
the tasks sequence and their statuses, just a final result of successful or
failed environment deployment.
It makes maintenance and troubleshooting of a cluster difficult and time
consuming in Fuel UI.

This change proposes to show all the information about particular deployments
for each particular cluster and its nodes.


----------------
Proposed changes
----------------


Web UI
======

#. Deployment progress bar on a cluster Dashboard should be clickable if
   'deployment' task is running in the cluster. By clicking on the progress
   bar a graph with the deployment data should appear.

#. Cluster page should be extended with the new 'History' tab that displays
   'Deployment History' section with data of finished cluster deployments.
   User should be able to choose a particular deployment on the tab
   (deployments are distinguished by their `id` and `time_start` attributes)
   and get the process details and see graphs for all the deployed nodes.

Deployment should be represented is a graph where x-axis is a timeline and
y-axis indicates cluster nodes. Each node section contains a sequence of
deployment tasks related to the node. An additional section shows tasks
executed on the master node. Node sections are grouped by node roles.

Each node deployment task is a bar, which should reflect the following data
about the task:

* start time
* end time
* status (failed tasks should have a special layout)

A task bar should be clickable and display a popover with the following task
data:

* name
* node ID
* node name (user-assigned name during the deployment)
* node roles
* start time
* end time
* status
* message (actual for failed tasks with 'error' status)

Timeline should support zooming for better UX.

Timeline does not include tasks with 'skipped' status because they don't
participate in the deployment.
The same for tasks with 'pending' status. They are not presented in timeline
because they are not started yet.

Deployment timeline should have a control to switch to its table
representation. It is a table that displays a list of deployment tasks and it
is divided into sections. Each section includes tasks executed on nodes of
specific roles and has an appropriate role combination as a title.

Deployment table has the following columns:

* task name
* node ID
* node name (user-assigned name during the deployment)
* task status
* start time
* end time
* details (link to a full list of the task properties)

The list of tasks in the table should be sorted by node ID, then by start time
attribute.

Link in the 'Details' column should open a pop-up with all the task
attributes listed.

All tasks, including skipped and pending, should be shown in a table view.

Deployment tasks table should support filtering by:

* task name
* node (the filter options are node name and ID pairs)
* node role
* task status

These filters should support multiple values selection (user may want to see
tasks for several nodes or with a specific set of statuses).
Filters panel should have 'Reset' button to reset applied filters.

When switching to deployment table view on the Dashboard, tasks in the table
should be filtered by 'ready', 'running' and 'error' statuses by default.

History of a particular cluster deployment comes from
`GET /api/transactions/<deployment_id>/deployment_history/` response.
The response is a list of deployment tasks in the following format (only
attributes used in Fuel UI are described):

.. code-block:: json

  {
    "task_name": "upload_configuration",
    "node_id": "6",
    "node_roles": ["compute", "cinder"],
    "node_name": "Node X",
    "status": "running",
    "time_start": "2016-06-24T06:37:51.735185",
    "time_end": null,
    "message": "",
    ...
  }

where

* `task_name` is a name of a deployment task
* `node_id` is id of node where a task was executed OR 'master' string if
  a task was executed on the master node
* `node_roles` is a list of the deployed node roles (an empty list in case of
  master node)
* `node_name` is a name that the node had at the moment of the deployment
  start (should be 'Master Node' in case of the master node)
* `status` is a status of a task and has one of the following values:
  'pending', 'ready', 'running', 'error', or 'skipped'
* `time_start` is a timestamp when a task was started (Null if a task is not
  started yet)
* `time_end` is a timestamp when a task was finished (Null if a task is not
  started or not finished yet)
* `message` is a text message that the finished task returns

`node_id` attribute can also have 'null' and '-' values.
Null here means that the task represents synchronization process on nodes and
refers to Virtual Sync Node. '-' value means that the task was not executed on
any node.
Fuel UI should not include such tasks to a timeline or deployment table, tasks
of cluster nodes or the master node should be shown only.

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

#. Model of a cluster deployment (named 'transaction') should be extended with
   `time_start` attribute, that will be used in Fuel UI to distinguish cluster
   deployments.

#. Model of a deployment task from a deployment history should be extended
   with `node_name` and 'node_roles' attributes.

#. The content of `custom` attribute of a deployment task should be merged
   with root and task should not contain the `custom` property.


REST API
--------

#. Need to add filtering of results by task names or/and statuses for
   `GET /api/transactions/` method. The following API calls should be
   supported:

   * `GET /api/transactions/?cluster_id=<cluster_id>&tasks_names=deployment`
   * `GET /api/transactions/?cluster_id=<cluster_id>&tasks_names=deployment&
     statuses=running`


Orchestration
=============


RPC Protocol
------------

No changes required.


Fuel Client
===========

None.


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

Migration should be prepared according to the changes in data models.


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
  bdudko (visual design)
  bgaifullin, ikutukov, dguryanov (Nailgun)

Mandatory design review:
  vkramskikh
  ashtokolov


Work Items
==========

* Display a deployment graph of a current deployment on the Dashboard tab.
* Display history graphs of all finished cluster deployments in a new
  History tab.
* Support both display modes for a deployment graph: a timeline view and
  a table view.
* Add filters toolbar for a table representation of a deployment history.


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
