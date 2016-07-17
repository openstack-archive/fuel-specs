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

Currently, the Fuel graph concept is tied on the deployment process.

As minimum, we need to use a graph execution process
for the following base actions:

    * verification
    * deletion
    * provisioning
    * deployment

For example, there is no mechanism to verify realistic network configurations
before the deployment. New changes will allow to execute the verification graph
that configures the production specific network and performs the necessary
checks for it on bootstrap nodes. Thus, we will have the opportunity
to find out network defects earlier.Such possibility may save hours of rework
during a large deployment.

We also need the provisioning process be more flexible.

----------------
Proposed changes
----------------

The main changes will be introduced in nailgun and astute parts.
It is necessarily to add new 'on-success' field to the task model
so the developer can specify by himself what should be changed in the system
if the curent task will be completed successfully. Thus, it will be possible
to avoid the hardcoded changes of nodes statuses in astute and extend the graph
execution mechanism in nailgun for different cases.

The default graphs will be created (or updated in deployment case) and loaded
during the Fuel installation. Although a cloud operator will be able to upload
the custom one via CLI or UI. The existing custom graph mechanism can be used
for these purposes [0].


Web UI
======

All changes should be described and implemented within the [1].

Nailgun
=======

* Update task serializer so it could handle 'on-success' field.
* Extend the deployment mechanism so it could work with different graphs
and actions.
* The current provisioning and deletion tasks should be removed.


Data model
----------

Task model should be extended with 'on-succes' part:

.. code::

  - id: task-id
    condition: yaql_exp: {some yaql expression}
    on-success:
      status: provisioned


REST API
--------

As the graph term was extended, some requests should be modified
to avoid misunderstanding.

`PUT /cluster/<cluster_id>/deploy/` should be changed by
`PUT /cluster/<cluster_id>/execute/`.

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

Deployment handlers should be renamed and rewritten for the extension purposes.

RPC Protocol
------------

None


Fuel Client
===========

For listing/uploading/downloading will be used the common custom graph
commands [0].

The graph execution command should stay practically the same, however it is
necessary to be able to define several graph types to run them one-by-one:

.. code::

    fuel2 graph execute --env env_id [--types graph_types] [--node node_ids]

Also, we need to extend CLI to perform the base actions with user-friendly
commands. For example, the default verification graph execution on all nodes of
'NewEnv' should look like this:

.. code::

    fuel2 graph execute verification --env NewEnv

The same mechanism should be added for deletion, provisioning, deployment
actions. It should be also possible to run them together with the defined graph
types. The full chain of necessary actions will contain all of them
in the following order: verification, deletion, provisioning, deployment.


Plugins
=======

None


Fuel Library
============

* Update tasks in the default deployment graph so they contain 'on-success'
field where needed.

* Compose the default provisioning and deletion graphs.

* Compose the default verification graph. This graph should contain
all necessary tasks for ‘netconfig’, ‘netconfig’ itself and tasks
for network checking.

* All default graphs should be loaded during the Fuel installation with
the corresponding 'default_verification', 'default_deletion',
'default_provisioning' and 'defaul_deployment' graph types.


------------
Alternatives
------------

None for the whole approach.

For the verification tool:
    * Use the standard network verification mechanism, although in this
    case we have a deal with non-realistic network configuration.
    * Use connectivity checker plugin [2] to verify network during
    the deployment, but it will take more time to rework.
    * Create an additional verification task in nailgun, implement task manager
    and receiver for it. Their structure will be very similar to the existing
    deployment one.


--------------
Upgrade impact
--------------

Graph concept extension will be introduced only for Fuel 10.0.


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
    * check the realistic network configuration design before
    the deployment process.


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

* Documentation on tasks fields should be updated.

* API and CLI documentations should be extended according to the appropriate
changes.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  bgaifullin

Other contributors:
  vsharshov (astute)
  sbogatkin (provisioning)
  lefremova (verification)

Mandatory design review:
  ashtokolov
  vkuklin


Work Items
==========

[Nailgun] Extend the deployment graph mechanism so we can execute a graph
for the different purposes. Use it instead of the previous one for provisioning
and deletion tasks.

[Astute] Remove all the hardcoded stasuses. They should be specified inside
the task description for now.

[Astute] All necessary packages (as minimum: puppet, puppet-common, daemonize)
for execution the verification graph on bootstrap-nodes should be installed.

[Fuel Library] Create and load the default verification, provisioning and
deletion graphs, make the necessary changes in the deployment one.

[Fuel Client] Extend CLI so the user is able to define several graph types
to run them one-by-one and perform the base actions via user-friendly commands.


Dependencies
============

Allow user to run custom graph on cluster [0].

-----------
Testing, QA
-----------

* New logic in nailgun should be covered by unit and integration tests.

* Functional test that executes verification graph on bootstrap nodes should be
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
