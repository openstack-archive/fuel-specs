==========================================
Get rid of the shotgun
==========================================

https://blueprints.launchpad.net/fuel/+spec/shotgun

--------------------
Problem description
--------------------

* It is not possible to create a diagnostic snapshot when WebUI,
  Nailgun or Astute is broken.

* There is a code duplication. There are at least two utilities doing
  the same thing: Shotgun and Timmy. In fact there are more, for
  instance Ansible is capable of doing the same thing.

* There is a problem with segregation of concerns. Shotgun is a part
  of the Fuel, however it gathers not only Fuel logs.

----------------
Proposed changes
----------------

The solution is to replace shotgun with Timmy.

Web UI
======

The button "Generate diagnostic snapshot is deleted". Instead there is
a paragraph of the text describing ways of gathering necessary
information with Timmy for MOS and also instructions of its obtaining
and installation for community version.


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

Timmy is expected to be faster than Shotgun.


-----------------
Deployment impact
-----------------

MOS ISO is expected to include Timmy package by default.


----------------
Developer impact
----------------

No impact.


---------------------
Infrastructure impact
---------------------

CI must be changed to adopt Timmy in order to be able to gather
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

Timmy CLI works. CI produces snapshot artifacts as a part of testing
process.


----------
References
----------

N/A
