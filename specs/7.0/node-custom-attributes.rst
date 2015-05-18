..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Node custom labels in Fuel UI
==========================================

https://blueprints.launchpad.net/fuel/+spec/node-custom-attributes

As a deployment engineer, I want to add custom labels (e.g. rack
location, etc.) so that I can work efficiently with large numbers of nodes
in Fuel UI.


Problem description
===================

There is no way in current UI to add custom labels to nodes. At the same time
this is an extremely useful feature for management of large environments.
Labels enable users to map their own organizational structures onto node list.


Proposed change
===============

In Fuel UI user should be able to create, read, update or delete unlimited
number of custom labels (i.e. rack number, position) of a particular node or
a node group. Unlike names and IDs, labels do not provide uniqueness. In
general, we expect many nodes to carry the same labels.

Labels are key value pairs. Label key must be unique for a given node
to avoid overwriting. Label value is a list of strings or Null if no values
are specified:

.. code-block:: json

  ...,
  labels: {
    "label1": ["value1", "value2"],
    "rack": null,
    "position": null,
    "label3": ["value3"],
    ...
  }

Both label key and values in label value list must be string with 100
(TBD: do we have any constraints about label key or value length from Python
side?) characters or less and must be empty or begin and end with
an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_),
dots (.), and alphanumerics between. Keys must not contain consecutive dashes,
underscores or dots ('...', '--', '___', etc.).

Both label key and values with unsupported characters or length should fail
gracefully.

Interface should support an autocompletion of label keys (i.e. show
dynamic list of previously assigned labels for nodes - user type "r"
and it automatically shows "rack number") during creation. This will also
prevent user from entering in incorrect keys.

Each node should have default labels `rack` and `position` with Null values:

.. code-block:: json

  ...,
  labels: {
    "rack": null,
    "position": null
  }

These labels can not be deleted, just modifying of label value are available.

All user labels should be included in node list filtering scope. User should
be able to choose a label key in filter list and select its particular values.
Filter options list should also include 'Not specified' value to filter nodes
with Null value of the label.

Labels should also be included in the list of node sorters. User should
be able to choose a label key in sorter list and group nodes according its
values. Nodes with Null value of chosen label go last in sorted node list.

List of assigned labels should be shown on node panel, both standard and
compact.

Alternatives
------------

None.

Data model impact
-----------------

New ``labels`` attribute of JSON type should be added to ``Cluster`` model
into Nailgun database.

The new field should also be added to already existing entries in database.
Migration should add ``labels`` column with empty JSON object value "{}".

REST API impact
---------------

No new methods needed.

Existing ``PUT /api/nodes/{node_id}`` method should be modified to be able
to accept data (Ok code 200, server error code starting from 500) in the form
of the following JSON:

.. code-block:: json

  {
    "labels": {
	  "rack": ["rack1", "rack2"],
	  "position": null,
	  "label3": ["value1"],
	  ...
	}
  }

API should return 400 Bad Request if user tries to attach invalid label.

Accordingly, this new ``labels`` field should be added to the method output:

.. code-block:: json

  {
    "id": 1,
    "name": "cluster#1",
    "release_id": 2,
    ...
    "labels": {
	  "rack": ["rack1", "rack2"],
	  "position": null,
	  "label3": ["value1"],
	  ...
	}
  }

Similarly existing ``GET /api/nodes/{node_id}`` method should return
the new field.

Collection methods ``PUT /api/nodes/` and ``GET /api/nodes/`` should
also be updated with the new field.

Node labels should be reset to defaults after deleting node from environment.

Upgrade impact
--------------

Since we have a "Data model impact" we have to prepare an Alembic migration
that should update clusters to fit the new format.

Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

There is a python-fuelclient impact:

(TODO)

Performance Impact
------------------

None.

Plugin impact
-------------

Plugins should be able to assign its own custom labels to nodes.

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

* Julia Aranovich (jkirnosova@mirantis.com) - JS code
* Vitaly Kramskikh (vkramskikh@mirantis.com) - Python code
* Bogdan Dudko (bdudko@mirantis.com) - visual design

Mandatory Design Reviewer:

* Vitaly Kramskikh (vkramskikh@mirantis.com)

Approver:

* Sheena Gregson (sgregson@mirantis.com)

Work Items
----------

* Describe custom node labels management workflow.
* Implement corresponding UI controls.
* Implement the same functionality in CLI.


Dependencies
============

* Node list sorters and filters
  https://blueprints.launchpad.net/openstack/?searchtext=node-list-sorters-and-filters


Testing
=======

* Custom node labels management in UI should be covered by functional tests.
* Python unit tests for the REST API change are also required.
* Custom node labels management in CLI should be covered by unit tests.

Aceptance Criteria
------------------

* User can create, read, edit, remove custom node labels.
* User can manage custom labels for a group of nodes.
* Custom node labels are validated during creation or update, so user is not
  able to assign invalid data to node.
* User can filter nodes to show only nodes that are characterized by specified
  custom parameters.
* User can sort list of nodes to group them by specified custom parameters.


Documentation Impact
====================

The documentation should cover how the end user experience has been changed.


References
==========

#fuel-ui on freenode
