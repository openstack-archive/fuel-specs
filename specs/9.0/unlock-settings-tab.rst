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

The 'Deploy Changes' button behavior should be changed for clusters in
'operational', 'stopped' and 'partially_deployed' states. UI should take into
account the 'changes' field and should show the 'Deploy Changes' button if
'attributes' or 'networks' sections are not empty. Nailgun should notify user
about the consequences of the changes on clusters in 'operational', 'error',
'stopped' and 'partially_deployed' states. This notification should be
shown right after the User clicked 'Deploy Changes' button and should have
2 options: to confirm changes and run the deployment or to close
this notification w/o any operations on cluster. The confirmation should
generate the API call with 'force' parameter.
New plugins can be enabled on already deployed cluster. For hot-pluggable
plugins it can be done w/o any warnings, but for not hot-pluggable plugins a
warning should be shown to user. Not hot-pluggable plugins should be detected
by 'always_editable' attribute in openstack.yaml
The 'Load Deployed' button should be implemented on 'Settings' tab. This button
should load deployed settings for this cluster.
The 'Load Deployed' button should be implemented on 'Networks' tab. This button
should load deployed network configuration for this cluster.

Nailgun
=======

Modify the calculation of 'is_locked' attribute.
'is_locked' should be "True" during deployment and provisioning and for old
clusters after deployment.

Data model
----------

The 'always_editable' attribute in openstack.yaml is not applicable anymore.
This attribute will be used to detect not hot-plugablle plugins.
The 'force' parameter should be supported in 'ClusterChangesHandler'

REST API
--------

New ClusterAttributesDeployedHandler should be introduced:
'/clusters/(?P<cluster_id>\d+)/attributes/deployed/?$'
This handler allows to load last deployed attributes for the cluster.
New NeutronNetworkConfigurationDeployedHandler should be introduced:
'/clusters/(?P<cluster_id>\d+)/network_configuration/neutron/deployed?$'
This handler allows to load last deployed network configuration
for the cluster.


Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

'fuel deploy-changes --env env_id' should support '--force' key

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
None
