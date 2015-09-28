..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================
Support node groups on the network tab in Fuel UI
=================================================

https://blueprints.launchpad.net/fuel/+spec/node-groups-network-tab

Currently on Fuel UI it's impossible to see the list of node network groups and
to see which networks belong to which node network group, this is possible
only via CLI.

--------------------
Problem description
--------------------

For now node network groups can be viewed only via command line
interface. It is important for users to have an ability to view node network
groups via Fuel UI.

Node network group will appear as a dropdown on Networks tab, so by switching
it the user will be able to see which networks correspond to which node network
group.


----------------
Proposed changes
----------------

Web UI
======

[tbd] - we need to decide whether group_id will be a cluster attribute or
cross-env. For now it's cluster level, but there are plans to make it
cluster-agnostic.

On Networks tab there will appear a dropdown (select box) where the user will
be able to choose the appropriate node network group and Networks tab content
would re-render according to this selection.


Nailgun
=======

[tbd] we need to decide how networks settings will be stored for each node
group

Data model
----------

None


REST API
--------

None


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

None


Fuel Library
============

None


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

The end user will be able to see the list of Networks per each node network
group


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

None


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
 Aleksandra Morozova, astepanchuk(astepanchuk@mirantis.com)

Mandatory design review:
  Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com)


Work Items
==========

#. The user should be able to see the networks according to node network groups

Dependencies
============

None


------------
Testing, QA
------------

* Manual testing
* UI functional tests


Acceptance criteria
===================

The user has an ability to manage networks separately for each node group


----------
References
----------

* Support multirack in Fuel UI
  https://blueprints.launchpad.net/fuel/+spec/multirack-in-fuel-ui
* #fuel-ui on freenode
