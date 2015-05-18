..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Node custom labels in Fuel UI
==========================================

https://blueprints.launchpad.net/fuel/+spec/node-custom-attributes

As a deployment engineer, I want to add custom properties (e.g. rack
location, etc.) so that I can work efficiently with large numbers of nodes
in Fuel UI.


Problem description
===================

There is no way in current UI to add custom properties/labels to nodes.
At the same time this is an extremely useful feature for management of large
environments. Labels enable users to map their own organizational structures
onto node list.


Proposed change
===============

In Fuel UI user should be able to create, read, update, delete unlimited
number of custom labels (i.e. rack number, position) of a particular node or
a node group. Unlike names and IDs, labels do not provide uniqueness. In
general, we expect many nodes to carry the same label(s).

Labels are key value pairs. Label key must be unique for a given node
to avoid overwriting. If user specifies the same key several times but with
different values, the values will be merged to one list.

Both valid label key and value must be string with 63 (TBD) characters or less
and must be empty or begin and end with an alphanumeric character
([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics
between. Keys may not contain consecutive dashes, underscores or dots.

Label key and value with unsupported characters or length should fail
gracefully.

Interface should support an autocompletion of label keys (i.e. show
dynamic list of previously assigned labels for nodes - user type "r"
and it automatically shows "rack number") during creation or update. This
will also prevent user from entering in incorrect keys.

Batch deletion of labels should raise a confirmation pop-up to prevent user
from accidental data loss.

All user labels should be included in node list filtering scope. User should
be able to choose a label key in filter list and select its particular values.
Filter values list should also include 'Not specified' value to filter nodes
with empty value of the label.

(TBD) So we want to include custom labels to sorting functionality?

Alternatives
------------

None.

Data model impact
-----------------

(TBD)

Node model in Nailgun DB should have an additional ``labels`` field to store
JSON with custom labels data.
This new field should not affect already existing attributes or models.

REST API impact
---------------

(TBD)

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

(TBD)

Performance Impact
------------------

None.

Plugin impact
-------------

(TBD) Plugins will be able to assign its own custom labels to nodes.

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

* Julia Aranovich (jkirnosova@mirantis.com) - UI part
* ??? - Python code

Other contributors (UI design):

* Bogdan Dudko (bdudko@mirantis.com)

Mandatory Design Reviewers:

* Sheena Gregson (sgregson@mirantis.com)
* Vitaly Kramskikh (vkramskikh@mirantis.com)

Work Items
----------

* Describe custom node labels management workflow.
* Implement UI for the feature.
* Implement the same functionality in CLI. 


Dependencies
============

* Node list sorters and filters https://mirantis.jira.com/browse/PROD-313


Testing
=======

* Custom node labels management in UI should be covered by both UI unit and
  functional tests.
* Python unit tests for the REST API change is also required.
* Custom node labels management in CLI should be covered by unit tests.

Aceptance Criteria
------------------

* User can create, edit, remove, observe custom node labels.
* User can manage custom labels for a group of nodes.
* Custom node labels are validated during creaction or update so user is not
  able to assign invalid data to node.
* User can filter lists of nodes to show only nodes that are characterized
  by specified custom parameters.


Documentation Impact
====================

The documentation should cover how the end user experience has been changed.


References
==========

#fuel-ui on freenode
