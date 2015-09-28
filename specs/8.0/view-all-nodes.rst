..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================
View of all nodes across environments
=====================================

https://blueprints.launchpad.net/fuel/+spec/view-all-nodes

Introduce a new page in Fuel UI that displays a list of all nodes across
environments.


--------------------
Problem description
--------------------

End User should be able to observe all nodes across environments in Fuel UI
with standard functionality: sorting, filtering, searching though the node
list, reading node data. This will make multi-racks management more efficient.


----------------
Proposed changes
----------------

Web UI
======

New Nodes page should appear in main Fuel menu (root-level page) and display
a list of nodes in Fuel across all environments, including unallocated nodes.

Nodes page should represent a standart node list functionality:

* display list of grouped nodes
* support node list sorting (by environment (default sortng in the list),
  roles, status, name, MAC address, IP address, manufacturer, real cores,
  total cores, HDD size, disks sizes, RAM size, interfaces amount)
* support node list filtering (by environment, roles, status, manufacturer,
  real cores, total cores, HDD size, disks amount, RAM size,
  interfaces amount)
* support searching through the node list
* support standard and compact modes of node view
* support node labels management
* support of node actions, which do not depend on environment
  (like removing from Fuel for offline nodes)

Environment name should be shown in node pop-up (if the node assigned to some
environment).

Nailgun
=======

Data model
----------

New ``ui_settings`` table should be created in DB.
The one ``node_list_settings`` column of JSON type should be created in the
table for now.
There will be one row in the table. Default ``node_list_settings`` value
should be:

.. code-block:: json

  {
    "view_mode": "standard",
    "filter": {},
    "sort": [{"environment": "asc"}],
    "filter_by_labels": {},
    "sort_by_labels": [],
    "search": ""
  }

* ``view_mode`` property of node list settings object has one of the following
  values: "standard" (default) or "compact".
* ``filter`` is a hash of applied filters in the following format:

  .. code-block:: json

    {"status": ["discovered", "error", ...], ...}

  (no filters applied by default).

* ``sort`` is a list of applied sorters in the following format:

  .. code-block:: json

    [{"environment": "asc"}, {"roles": "desc"}, ...]

* ``filter_by_labels`` has the same format as ``filter`` but filter names are from
  Fuel node labels scope (no label filters applied by default).
* ``sort_by_labels`` has the same format as ``sort`` but sorter names are from
  Fuel node labels scope (no label sorters applied by default).
* ``search`` is a string to search nodes by their name, IP or MAC address
  (default value is an empty string that means no active search).

All the properties above are mandatory for ``node_list_settings`` attribute
value.

The new ``ui_settings`` table is an extendable way to handle future Fuel UI
changes that are not related to any particular environment (Cluster model has
its own ``ui_settings`` attribute for storing custom UI settings).

[TBD] Should Cluster model ``ui_settings`` data be moved to the new table?

This new ``ui_settings`` table should be validated on backend using JSON
schema.


REST API
--------

New API methods should be created to support reading and setting of common
Fuel UI settings:

* GET /api/ui_settings (Ok code 200) to read UI settings from DB.
  Response format:

  .. code-block:: json

    {"node_list_settings": {
        "view_mode": "standard",
        "filter": {"status": ["error", ...], ...},
        "sort": [{"environment": "asc"}, ...],
        "filter_by_labels": {"some_label": ["value1", ...], ...},
        "sort_by_labels": [],
        "search": ""
      }
    }

* PUT /api/ui_settings (Ok code 200) to update UI settings in DB.
  Expected error HTTP response code: 400 Bad Request in case of malformed
  request body or missing parameters.

  The method should be able to accept data in the following format
  (the method response should have exactly the same format):

  .. code-block:: json

    {"node_list_settings": {
        "view_mode": "standard",
        "filter": {"status": ["error", ...], ...},
        "sort": [{"environment": "asc"}, ...],
        "filter_by_labels": {"some_label": ["value1", ...], ...},
        "sort_by_labels": [],
        "search": ""
      }
    }


Orchestration
=============

No changes required.


RPC Protocol
------------

No changes required.


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

None


--------------
Upgrade impact
--------------

Since there is data model impact, Alembic migration that updates Fuel
to fit the new format, should be provided.


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

Fuel UI feature only.


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

New ``ui_settings`` DB table will be available for storing new settings
(which are not related to some particular environment) within other
features.


--------------------------------
Infrastructure/operations impact
--------------------------------

None


--------------------
Documentation impact
--------------------

Documentation should be updated to include a description for new Nodes page
in Fuel UI.


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
  jkirnosova (jkirnosova@mirantis.com)

Mandatory design review:
  vkramskikh (vkramskikh@mirantis.com)

QA engineer:
  apalkina (apalkina@mirantis.com)


Work Items
==========

#. Create new Nodes item in main Fuel UI navigation menu.
#. Create new Nodes page in Fuel UI.
#. Cover the new page with functional test.
#. Create new DB table and new API to support saving of the node list
   settings.
#. Prepare JSON schema for new DB table validation.
#. Prepare Alembic migration.
#. Support updating of node list settings from UI.


Dependencies
============

None


------------
Testing, QA
------------

* Manual testing
* Functional test should be created for the new Nodes page in Fuel UI


Acceptance criteria
===================

* It should be possible to view and manage all nodes in Fuel
  across all environments including unallocated nodes
* Node list custom settings (applied sorters, filters, etc.) are stored in DB,
  so the page has the same configuration after refresh
* Environment name should be shown in node pop-up (if the node assigned
  to some environment)

----------
References
----------

* Support multirack in Fuel UI
  https://blueprints.launchpad.net/fuel/+spec/multirack-in-fuel-ui

* #fuel-ui on freenode
