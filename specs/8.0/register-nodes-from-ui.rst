..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================================
Support registration of pre-provisioned nodes in Fuel UI
========================================================

https://blueprints.launchpad.net/fuel/+spec/register-nodes-from-ui

Introduce an ability to add node(s) with already installed OS in Fuel
environment via web interface. Introduce pre-povisioned node support
in Fuel UI, inlcuding role management, disks configuration.


--------------------
Problem description
--------------------

For now nodes which were provisioned without Fuel can not be added to Fuel
environment (if user install all required packages and configure it properly).
So, Fuel UI web interface should support this case.

----------------
Proposed changes
----------------

Web UI
======

User obtains a node with vanilla OS (for example, RHEL 7) installed and
enables the plugin [1] for particular environment. Then Fuel UI should
represent the new workflow:

* User adds a pre-provisioned node to the environment (nodes can be added
  one by one via Fuel UI) with the form, which includes the following
  fields:

  * node IP address (mandatory)
  * login
  * password
  * SSH key

  The fields should have a basic validation.
  User can access the node via login-password credentials OR SSH key.

* Then Fuel Master tries to access the node via provided credentials,
  performs basic OS verification according to installed plugins,
  installs base Fuel services.
  All of it looks like some continious process on UI.
  (TODO: an appropriate task name should be specified)

    * if the process successful: new node with `pre-discover` status
      should appear in environment node list (the node will have no roles
      assigned)
    * if the process failed: an appropriate error message should be shown
      on UI (node with specified IP is not found, node OS is not supported,
      the plugin is not enabled, etc.)

* User should be able to assign roles to the new pre-provisioned node.
  BUT a standard list of release roles can not be applied to this node.
  Roles that can be assigned to the node are provided by the plugin
  (for example, only Compute role for RHEL).

* User is not able to configure pre-provisioned node disks.
  Fuel UI should show an appropriate warning message.

* User is not able to reprovision pre-provisioned by Fuel.
  This limitation refers to [2].

* Deletion of a pre-provisioned node from an environment:
  as node was provisioned without Fuel, it can not be sent to bootstrap.
  The node will be deleted from Fuel DB and disconnected from all
  networks exclude admin.
  So, Fuel UI should display a special warnign in case of deletion of
  pre-provisioned nodes and warn user about the consequences.


Nailgun
=======

Data model
----------

No changes required.


REST API
--------

No changes required. Existing API should be used to manage pre-provisioned
nodes.

To add pre-provisioned node to Fuel `POST api/nodes/discover_pre_provisioned`
request should be used with the following parameters:

.. code-block:: json

  {
    "ip": <node IP>,
    "login": <login>,
    "password": <password>,
    "ssh_key": <ssh_key>
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

The current spec is about Fuel UI changes only.


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
Since logic of role dependency on node status will be implemented, it can be
used within other features.


--------------------------------
Infrastructure/operations impact
--------------------------------

None


--------------------
Documentation impact
--------------------

Documentation shold be updated to reflect the changes in FUel UI.


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
  ?

Other contributors:
  bdudko (bdudko@mirantis.com) - Visual design

Mandatory design review:
  vkramskikh (vkramskikh@mirantis.com)


Work Items
==========
#. Implement an ability to add pre-povisioned node in Fuel via Fuel UI.
#. Implement logic of role dependency on node status.
#. Restrict disks configuration for pre-provisioned nodes.


Dependencies
============

* Blueprint with the feature backend changes should be here.


------------
Testing, QA
------------

* Manual testing.
* Functional tests should cover the UI changes.


Acceptance criteria
===================

* It should be possible to add pre-provisioned node to Fuel via Fuel UI.
* It should not be possible to assign standard release roles to
  a pre-provisioned node. List of roles that can be applied to
  a pre-provisioned node is limited.
* It should not be possible to configure configure disks of a pre-provisioned
  node.
* It should be possible to configure plugin's repositories in Fuel UI.
* It should not be possible to reprovision a pre-provisioned node.
* It should be possible to deploy environment with pre-provisioned node(s).


----------
References
----------

[1] Ability to register pre-provisioned nodes in Fuel
    https://blueprints.launchpad.net/fuel/+spec/pre-provisioned-nodes-support

[2] Support for separate provisioning and deployment in UI
    https://blueprints.launchpad.net/fuel/+spec/support-separate-provisioning-and-deployment-in-ui

[3] #fuel-ui on freenode
