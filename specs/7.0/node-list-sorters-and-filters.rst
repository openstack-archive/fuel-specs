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

We should introduce a form-based panels on node list screens in UI with
filtering and sorting controls based on node attributes.

A filter bar should be located to the left of the node list on a screen.
The panel should be sticky as well as the whole node management panel.

If there is a limited list of node attribute values then the filter should
be a named list of checkboxes for multiple choice support. If node attribute
has boolean type of value then there should be a single checkbox control on
UI. In other cases filtering is performed by a single text search field.

Those filter values which don't have matched nodes in the list should be
marked as disabled options.

The filter bar should be extendable for adding custom user filters [1].

Applying the filters should be performed by click on Apply button in the
filter bar. Also there should be Clear All button in order to help user
immediately reset his selection to defaults and not to change each filtering
control.

Node list should include info about filtering results: amount of filtered
nodes and names of applied filters with its selected values.

User should also have an ability to sort node list by multiple node attributes
both in forward (ascending) and reverse (descending) order. The order can be
set separately for each sorter (ascending is default).

Existing grouping control in node management panel will be totally replaced
by sorting. Sorted node list should be grouped by the sorting parameters
to provide the user a UI for effective node group selection.
For example, if a node list sorted by roles and status, then there will be
groups by roles in the list with subgroups by node status.

Sorting by node name, IP or MAC address does not involve grouping because
these attributes are unique for each node.

Below I describe all the possible filters for each of node list screens.

* screen of environment nodes

  * **STATUS filter** should have the following values ((TBD) Can we
    automatically get a list of all possible node status attribute values
    not to hardcode the values list?):

    * **ready** - checks node model ``status`` attribute
    * **pending addition** - checks node model ``pending_addition`` attribute
    * **pending deletion** - checks node model ``pending_deletion`` attribute
    * **provisioned** - checks node model ``status`` attribute
    * **provisioning** - checks node model ``status`` attribute
    * **deploying** - checks node model ``status`` attribute
    * **removing** - checks node model ``status`` attribute
    * **error** - checks node model ``status`` attribute

  * **OFFLINE filter** is a checkbox to filter nodes with falsy 'online'
    attribute.
  * **ROLE filter** values are the list of environment release roles (release
    model ``roles`` attribute).
  * **MANUFACTURER filter** values are the list of ``manufacturer`` attribute
    value from all nodes on the screen. *This filter shoud not be shown
    in case of one possible value.*
  * **CPU filter** values are ranges among the total CPU amounts of nodes in
    the list. *This filter shoud not be shown in case of one possible value.*
  * **HDD filter** values are ranges among the node total HDD sizes. *This
    filter shoud not be shown in case of one possible value.*
  * **RAM filter** values are ranges among the node total memory sizes. *This
    filter shoud not be shown in case of one possible value.*

* screen of unallocated nodes

  * **STATUS filter** should have the following values:

    * **error** - checks node model ``status`` attribute

  * **OFFLINE filter** is a checkbox to filter nodes with falsy 'online'
    attribute.
  * **MANUFACTURER filter** values are the list of ``manufacturer`` attribute
    value from all nodes on the screen. *This filter shoud not be shown
    in case of one possible value.*
  * **CPU filter** values are ranges among the total CPU amounts of nodes in
    the list. *This filter shoud not be shown in case of one possible value.*
  * **HDD filter** values are ranges among the node total HDD sizes. *This
    filter shoud not be shown in case of one possible value.*
  * **RAM filter** values are ranges among the node total memory sizes. *This
    filter shoud not be shown in case of one possible value.*

(TODO) Need to describe a logic of split CPU/HDD/RAM values into ranges.

Both environment nodes and unallocated nodes screens also should have
a simple **Search nodes** text field for case insensitive filtering nodes by
the following attributes:

* **name** - checks node model ``name`` attribute
* **MAC address** - checks node model ``mac`` attribute
* **IP address** - checks node model ``ip`` attribute

(TBD) Do we want this field accompained by a dynamic list of possible options?
For example, user types "172.18." and it automatically shows a list of values:
"172.18.33.56", "172.18.33.58" so user do not need to type a full address and
select a value from the list.

Below I describe all the possible sorters for each of node list screens.

