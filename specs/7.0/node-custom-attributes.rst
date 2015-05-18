..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Node custom attributes in Fuel UI
==========================================

https://blueprints.launchpad.net/fuel/+spec/node-custom-attributes

As a deployment engineer, I want to add custom properties (e.g. rack
location, etc.) so that I can work efficiently with large numbers of nodes
in Fuel UI.


Problem description
===================

There is no way in current UI to add custom user properties to nodes.
At the same time this is an extremely useful feature for management of
large environments.


Proposed change
===============

(TBD)

In Fuel UI user should be able to create, read, update, delete unlimited
number of custom attributes (i.e. rack number, position) of a particular
node or a node group.

An attribute represented by its key-value pair. Undefined value should be
``null``.

Interface should support an autocompletion of attributes keys (i.e. show
dynamic list of previously assigned attributes for nodes - user type "r"
and it automatically shows "rack number") during creation or update. This
will also prevent user from entering in incorrect keys.

(TODO) Attribute key should be a string limited by ? symbols and match the
following regexp:
(TODO) Attribute value should be a string limited by ? symbols and match the
following regexp:
Attribute key and value with unsupported characters or length should fail
gracefully.

Batch deletion of node attribute should raise a confirmation pop-up to prevent
user from accidental data loss.

All user attrubutes should be included in node list filtering scope.
User should be able to choose an attribute in filter list and select its
particular values. Filter values list should also include 'Not defined' value
to filter nodes with the attribute with not defined value.

(TBD) So we want to include custom attributes to sorting functionality?

(TBD) Should user be able to manage attributes on a master node level (common
attributes for all environemnts)?

Alternatives
------------

None.

Data model impact
-----------------

(TBD)

Node model in Nailgun DB should have an additional ``custom`` field to store
JSON with custom attributes data.
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

(TBD) Plugins will be able to assign its own custom attributes to nodes.

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

* Describe custom node attributes management workflow.
* Implement UI for the feature.
* Implement the same functionality in CLI. 


Dependencies
============

* Node list sorters and filters https://mirantis.jira.com/browse/PROD-313


Testing
=======

* Custom node attributes management in UI should be covered by both UI unit
  and functional tests.
* Python unit tests for the REST API change is also required.
* Custom node attributes management in CLI should be covered by unit tests.

Aceptance Criteria
------------------

* User can create, edit, remove, observe custom node attributes.
* User can manage custom attributes for a group of nodes.
* Custom node attributes are validated during creaction so user is not able
  to assign invalid data to node.
* User can filter lists of nodes to show only nodes that are characterized
  by specified custom parameters.
* (TBD) User can manage custom attributes on a master node level. These
  attributes are common for each environment.


Documentation Impact
====================

The documentation should cover how the end user experience has been changed.


References
==========

#fuel-ui on freenode
