..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================================
Separate diagnostic snapshot for each OpenStack environment in UI
=================================================================

https://blueprints.launchpad.net/fuel/+spec/diagnostic-snapshot-for-environment-in-ui

As a MOS support member, I would like to have diagnostic snapshots based on an
individual environment so that I don't have to look at information that does
not pertain to the environment I am troubleshooting.


--------------------
Problem description
--------------------

It's required to have a possibility of creating a separate
"Download Diagnostic Snapshot" button for each cluster.

Because for support it's very hard:
#. To get/upload diagnostic when client have 2-3 environments with 10-20 nodes
 each
#. To analyze as the process requires extra steps to parse and understand the
 relationship between servers and environments

Also there may be a case when one environment has support contract but 2 others
may have not. Support is now asking for customers to take screenshots of their
environment Settings because of the size of the Diagnostic Snapshot and the
pain associated with requesting that artifact.


----------------
Proposed changes
----------------

It's required to have a "Download Diagnostic Snapshot" for each cluster in
Fuel UI.

There are two ways of implementing this:

#. Add a "Download Diagnostic Snapshot" button on OpenStack Environment
Dashboard
#. Add a "Download Diagnostic Snapshot" button on Support page and let the user
choose the environment for which he would like to download diagnostic snapshot


Web UI
======

"Download Diagnostic Snapshot" button will be added on Fuel UI giving an
ability for the user download diagnostic snapshot per each OpenStack
environment separately.


Nailgun
=======

API to download diagnostic snapshot per each OpenStack Environment should be
implemented.


Data model
----------

None.


REST API
--------

[tbd]
api to be discussed
/api/dump/:cluster_id


Orchestration
=============

None.


RPC Protocol
------------

None.


Fuel Client
===========

None.


Plugins
=======

None.


Fuel Library
============

None.


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

None.


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


--------------------------------
Infrastructure/operations impact
--------------------------------

None.


--------------------
Documentation impact
--------------------

The ability to download diagnostic snapshot per OpenStack environment should
be reflected in the 8.0 documentation.


--------------------
Expected OSCI impact
--------------------

None.


--------------
Implementation
--------------

Assignee(s)
===========


Primary assignee:
  TBD

Mandatory design review:
  Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com)


Work Items
==========

#. Decide where to place "Download Diagnostic Snapshot" button
#. Implement it


Dependencies
============

None.


------------
Testing, QA
------------

#. Manual testing


Acceptance criteria
===================

User can create a diagnostic snapshot at the individual OpenStack environment
level.


----------
References
----------

* #fuel-ui on freenode
