..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Store Deployment Tasks Execution History in DB
==============================================

https://blueprints.launchpad.net/fuel/+spec/store-deployment-tasks-history

As Fuel user leveraging its LCM feature set I would like to have an
opportunity to fetch history of all deployment tasks ever ran against
any of my environments. This would allow me to perform configuration change
and maintenance of my cluster with ability to do troubleshooting and audit of
things happening in the cluster.

--------------------
Problem description
--------------------

Currently, it is almost impossible for any Fuel user to understand the history
of changes happened to his cluster. This puts a barrier onto adoption of Fuel
as not only as an OpenStack installer, but also as a cloud management tool.
This change proposes to store all the information about particular deployment
tasks ever executed for each particular cluster.

This would allow for anyone to understand status of the cluster it is
currently in, which tasks were ever ran and what could have possibly gone
wrong.


----------------
Proposed changes
----------------

Main changes are going to happen within Nailgun Data Model. This assumes
creation of additional relation in Nailgun DB that will store history of
deployment tasks with relation to particular global Nailgun tasks.

The other part that is going to be changed is Nailgun receiver module code
that is going to update deployment tasks status.

Web UI
======

None

Nailgun
=======

Modules to be changed:

* add tasks history DB table

* introduce tasks history table update in receiver

* add reset api

Data model
----------

Add new table deployment_history with the following scheme:

* FK task_id default not NULL - ID of deploy task in Nailgun tasks table
* deployment_graph_task_name not NULL - task name in the deployment graph
  associated with the particular Nailgun task_id
* String node_id not NULL - ID of the node (or master) where task is being
  run (was run)
* time_start  - timestamp of task start
* time_end - timestamp of task end
* status not NULL - enum of task statuses returned by astute with
  default `pending` [0]


Add new time field for tasks table `deleted_at`. Change deletion behavior
for tasks: instead of deletion from DB Nailgun should write deleted_at
time and stay it in DB.

Old API endpoint `/api/tasks` return only tasks with `deleted_at is null`
column in order to keep backward compatibility with UI.
Also `/api/tasks` endpoint has mark as deprecated because it superseded
by `/api/transactions`.

Add new unique constraint for such fields: task_id, node_id,
deployment_graph_task_name.

Add index for such fields combination to support API calls:

* task_id and node_id
* task_id and status
* task_id and node_id and status

REST API
--------

There will be a REST API handler allowing to get a list of tasks and
(tentatively) particular task details in case of failure

+--------+---------------------------------+-------------------+-------------+
| method | URL                             | action            | auth exempt |
+========+=================================+===================+=============+
|  GET   | /api/transactions/\             | get list of all   | false       |
|        | :transaction_id/\               | deployment tasks  |             |
|        | deployment_history              | of a nailgun task |             |
+--------+---------------------------------+-------------------+-------------+
|  GET   | /api/transactions/              | get list of all   | false       |
|        |                                 | nailgun tasks     |             |
|        |                                 | including deleted |             |
+--------+---------------------------------+-------------------+-------------+

The methods should return the following statuses in case of errors:

* 404 Not found - in case of missing entry
* 405 Not Allowed - for `PUT /api/transactions/:transaction_id/\
  deployment_history`

GET method should also support filters by node or/and by history tasks
statuses:

* /api/transactions/:transaction_id/deployment_history/\
  ?nodes={nodes ids} - to get all tasks for such nodes
* /api/transactions/:transaction_id/deployment_history/\
  ?statuses={list of statuses} - to get all tasks with such statuses
* /api/transactions/:transaction_id/deployment_history/\
  ?statuses={list of statuses}&nodes={nodes ids} - to get the list of all
  tasks with such statuses on the selected nodes

GET method returns JSON of the following format:

.. code-block:: json

    [
      {
        'id': 13,
        'task_id': 12,
        'node_id': '5',
        'deployment_graph_task_name': 'swift-keystone',
        'time_start': 1457362146,
        'time_end': 1457362276,
        'status': 'ready',
      },
      {
        'id': 15,
        'task_id': 12,
        'node_id': 'master',
        'deployment_graph_task_name': 'generate_keys',
        'time_start': 1457362143,
        'time_end': 1457362273,
        'status': 'ready'
       }
     ...
   ]

Orchestration
=============

Rename field `task` in Nailgun report to `deployment_graph_task_name`

RPC Protocol
------------

None

Fuel Client
===========

Fuel Client have to show task statuses for particular Nailgun task.
New command should be added:

.. code-block:: console

  fuel deployment-tasks --task-id 1
  fuel deployment-tasks --task-id 1 --node-id 5,6
  fuel deployment-tasks --task-id 1 --status error,ready
  fuel deployment-tasks --task-id 1 --node-id 5,6 --status error,ready

Also, appropriate commands should be added to fuel2 client:

.. code-block:: console

  fuel2 task history show 1
  fuel2 task history show 1 --nodes node_id_1,[node_id_2 ...]
  fuel2 task 1 history show --statuses task_status_1,[task_status_2 ...]
  fuel2 task 1 history show --nodes 1 --statuses error


Plugins
=======

None

Fuel Library
============

None

--------------
Upgrade impact
--------------

Should be disabled for pre-9.0 clusters

---------------
Security impact
---------------

None so far

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

Ability to easier troubleshoot and perform maintenance and day-2 operations

------------------
Performance impact
------------------

Insignificant

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

None except for generic feature documentation

--------------
Implementation
--------------

Assignee(s)
===========


Primary assignee:
  vsharshov

Other contributors:
  bgaifullin
  ashtokolov

Mandatory design review:
  ikalnitsky
  rustyrobot

Work Items
==========

* Add new relation for tasks history in the DB

* Modify Receiver part to update tasks history DB

* Add REST API list and show handlers

* Modify Fuel CLI behaviour to work with "non-purging" tasks in nailgun tasks

Dependencies
============

------------
Testing, QA
------------

Basic unit tests, scalability tests for 10000 transaction of Nailgun
**deploy** tasks, simple functional testing.

Acceptance criteria
===================

As a user I should be able to run several deployments and list results
of tasks execution per-node, per-cluster and per-run

----------
References
----------

[0] https://blueprints.launchpad.net/fuel/+spec/task-based-deployment-astute
