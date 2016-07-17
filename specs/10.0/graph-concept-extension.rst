..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================
Fuel Graph Concept Extension And Usage
======================================

https://blueprints.launchpad.net/fuel/+spec/graph-concept-extension

There is introduced a new opportunity that allows to execute graphs
for different purposes by the Fuel graph concept extension.


-------------------
Problem description
-------------------

Currently, the Fuel graph concept is tied to the deployment process.

As minimum, we need to use a graph execution process
for the following base actions:

    * verification
    * deletion
    * provisioning
    * deployment

For example, there is no mechanism to verify realistic network configurations
before the deployment. New changes will allow to execute the verification graph
that configures the production specific network and performs the necessary
checks for it on bootstrap nodes. Thus, we will have an opportunity
to find out network defects earlier. Such possibility may save hours of rework
during a large deployment.

We also need the provisioning process be more flexible. We would like to be able
to extend the provisioning with plugins or to inject additional steps into it.
For example, for more scalable provisioning it is a common practice to use p2p protocols,
e.g. bittorrent. If we have provisioning as a graph, it is much easier to implement
this approach: we can simply replace "image getting" task with a torrent client spawning.

There were described only two base examples, although the extension of the fuel graph
concept will allow us to execute all necessary actions on the necessary stage. We only
should create the corresponding graph and describe new graph tasks if needed.

----------------
Proposed changes
----------------

The main changes will be introduced in nailgun, astute and library parts.

New 'transactions manager' should be implemented, so the execution of some graph
or a bunch of graphs should be considered as transaction. The transaction translates
cluster from the state A to the state B even A and B are same.

It is also necessarily to add new task type 'set_node_properties' that sends custom node status
to Nailgun. The task with such type may be added at the end of the graph and developer may specify
in it what should be changed in nodes properties after the current graph execution.

For example,

.. code::

    - id: set_status_provisioned
      type: set_node_properties
      version: 2.1.0
      role: ['/.*/']
      requires: [node_reboot]
      required_for: [provision_end]
      parameters:
        status: 'provisioned'
        pending_addition: false

Thus, it will be possible to avoid the hardcoded changes of nodes statuses and extend the graph execution
mechanism for different cases.

The default graphs for verification, deletion, provisioning and deployment should be composed
(or updated in deployment case) and loaded during the Fuel installation. Some additional task types
should be introduced.

The existing custom graph mechanism can be used [0] to upload and execute the custom graph via CLI. Although,
we need to extend it for executing several graphs one by one.


Web UI
======

Custom graphs management in Fuel UI was described and implemented within the [1], although the ability
to execute a sequence of graphs is introduced in this spec as extension.

Working in 'Custom Workflows' deployment mode, user should be able to specify a sequence of space-separated
graph types, that he wants to execute.

Also, it is necessary to use a new /api/v1/graphs/execute/ handler (that works with transactions manager)
in Fuel UI to run a graph/graphs.


Nailgun
=======

* Introduce the Transactions Manager.

* Implement the corresponging handler for graph(s) execution via the Transactions Manager.

* Handle the transaction rpc responce.

* Extend the upgrade/downgrade procedure with task models and task types.

* Implement the corresponding unit tests.


Data model
----------

Task model should be extended with 'graph_type' and 'dry_run' fields.


REST API
--------

New API call to execute graph(s) via the Transaction Manager should be added:

    * `POST /graphs/execute`

    with the data in the following format:

      .. code-block:: json

        {
          cluster: [cluster id],
          nodes: [list of nodes, optional],
          graph_types: [list of graph types, optional],
          task_names: [list of tasks names, optional],
          dry_run: [default:false, optional],
          force: [default:false, optional]
        }

As the graph term was extended, some requests should be modified to avoid misunderstanding.
In the following requests the deployment/deploy word should be removed:

    * `GET /releases/<release_id>/deployment_graphs/`

    * `GET/POST/PUT/PATCH/DELETE /releases/<release_id>/deployment_graphs/<graph_type>/`

    * `GET /releases/<release_id>/deployment_tasks/`

    * `GET /clusters/<cluster_id>/deployment_graphs/`

    * `GET /clusters/<cluster_id>/deployment_tasks/`

    * `GET/POST/PUT/PATCH/DELETE /clusters/<cluster_id>/deployment_graphs/<graph_type>/`

    * `GET /plugins/<cluster_id>/deployment_graphs/`

    * `GET/POST/PUT/PATCH/DELETE /plugins/<plugin_id>/deployment_graphs/<graph_type>/`

    * `GET /clusters/<cluster_id>/deploy_tasks/graph.gv`


