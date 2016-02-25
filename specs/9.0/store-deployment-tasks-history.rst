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

id -  autoincrement primary key
FK deployment_task - ID of deploy task in Nailgun tasks table
task_name - task name as in deployment_tasks.yaml, for example
node_id - ID of the node where task is being run (was run)
time_started  - timestamp of task start
time_ended - timestamp of task end
status - enum of task statuses returned by astute - consult
[0] task-based deployment blueprint task statuses for the details

REST API
--------

There will be a REST API handler allowing to get a list of tasks and
(tentatively) particular task details in case of failure

+--------+-----------------------------+---------------------+-------------+
| method | URL                         | action              | auth exempt |
+========+=============================+=====================+=============+
|  GET   | /api/tasks/:task_id/        | get list of all     | false       |
|        | tasks_history               | history tasks       |             |
+--------+-----------------------------+---------------------+-------------+
|  PUT   | /api/tasks/:task_id/        | update history task | false       |
|        | tasks_history/              | _____               |             |
|        | :history_task_id            | _____               |             |
+--------+-----------------------------+---------------------+-------------+
| DELETE_| /api/tasks/:task_id/        | delete history task | false       |
|        | tasks_history/              | _____               |             |
|        | :history_task_id            | _____               |             |
+--------+-----------------------------+---------------------+-------------+

The methods should return the following statuses in case of errors:

* 400 Bad Request - in case of invalid data (missing field, wrong format)
* 404 Not found - in case of missing entry
* 405 Not Allowed - for `PUT /api/tasks/:task_id/tasks_history`


GET method returns JSON of the following format:

.. code-block:: json

   [
     {
       'id': 13,
       'deployment_task_id': 12,
       'node_id': 5,
       'task_name': 'swift-keystone',
       'time_started': 1457362146,
       'time_ended': 1457362276,
       'status': 'error'
     },
     {
       'id': 15,
       'deployment_task_id': 12,
       'node_id': 6,
       'task_name': 'openstack-network-common-config',
       'time_started': 1457362143,
       'time_ended': 1457362273,
       'status': 'ready'
     }
     ...
   ]

PUT method accepts data of the following format:

.. code-block:: json

   {
     'status': 'error'
   }

and returns:

.. code-block:: json

   {
     'id': 13,
     'deployment_task_id': 12,
     'node_id': 5,
     'task_name': 'swift-keystone',
     'time_started': 1457362146,
     'time_ended': 1457362276,
     'status': 'error'
   }

DELETE method accepts data of the following format:

.. code-block:: json

   {
     id: Number(identificator)
   }

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

Fuel Client have to show task statuses for particular Nailgun task.
New command should be added:

.. code-block:: console

  fuel tasks-history --task-id 1

Also, appropriate commands should be added to fuel2 client:

.. code-block:: console

  fuel2 tasks-history 1


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
