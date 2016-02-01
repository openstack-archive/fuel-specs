..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Enable users to specify nodes for provisioning and/or deployment
================================================================

https://blueprints.launchpad.net/fuel/+spec/allow-choosing-nodes-for-provisioning-and-deployment

Introduce an ability to run provisioning and deployment tasks separately
for the environment nodes.


--------------------
Problem description
--------------------

In large OpenStack environment, it might be important to find errors early,
without long-running deployment step. So that when provisioning fails, there
will be no need to start deployment.

Currently, UI can only run both provisioning and deployment one after another
for all the environment nodes. Fuel UI should have a possibility to run
the tasks separately and for a particular set of nodes. This will give
the End User a control over the action and scope of the changes being made.


----------------
Proposed changes
----------------


Web UI
======

If there are nodes in an environment, User should be able to start
separate provisioning or deployment task for the environment nodes,
as well as a regular deployment of the entire environment.

.. image:: ../../images/9.0/
   allow-choosing-nodes-for-provisioning-and-deployment/dashboard-1.png
   :scale: 75 %

There is a new control in the top block of Dashboard tab to choose
a deployment mode: regular deployment of the environment, advanced
provisioning of nodes or advanced deployment of nodes.

UI of regular environment deployment is not changed. The dashboard block for
the task should include a list of node changes, warning and alert list, and
"Deploy Changes" button.

Block of a separate provisioning task should include the task description,
alert list if any, and a button to start the process or to go to a node
selection dialog:

.. image:: ../../images/9.0/
   allow-choosing-nodes-for-provisioning-and-deployment/dashboard-2.png
   :scale: 75 %

Block of a separate deployment task should also include the task description,
alert list if any, and a button to start the process or to go to a node
selection dialog. The button should be locked id there are no nodes to deploy
in an environment:

.. image:: ../../images/9.0/
   allow-choosing-nodes-for-provisioning-and-deployment/dashboard-3.png
   :scale: 75 %

Separate provisioning task can be started for online discovered
(not provisioned and not deployed) environment nodes. Nodes with 'error'
status and 'provisioning' error type (`error_type` attribute of a node model)
can also be reprovisioned.

Separate deployment task can be started for online provisioned and
not yet deployed environment nodes. Nodes with 'error' status and 'deploy'
error type are also considered as not deployed.

If user clicks 'Deploy Changes' button on the Dashboard tab to run both
provisioning and deployment for the entire environment (for all environment
nodes):

* not provisioned (discovered) nodes will be provisioned and deployed,
* provisioned and not deployed nodes will be deployed,
* already deployed nodes will be redeployed to change environment or list
  of controllers on compute, for example.

There can be only one running provisioning or deployment task for environment
at the moment.
The running separate provisioning or deployment task cannot be stopped
from UI for now. This should be considered as a separate feature.

User can choose a particular set of nodes when he runs a separate provision
or deployment task:

.. image:: ../../images/9.0/
   allow-choosing-nodes-for-provisioning-and-deployment/node-selection.png
   :scale: 75 %

Already provisioned, deployed and offline nodes should not be visible in
the list when choosing nodes for provisioning.

Not provisioned, already deployed and offline nodes should not be visible in
the list when choosing nodes for a separate deployment task.

The node selection dialog should have the following node list functionality:

* batch node selection
* sorting (nodes are sorted by roles by default)
* filtration (no filters applied by default)
* search by node name, MAC or IP address
* switching of node view modes (default view mode is 'compact')

No batch action buttons like node deletion, roles, disks or interfaces
configuration should be displayed in the dialog.

User selection in the node list management toolbar (applied sorters, filters,
etc.) is not stored in Nailgun DB, because this is not a frequently used
screen.


Nailgun
=======

The feature requires Fuel UI changes only.

Data model
----------

No changes required.


REST API
--------

No changes required.

Existing API is used to handle separate provisioning and deployment tasks:

* `PUT /api/clusters/<cluster_id>/changes` - to run deployment super task
  (both provisioning and deployment of all environment nodes)
* `PUT /api/clusters/<cluster_id>/provision` - to run separate provisioning
  of all environment nodes
* `PUT /api/clusters/<cluster_id>/provision?nodes=<node_id>,...` - to run
  separate provisioning of selected nodes (node ids should be provided)
* `PUT /api/clusters/<cluster_id>/deploy` - to run deployment only of all
  environment nodes
* `PUT /api/clusters/<cluster_id>/deploy?nodes=<node_id>,...` - to run
  separate deployment of selected nodes (node ids should be provided)

To track a status of deployment super task (that runs both provisioning and
deployment for the entire environment), Fuel UI should handle `deploy` task.
To track a separate provisioning progress, Fuel UI should handle `provision`
task.
To track a separate deployment task status, Fuel UI should handle `deployment`
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

Fuel User Guide should be updated according to the changes.


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


Work Items
==========

#. Prepare visual mockups for the Fuel UI changes.
#. Implement an ability to run separate provisioning task for an environment.
#. Implement an ability to run separate deployment task for an environment.
#. Implement an ability to run separate provisioning and deployment tasks
   for a particular set of environment nodes.


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

* It is possible to run provisioning of environment nodes separately from
  deployment.
* It is possible to deploy pre-provisioned environment nodes.
* It is possible to run the separate provisioning and deployment tasks
  for a particular set of environment nodes.
* Ability to deploy the entire environment changes with one task is saved.


----------
References
----------

#fuel-ui on freenode
