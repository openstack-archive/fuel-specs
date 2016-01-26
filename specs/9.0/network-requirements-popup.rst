..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================
Networking extended help popover
================================

https://blueprints.launchpad.net/fuel/+spec/network-requirements-popup

All network on the tab should accompanied by list of requirements and/or
instructions how to set up the network settings properly.

It also may contain links to documentation.


--------------------
Problem description
--------------------

Networks tab contains many settings for many networks and this is not simple
UXfor the End User.

It needs to show all restrictions or requirements around the Network settings
to help User to correctly set up network setting values.


----------------
Proposed changes
----------------


Web UI
======

On the Network settings tab will be a special info buttons - if user click on
it, additonal information about the requirements will be shown in the popover.
This buttons are visible and enabled in all cases, even if tab is locked.

The following mockup contains a design how this popover will look like:

.. image:: ../../images/9.0/network-requirements-popup/network-requirements-popup.png

Popover can also contains links to documentation.


Nailgun
=======

No changes required.


Data model
----------

None.


REST API
--------

None.


Orchestration
=============

No changes required.


RPC Protocol
------------

None.


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

None.


--------------
Upgrade impact
--------------

None.


---------------
Security impact
---------------

None.


--------------------
Notifications impact
--------------------

None.


---------------
End user impact
---------------

There is Fuel UI change only.


------------------
Performance impact
------------------

None.


-----------------
Deployment impact
-----------------

None.


----------------
Developer impact
----------------

Network settings developer should provide such instructions for the new
network or add new requirements to an existing network.


---------------------
Infrastructure impact
---------------------

None.


--------------------
Documentation impact
--------------------

The user guide should be updated according the described feature.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  kpimenova (kpimenova@mirantis.com)

Other contributors:
  bdudko (bdudko@mirantis.com) - visual design

Mandatory design review:
  vkramskikh (vkramskikh@mirantis.com)


Work Items
==========

#. Visual mockups creation.
#. JavaScript development of the feature.


Dependencies
============

None.


------------
Testing, QA
------------

Functional tests should be added to check popovers is shown on UI and
contains data.


Acceptance criteria
===================

* In case if Network has a list of restrictions or requirements, they should
  be shown on Network settings tab.

----------
References
----------

#fuel-ui on freenode
