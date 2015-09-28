..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Enable users to specify nodes for provisioning and/or deployment
================================================================

https://blueprints.launchpad.net/fuel/+spec/allow-choosing-nodes-for-provisioning-and-deployment

Introduce an ability to select environment node(s) and choose whether
to provision (operating system), deploy (OpenStack) or both onto the node(s).


--------------------
Problem description
--------------------

In large OpenStack environment it might be important to find errors early,
without long-running deployment step. So that when provisioning fails, there
will be no need in starting deployment.

Currently UI can only run both provisioning and deployment one after another.
Fuel UI should have a possibility to run the tasks separately. This will give
the End User a control over the action and scope of the changes being made.

Moreover, Fuel UI should enable users to specify particular node(s) for
provisioning and/or deployment.


----------------
Proposed changes
----------------

Web UI
======

For new not-deployed environment with nodes added, it should be a new control
on Dashboard tab to start provisioning task only:

.. image:: ../../images/8.0/
   allow-choosing-nodes-for-provisioning-and-deployment/
   dashboard-tab-change.png
   :scale: 75 %

.. image:: ../../images/8.0/
   allow-choosing-nodes-for-provisioning-and-deployment/
   separate-tasks-control.png
   :scale: 75 %

[TBD] 'Provision' button should be visible if there are some not-provisioned
and not-deployed node(s) in environment, except the following errors in
the environment:

* not enough controllers (minumim is 1 controller node)
* not enough Ceph OSD nodes (if Ceph storage settings are active)
* not enough Mongo DB nodes (if Ceilometer service is enabled)
* not enough Ironic nodes (if Ironic service is enabled)
* invalid environment settings configuration
* invalid vCenter configuration (for vCenter environment)

[TBD] How UI button should look like if it is possible to run provisioning
task only for the environment (deployment is impossible due to some errors)?

If the environment already has provisioned nodes but also has not-provisioned
and not-deployed nodes - only the last nodes will be provisioned.

[TBD] If the environment already has deployed nodes but also has new
not-provisioned nodes - the last ones can be provisioned.

[TBD] If provisioning was failed on some nodes, are they available for
re-provisioning?

[TBD] Can we stop provisioning process from UI as well as we can do with
deployment?

If user clicks the main 'Deploy Changes' button on Dashboard tab to run
both provisioning and deployment for the whole environment (for all
environment nodes), only unprovisioned nodes will be provisioned and
deployed, and provisioned and not-deployed nodes will be deployed only.

Provisioning or deployment tasks can not be launched for already
provisioning or deploying environment (an appropriate tasks are active).

Fuel UI environment workflow is not changed if the environment has Virtual
nodes. Then 'Provision VMs' button is available from Dashborad tab only.

User should also be able to choose particular node(s) when he clicks
an appropriate button of a separate task:

.. image:: ../../images/8.0/
   allow-choosing-nodes-for-provisioning-and-deployment/
   provisioning-screen.png
   :scale: 75 %

[TBD] Provisioned and deployed nodes should be locked from the selection
on this screen, when choosing nodes for provisioning only.

[TBD] Unprovisioned and deployed nodes should be locked from the selection
on this screen, when choosing nodes for separate deployment task. This
deployment task can be run for provisioned nodes only.

The screen of node selection for the specific task should support a standard
node list functionality: sorting, filtration, labelling, search, switching
of node view modes. But no action buttons (like node deletion, discarding node
changes, disks or interfaces configuration) should be displayed on the screen.
User selection in node management toolbar (applied sorters, filters, etc.) is
not stored in Nailgun DB, because this is not a frequently used screen, and
Fuel UI also does not store informtion about what particular nodes was
selected for provisioning or deployment.

Environment settings (OpenStack settings, networking settings) should be
locked if any environment node is already deployed.


Nailgun
=======

No changes required.


Data model
----------

No changes required.


REST API
--------

[TBD] No changes required. Existing API is used to handle separate
provisioning and deployment tasks:

* sending `PUT /api/clusters/<cluster_id>/changes` request with empty data
  is used to run deployment super task (both provisioning and deployment,
  one after another)
* `PUT /api/clusters/<cluster_id>/provision` is used to run provisioning task
* `PUT /api/clusters/<cluster_id>/deploy` is used to run deployment only task

[TBD] What format of data should be send in PUT requests: selected node(s)
id(s)

To track a status of super deployment task (that runs botn provisioning and
deployment for all environment) Fuel Ui shoould continue to poll `deploy`
task.
To track provisioning progress Fuel UI should poll `provision` task status.
To track separate deployment task status Fuel UI should poll `deployment`
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

None


--------------
Upgrade impact
--------------

None


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

[TBD] Does notification of successful/failed provisioning already exist?


---------------
End user impact
---------------

None


------------------
Performance impact
------------------

None


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

User guide should be changed according to the changes.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  vkramskikh (vkramskikh@mirantis.com)

Other contributors:
  jkirnosova (jkirnosova@mirantis.com) - JS code
  bdudko (bdudko@mirantis.com) - visual design

QA engineer:
  apalkina (apalkina@mirantis.com)

Mandatory design review:
  vkramskikh (vkramskikh@mirantis.com)


Work Items
==========

#. Prepare visual mockups for the Fuel UI changes
#. Implement an ability to run provisioning and deployment separately
   for an environment
#. Implement an ability to select particular node(s) for provisioning
   and/or deployment


Dependencies
============

None


------------
Testing, QA
------------

* Manual testing
* UI functional tests should be updated to cover the changes


Acceptance criteria
===================

* It is possible to run provisioning separately from deployment for
  environment
* There is an ability to deploy OpenStack environment with pre-provisioned
  nodes
* It is possible to select particular node(s) for provisioning or
  deployment


----------
References
----------

#fuel-ui on freenode
