..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================
Collapsible node groups in Fuel Web UI
======================================

https://blueprints.launchpad.net/fuel/+spec/collapsible-node-groups

Implement possibility to collapse and expand node groups in Fuel Web UI.


Problem description
===================

In Fuel Web UI it becomes difficult to scroll through a large list of nodes
to observe overall nodes state. As long as nodes are always grouped by their
parameters, which corresponds to applied sorting on the screen, user does not
always need to see the entire list of nodes in a group. In most cases nodes
in a group will not have many differences. For everyday work with a cloud some
aggregated information about a node group would be enough.


Proposed change
===============

Collapsible behaviour of node groups should be introduced in Fuel Web UI.

Collapsible node group should represent an aggregated information about its
nodes and a set of controls:

* A title which reflects node parameters by which they are grouped.
* Number of total nodes in the group.
* Number of selected nodes in the group.
* 'Select All' control to (un)select nodes in the group.
* Button to toggle the group.
* A short summary of node statuses to give user an important information
  if some nodes in the group failed or went offline.

There are mockups for the feature:

.. image:: ../../images/7.0/collapsible-node-groups/expanded-view.png

.. image:: ../../images/7.0/collapsible-node-groups/collapsed-view.png


Alternatives
------------

It would be a good UX to store collapsed state of node groups on backend.
This would help user not to toggle groups every time nodes screen is loaded.
Since node grouping depends on applied sorting for node list, sorting should
also be stored on backend.
So, these UI settings (collapsed state of node groups, current sorting) should
be saved every time user toggles a node group or changes sorting on nodes
screen.
This UI settings should be coupled with a particular user to give the user an
ability to keep his own settings for all clients (browsers).
This proposal should be considered in the next iterations of node namanement
flow rework.

Data model impact
-----------------

None

REST API impact
---------------

None.

Upgrade impact
--------------

None.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Plugin impact
-------------

None

Other deployer impact
---------------------

None.

Developer impact
----------------

None

Infrastructure impact
---------------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Julia Aranovich (jkirnosova@mirantis.com)

Developers:

* Julia Aranovich (jkirnosova@mirantis.com) - JS code
* Bogdan Dudko (bdudko@mirantis.com) - visual design

Mandatory Design Reviewer:

* Vitaly Kramskikh (vkramskikh@mirantis.com)

Approver:

* Sheena Gregson <sgregson@mirantis.com>

QA engineer:

* Anastasia Palkina <apalkina@mirantis.com>

Work Items
----------

* Provide a new visual design for collapsible node groups.
* Implement JS part of the task.


Dependencies
============

* `Sorting and filtering of node list in Fuel Web UI
  <https://blueprints.launchpad.net/fuel/+spec/node-list-sorters-and-filters>`_


Testing
=======

* The feature should be covered by UI functional tests.

Acceptance criteria
-------------------

* User can toggle node groups both on the screen of environment nodes and
  the screen of unallocated nodes.
* User can select all nodes in group by an appropriate 'Select All' checkbox.
* Node group title accompanied by numbers of selected and total nodes in
  the group.
* Collapsed node groups show an aggregated node statuses summary.


Documentation Impact
====================

The documentation should cover how the end user experience has been changed.


References
==========

* #fuel-ui on freenode
