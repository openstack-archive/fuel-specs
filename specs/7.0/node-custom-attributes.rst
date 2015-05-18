..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
Support of custom node labels
=============================

https://blueprints.launchpad.net/fuel/+spec/node-custom-attributes

Custom node labels support should be introduced in Fuel to allow the user
to filter and sort nodes in OpenStack environment.


Problem description
===================

Now there is no way in Fuel to add custom labels to nodes. At the same time
this is an extremely useful feature for management of large environments:
labes can be used for sorting and filtering of node list to show only nodes
that are characterized by specified parameters. Labels enable users to map
their own organizational structures onto node list.


Proposed change
===============

In Fuel (both Web UI and CLI) user should be able to create, read, update or
delete unlimited number of custom labels (i.e. rack number, position) of
a particular node or a node group. Unlike names and IDs, labels do not provide
uniqueness. In general, it is expected many nodes to carry the same labels.

Labels are key-value pairs. Label key must be unique for a given node. Both
label key and value must be strings of 100 characters or less, including
an empty string.

.. code-block:: json

  ...,
  labels: {
    "label1": "value1",
    "label2": "",
    ...
  }

For Web UI
----------

List of assigned labels should be shown on node panel, both standard (under
a role list) and compact (in its extended view when user hovers a node).

There should be a panel in Web UI to manage node or node group labels (CRUD
operations).

Interface should support an autocompletion of label keys (i.e. show
dynamic list of previously assigned labels for nodes - user type "r"
and it automatically shows "rack number") during creation. This will also
prevent user from entering in incorrect keys.

All custom labels should be included in node list filtering and sorting
scopes.

User should be able to choose a label key from filter list and select its
particular values. Filter options list should also include 'Not specified'
value to filter nodes with empty value of the label.

User should be able to choose a label key in sorter list and group nodes
according its values. Nodes with empty value of chosen label go last in
sorted node list.

For Nailgun
-----------

Data model impact
^^^^^^^^^^^^^^^^^

New ``labels`` attribute of JSON type should be added to ``Cluster`` model
into Nailgun database.

The new field should also be added to already existing entries in database.
Migration should add ``labels`` column with empty JSON object value "{}".

REST API impact
^^^^^^^^^^^^^^^

No new methods needed.

Existing ``PUT /api/nodes/{node_id}`` method should be modified to be able
to accept data (Ok code 200, server error code starting from 500) in the form
of the following JSON:

.. code-block:: json

  {
    labels: {
      "label1": "value1",
      "label2": "",
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
    labels: {
      "label1": "value1",
      "label2": "",
      ...
    }
  }

Similarly existing ``GET /api/nodes/{node_id}`` method should return
the new field.

Collection methods ``PUT /api/nodes/` and ``GET /api/nodes/`` should
also be updated with the new field.

Node labels should be reset to defaults (an empty object) after deleting
node from environment.

For Fuel Client
---------------

Adding support for key-value labels is pretty easy as far as all logic is
incapsulated in the Fuel API. Adding, removing or changing these labels
shoud only be done on the Nailgun's side so the official python-fuelclient
and the rest of the client will be able to use it in a unified way.

There is a list of commands to be added to work with labels from CLI:

to add new label to node(s)

::

  fuel label add --nodes 1 2 3 --name test label --value test value

to add new label to node(s) with empty value

::

  fuel label add --nodes 1 2 3 --name test label

to remove a partiular label of node(s)

::

  fuel label remove --nodes 1 2 3 --name test label

to remove all labels of node(s)

::

  fuel label remove --nodes 1 2 3

to update a value of particular node(s) label

::

  fuel label update --nodes 1 2 3 --name test label --value test value 2

to display a list of values of particular label of node(s)

::

  fuel label list --nodes 1 2 3 --name test label

  node_id | name       | value
  1       | test label | value1
  2       | test label | value2
  3       | test label | value3

to display a list of labels of node(s)

::

  fuel label list --nodes 1 2 3

  node_id | name         | value
  1       | test label   | value11
  1       | test label 2 | value12
  1       | test label 3 | value13
  2       | test label 2 | value22
  2       | test label 3 | value23
  3       | test label   | value

Alternatives
------------

None.

Data model impact
-----------------

See `For Nailgun`_ section of the proposed change.

REST API impact
---------------

See `For Nailgun`_ section of the proposed change.

Upgrade impact
--------------

Since we have data model impact, we have to prepare an Alembic migration
that should update clusters to fit the new format.

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

Mandatory Design Reviewers:

* Vitaly Kramskikh (vkramskikh@mirantis.com)
* Roman Prikhodchenko (rprikhodchenko@mirantis.com)

Approver:

* Sheena Gregson (sgregson@mirantis.com)

Work Items
----------

* Describe custom node labels management workflow.
* Modify DB structure and API to work with labels.
* Implement corresponding UI controls.
* Implement the same functionality in CLI.


Dependencies
============

* Node compact representation
  https://blueprints.launchpad.net/openstack/?searchtext=node-list-view-modes
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
