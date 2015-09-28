..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================================
Support sorting and filtering by node group in Fuel UI
======================================================

https://blueprints.launchpad.net/fuel/+spec/node-groups-in-sorters-and-filters

In order to support multi-rack management in Fuel UI, an ability to sort and
filter node list by node network group attribute should be provided.


-------------------
Problem description
-------------------

End User should be able to sort and filter node list by node network group
in Fuel UI. This information should be available from UI to help End User
manage his multi-rack environment.


----------------
Proposed changes
----------------

Web UI
======

The change affects Fuel UI only. Existing sorting and filtering controls
in node management panel should include new `Node network group` option
(`group_id` attribute of Node model). All the other sorting and filtering
behaviour remains the same.

When `Node network group` filter is applied and specific node network group
chosen, only nodes from this network group should be shown in the node list.
`Node network group` filter should contain a list of network group names.
'default' node network group (group id = 1) should go first in the list.

When `Node network group` sorter is applied, node list should be grouped by
node network group name. Nodes from 'default' node network group
(group id = 1) should go first in the list.

For now, the change affects environment node list only, as well as unallocated
nodes do not belong to any node network group (`group_id` attribute has `null`
value).

Also, node network group name should be shown in node details pop-up.


Nailgun
=======

No changes required. Existing `group_id` attribute of Node model should be
used to sort and filter node list in Fuel UI.

Data model
----------

No changes required.


REST API
--------

No changes required. Node network groups data is provided by existing
`GET /api/nodegroups?cluster_id=<id>` request.


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

None


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

None


--------------------------------
Infrastructure/operations impact
--------------------------------

None


--------------------
Documentation impact
--------------------

Documentation should be updated to document the ability of sort and filter
node list by node group in Fuel UI.

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

#. Include node network group option to environment node list sorters
   and filters scope.
#. Display node network group name in the node details pop-up.


Dependencies
============

None


------------
Testing, QA
------------

* Manual testing


Acceptance criteria
===================

* It is possible to sort environment node list by node network group
  in Fuel UI
* It is possible to filter environment node list by node network group
  in Fuel UI
* Node network group name is shown in node details pop-up

----------
References
----------

* Support multirack in Fuel UI
  https://blueprints.launchpad.net/fuel/+spec/multirack-in-fuel-ui

* #fuel-ui on freenode
