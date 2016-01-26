..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================
Networking extended help pop-ups
================================

https://blueprints.launchpad.net/fuel/+spec/network-requirements-popup

On the Network settings Tab we need to show special popups containing
information about requirements around the Networking inputs.

It also may contain links to documentation.


--------------------
Problem description
--------------------

It needs to show all restrictions or requirements around the Network settings
so that user can correctly assign the values the first time.


----------------
Proposed changes
----------------

On the Network settings Tab will be a special info buttons - if user click on
it, additonal information about the requirements will be shown in the popop.


Web UI
======

The following mockup contains a design how this popup will looks like:

.. image:: ../../images/9.0/network-requirements-popup/network-requirements-popup.png

Popup is showing on the page after user click the info button and closes after
any outer click. Popup can also contains links to documentation, so it is
possible to click to the link inside.


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

None.


---------------------
Infrastructure impact
---------------------

None.


--------------------
Documentation impact
--------------------

Screenshots of Network settings should be updated in the user guide.


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

None.


Acceptance criteria
===================

* Every Network type has a list of restrictions or requirements should be
  shown on Network settings Tab.

----------
References
----------

#fuel-ui on freenode
