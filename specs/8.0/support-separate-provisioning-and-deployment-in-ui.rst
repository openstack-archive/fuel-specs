..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================================
Support for separate provisioning and deployment in UI
======================================================

https://blueprints.launchpad.net/fuel/+spec/support-separate-provisioning-and-deployment-in-ui

It is now possible to run provisioning only, without deploy, via CLI, the same
functionality is needed to be supported from Fuel UI.

--------------------
Problem description
--------------------

In large OpenStack environment it might be important to find errors early,
without long-running deployment step. So that when provisioning fails, there
will be no need in starting deployment.


----------------
Proposed changes
----------------

Web UI
======

[tbd]
Add a button on Dashboard tab to provision all nodes. This button should be
visible only for not-deployed environment.

'Provision' button will not be visible in case of any errors with OpenStack
Environment. If the environment already has provisioned nodes but also contains
nodes with 'pending_provisioning' status - only 'pending_provisioning' nodes
will be provisioned.

'Deploy' button will be hidden until provisioning is done instead there will be
'Provision and Deploy' button aside with 'Provision' button.


Nailgun
=======

[tbd] - provisioning task name to be clear up as well as the whole API for this


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
[Note] - python engineer is needed here


---------------
End user impact
---------------

User will now have an ability to provision all nodes in the OpenStack
environment independently from deploying OpenStack environment.


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

QA engineer:
    Anastasia Palkina, apalkina (apalkina@mirantis.com)

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

*. It is possible to run provisioning separately from deployment for all nodes
*. There is an ability to deploy OpnStack environment with pre-provisioned
nodes


----------
References
----------

* Support for separate provisioning and deployment in UI
https://blueprints.launchpad.net/fuel/+spec/support-separate-provisioning-and-deployment-in-ui
* #fuel-ui on freenode

