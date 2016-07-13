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

The solution is to use self-sufficient tool which is able collect a
diagnostic snapshot even when some Fuel functionality is broken.  
Taking into account the additional functionality provided Timmy looks
like very good candidate.

Web UI
======

Below "Generate diagnostic snapshot button" there is a paragraph of
text describing how to use command line to limit (or extend) the data
included into the diagnostic snapshot.

Nailgun
=======

Get rid of shotgun config generation code.

Data model
----------

No changes.


REST API
--------

No changes


Orchestration
=============

Call Timmy instead of Shotgun.


RPC Protocol
------------

No changes.


Fuel Client
===========

Get rid of fuel2 snapshot command.


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
Ansible. However, integrating them would require a lot more
effort. Existing solution, Shotgun, is not designed to gather
diagnostic data on its own.

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

The commmand line tools gives more flexibility.


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

Documentation must be supplemented with a link to Timmy documentation.

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

* Replace Shotgun calls with Timmy.

* Get rid of Shotgun configuration generation in Nailgun.

Dependencies
============

No dependencies.


------------
Testing, QA
------------

See below.

Acceptance criteria
===================

Timmy command line utility is available on the Master node. 

----------
References
----------

N/A