Orchestration
=============

'GraphsExecutorHandler' should be added with the following possible http response codes:

        * 200 (task successfully executed)
        * 202 (task scheduled for execution)
        * 400 (data validation failed)
        * 404 (cluster or nodes not found in db)


RPC Protocol
------------

None


Fuel Client
===========

For listing/uploading/downloading will be used the common custom graph commands [0].

The graph execution command should stay practically the same, however it is necessary to be able
to define several graph types to run them one by one. Also it should be possible to enforce execution
of tasks without skipping and to run only specific tasks ignoring dependancies.

.. code::

    fuel2 graph execute --env 1 [--nodes 1 2 3] [--graph_types gtype1 gtype2] [--task-names task1 task2] [--force] [--dry-run]


Plugins
=======

None


Fuel Library
============

* Update the default deployment graph with 'set_node_properties' task.

* Compose the default provisioning and deletion graphs.

* Compose the default verification graph. This graph should contain tasks
  for the network configuring and checking.

* All default graphs should be loaded during the Fuel installation with
  the corresponding graph types.


------------
Alternatives
------------

None for the whole approach.

For the verification tool:
    * Use the standard network verification mechanism, although in this
      case we have a deal with non-realistic network configuration.
    * Use connectivity checker plugin [2] to verify network during
      the deployment, but it will take more time to rework.


--------------
Upgrade impact
--------------

Graph concept extension will be introduced for Fuel 10.0.


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

Ability to:
    * execute different graphs for different purposes.
    * check the realistic network configuration design before the deployment process.


------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

The whole mechanism is more flexible. The provisioning part is configurable
and easier to debug. Thanks to the verification graph mechanism, errors
detection before the deployment stage may save a lot of time in case of
reconfiguration necessity.


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

* API, CLI and UI documentations should be extended according to the appropriate changes.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  bgaifullin

Other contributors:
  vsharshov (astute)
  sbogatkin (library: deletion, provisioning)
  lefremova (library: verification)
  ikutukov  (client)

Mandatory design review:
  ashtokolov
  vkuklin


Work Items
==========

[Nailgun] Extend the deployment graph mechanism so we can execute a graph
for the different purposes: implement the transactions manager.

[Astute] A number of new task types should be added.

All the hardcoded stasuses (except for 'error' and 'stopped') should be removed.
They should be specified inside the task with 'set_node_properties' type.

[Agent] All necessary packages (as minimum: puppet, puppet-common, daemonize)
for execution the graphs on bootstrap-nodes should be installed.

[Fuel Library] Create and load the default verification, provisioning and
deletion graphs, make the necessary changes in the deployment one.

[Fuel Client] Extend CLI so the user is able to define several graph types
to run them one-by-one and perform the base actions via user-friendly commands.


Dependencies
============

Custom graph management on UI [1].


-----------
Testing, QA
-----------

* New logic in nailgun should be covered by unit and integration tests.

* Functional tests that executes verification and provisioning graphs on bootstrap nodes should be
  introduced.


Acceptance criteria
===================

* The Fuel graph concept is extended so we can use a graph mechanism
  for different purposes.

* Network checking tool in Fuel is introduced for realistic configurations
  via execution an appropriate verification graph on bootstrap nodes.
  So as a cloud operator I have the possibility to investigate the production
  specific network defects before the deployment.

* Provisioning and deletion mechanisms also work via the corresponding graphs
  execution.

* While the default graphs for the base actions are loaded during the Fuel
  insallation, user may specify and execute custom graphs.


----------
References
----------

[0] Allow user to run custom graph on cluster
    https://blueprints.launchpad.net/fuel/+spec/custom-graph-execution
[1] Custom graph management on UI
    https://blueprints.launchpad.net/fuel/+spec/ui-custom-graph
[2] Connectivity checker plugin
    https://github.com/xenolog/fuel-plugin-connectivity-checker
