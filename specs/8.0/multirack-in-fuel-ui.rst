..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
Support for multi-rack in Fuel UI
=================================

https://blueprints.launchpad.net/fuel/+spec/multi-rack-in-fuel-ui

Fuel UI should allow End User to manage OpenStack deployment for multiple
racks with a scalable underlay network design.


-------------------
Problem description
-------------------

Current Fuel UI has no support for multi-rack management. Fuel user has to use
CLI interface and other ways to manage his multi-rack environments.


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

#. Node network group name should be shown in node details pop-up.

Networks tab changes:

#. The list of node network groups can be seen at Networks tab
#. Networks tab is segmented into sections for node network groups:

  * one, called 'Networks' if only one node network group is given;

  * a separate sections in case of multi-rack OpenStack environment (several
  node network groups)

#. Neutron L2 and Neutron L3 settings will form a separate group, as well as
   network verification control:

   .. image:: ../../images/8.0/multi-rack-in-fuel-ui/verification_control.png

  In case of Nova network - Nova configuration will also be availbale in a
  separate section.

Also it will be possible to see all node network groups at once by clicking
'Show All Node network groups' checkbox.

Node network groups will appear as pills on the left side of the screen on
Networks tab, so by switching them the user will be able to see which networks
and which  parameters correspond to which node network group and configure
them.

   .. image:: ../../images/8.0/multi-rack-in-fuel-ui/node_network_groups.png

After changing some network settings for particular node network group it
will be possible to switch to the other node network group and change
settings for it without confirmation dialog on leaving unsaved data. In case
of invalid network settings appropriate section will be marked as invalid. All
the changes are applied only after clicking Save Settings button at the bottom
of the page. Saving errors will be displayed at the bottom of each section,
right above 'Save' button. Network verification result will be shown only on
Network Verification section.

To create a new node network group user will be prompted to enter its name:

   .. image:: ../../images/8.0/multi-rack-in-fuel-ui/new_group.png

Special cases:

#. Default node network group should always be the first one on the list.
#. It should not be possible to create new node network group without saving
   changes.
#. It should be possible to edit parameters of Admin networks for node network
   groups.
#. Gateways must be set for all networks when more than one node network group
   is present (in case of multi-rack environment).
#. Arbitrary node network group names should be supported - it should be
   possible to modify node network group names on UI.
#. It should be possible to delete node network groups in multi-rack OpenStack
   environment.


Nailgun
=======

* Existing `group_id` attribute of Node model should be used to sort and
  filter node list in Fuel UI.

* [2] When new environment is created default node network group is created in
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
`clusters` table should be extended with new attribute
`default_node_net_group` (Integer). The attribute can have Null value since
the default node network group can be deleted from environment.

REST API
--------

Node network groups data is provided by existing
`GET /api/nodegroups?cluster_id=<id>` request. No changes requred here.

Existing ``GET /api/clusters/{cluster_id}`` method should return the new
`default_node_net_group` cluster attribute:

.. code-block:: json

  {
    "id": 1,
    "name": "cluster#1",
    ...
    "default_node_net_group": <id>
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

Since there is a data model impact, an apropriate Alembic migration should be
prepared to update existing clusters to fit the new format.


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

#. Extend `Cluster` DB model with the new attribute, make corresponding
   changes in API
#. Include node network group option to environment node list sorters
   and filters scope.
#. Display node network group name in the node details pop-up.
#. Reorganize Networks tab to include common network settings, verification
   block changes and node network groups list.
#. Implement node network groups creation and editing support.


Dependencies
============

None


------------
Testing, QA
------------

* Manual testing
* Nailgun tests should cover the `Cluster` model change
* Functional UI auto-tests should cover the changes


Acceptance criteria
===================

* It is possible to sort environment node list by node network group
  in Fuel UI
* It is possible to filter environment node list by node network group
  in Fuel UI
* Node network group name is shown in node details pop-up
* Networks tab is segmented with the list of node network groups
* It is possible to create a new node network group
* It is possible to edit and delete existing node network groups

----------
References
----------

[1] #fuel-ui on freenode
[2] https://bugs.launchpad.net/fuel/+bug/1508973
