==========================================
Get rid of the shotgun
==========================================

https://blueprints.launchpad.net/fuel/+spec/shotgun

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
hand it over to separate tool (such as Timmy).

Web UI
======

The button "Generate diagnostic snapshot" is deleted. Instead there is
a paragraph describing ways of gathering necessary information with
Timmy for MOS and also instructions of its obtaining and installation
for community version.


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

CI must be changed to adopt other tools in order to be able to gather
diagnostic snapshots.


--------------------
Documentation impact
--------------------

Documentation must be supplemented with a chapter devoted to Timmy
installation and usage and alternative tools to perform the diagnostic
snapshot gathering.


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

* Ensure Timmy default configuration produces snapshot with enough
  information.

* Add Timmy package to the master node.

* Get rid of existing snapshotting UI.

* Switch QA snapshotting code to Timmy.

* Get rid of snapshotting code in Nailgun and Astute.

* Implement filtering by date range in Timmy.

* Reflect a switch to Timmy in the fuel documentation.

Dependencies
============

No dependencies.


------------
Testing, QA
------------

Testing involves ensuring that default Timmy configuration produces a
snapshot with not less information than a snapshot produced by
Shotgun.

Acceptance criteria
===================

Fuel is not used to gather diagnostic snapshots.


----------
References
----------

N/A
