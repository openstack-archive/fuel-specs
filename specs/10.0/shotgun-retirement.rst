======================
Shotgun replacement
======================

https://blueprints.launchpad.net/fuel/+spec/shotgun-retirement

--------------------
Problem description
--------------------

* It is not possible to limit a diagnostic snapshot content to
  particular nodes, dates and services

* Snapshot gathering is slow and requires quite a lot of space because
  it is suboptimal - gathering process is sequential, data in transit
  is not compressed.

----------------
Proposed changes
----------------

The solution is to use existing tool which has already solved almost
all of the above problems - Timmy.

Web UI
======

No changes.

Nailgun
=======

Data model
----------

No changes.

REST API
--------

No changes.

Orchestration
=============

Astute code which calls Shotgun should be replaced with Timmy call. Since
no new elements is added into Web UI no new parameters are expected to be
passed to Timmy.

RPC Protocol
------------

No changes.


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

* We could continue with shotgun improving it if necessary. This would
  require rewriting it.
* We could use one of existing 3rd party tools. There is no tool which
  covers the whole use case. LMA solutions are not inteded to collect
  configuration information, arbitrary command outputs etc. Generic
  solutions such as Ansible requires a lot of additional effort to
  make it do what we want.

--------------
Upgrade impact
--------------

Timmy packages must be installed on master node during the upgrade procedure.

---------------
Security impact
---------------

No.

--------------------
Notifications impact
--------------------

No.

---------------
End user impact
---------------

No.

------------------
Performance impact
------------------

No.

-----------------
Deployment impact
-----------------

Timmy package must be installed on master node.

----------------
Developer impact
----------------

No.

---------------------
Infrastructure impact
---------------------

No.

--------------------
Documentation impact
--------------------

There must be reference to Timmy documentation in Fuel documentation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  gkibardin

Mandatory design review:
  vkozhukalov

Work Items
==========

* Ensure Timmy default configuration produces snapshot with enough
  information.

* Add Timmy package to the master node.

* Make "generate snapshot" button use Timmy.

Dependencies
============

No.

------------
Testing, QA
------------

No.

Acceptance criteria
===================

* Timmy is available on master node.
* "Generate snapshot" button in UI uses Timmy and time frame for logs
  is limited by 3 days.

----------
References
----------

No.

