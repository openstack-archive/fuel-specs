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

Web UI should not delete any deployment tasks. In other case this will
be erase tasks history.

Nailgun
=======

Modules to be changed:

* add tasks history DB table

* introduce tasks history table update in receiver

* add reset api

Data model
----------

Add new table tasks_history with the following scheme:

* FK deployment_task_id - ID of deploy task in Nailgun tasks table
* task_name - deployment task name
* node_id - ID of the node where task is being run (was run)
* time_start  - timestamp of task start
* time_end - timestamp of task end
* status - enum of task statuses returned by astute [0]
* summary  - json field. It contains additional info for audit.
  It can be a `stdout`, puppet `last run summary` or any task
  information defined on astute side. In case of puppet it provides
  the information about changed resources, failures, retries, like
  Puppet Master or Foreman. In case of rsync or upload_files we will
  be able to analyse the stdout of failed commands


REST API
--------

There will be a REST API handler allowing to get a list of tasks and
(tentatively) particular task details in case of failure

+--------+---------------------------------+-------------------+-------------+
| method | URL                             | action            | auth exempt |
+========+=================================+===================+=============+
|  GET   | /api/tasks/:task_id/            | get list of all   | false       |
|        | deployment_tasks                | history tasks     |             |
+--------+---------------------------------+-------------------+-------------+

The methods should return the following statuses in case of errors:

* 404 Not found - in case of missing entry
* 405 Not Allowed - for `PUT /api/tasks/:task_id/tasks_history`

GET method should also support filters by node or/and by history tasks
statuses:

* /api/tasks/:task_id/tasks_history/?nodes={nodes ids} - to get all tasks
  for such nodes
* /api/tasks/:task_id/tasks_history/?statuses={list of statuses} - to get all
  tasks with such statuses
* /api/tasks/:task_id/tasks_history/?statuses={list of statuses}
  &nodes={nodes ids} - to get list of all tasks with such statuses on
  selected nodes

GET method returns JSON of the following format:

.. code-block:: json

    [
      {
        'id': 13,
        'deployment_task_id': 12,
        'node_id': 5,
        'task_id': 34,
        'task_name': 'swift-keystone',
        'time_start': 1457362146,
        'time_end': 1457362276,
        'status': 'ready',
        'summary': {
          "sender": "5",
          "statuscode": 0,
          "statusmsg": "OK",
          "data": {
            "time": {
              "anchor": 0.00019831,
              "config_retrieval": 1.015772457,
              "file": 0.0012266030000000002,
              "filebucket": 8.4232e-05,
              "mysql_database": 0.018598403,
              "mysql_grant": 0.076972123,
              "mysql_user": 0.073092031,
              "package": 0.000257408,
              "schedule": 0.0005276500000000001,
              "total": 1.186729217,
              "last_run": 1456971170
            },
            "resources": {
              "failed": 0,
              "changed": 7,
              "total": 19,
              "restarted": 0,
              "out_of_sync": 7,
              "failed_to_restart": 0,
              "scheduled": 0,
              "skipped": 0
            },
            "changes": {
              "total": 7
            },
            "events": {
              "failure": 0,
              "success": 7,
              "total": 7
            },
            "version": {
              "config": 1456971167,
              "puppet": "3.8.3"
            },
            "status": "stopped",
            "running": 0,
            "enabled": 1,
            "idling": 0,
            "stopped": 1,
            "lastrun": 1456971170,
            "runtime": 0,
            "output": "Currently stopped; last completed run 0 seconds ago"
          }
        }
      },
      {
        'id': 15,
        'deployment_task_id': 12,
        'node_id': 6,
        'task_id': 67,
        'task_name': 'openstack-network-common-config',
        'time_start': 1457362143,
        'time_end': 1457362273,
        'status': 'ready',
        'summary': {
          "sender": "6",
          "statuscode": 0,
          "statusmsg": "OK",
          "data": { ... }
        }
     ...
   ]

Orchestration
=============

Add new fields to Nailgun report:

* deployment_graph_task_id — this is task_id in term of Nailgun Tasks History
  which will be used to update tasks
* summary — last run puppet summary for success or error statuses

RPC Protocol
------------

None

Fuel Client
===========

Fuel Client have to show task statuses for particular Nailgun task.
New command should be added:

.. code-block:: console

  fuel tasks-history --task-id 1
  fuel tasks-history --task-id 1 --node-id 5,6
  fuel tasks-history --task-id 1 --statuses error,ready
  fuel tasks-history --task-id 1 --node-id 5,6 --statuses error,ready

Also, appropriate commands should be added to fuel2 client:

.. code-block:: console

  fuel2 tasks-history 1
  fuel2 tasks-history 1 --nodes node_id_1 [node_id_2 ...]
  fuel2 tasks-history 1 --statuses task_status_1 [task_status_2 ...]
  fuel2 tasks-history 1 --nodes 1 --statuses error


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
