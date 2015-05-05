..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Node list standard and compact view modes in Fuel UI
====================================================

https://blueprints.launchpad.net/fuel/+spec/node-list-view-modes

Implement possibility to switch between standard and compact node list view
modes.


Problem description
===================

In big environments it becomes hard to manage a large number of nodes.

Node panel takes an entire row on environment nodes screen now and End User
is forced to scroll through a large list of nodes before finding
the right one.
At the same time not all information on a node panel is needed for everyday
work with operational cloud.


Proposed change
===============

We should introduce a compact view for a clickable node panel which shows
the most significant information about the node such as:

* name
* status (including deployment progress bar)
* hardware information (HDD/CPU/RAM) in a short form
* checked state

And add an ability to switch between standard and compact modes in particular
environment. The choice should be stored in the database as a Cluster model
attribute.

Standard mode should be default view mode for new environments.

Switching node list view is available for both new and operational
environments.

In compact mode there should be about 5 nodes in row in the node list.

When user hovers the mouse over a compact node it should transform to extended
view with more detailed info:

* name
* status (including deployment progress bar)
* checked state
* role list
* hardware information (HDD/CPU/RAM) in a short form
* action buttons (such as Discard Addition, Discard Deletion, Remove
  (for offline nodes), View Logs)
* Details button to launch node pop-up with detailed hardware information.

Alternatives
------------

None

UX impact
-----------------

Proposed solution mostly affects UI/UX:

* New control for changing node list view mode should be added in a node
  management panel.
* A node panel should have a new layout in case of 'compact' mode with less
  node data.
* Compact node panel should transform to extended view with more details when
  user hovers the mouse over a node.
* The proposed change does not affect neither standard node view nor existing
  node pop-up with detailed hardware configuration.

Data model impact
-----------------

New ``view_mode`` attribute of string type with the following set
of possible values:

* "standard" (default)
* "compact"

should be added to Cluster model into Nailgun. This new attribute should not
affect already existing attributes or models.

REST API impact
---------------

No new methods needed.

Existing ``PUT /api/cluster/{cluster_id}`` method should be modified to be able
to accept data (Ok code 200, server error code starting from 500) in the form
of the following JSON:

.. code-block:: json

  {
    "view_mode": "compact"
  }


Accordingly, this new ``view_mode`` field should be added to the method output:

.. code-block:: json

  {
    "id": 1,
    "name": "cluster#1",
    "release_id": 2,
    ...
    "view_mode": "compact"
  }

Similarly existing ``GET /api/cluster/{cluster_id}`` method should return
the new field.

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

None

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
* Bogdan Dudko (bdudko@mirantis.com) - Design
* Vitaly Kramskikh (vkramskikh@mirantis.com) - Python code

Mandatory Design Reviewer:

* Vitaly Kramskikh (vkramskikh@mirantis.com)

Approver:

* Sheena Gregson <sgregson@mirantis.com>

Work Items
----------

* provide a control to switch between standard and compact node list views
* implement a new compact node panel layout
* implement layout of an extended view of compact node


Dependencies
============

None


Testing
=======

* This new Fuel UI feature should be covered by UI functional tests.
* Addition of ``view_mode`` attribute to Cluster model should be covered by
  Python unit tests.

Aceptance criteria
------------------

* User can switch between standard and compact view mode on environment nodes
  screen. The view mode choice is saved for particular environment, so user
  does not need to switch again when he returned to environment.
* When switching to compact view node panels should transform to its compact
  view.
* Compact node panel tranforms to extended view with more detailed information
  when user hovers the mouse over a node.


Documentation Impact
====================

The documentation should cover how the end user experience has been changed.


References
==========

* #fuel-ui on freenode
