..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Unlock Settings Tab
==========================================

https://blueprints.launchpad.net/fuel/+spec/unlock-settings-tab

This blueprint introduces new feature allowing a user
to change cluster parameters on Settings Tab for a deployed,
partially deployed cluster (e.g. a stopped deployment case)
for further redeployment with new parameters

--------------------
Problem description
--------------------

As an Operator I want to be able to adjust configuration on Settings tab and
hit "Deploy changes" (or do equivalent operation on CLI) in a post-deployment
stage of cloud lifecycle so that I could perform "Day 2" operations
(reconfigure cloud parameters, enable plugins etc)

----------------
Proposed changes
----------------

We proposed to unlock Settings tab for clusters in 'operational',
'error', 'stoppped' and 'partially_deployed' states. And allow user to change
and save new settings and then rerun the deployment.

Web UI
======

None

All changes should be implemented on Nailgun side

Nailgun
=======

Modify the calculation of 'is_locked' attribute

Data model
----------

None

REST API
--------

None

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

Nailgun should notify user about the consequences of the changes on
clusters in 'operational' state

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
  vsharshov
  ikutukov
  vkuklin
  ashtokolov

Mandatory design review:
  ikalnitsky
  rustyrobot

Work Items
==========

Unlock "Settings" tab

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
stopped or errored cluster and run redeployment with new parameters

----------
References
----------
None
