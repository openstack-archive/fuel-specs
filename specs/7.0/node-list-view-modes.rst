..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Node list standard and compact view modes in Fuel UI
====================================================

Include the URL of your launchpad blueprint:

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
* status
* hardware information (HDD/CPU/RAM) in a short form

And add an ability to switch between standard and compact modes in particular
environment. The choice should be stored in the database as a cluster model
attribute.

Standard mode should be default view mode for new environments.

Switching node list view is available for both new and operational
environments.

Please consider proposed mockup for compact node list view:

 .. image:: ../../images/7.0/node-list-view-modes/compact-node-view.png
    :scale: 50 %

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

Data model impact
-----------------

New 'node_list_mode' attribute with 'standard' default value should be added
to cluster model into Nailgun. This new attribute should not affect already
existing attributes or models.

REST API impact
---------------

No new methods needed.

Existing ``PUT /api/cluster/{cluster_id}`` method should be able to accept a new
attribute in the form of JSON: ``{"grouping": "hardware"}``

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

* Julia Aranovich (jkirnosova@mirantis.com)
* Bogdan Dudko (bdudko@mirantis.com)

Mandatory Design Reviewers:

* Sheena Gregson (sgregson@mirantis.com)
* Vitaly Kramskikh (vkramskikh@mirantis.com)

Work Items
----------

* provide a new compact node panel layout
* provide a control to switch between standard and compact node list views


Dependencies
============

None


Testing
=======

This new Fuel UI feature should be covered by UI functional tests.


Documentation Impact
====================

The documentation should cover how the end user experience has been changed.


References
==========

* #fuel-ui on freenode
