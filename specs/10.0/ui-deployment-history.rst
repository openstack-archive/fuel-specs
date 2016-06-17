..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Deployment task execution history in Fuel UI
============================================

https://blueprints.launchpad.net/fuel/+spec/ui-deployment-history

Show deployment task execution graphs for all deployments in the Cluster page
in Fuel UI. This would allow End User to perform maintenance of a cluster with
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

#. If deployment was started once for a cluster, then the cluster page should
   include a new tab that displays graphs of all cluster deployments including
   the running one if it exists.
   Use should be able to choose a particular deployment on the tab
   to get the process details and see graphs for all the deployed nodes. 

Deployment graph is a set of timelines, which represent a subtask sequence
of 'deployment' Nailgun task for each deployed cluster node.
An additional timeline shows execution of deployment subtasks on the master
node.

Each subtask is an area on a node timeline, which should reflect the following
data about the subtask:

* name
* the start time
* the end time
* status

Timelines should be scalable and support zooming for better UX.

[TBD] Deployment process of a node can be finished with success or error
result. Deployment graph should display an error message of the failed subtask.

[TBD] A timeline does not include subtasks with 'skipped' status because they
don't participate in the deployment. BUT a list of skipped subtasks should be
available for the End User.

[TBD] The same for subtasks with 'pending' status. They are not presented in
a timeline because they are not started yet. BUT a list of pending subtasks
should be available for the End User.

All the data about a cluster deployment comes from
`GET /api/transactions/<deployment_task_id>/deployment_history/` response.
The response is a list of objects in the following format (only attributes
used in Fuel UI are described):

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

* `task_name` is a name of the deployment subtask
* `node_id` is id of node where the subtask executed OR 'master' string,
  that means the subtask is executed on the master node
* `status` is a status of the subtask and has one of the following values:
  'pending' (default), 'ready', 'running', 'error', or 'skipped'
* `time_start` is a timestamp when the subtask was started
  (Null if the subtask is not started yet)
* `time_end` is a timestamp when the subtask was finished
  (Null if the subtask is not started or not finished yet)

Ids of all cluster deployment tasks come from the response of
`GET /api/transactions?cluster_id=<cluster_id>&tasks_names=deployment` API 
call.

For the Dashboard tab it makes sense to send `GET /api/transactions/
/?cluster_id=<cluster_id>&tasks_names=deployment&statuses=running`
API call to get id of running deployment only.


Nailgun
=======


Data model
----------

No changes required.


REST API
--------

Need to add filtering of results by task names or/and statuses for
`GET /api/transactions/` method. The following API calls should be supported:

* `GET /api/transactions/?cluster_id=1&tasks_names=deployment`
* `GET /api/transactions/?cluster_id=1&tasks_names=deployment&statuses=running`


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

Fuel UI user guide should be updated to include information about
the new feature.


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

* Display a task history graph of a current deployment on the Dashboard tab.
* Display graphs of all cluster's deployment tasks in a new separate tab.


Dependencies
============

* Store Deployment Tasks Execution History in DB (implemented)
  https://blueprints.launchpad.net/fuel/+spec/store-deployment-tasks-history


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

#fuel-ui on freenode