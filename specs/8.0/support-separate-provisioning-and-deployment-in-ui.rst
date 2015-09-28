..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================================
Support for separate provisioning and deployment in UI
======================================================

https://blueprints.launchpad.net/fuel/+spec/support-separate-provisioning-and-deployment-in-ui

It is now possible to run provisioning only without deploy via CLI, the same
functionality is needed to be supported from Fuel UI.

--------------------
Problem description
--------------------

In large cluster it might be important to find errors early, without
long-running deployment step. So that when provisioning fails, there won't be
no need in starting deployment.


----------------
Proposed changes
----------------

Web UI
======

tbd
Add a button on Dashboard tab to provision all nodes.

Nailgun
=======

None

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

None


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

Notification of successful or error provisioning should be added.


---------------
End user impact
---------------

User will now have an ability to provision all nodes in the cluster
independently from deploying cluster.


------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

Deployment process will slightly change, with th one major change - ability
to deploy already provisioned nodes.

(tbd - will it be possible to run old classic deploy & provisioning?)


----------------
Developer impact
----------------

None


--------------------------------
Infrastructure/operations impact
--------------------------------

None


--------------------
Documentation impact
--------------------

Documentation should be changed according to new ability added


--------------------
Expected OSCI impact
--------------------

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
 Aleksandra Morozova, astepanchuk (astepanchuk@mirantis.com)

Visual design:
  Bogdan Dudko, bdudko (bdudko@mirantis.com)

Mandatory design review:
  Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com)


Work Items
==========

#. Visual design clarification and implementation
#. UI logics implementation
#. New notifications should be implemented and shown


Dependencies
============

None


------------
Testing, QA
------------

#. Manual testing - we should check that nodes have new status - provisioned
#. UI functional tests should be implemented


Acceptance criteria
===================

*. It is possible to run provisioning seperately from deployment


----------
References
----------


