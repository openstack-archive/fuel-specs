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

Current Fuel UI does not have a support for multi-rack management. Fuel users
are forced to use CLI or raw API to manage their multi-rack environments.


----------------
Proposed changes
----------------

Web UI
======

Environment page changes:

#. Existing sorting and filtering controls in node management panel should
   include new `Node network group` option (which corresponded to ``group_id``
   attribute of `Node` model).
   All the other sorting and filtering behaviour remains the same.

   When `Node network group` filter is applied and specific node network group
   chosen, only nodes from this network group should be shown in the node
   list.
   `Node network group` filter should contain a list of network group names
   (that can be taken from ``GET /api/nodegroups?cluster_id=<id>`` request
   response). Node network groups should be sorted by their `id` in the
   options list, so that a default node network group, which has a minimum
   id among the environment node network groups, will go first in the list.

   When `Node network group` sorter is applied, node list should be grouped by
   node network group name. Nodes from default node network group should go
   first in the list.

   This change affects environment node list only, as well as unallocated
   nodes do not belong to any node network group (``group_id`` node attribute
   has `null` value in this case).

     .. image:: ../../images/8.0/multirack-in-fuel-ui/
        node-net-group-sorter-filter.png
        :scale: 75 %

#. Node network group name should be shown in node details pop-up.

     .. image:: ../../images/8.0/multirack-in-fuel-ui/
        node-net-group-node-data.png
        :scale: 75 %


Nailgun
=======

Data model
----------

No changes required.


REST API
--------

No changes required.


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

User guide should be updated to document the changes described above.

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

#. Include node network group option to environment node list sorters
   and filters scope
#. Display node network group name in the node details pop-up


Dependencies
============

None


------------
Testing, QA
------------

* Manual testing
* Functional UI auto-tests should be updated according the changes


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

#fuel-ui on freenode
