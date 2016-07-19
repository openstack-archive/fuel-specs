..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
Manage Custom Graphs from Fuel UI
=================================

https://blueprints.launchpad.net/fuel/+spec/ui-custom-graph

This blueprint extends Fuel UI with ability to list, upload, download, and
run custom workflows (custom graphs) that are sets of arbitrary deployment
actions such maintenance of cluster, security updates and even upgrades [1].


--------------------
Problem description
--------------------

Now Fuel UI gives User no instruments to view, upload, download, or execute
custom deployment graphs. At the same time, an ability to do this will help
to operate with complex life-cycle management (LCM) use cases such bug fixing
and other cluster updates.


----------------
Proposed changes
----------------


Web UI
======

Workflows tab
-------------

Fuel UI should be extended with new 'Workflows' tab.

The 'Workflows' tab should contain a table with all graphs for the current
cluster.
Rows in a workflows table should be grouped by graph level that can be
'release', 'plugin' or 'cluster'.

Workflows table should have the following columns:

* graph name
* graph type
* 'Download' button (to download the graph as yaml file)

+-------------------+-------------+-----------+
| Graph Name        | Graph Type  |           |
+===================+=============+===========+
| RELEASE           |             |           |
+-------------------+-------------+-----------+
| release_graph     | default     | Download  |
+-------------------+-------------+-----------+
| mu-1-release      | 9.0-mu-1    | Download  |
+-------------------+-------------+-----------+
+-------------------+-------------+-----------+
| PLUGIN "LMA"      |             |           |
+-------------------+-------------+-----------+
| lma-plugin        | default     | Download  |
+-------------------+-------------+-----------+
| lma-plugin        | upgrade     | Download  |
+-------------------+-------------+-----------+
+-------------------+-------------+-----------+
| PLUGIN "CONTRAIL" |             |           |
+-------------------+-------------+-----------+
| release_graph     | default     | Download  |
+-------------------+-------------+-----------+
+-------------------+-------------+-----------+
| CLUSTER           |             |           |
+-------------------+-------------+-----------+
| cluster_graph     | default     | Download  |
+-------------------+-------------+-----------+
| mu-1-cluster      | 9.0-mu-1    | Download  |
+-------------------+-------------+-----------+

Note that workflows table should not include graphs of not enabled cluster
plugins.

Graph should be sorted by name in the table, but graphs with 'default' type
should go first.

Workflows table should support filtering by deployment graph level and by
graph type. Both filters should support multiple values selection.

[TBD] Is User able to remove a particular graph of 'cluster' level from UI?


The 'Workflows' tab should also display a form for uploading a new graph for
the current cluster (the new graph level will be 'cluster').
To upload a graph User should fill the following fields:

* graph verbose name (optional; graph can have an empty verbose name)
* graph type
* graph yaml file (optional; graph can be empty `{}`)

Deployment graphs should have unique types within their level.


There should be also a list of merged graphs on the tab (graphs of all levels
that have the same type are merged into a single resulting graph).
Fuel UI user should be able to download yaml file of a merged graph.

+-------------------+-------------+-----------+
| Graph Type        |             |           |
+===================+=============+===========+
| default           | Download    | Run       |
+-------------------+-------------+-----------+
| 9.0-mu-1          | Download    | Run       |
+-------------------+-------------+-----------+
| upgrade           | Download    | Run       |
+-------------------+-------------+-----------+


Dashboard tab
-------------

Fuel UI user should be able to start execution of merged graph of a particular
type.

In deployed cluster, the top block on the 'Dashboard' tab that represents
deployment modes should be extended by a new 'Custom Graph' mode (custom
graphs can be executed for deployed environment only).

When user chooses this deployment mode, a dropdown with all merged cluster
custom graphs (list of graph types) should appear.

Note that a resulting graph with 'default' type executed by clicking
existing 'Deploy Changes' button in Fuel UI. So, there will be no 'default'
graph in this custom graphs dropdown.

User should specify the graph type and click 'Select Nodes' button to open
a standard 'Select Nodes' pop-up to select nodes for current graph execution.
All cluster nodes are selected for the graph execution by default.
When nodes are chosen User is able to run the selected graph.

Graph execution can not be started if some of the selected nodes are offline.


Nailgun
=======


Data model
----------

No changes required.


REST API
--------

No changes required.

Existing API should be used:

* `GET /clusters/<cluster_id>/deployment_graphs/` to get all graphs of
  'cluster' level for a particular cluster

  Response data is returned in the following format:

  .. code-block:: json

    [
      {
        id: 1,
        name: null,
        relations: {
          type: 'default',
          model: 'cluster',
          model_id: 1
        },
        tasks: [...]
      },
      ...
    ]

* `GET /clusters/<cluster_id>/deployment_tasks/?graph_type=<graph_type>`
  to get merged tasks for a particular graph of 'cluster' level

* `GET /releases/<release_id>/deployment_graphs/` to get all graphs of
  'release' level for a particular cluster release

  Response data is returned in the following format:

  .. code-block:: json

    [
      {
        id: 1,
        name: null,
        relations: {
          type: 'default',
          model: 'release',
          model_id: 1
        },
        tasks: [...]
      },
      ...
    ]

* `GET /releases/<release_id>/deployment_tasks/?graph_type=<graph_type>`
  to get merged tasks for a particular graph of 'release' level

* `GET /plugins/<plugin_id>/deployment_graphs/` to get all graphs of
  'plugin' level for a particular cluster plugin

  Response data is returned in the following format:

  .. code-block:: json

    [
      {
        id: 1,
        name: 'My Plugin Graph',
        relations: {
          type: 'my_plugin',
          model: 'plugin',
          model_id: 1
        },
        tasks: [...]
      },
      ...
    ]

* `GET /plugins/<plugin_id>/deployment_tasks/?graph_type=<graph_type>`
  to get merged tasks for a particular graph of 'plugin' level

* `GET /clusters/<cluster_id>/deployment_tasks/?graph_type=<graph_type>`
  to get merged tasks for a particular graph

* `POST /clusters/<cluster_id>/deployment_graphs/` to create a new graph for
  the current cluster (the graph level will be 'cluster').

  Data in the following format should be sent by Fuel UI:

  .. code-block:: json

    {
      name: 'my graph name',
      relations: {
        type: 'my_graph_type',
        model: 'cluster',
        model_id: 1
      },
      tasks: {
        name: 'my yaml file name',
        content: '...'
      }
    }

* `PUT /cluster/<cluster_id>/deploy/?graph_type=<graph_type>`
  with empty data to run merged graph of a particular type on all cluster
  nodes

* `PUT /cluster/<cluster_id>/deploy/?graph_type=<graph_type>&nodes=<node_ids>`
  with empty data to run merged graph of a particular type on a subset of
  nodes


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

Mandatory design review:
  vkramskikh
  ashtokolov


Work Items
==========

#. Add a new 'Workflows' tab with all cluster graphs listing.
#. Add controls to upload a new cluster graph.
#. Add controls to run a particular custom graph on a subset of cluster nodes.


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

Fuel UI user is able to list, download deployment graphs and run the graph of
the selected type on the subset of nodes or on the whole cluster.


----------
References
----------

[1] Allow user to run custom graph on cluster
    https://blueprints.launchpad.net/fuel/+spec/custom-graph-execution