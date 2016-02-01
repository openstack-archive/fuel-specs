..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Enable users to specify nodes for provisioning and/or deployment
================================================================

https://blueprints.launchpad.net/fuel/+spec/allow-choosing-nodes-for-provisioning-and-deployment

Introduce an ability to run provisioning and deployment tasks
separately for the all environment nodes or a particular node selection.


--------------------
Problem description
--------------------

In large OpenStack environment, it might be important to find errors early,
without long-running deployment step. So that when provisioning fails, there
will be no need to start deployment.

Currently, UI can only run both provisioning and deployment one after another.
Fuel UI should have a possibility to run the tasks separately. This will give
the End User a control over the action and scope of the changes being made.

Moreover, Fuel UI should enable users to specify particular node(s) for
provisioning and/or deployment.


----------------
Proposed changes
----------------


Web UI
======

For new not deployed environment with nodes added, it should be a new control
on Dashboard tab to start a separate provisioning task or a super deployment
task to provision and deploy node(s):

.. image:: ../../images/9.0/
   allow-choosing-nodes-for-provisioning-and-deployment/deploy-button.png
   :scale: 75 %

Separate provisioning task can be started if there are not provisioned and
not deployed node(s) in the environment.
Nodes with 'error' status and 'provisioning' error type (`error_type`
attribute of a node model) are also considered as not provisioned.

[TODO] How the new control should look like if it is possible to run
provisioning task only for the environment (deployment is impossible due to
some errors)?

Running provisioning can not be stopped fro UI for now. This planned to be
considered as a separate feature.

If user clicks the main 'Deploy Changes' button on Dashboard tab to run
both provisioning and deployment for the whole environment (for all
environment nodes), only not provisioned nodes will be provisioned and
deployed, and provisioned and not deployed nodes will be deployed only.

Provisioning or deployment separate tasks can not be launched for already
provisioning or deploying environment (if appropriate tasks are active).

Fuel UI environment workflow is not changed if the environment has Virtual
nodes. Then 'Provision VMs' button is available from Dashboard tab only.

User should also be able to choose particular node(s) when he run
a separate task provision or deployment task:

[TODO] screenshot of node selection flow should be here

Already provisioned, deployed and offline nodes should not be visible on
this screen when choosing nodes for provisioning.

Not provisioned and already deployed nodes should not be visible on
this screen when choosing nodes for separate deployment task. This deployment
task can be run for provisioned nodes only.

The screen of node selection for provisioning or deployment task should
have a standard node list functionality: sorting, filtration, labelling,
search, switching of node view modes.
But no action buttons (like node deletion, disks or interfaces configuration)
should be displayed on the screen.
User selection in node list management toolbar (applied sorters, filters,
etc.) is not stored in Nailgun DB, because this is not a frequently used
scree.


Nailgun
=======

The feature required Fuel UI changes only.

Data model
----------

No changes required.


REST API
--------

No changes required.

Existing API is used to handle provisioning and deployment tasks:

* `PUT /api/clusters/<cluster_id>/changes` request with empty data
  is used to run deployment super task (both provisioning and deployment,
  one after another)
* `PUT /api/clusters/<cluster_id>/provision` is used to run provisioning task
  (empty data should be sent if the task should be run for all environment
  nodes)
* `PUT /api/clusters/<cluster_id>/deploy` is used to run deployment only task
  (empty data should be sent if the task should be run for all environment
  nodes)

[TODO] What format of data should be sent in PUT requests to run a task for
particular nodes?

To track a status of super deployment task (that runs both provisioning and
deployment for all environment) Fuel UI should process `deploy` task.
To track provisioning progress Fuel UI should process `provision` task.
To track separate deployment task status Fuel UI process poll `deployment`
task.


Orchestration
=============

No changes required.


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

None.


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

User Guide should be updated according to the changes.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  jkirnosova (jkirnosova@mirantis.com)

Other contributors:
  bdudko (bdudko@mirantis.com) - visual design

Mandatory design review:
  vkramskikh (vkramskikh@mirantis.com)
  ikalnitsky (ikalnitsky@mirantis.com)


Work Items
==========

#. Prepare visual mockups for the Fuel UI changes.
#. Implement an ability to run provisioning and deployment separately
   for an environment.
#. Implement an ability to run provisioning or deployment for
   particular node selection.


Dependencies
============

None.


------------
Testing, QA
------------

* Manual testing.
* UI functional tests should be updated to cover the changes.

Acceptance criteria
===================

* It is possible to run provision of nodes separately from deployment in
  environment.
* It is possible to deploy OpenStack environment with pre-provisioned nodes.
* It is possible to run provisioning or deployment for particular environment
  node(s).


----------
References
----------

#fuel-ui on freenode
