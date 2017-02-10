..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================
Manage Custom Workflows from Fuel UI
====================================

https://blueprints.launchpad.net/fuel/+spec/ui-custom-graph

This blueprint extends Fuel UI with ability to list, remove, upload, download,
and run custom workflows (custom graphs) that are sets of arbitrary deployment
actions such maintenance of cluster, security updates and even upgrades [1].


--------------------
Problem description
--------------------

Now Fuel UI gives User no instruments to view, remove, upload, download, or
execute custom deployment graphs. At the same time, an ability to do this
would help to operate with complex life-cycle management (LCM) use cases
such as bug fixing or other cluster updates.


----------------
Proposed changes
----------------


Web UI
======

Workflows tab
-------------

Cluster page in Fuel UI should be extended with new 'Workflows' tab.

The 'Workflows' tab should contain a table with all graphs available for
the cluster.
Rows in a workflows table should be grouped by graph type attribute.

Workflows table should have the following columns:

* 'Name' - to display a graph name
* 'Level' - to display a graph level
* 'Actions' - contains 'Delete' button to remove a graph
  (this action available for cluster-level graphs only)
* 'Download' - contains 'JSON' and 'YAML' buttons
  (to download graph tasks in JSON or YAML format)

+-------------------+---------------+-----------+-----------+
| Name              | Level         |  Actions  | Download  |
+===================+===============+===========+===========+
| Type "default"    |               |           | JSON/YAML |
+-------------------+---------------+-----------+-----------+
| -                 | Release       |           | JSON/YAML |
+-------------------+---------------+-----------+-----------+
| -                 | Environment   | Delete    | JSON/YAML |
+-------------------+---------------+-----------+-----------+
| Type "9.0-mu-1"   |               |           | JSON/YAML |

+-------------------+---------------+-----------+-----------+
| mu-1-plugin       | Plugin        |           | JSON/YAML |
|                   | Fuel Contrail |           |           |
|                   | plugin        |           |           |
+-------------------+---------------+-----------+-----------+
| mu-1-release      | Environment   | Delete    | JSON/YAML |
+-------------------+---------------+-----------+-----------+
| Type "upgrade"    |               |           | JSON/YAML |
+-------------------+---------------+-----------+-----------+
| -                 | Release       |           | JSON/YAML |
+-------------------+---------------+-----------+-----------+
| my-plugin-graph   | Plugin        |           | JSON/YAML |
|                   | Fuel Contrail |           |           |
|                   | plugin        |           |           |
+-------------------+---------------+-----------+-----------+
| upgrade-graph     | Environment   | Delete    | JSON/YAML |
+-------------------+---------------+-----------+-----------+

Note that workflows table should not include graphs of not enabled cluster
plugins.

Graphs of 'default' type should go first in the table. Inside each group
graphs should be sorted by its level (release, plugin, and then environment
graphs).

Workflows table should support filtering by deployment graph level and by
graph type. Both filters should support multiple values selection.

To delete a graph User have to confirm the action in confirmation pop-up by
entering the graph type.

User should also be able to download JSON or YAML file with merged tasks of
resulting graph by its type (tasks of graphs that have this type and related
to different levels are merged together).


The 'Workflows' tab should also have 'Upload New Workflow' button to launch
a pop-up with a form for uploading a new graph for the current cluster
(the new graph level will be 'cluster', it is shown on UI as 'Environment').
To do this User should fill the following fields:

* graph verbose name (optional; graph can have an empty verbose name;
  if not empty, then graph name should be limited by 255 symbols)
* graph type (mandatory; should be unique within graphs of cluster level and
  related to current cluster; the input should be validated across
  `^[a-zA-Z0-9-_]+$` regexp and limited by 255 symbols)
* file with graph tasks data in JSON format (optional; graph can be empty)


Dashboard tab
-------------

Fuel UI user should be able to start execution of custom graph of a particular
type.

Top block on the 'Dashboard' tab that represents deployment modes should be
extended by a new 'Custom Workflows' mode.

Working in this deployment mode, User should specify a graph type he wants
to execute. All cluster graphs except 'default' type are available in this
deployment mode. And 'default' graph already executed by clicking existing
'Deploy Changes' button in Fuel UI.

User should also click 'Select Nodes' button to open a standard 'Select Nodes'
pop-up to specify nodes for selected graph execution.
All cluster nodes are selected in the pop-up by default.

Graph execution can not be launched from Fuel UI if no cluster nodes selected.
Graph also can not be executed if any of the selected nodes is offline.

When execution of the selected graph started, an appropriate task
(aka transaction) comes to UI. Fuel UI should display a progress bar on
Dashboard to represent a progress of the graph execution. By clicking
on the progress bar, deployment history [2] of the task should be shown.


Nailgun
=======


Data model
----------

No changes required.


REST API
--------

Existing API should be used by Fuel UI:

* `GET /graphs/?cluster_id=<cluster_id>` to get all graphs available for
  a particular cluster (graphs of different levels)

  Response data is returned in the following format:

  .. code-block:: json

    [
      {
        id: 1,
        name: null,
        relations: [{
          type: 'default',
          model: 'cluster',
          model_id: 1
        }],
        tasks: [...]
      },
      {
        id: 2,
        name: 'some name',
        relations: [{
          type: 'default',
          model: 'release',
          model_id: 1
        }],
        tasks: [...]
      },
      {
        id: 3,
        name: 'my plugin graph',
        relations: [{
          type: 'plugin123',
          model: 'plugin',
          model_id: 12
        }],
        tasks: [...]
      },
      ...
    ]

* `GET /clusters/<cluster_id>/deployment_tasks/?graph_type=<graph_type>`
  to get merged tasks of a particular graph

* `DELETE /graphs/<graph_id>` to remove a graph.

* `POST /clusters/<cluster_id>/deployment_graphs/<graph_type>` to create
  a new graph for the current cluster (the graph level will be 'cluster').

  Data in the following format should be sent by Fuel UI:

  .. code-block:: json

    {
      name: 'my graph name',
      tasks: [...]
    }

* `PUT /cluster/<cluster_id>/deploy/?graph_type=<graph_type>`
  with empty data to run a graph on all cluster nodes

* `PUT /cluster/<cluster_id>/deploy/?graph_type=<graph_type>&nodes=<node_ids>`
  with empty data to run a graph on a subset of nodes


Orchestration
=============


RPC Protocol
------------

No changes required.


Fuel Client
===========

No changes required.


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

Ability to perform maintenance of a cluster including applying of bugfixes,
security updates or even upgrade.


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
  kpimenova (JavaScript code)
  bgaifullin, ikutukov (Nailgun code)

Mandatory design review:
  vkramskikh
  ikutukov


Work Items
==========

#. Add a new 'Workflows' tab with all cluster graphs listing.
#. Add controls to upload a new cluster graph.
#. Add controls to run custom graph on cluster nodes.


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

Fuel UI user is able to list, remove, download, upload deployment graphs and
run the graph of the selected type on the subset of nodes or on the whole
cluster.


----------
References
----------

[1] Allow user to run custom graph on cluster
    https://blueprints.launchpad.net/fuel/+spec/custom-graph-execution

[2] Deployment task execution history in Fuel UI
    https://blueprints.launchpad.net/fuel/+spec/ui-deployment-history
