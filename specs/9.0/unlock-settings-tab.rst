..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Unlock Settings and Networks Tabs
==========================================

https://blueprints.launchpad.net/fuel/+spec/unlock-settings-tab

This blueprint introduces new feature allowing a user
to change cluster parameters on Settings and Networks Tabs for a deployed,
partially deployed cluster (e.g. a stopped deployment case)
for further redeployment with new parameters

--------------------
Problem description
--------------------

As an Operator I want to be able to adjust configuration on Settings and
Networks tabs and hit "Deploy changes" (or do equivalent operation on CLI)
in a post-deployment stage of cloud lifecycle so that I could perform "Day 2"
operations (reconfigure cloud and plugins parameters, etc)

----------------
Proposed changes
----------------

We proposed to unlock Settings an Networks tabs for clusters in 'operational',
'error', 'stopped' and 'partially_deployed' states. And allow user to change
and save new settings and then rerun the deployment.

Web UI
======

The Dashboard tab
-----------------

The 'Deploy Changes' button behavior should be changed for clusters in
'operational', 'stopped', 'error' and 'partially_deployed' states.

UI should take into account the 'changes' field of Cluster model and should
show the 'Deploy Changes' button if 'attributes' or 'networks' sections are not
empty. UI should notify user about the consequences of the changes on clusters
in 'operational', 'error', 'stopped' and 'partially_deployed' states.
This notification should be added to the existing notification displayed right
after the User clicked 'Deploy Changes' button

The 'List of changes' to deploy should include notifications about changed
cluster attributes or network configuration (and such a notification should
have Discard button to load deployed attributes/network configuration).

The Settings Tab
----------------

New plugins can be enabled on already deployed cluster. For hot-pluggable
plugins it can be done w/o any warnings, but for not hot-pluggable plugins a
warning should be shown to user. Not hot-pluggable plugins should be detected
by 'hot_pluggable' attribute in openstack.yaml. 'always_editable' attribute
should be depricated.

The 'Load Deployed' button should be implemented on 'Settings' tab. This button
should load deployed settings for this cluster. This button is actual for
cluster with not 'new' status. And the existing 'Load Defaults' button is
actual for not "new" cluster too.

The Networks Tab
----------------

The 'Load Deployed' button should be implemented on 'Networks' tab. This button
should load deployed network configuration for this cluster. This button is
actual for cluster with not 'new' status

Nailgun
=======

Modify the calculation of 'is_locked' attribute.
'is_locked' should be "True" during deployment and provisioning and for old
clusters after deployment.

Data model
----------

The 'always_editable' attribute in openstack.yaml is not applicable anymore.
The 'hot_pluggable' attribute in openstack.yaml should be introduced. It will
be set for hot-pluggable plugins during plugin installation and will be used
to detect hot-plugablle plugins for UI warnings.

REST API
--------

- New ClusterAttributesDeployedHandler should be introduced:

  `/clusters/(?P<cluster_id>\d+)/attributes/deployed/?$`

  This handler allows to load last deployed attributes for the cluster.
- New NetworkConfigurationDeployedHandler should be introduced:

  `/clusters/(?P<cluster_id>\d+)/network_configuration/deployed?$`

  This handler allows to load last deployed network configuration
  for the cluster.

- The existing handler

  `/clusters/(?P<cluster_id>\d+)/changes/redeploy/?$`

  should be extended to support YAQL expressions [0] and to keep the expected
  behavior: rerun all tasks on all nodes in the cluster.

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

All settings introduced by activated plugins can be changed by user as well
User can activate any plugins. For not hot-pluggable plugins there should be a
warning from UI

Fuel Library
============

None

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

None

---------------
End user impact
---------------

End user can enjoy the full advantage of Life Cycle Management
and 2nd-day operations on deploying and deployed clusters

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

Developers should take into account the fact that all tasks can be rerun
on already deployed clusters and make them work with same input parameters
(idempotency) and with changed input parameters.

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

As part of Basic LCM this feature should be properly documented

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  bgaifullin

Other contributors:
  jaranovich
  vkramskikh
  vsharshov
  ikutukov
  vkuklin
  ashtokolov

Mandatory design review:
  ikalnitsky
  vkramskikh
  rustyrobot

Work Items
==========

Data model changes
UI support
CLI support

Dependencies
============

* https://blueprints.launchpad.net/fuel/+spec/computable-task-fields-yaql

* https://blueprints.launchpad.net/fuel/+spec/store-deployment-tasks-history

* https://blueprints.launchpad.net/fuel/+spec/dry-run-redeployment

* https://blueprints.launchpad.net/fuel/+spec/save-deployment-info-in-database

* https://blueprints.launchpad.net/fuel/+spec/custom-graph-execution

------------
Testing, QA
------------

This feature should be covered by test cases with redeployment
for each parameter changes.

Acceptance criteria
===================

As a user I should be able to change settings of deployed, partialy deployed,
stopped or erred cluster and run redeployment with new parameters

----------
References
----------

[0] - https://blueprints.launchpad.net/fuel/+spec/computable-task-fields-yaql

