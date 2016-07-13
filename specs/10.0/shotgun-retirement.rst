==========================================
Get rid of the shotgun
==========================================

https://blueprints.launchpad.net/fuel/+spec/shotgun-retirement

--------------------
Problem description
--------------------

* It is not possible to create a diagnostic snapshot when WebUI,
  Nailgun or Astute is broken.

* Fuel is a deployment tool, gathering logs is out of its scope.

----------------
Proposed changes
----------------

The solution is to get rid of snapshotting functionality in Fuel and
hand it over to separate tool.

Web UI
======

The button "Generate diagnostic snapshot" is deleted. Instead there is
a paragraph describing ways of gathering necessary information with
3rd party tools and favorite support guys tool Timmy.


Nailgun
=======

Get rid of the code which handles snapshot creation.

Data model
----------

No changes.


REST API
--------

Get rid of snapshot creation API.


Orchestration
=============

Get rid of Astute snapshot creation logic.


RPC Protocol
------------

Get rid of dump_environment message.


Fuel Client
===========

No changes.


Plugins
=======

No changes.


Fuel Library
============

No changes.


------------
Alternatives
------------

There are tools capable of performing the same task, for instance,
Ansible. However, integrating them would require a lot more effort.

--------------
Upgrade impact
--------------

No impact.


---------------
Security impact
---------------

No impact.


--------------------
Notifications impact
--------------------

No impact.


---------------
End user impact
---------------

It slightly worsens user experience, but in exchange there is more
flexibility.


------------------
Performance impact
------------------

No impact.


-----------------
Deployment impact
-----------------

No impact.


----------------
Developer impact
----------------

No impact.


---------------------
Infrastructure impact
---------------------

No.

--------------------
Documentation impact
--------------------

Documentation must be supplemented with a chapter devoted to 3rd party
tools to perform the diagnostic snapshot gathering.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  gkibardin

Other contributors:
  None

Mandatory design review:
  vkozhukalov


Work Items
==========

* Get rid of existing snapshotting UI.

* Get rid of snapshotting code in Nailgun and Astute.

Dependencies
============

No dependencies.


------------
Testing, QA
------------

See below.

Acceptance criteria
===================

WebUI isn't able to generate diagnostic snapshots. Nailgun API doesn't
contain snapshot related entry points.


----------
References
----------

N/A