* screen of environment nodes

  * **name** - natural sorting by node model ``name`` attribute ('123asd',
    '19asd', '12345asd', 'asd123', 'asd12' should turn into '19asd', '123asd',
    '12345asd', 'asd12', 'asd123')
  * **status** - preffered order for sorting of nodes is 'ready',
    'pending addition', 'pending deletion', 'provisioned', 'provisioning',
    'deploying', 'removing', 'error' (node model 'status', 'pending_addition',
    'pending_deletion' attributes are checked)
  * **offline** - nodes with falsy ``online`` attribute go first
  * **roles** - nodes should have the same order as in environment release
    model role list
  * **manufacturer** - natural sorting by node model ``manufacturer``
    attribute
  * **IP address** - natural sorting by node model ``ip`` attribute
  * **MAC address** - natural sorting by node model ``mac`` attribute
  * **CPU** - numeric sorting by node total ((TBD) or real?) CPU amount
  * **HDD** - numeric sorting by node HDD total size (a sum of node disk
    sizes)
  * **RAM** - numeric sorting by node total memory size

* screen of unallocated nodes

  * **name** - natural sorting by node model ``name`` attribute
  * **status** - nodes with 'error' ``status`` attribute go last
  * **offline** - nodes with falsy ``online`` attribute go first
  * **manufacturer** - natural sorting by node model ``manufacturer`` attribute
  * **IP address** - natural sorting by node model ``ip`` attribute
  * **MAC address** - natural sorting by node model ``mac`` attribute
  * **CPU** - numeric sorting by node total ((TBD) or real?) CPU amount
  * **HDD** - numeric sorting by node HDD total size (a sum of node disk
    sizes)
  * **RAM** - numeric sorting by node total memory size

All the sorters above described with the assumption of direct sorting order
(ascending).

Nodes are sorted by its roles by default.

(TBD) **SCREEN OF ROLE MANAGEMENT** should not have a filter bar because all
nodes are always chosen on this screen. Only node roles changed there. Also it
does not make sense to introduce sorting functionality on this screen
because sorting by roles only does make sense on the screen.
The only option when node management controls can be useful on this screen is
to be sure that all nodes user selected on previous screen are presented in
the list. I find this option doubtful.

User selection for filters and sorters is not stored neither on the backend,
not in browser cookies. But the selection is automatically translated to
a query and added to the page location string:

.. code-block:: text

  #cluster/x/nodes/status:pending_addition;offline:true;role:controller,cinder;
  manufacturer:Dell;has:00.b1;name:asc,status:asc,offline:desc,roles:asc,
  manufacturer:asc,ip:asc,mac:desc,cpu:asc,hdd:desc,ram:asc

The query contains filtering ``key:value`` pairs divided by ';'. Value list
represented as a string of its values joined by ',' character. Search text
field has a ``has`` key.

The last item of the query is always a sorting query which includes
``key:order`` pairs divided by comma. Default sorting quesry is ``roles:asc``.

Any special character should be ignored when composing the query. Filter
query value should match ``^[\w-.]+$`` regexp. Spaces in value string are
replaced by '_' character.
Note that ':' in MAC address substring is replaced by '.' because ':'
character is reserved for dividing a pair onto key and value.

(TODO) The query should also support CPU/HDD/RAM filters.

User is able to use these urls to filter and sort node list. So that we
need a javascript parser to handle such urls.

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

Existing ``grouping`` attribute of ``cluster`` model is no longer needed.

REST API impact
---------------

None.

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

* Fix the list of node attributes to filter with all possible values.
* Fix the list of node attributes to sort with all possible values.
* Implement the new filter bar for node management.
* Implement the new sorting bar for node management.
* Automatically update page location string with user sorting and filtering
  selection.
* Implement a parser for handling of filtering query from page location string.

Dependencies
============

None.


Testing
=======

* Filtering and sorting node list features should be covered by UI functional
  tests.
* Composing and handling of filter selections to the query in location string
  and the query parser should be covered by UI unit tests.
* Python unit tests should be revisited because of removal of ``cluster``
  model ``grouping`` attribute.

Aceptance criteria
------------------

* User can filter lists of nodes to show only nodes that are characterized
  by specified parameters.
* Filter bar always persists on the screen when scrolling the node list and
  has a "sticky" behaviour.
* User can sort nodes based on a parameter type (ascending, descending) or
  on multiple parameters.
* Sorted node list is grouped by sorting parameters.
* Filtering and sorting selections are transformed to url query string that
  can be used also for managing nodes.


Documentation Impact
====================

The documentation should cover how the end user experience has been changed.


References
==========

[1] Support adding custom attributes to nodes in Fuel
https://mirantis.jira.com/browse/PROD-144

#fuel-ui on freenode
