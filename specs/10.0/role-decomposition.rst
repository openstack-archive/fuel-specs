..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Role decomposition
==========================================

https://blueprints.launchpad.net/fuel/+spec/role-decomposition


--------------------
Problem description
--------------------

Currently the controller role encompasses many tasks that cannot be separated
from a controller node. Deployers should have the flexibility to distrubute
services across nodes in any combination they see fit.


----------------
Proposed changes
----------------

Task placement will be determined based on a node's label. Task definitions
will contain a list of labels which will be used to match them to nodes.
This requires a new task resolver.

Web UI
======

None

Nailgun
=======

A new resolver which matches node labels to task labels will be added.

Data model
----------

An additional field named ``labels`` will be added to roles_metadata in each
Release. This list of labels will be used during task serialization. The
labels for a node's role will be added to the any labels assigned explicitly
by the user.


REST API
--------
None

Orchestration
=============


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

All tasks will need to have one or more labels assigned to them. There will
be some tasks that require decomposition.

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

Describe how to decompose roles using node labels.

--------------
Implementation
--------------

Assignee(s)
===========


Primary assignee:
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

 #. Add new task resolver [0]_.
 #. Role/Service decomposition:
     Update fuel-library tasks to support role decomposition
 #. Update composition data access methods in fuel-library:
     Fuel-library should not rely on node roles when collecting set of
     IP addresses for a particular service (neutron, rabbitmq, etc.)
     It should be based on a node label instead.
 #. Decouple Neutron component:
     Allow different Neutron components (server, l3-agent, dhcp-agent) to
     be installed on separate nodes.


Dependencies
============

None

------------
Testing, QA
------------

Introduce tests for various combinations of controller decomposition.

Acceptance criteria
===================

User is able to deploy services currently tied to the controller (e.g. Keystone,
Neutron, MySQL) on separate nodes.

----------
References
----------

.. [0] https://review.openstack.org/#/c/341678/
