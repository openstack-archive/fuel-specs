..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================
Redesign of node roles panel
============================

https://blueprints.launchpad.net/fuel/+spec/redesign-of-node-roles-panel

Visual redesign of node roles panel in Fuel UI without changing its
functionality.


--------------------
Problem description
--------------------

Currently, node roles panel takes a big part of Add Nodes and Edit Roles
screens. User has to scroll down to node list to check nodes and then
scroll up again to check roles. This becomes more actual for desktops with
a small screen.

We also need to take into account plugins that can add its own roles, so it
can be a large list of node roles on the screen.


----------------
Proposed changes
----------------

A suggestion is to redesign the panel to improve UX of node addition and role
assignment.


Web UI
======

The following mockup contains a new visual design for different role statuses:

* unselected
* hovered
* selected
* disabled because of conflicts/limitations
* indeterminated (if not all nodes from the node list have the role assigned)

.. image:: ../../images/9.0/redesign-of-node-roles-panel/role-panel-views.png

Role becomes selected by clicking on its container.

Role description and warning are shown in a popover, which appears after
hovering over the role container with a slight delay.


Nailgun
=======

No changes required.


Data model
----------

None.


REST API
--------

None.


Orchestration
=============

No changes required.


RPC Protocol
------------

None.


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

There is Fuel UI change only.


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

Screenshots of node roles panel should be updated in the user guide.


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

#. Visual mockups creation.
#. JavaScript development of the feature.


Dependencies
============

None.


------------
Testing, QA
------------

New role panel should be covered by automated UI functional tests.


Acceptance criteria
===================

* New role list takes up less space on a screen.
* New role panel keeps functionality of the initial panel version:
  * contains all role data (name, description)
  * displays role conflicts and limitations
  * each role is selectable.


----------
References
----------

#fuel-ui on freenode
