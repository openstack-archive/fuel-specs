..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
Support for multi-rack in Fuel UI
=================================

https://blueprints.launchpad.net/fuel/+spec/multirack-in-fuel-ui

Fuel UI should allow End User to manage OpenStack deployment for multiple
racks with a scalable underlay network design.


-------------------
Problem description
-------------------

Current Fuel UI has no support for multi-rack management. Fuel user has to use
CLI interface and other ways to manage his multi-rack environments.

Also it is impossible to observe all nodes across environments in Fuel UI.
At the same time such a node list with standard functionality (sorting,
filtering, labelling) will make multi-racks management more efficient.


----------------
Proposed changes
----------------

Web UI
======

Environment page changes:

#. Existing sorting and filtering controls in node management panel should
   include new `Node network group` option (`group_id` attribute of Node
   model).
   All the other sorting and filtering behaviour remains the same.

   When `Node network group` filter is applied and specific node network group
   chosen, only nodes from this network group should be shown in the node
   list.
   `Node network group` filter should contain a list of network group names.
   Default node network group (its id is stored in Cluster model attribute)
   should go first in the list.

   When `Node network group` sorter is applied, node list should be grouped by
   node network group name. Nodes from default node network group should go
   first in the list.

   This change affects environment node list only, as well as unallocated
   nodes do not belong to any node network group (`group_id` attribute has
   `null` value).

New root-level 'Nodes' page:

#. 'Nodes' page should appear in main Fuel menu and display a list of nodes
   in Fuel across all environments, including unallocated nodes.

#. 'Nodes' page should represent a standart node list functionality:

   * display list of grouped nodes
   * support node list sorting (by node network group (default sortng
     in the list), environment, roles, status, name, MAC address, IP address,
     manufacturer, real cores, total cores, HDD size, disks sizes, RAM size,
     interfaces amount)
   * support node list filtering (by node network group, environment, roles,
     status, manufacturer, real cores, total cores, HDD size, disks amount,
     RAM size, interfaces amount)
   * support searching through the node list by node name, MAC or IP address
   * support standard and compact modes of node view
   * support node labels management
   * support of node actions, which do not depend on environment
     (like removing from Fuel for offline nodes)

Node pop-up changes:

#. Node network group name should be shown in node details pop-up.

#. Environment name should be shown in node pop-up (if the node assigned to
   some environment).

Nailgun
=======

* Existing `group_id` attribute of Node model should be used to sort and filter
  node list in Fuel UI.

* When new environment is created default node network group is created in
  there (which is connected to shared Admin network). It is named "default".
  This name is the only distinguisher of default node network group which is
  being used in several places in code. But the name of node network group
  is not read-only entity. It can be changed via API. So, this distinguisher
  can be lost easily, data processing in Nailgun become broken in this case.

  So that a permanent distinguisher for default node network group should be
  introduced. `Cluster` model should be extended to store id of default node
  network group for the particular environment.

Data model
----------

#. `clusters` table should be extended with new foreign key
   `default_node_net_group` (Integer type, can not be Null).

#. New ``ui_settings`` table should be created in DB.
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
   
   * ``view_mode`` property of node list settings object has one of
     the following values: "standard" (default) or "compact".
   * ``filter`` is a hash of applied filters in the following format:
   
     .. code-block:: json
   
       {"status": ["discovered", "error", ...], ...}
   
     (no filters applied by default).
   
   * ``sort`` is a list of applied sorters in the following format:
   
     .. code-block:: json
   
       [{"environment": "asc"}, {"roles": "desc"}, ...]
   
   * ``filter_by_labels`` has the same format as ``filter`` but filter names
     are from Fuel node labels scope (no label filters applied by default).
   * ``sort_by_labels`` has the same format as ``sort`` but sorter names
     are from Fuel node labels scope (no label sorters applied by default).
   * ``search`` is a string to search nodes by their name, IP or MAC address
     (default value is an empty string that means no active search).
   
   All the properties above are mandatory for ``node_list_settings`` attribute
   value.

   The new ``ui_settings`` table is an extendable way to handle future Fuel UI
   changes that are not related to any particular environment (Cluster model
   has its own ``ui_settings`` attribute for storing custom UI settings).

   [TBD] Should Cluster model ``ui_settings`` data be moved to the new table?
   
   This new ``ui_settings`` table should be validated on backend using JSON
   schema.

REST API
--------

#. Node network groups data is provided by existing
   `GET /api/nodegroups?cluster_id=<id>` request. No changes requred here.

#. Existing ``GET /api/clusters/{cluster_id}`` method should return the new
   `default_node_net_group` cluster attribute:
   
   .. code-block:: json
   
     {
       "id": 1,
       "name": "cluster#1",
       ...
       "default_node_net_group": <id>
     }

#. New API methods should be created to support reading and setting of common
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

Since there is a data model impact, apropriate Alembic migrations should be
prepared.


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
(which are not related to some particular environment) within other features.


--------------------------------
Infrastructure/operations impact
--------------------------------

None


--------------------
Documentation impact
--------------------

Documentation should be updated to document the changes described above.

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
  vkramskikh (vkramskikh@mirantis.com)

Mandatory design review:
  vkramskikh (vkramskikh@mirantis.com)
  alekseyk-ru (akasatkin@mirantis.com)

Other contributors:
  jkirnosova (jkirnosova@mirantis.com)
  astepanchuk (astepanchuk@mirantis.com)
  bdudko (bdudko@mirantis.com)

QA engineer:
  apalkina (apalkina@mirantis.com)


Work Items
==========

#. Extend `Cluster` DB model with the new `default_node_net_group` attribute,
   make corresponding changes in API.
#. Include node network group option to environment node list sorters
   and filters scope.
#. Display node network group name in the node details pop-up.
#. Create new root-level 'Nodes' page in Fuel UI with all Fuel nodes list
   and standart node list management functionality.
#. Display environment name in the node details pop-up.
#. Support saving and updating of node list settings of 'Nodes' page
   from UI.
#. Prepare Alembic migrations and update JSON schemas.
#. Cover the changes with functional tests.


Dependencies
============

None


------------
Testing, QA
------------

* Nailgun tests should cover `clusters` table change
* Nailgun tests should be updated to handle default node network groups
* Nailgun tests should cover new `ui_settings` table and corresponding API
  changes
* Functional UI auto-tests should cover the changes
* Manual testing


Acceptance criteria
===================

* It is possible to sort environment node list by node network group
  in Fuel UI
* It is possible to filter environment node list by node network group
  in Fuel UI
* Node network group name is shown in node details pop-up
* It should be possible to view and manage all Fuel nodes across all
  environments including unallocated nodes
* Node list custom settings (applied sorters, filters, etc.) of 'Nodes' page
  are stored in DB, so the page has the same configuration after refresh
* Environment name should be shown in node pop-up (if the node assigned
  to some environment)

----------
References
----------

* #fuel-ui on freenode
