..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================
Support node groups on the network tab in Fuel UI
=================================================

https://blueprints.launchpad.net/fuel/+spec/node-groups-network-tab

Introduce an ability to view and configure networks settings with regard to
node network groups.

--------------------
Problem description
--------------------

For now network settings per each node network groups can be configured via
command line interface. It is important for users to have an ability to
configure network settings for node network group via Fuel UI.

Node network group will appear as a dropdown on Networks tab, so by switching
it the user will be able to see which networks and which parameters correspond
to which node network group and configure them.


----------------
Proposed changes
----------------

Web UI
======

If OpenStack environemnt has more then one node network group on Networks tab
there will appear a dropdown (select box) where the user will be able to choose
the appropriate node network group and Networks tab content would re-render
according to this selection. Common network settings would stay the same for
each node network group (they are placed at the bottom of the page) so only the
upper part of Networks tab will change.

After changing some network settings for particular node network group it will
be possible to switch to the other node network group and change setting for it
also without confirmation dialog on leaving unsaved data. All the changes are
applied only after clicking Save Settings button at the bottom of the page.


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

The end user should be able to manage network settings for each node network
group.


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
 Aleksandra Morozova, astepanchuk (astepanchuk@mirantis.com)

QA engineer:
    Anastasia Palkina, apalkina (apalkina@mirantis.com)

Mandatory design review:
  Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com)


Work Items
==========

#. The user should be able to manage network settings according to node
network groups.


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

The user has an ability to manage networks separately for each node group.


----------
References
----------

* Support multirack in Fuel UI
  https://blueprints.launchpad.net/fuel/+spec/multirack-in-fuel-ui
* #fuel-ui on freenode
