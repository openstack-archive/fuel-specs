..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================
Support node groups on the network tab in Fuel UI
=================================================

https://blueprints.launchpad.net/fuel/+spec/node-groups-network-tab

Currently there is no support on the Network tab for node groups - validation
fails for valid cases, group_id is not show, it's impossible to add/remove
network groups.


--------------------
Problem description
--------------------

For now node network groups can be viewed and managed only via command line
interface. It is important for users to have an ability to view and modify
node network groups via Fuel UI.

There should a clear and understandable UI to see the node network groups (TBD)
Nodes should be grouped by node network group for group operations.


----------------
Proposed changes
----------------

Web UI
======

tbd - we need to decide whether NNG will be a cluster attribute or cross-env

On Network tab there will appear a dropdown (select box) where the user will be
able to choose the appropriate node network work and Networks tab content would
rerender according to this selection.


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

None


---------------
End user impact
---------------

The end user will be able to see and configure the list of Networks per each
node network group

TBD


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

None


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
 Aleksandra Morozova, astepanchuk(astepanchuk@mirantis.com)

Mandatory design review:
  Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com)


Work Items
==========

#. The list of node network groups should be visible for the user on Fuel UI
#. The user should be able to see the networks according to node network groups

Dependencies
============

None


------------
Testing, QA
------------

* Manual testing
* UI functional tests


Acceptance criteria
===================

The list of node network groups is visible and easily accessable by the user.


----------
References
----------

None
