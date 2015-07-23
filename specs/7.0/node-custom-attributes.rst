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
labels can be used for sorting and filtering of node list to show only nodes
that are characterized by specified parameters. Labels enable users to map
their own organizational structures onto node list.

As a side effect, labels may be used by Fuel plugins to provide node-specific
attributes.


Proposed change
===============

In Fuel (both Web UI and CLI) user should be able to create, read, update or
delete unlimited number of custom labels (i.e. rack number, position) of
a particular node or a node group. Unlike names and IDs, labels do not provide
uniqueness. In general, it is expected many nodes to carry the same labels.

Labels are key-value pairs. Label key must be unique for a given node. Both
label key and value must be strings of 100 characters or less excluding an
empty string. We need 100 characters length limitation to avoid storing tons
of data in labels.
Label can also have `null` value that means an absence of label value (label
is like a simple tag in this case).
Also valid label key and value strings should not contain '=' character. This
limitation goes from CLI command syntax (see `For Fuel Client`_ section).

.. code-block:: json

  ...,
  "labels": {
    "label1": "value1",
    "label2": null,
    ...
  }

For Web UI
----------

List of assigned labels should be shown on node panel, both standard (under
a role list) and compact (in its extended view when user hovers a node).

There should be an interface in Web UI to manage node or node group labels
(CRUD operations).

Interface should also support an autocompletion of label keys (i.e. show
dynamic list of previously assigned labels for nodes - user type "r"
and it automatically shows "rack number") during creation. This will also
prevent user from entering in incorrect keys.

All custom labels should be included in node list filtering and sorting
scopes.

User should be able to choose a label key from filter list and select its
particular values. Filter options list should also include 'Not specified'
option to filter nodes with not specified value of the label.

User should be able to choose a label key in sorter list and group nodes
according its values. Nodes with not specified value of chosen label go last
in sorted node list.

For Nailgun
-----------

Data model impact
^^^^^^^^^^^^^^^^^

New ``labels`` attribute of JSON type should be added to ``Node`` model
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
    "id": 1,
    "labels": {
      "label1": "value1",
      "label2": null,
      ...
    }
  }

API should return 400 Bad Request in case of the following bad scenarios:

* user tries to add invalid label (label key or value is not a string or
  an empty string or a string with more that 100 characters)
* user tries to apply invalid value to existing label (this value is not a
  string or an empty string or a string with more that 100 characters)
* user tries to add/update label of non-existing node
* user wants to delete label(s) of non-existing node (the operation possible
  from CLI)
* user wants to get a non-existing label of node(s) (the operation possible
  from CLI)
* user wants to get label(s) of non-existing node (the operation possible
  from CLI)

Accordingly, this new ``labels`` field should be added to the method output:

.. code-block:: json

  {
    "id": 1,
    "name": "Node(ab:15)",
    ...
    "labels": {
      "label1": "value1",
      "label2": null,
      ...
    }
  }

Similarly existing ``GET /api/nodes/{node_id}`` method should return
the new field.

Collection methods ``PUT /api/nodes/` and ``GET /api/nodes/`` should
also be updated with the new field.

Node labels should be reset to defaults (an empty object) after deleting
node from environment.

Data Serialization for Astute
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For v7.0 environments labels should be serialized and landed to astute.yaml:

.. code-block:: yaml

  uid: 1
  name: "Node(74:57)"
  ...
  labels:
    label1: value1
    label2: none
    ...

For v7.0 environments labels should be added into provisioning data under
the "ks_meta" section:

.. code-block:: yaml

  uid: 1
  name: "Node(74:57)"
  ...
  ks_meta:
    fuel_version: "6.1"
    ...
    labels:
      label1: value1
      label2: none
      ...


For Fuel Client
---------------

Adding support for key-value labels is pretty easy as far as all logic is
incapsulated in the Fuel API. Adding, removing or changing these labels
shoud only be done on the Nailgun's side so the official python-fuelclient
and the rest of the client will be able to use it in a unified way.

There is a list of new commands to be added to work with labels from CLI:

to create or update label(s) for node(s)

::

  fuel2 node label set -l | --label key_1=[value_1] \
    [-l | --label key_2=[value_2] ... ] -n | --nodes node_id_1 [node_id_2 ...]

to create or update label(s) for ALL nodes

::

  fuel2 node label set -l | --label key_1=[value_1] \
    [-l | --label key_2=[value_2] ... ] -n | --nodes all

to delete label(s) of node(s)

::

  fuel2 node label delete -l | --label key1 [-l | --label key2 ... ] \
    -n | --nodes node_id_1 [node_id_2 ...]

to delete ALL labels of ALL nodes

::

  fuel2 node label delete -l | --label all -n | --nodes all

to display values of label(s) of node(s)

::

  fuel2 node label list -l | --label key1 [-l | --label key2 ... ] \
    -n | --nodes node_id_1 [node_id_2 ...]

  node_id | label_name   | label_value
  1       | key1         | value1
  2       | key2         | value2
  3       | key2         | value3

Node labels should also be shown in the output of ``fuel2 node show`` command,
but should not be included to the output of the command ``fuel2 node list``,
because formatting of the table may be screwed up if there is a lot of labels
on a single node.

Also white spaces will be trimmed from the key-value label pair:
``"   some key    =     some value"`` will be led to ``"some key=some value"``

All the commands above should fail and not to apply any changes if they get
400 Bad Request response from Nailgun API (see `For Nailgun`_ section).

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

This should be extremely useful for plugins. Labes will be available in
astute.yaml and may be used by plugin tasks to do node-specific modifications.
For instance, for Xen integration we need to provide separate Xen Server
credentials for each Compute node.

Restrictions:
Labels will be set independently from plugins. A Fuel plugin may not set
labels automatically. If a plugin developer decides to go with label's approach
there will be no pre-deployment validation of labels available at this time.

Other deployer impact
---------------------

Labes will be available in astute.yaml and during the provisioning. It will be
possible to use special labels to override global values (i.e. libvirt_type,
thus implementing BP
https://blueprints.launchpad.net/fuel/+spec/auto-virt-type). Another case may
be the fenthing. A user may put IPMI credentials into labels.

Also custom information may be added into provisioning data and using a custom
bootstrap image (or a custom fuel-agent) a deployer may consume this data.

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
* Implement corresponding UI controls including tests coverage.
* Implement CLI functionality (CRUD operations).
* Implement label serialization in Nailgun and cover it with unit tests.


Dependencies
============

* Node compact representation
  https://blueprints.launchpad.net/openstack/?searchtext=node-list-view-modes
* Node list sorters and filters
  https://blueprints.launchpad.net/openstack/?searchtext=node-list-sorters-and-filters


Testing
=======

* Custom node labels management in UI should be covered by functional tests.
* Python unit tests for the REST API and DB change are also required.
* Python unit tests for deployment and provisioning serializers are required.
* Custom node labels management in CLI should be covered by unit tests.

Acсeptance Criteria
-------------------

* User can create, read, edit, remove custom node labels both from Fuel Web UI
  and CLI.
* User can manage custom labels for a group of nodes both from Fuel Web UI
  and CLI.
* Custom node labels are validated during creation or update, so user is not
  able to assign invalid data to node.
* User can filter nodes in Fuel Web UI to show only nodes that are
  characterized by specified custom parameters.
* User can sort list of nodes in Fuel Web UI to group them by specified
  custom parameters.
* Labels appear in astute.yaml and in provisioning data.


Documentation Impact
====================

The Fuel documentation should cover how the end user experience has been
changed. The Fuel Plugin documentation should cover how to use labels in
plugins.


References
==========

#fuel-ui on freenode
