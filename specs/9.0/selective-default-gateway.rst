..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================================================================
Allow to select a network where default gateway will be taken from
==================================================================

https://blueprints.launchpad.net/fuel/+spec/selective-default-gateway-net

It should be possible to select any network from existing ones where default
gateway will be taken from.

-------------------
Problem description
-------------------

Default gateway for nodes is always taken from Public network (or Admin network
where Public network is absent). It should be possible to select any network
from existing ones where default gateway will be taken from. Selection should
be environment-wide for the first implementation.

----------------
Proposed changes
----------------

API/CLI/UI must allow to select a network where default gateway will be taken
from. It can be any of existing networks where gateway (and other L3
parameters) is set.

Changes are proposed for Nailgun. Additional parameters for CLI/UI will be
added into cluster attributes so CLI/UI changes are not required.

Web UI
======

None. Cluster attributes (fixture) will contain a new parameter
(network selection) that will be shown in UI.

Nailgun
=======

Need to update possible values for a new cluster attribute (see Data model)
when networks are changed.

Data serialization for orchestrator will take selected network (from cluster
attributes) into account when serializing default gateways for nodes.
So, gateway of selected network will be taken as default gateway for a node if
the network exists on given node. It the network does not exist on the node
then gateway of Admin network is taken as default gateway for the node.

Data model
----------

Cluster attributes (openstack.yaml fixture):
add a selector ``Network to take default gateway from`` which will allow to
select a network by name from all the networks which have gateway being set.

REST API
--------

None. Cluster attributes (fixture) will contain a new parameter.

Orchestration
=============

None

RPC Protocol
------------

None. Algorithm of default gateway selection will be changed.

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

N/A

--------------
Upgrade impact
--------------

N/A

---------------
Security impact
---------------

N/A

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

User will be able to select a network from existing ones where default
gateway will be taken from.

------------------
Performance impact
------------------

N/A

-----------------
Deployment impact
-----------------

TBD

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

TBD

--------------------
Documentation impact
--------------------

TBD

--------------------
Expected OSCI impact
--------------------

N/A

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee: Aleksey Kasatkin

Other contributors: Artem Roma

Mandatory design review: Alex Didenko


Work Items
==========

- Add new attribute into cluster attributes (in the fixture)
- Auto-update attribute in Nailgun on networks changes
- Change gateway serialization for orchestrator in Nailgun


Dependencies
============

N/A

-----------
Testing, QA
-----------

In order to verify the quality of new features, automatic system tests will be
expanded by the cases listed below:

1. Default gateway is selected on management network (or/and other network that
   exists on all nodes). Single and multi rack cases.

2. Default gateway is selected on a network that exists not on all nodes.
   Single and multi rack cases.


Acceptance criteria
===================

It should be allowed to select a network where default gateway for nodes
will be taken from.

----------
References
----------

https://blueprints.launchpad.net/fuel/+spec/selective-default-gateway-net
