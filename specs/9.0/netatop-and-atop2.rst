..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
netatop and atop2 on nodes
==========================================

https://blueprints.launchpad.net/fuel/+spec/netatop-and-atop2

A proposal to integrate netatop (http://www.atoptool.nl/netatop.php)
and atop2 (required by netatop) into future MOS releases.

This will allow to see networking stats per process which is very useful
for troubleshooting and performance analysis.

Currently there is no tool in Linux which allows getting this data
with any comparable level of ease. The only tool which is close to that is
`nethogs` but apparently it does not provide any historical data
AND it is buggy.

--------------------
Problem description
--------------------

For performance analysis and performance-related troubleshooting it is
important to be able to see per-process metrics, including network counters.
Such feature is not available at the moment in MOS releases.

----------------
Proposed changes
----------------

For CentOS - add installation of netatop and atop2 (rpms available online)
to node deployment routines.
For Ubuntu - build our own packages from sources and bundle them in our repo,
add installation of these to node deployment routines.

Web UI
======

No changes

Nailgun
=======

No changes

Data model
----------

No changes

REST API
--------

No changes

Orchestration
=============

No changes

RPC Protocol
------------

No changes

Fuel Client
===========

No changes

Plugins
=======

No changes

Fuel Library
============

Build packages for Ubuntu
Add packages to node deployment routines

------------
Alternatives
------------

No idea

--------------
Upgrade impact
--------------

No impact

---------------
Security impact
---------------

No impact

--------------------
Notifications impact
--------------------

No impact

---------------
End user impact
---------------

User will be able to see per-proccess network data in atop
in real-time and in logs

------------------
Performance impact
------------------

Negligible, kernel netatop module adds minimal load

-----------------
Deployment impact
-----------------

No impact

----------------
Developer impact
----------------

No impact

---------------------
Infrastructure impact
---------------------

No impact

--------------------
Documentation impact
--------------------

No impact

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  None

Other contributors:
  None

Mandatory design review:
  None


Work Items
==========

* set up repos for netatop and atop2 for Ubuntu
  or do a one-time build of .deb packages
* embed netatop and atop2 packages into node installation repos
* add package netatop installation to node deployment process
* substitute atop installation with atop2 installation

Dependencies
============

None

------------
Testing, QA
------------

No specific tests necessary

Acceptance criteria
===================

* atop-2.X running on every deployed node
* netatop service running on every deployed node
* per-process network data visible in atop

----------
References
----------

http://www.atoptool.nl/netatop.php
http://www.atoptool.nl/index.php
