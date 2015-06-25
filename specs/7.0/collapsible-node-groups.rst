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

For big environments in Fuel Web UI it becomes hard to scroll through a large
list of nodes to observe overall nodes state.
As long as environment nodes are always grouped by their parameters (roles or
hardware info or both), user does not always need to see the entire list of
nodes in a group. In most cases nodes in a group will have not many
differences. For everyday work with a cloud some aggregated information about
a node group will be enough.


Proposed change
===============

We should introduce a collapsible behaviour of node groups in Fuel Web UI.
Their collapsed state should be stored on backend to not to force user toggle
groups every time he loads Nodes tab.

Collapsible node group should represent an aggregated information about its
nodes and a set of controls:

* a title which reflects node parameters by which they are grouped
* number of total nodes in the group
* number of selected nodes in the group
* 'Select All' control to (un)select nodes in the group
* button to toggle the group
* a short summary of node statuses to give user an inportant information
  if some nodes in the group failed or went offline

There are mockups for the feature:

.. image:: ../../images/7.0/collapsible-node-groups/expanded-view.png

.. image:: ../../images/7.0/collapsible-node-groups/collapsed-view.png

Alternatives
------------

None

Data model impact
-----------------

(TODO)

New property should be added to ``ui_settings`` JSON attribute of ``Cluster`` DB model:

.. code-block:: json

  "ui_settings": {
    "view_mode": "standard",
    "grouping": "roles",
    "collapsed_groups": ""
  }

This change should be reflected in an appropriate JSON schema.

REST API impact
---------------

No new methods needed.

Existing ``PUT /api/cluster/{cluster_id}`` method should be modified to be able
to accept data (Ok code 200, server error code starting from 500) in the form
of the following JSON:

.. code-block:: json

  {
    "ui_settings": {
      "view_mode": "compact",
      "grouping": "roles",
      "collapsed_groups": ""
    }
  }


Accordingly, this new property of ``ui_settings`` field should be presented in
the method output:

.. code-block:: json

  {
    "id": 1,
    "name": "cluster#1",
    "release_id": 2,
    ...
    "ui_settings": {
      "view_mode": "compact",
      "grouping": "roles",
      "collapsed_groups": ""
    }
  }

Similarly existing ``GET /api/cluster/{cluster_id}`` method should return
this new property of ``ui_settings`` cluster attribute.

Upgrade impact
--------------

Since we have a "Data model impact" we have to prepare an Alembic migration
that should update clusters to fit the new format.

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

None. This feature is about UI changes only, so no new data goes to deployment info.

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
* Vitaly Kramskikh (vkramskikh@mirantis.com) - Python code

Mandatory Design Reviewer:

* Vitaly Kramskikh (vkramskikh@mirantis.com)

Approver:

* Sheena Gregson <sgregson@mirantis.com>

QA engineer:

* Anastasia Palkina <apalkina@mirantis.com>

Work Items
----------

* provide a new visual design for collapsible node groups
* implement JS part of the task
* implement backend changes


Dependencies
============

* `Node list view modes
  <https://blueprints.launchpad.net/fuel/+spec/node-list-view-modes>`_


Testing
=======

* The feature should be covered by UI functional tests.
* Changes in ``ui_settings`` attribute of ``Cluster`` DB model should be
  covered by Python tests.

Acceptance criteria
-------------------

* User can toggle node groups and their collapsed state is stored on
  backend. So user does not need to toggle groups each time he loads Nodes
  tab.
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
