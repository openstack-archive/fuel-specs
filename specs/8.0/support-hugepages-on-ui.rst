..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================
Support of Huge Pages on UI
===========================

https://blueprints.launchpad.net/fuel/+spec/support-hugepages-on-ui

Introduce ability to manage Huge Pages settings for compute nodes in Fuel UI.


--------------------
Problem description
--------------------

Need support of Huge Pages settings management in Fuel UI for compute nodes.
For now this is available via API and CLI interface only.


----------------
Proposed changes
----------------

Web UI
======

Node management interface should be updated in Fuel UI to give the End User
an ability to manage Huge Pages settings.
This change refers to compute nodes only.
User should be able to enable/disable Huge Pages support for a particular
node. If Huge Pages support is active for the node, then user should be able
to select a particular page size for the node from a list of available page
sizes.


Nailgun
=======

Data model
----------

No changes required.

Existing ``available_pagesizes`` attribute of Node model should be used to
represent dropdown with available page sizes for the node.

Existing ``pagesize`` attribute of Node model should be used to set
a particular page size for the node. `Null` value of ``pagesize`` attribute
means that Huge Pages setting is not activated for the node.

REST API
--------

No changes required. Existing API for nodes is used to manage Huge Page
settings in Fuel UI:

* GET /api/nodes/<node_id> to read node data.
* PUT /api/nodes/<node_id> to update node Huge Pages settings.
  The following data should be passed to the request:

  .. code-block:: json

    {
      "id": 1,
      "pagesize": 500
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

Documentation should be updated to reflect the change.


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


Work Items
==========

#. Add control to enable/disable Huge Pages setting for compute nodes
   in Fuel UI
#. Add control to setup particular page size if Huge Pages setting enabled
   for compute node in Fuel UI


Dependencies
============

* Collecting available pagesizes from nodes
  https://blueprints.launchpad.net/fuel/+spec/collecting-available-pagesizes


------------
Testing, QA
------------

* Manual testing
* Existing functional test of node component should cover the change


Acceptance criteria
===================

* It should be possible to enable/disable Huge Pages setting for compute nodes
  in Fuel UI
* It should be possible to setup particular page size if Huge Pages setting
  enabled for compute node in Fuel UI


----------
References
----------

* Support for Huge pages for improved performance
  https://blueprints.launchpad.net/fuel/+spec/support-hugepages
* #fuel-ui on freenode
