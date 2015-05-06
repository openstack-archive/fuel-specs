..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Node list sorters and filters
==========================================

https://blueprints.launchpad.net/fuel/+spec/node-list-sorters-and-filters

Implement possibility to sort and filter nodes based on its properties
(e.g. name, status, etc) so that user can work efficiently with large number
of nodes in Fuel UI


Problem description
===================

Now user can filter nodes just by it's name or MAC address using simple text
field and no special sorters are available for node list. Nodes are
automatically sorted by their id attribute that is useless for the end user.

It is rather poor UI for managing large environments. There are many use cases
that are desirable to maintain in the Fuel UI. For example, an ability
to filter/sort nodes by their status or online state would save some time
finding faulty/offline nodes in the list and performing bulk actions (like
Delete) on them.


Proposed change
===============

We should introduce a form-based panel on node list screens in UI with
filtering and sorting controls.

If there is a limited number of node attribute values then the control should
be a dropdown with multiple choice support. In other case it should be
a single text field.

User selection for filters and sorters is not stored neither on the backend,
not in browser cookies. But the selection is automatically translated to
a query and added to the page location string:

.. code-block:: text

  #cluster/x/nodes/status:error;online:true;role:controller

User is able to use such urls to filter and sort node list.

Also node managegent panel should include Reset Filters button in order
to help user immediately reset his selection to defaults and not to change
each filtering control.

Here a list of existing node attributes that should be used for sorting and
filtering:


+------------------+---------------+---------------+---------------+
| Node attribute   |    Sorters    | Filter        | Filter        |
|                  |               | (dropdown)    | (text field)  |
+==================+===============+===============+===============+
| Name             |       +       |               |       +       |
+------------------+---------------+---------------+---------------+
| Manufacturer     |       +       |       +       |               |
+------------------+---------------+---------------+---------------+
| Public IP        |       +       |               |       +       |
+------------------+---------------+---------------+---------------+
| Management IP    |       +       |               |       +       |
+------------------+---------------+---------------+---------------+
| MAC address      |       +       |               |       +       |
+------------------+---------------+---------------+---------------+
| HDD size         |       +       |       +       |               |
+------------------+---------------+---------------+---------------+
| CPU              |       +       |       +       |               |
+------------------+---------------+---------------+---------------+
| RAM              |       +       |       +       |               |
+------------------+---------------+---------------+---------------+
| Interfaces speed |       +       |       +       |               |
+------------------+---------------+---------------+---------------+
| Status           |       +       |       +       |               |
+------------------+---------------+---------------+---------------+
| Online           |       +       |       +       |               |
+------------------+---------------+---------------+---------------+
| Assigned roles   |       +       |       +       |               |
+------------------+---------------+---------------+---------------+


Please note that the changes above should not affect DB and backend code.

Alternatives
------------

The alternative here can be query-based language that could replace all
the filtering and sorting controls. It is something like:

.. code-block:: text

  status = error AND role in (controller, compute) and online = true
  ORDER BY name ASC, role DESC

This method is rather flexible and requires no support when adding new node
properties. But it is suitable for advanced user and we must first think of
the newbies. So, as a first iteration of node management optimization it is
suggested to introduce a form-based filter panel in the Fuel UI.

Data model impact
-----------------

None.

REST API impact
---------------

None. This is just the UI/UX feature which doesn't affect backend somehow.

Upgrade impact
--------------

None.

Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

None.

Performance Impact
------------------

None.

Plugin impact
-------------

None.

Other deployer impact
---------------------

None.

Developer impact
----------------

None.

Infrastructure impact
---------------------

None.


Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Julia Aranovich (jkirnosova@mirantis.com)

Developers:

* Julia Aranovich (jkirnosova@mirantis.com)

Other contributors (UI design):

* Bogdan Dudko (bdudko@mirantis.com)
* Steve Doll (sdoll@mirantis.com)

Mandatory Design Reviewers:

* Sheena Gregson (sgregson@mirantis.com)
* Vitaly Kramskikh (vkramskikh@mirantis.com)

Work Items
----------

* fix the list of node attributes to sort
* fix the list of node attributes to filter
* implement the new node management toolbar
* provide an ability to automatically update page location string with user
  sorting and filtering selection


Dependencies
============

None.


Testing
=======

This new Fuel UI feature should be covered by UI functional tests.


Documentation Impact
====================

The documentation should cover how the end user experience has been changed.


References
==========

* #fuel-ui on freenode
