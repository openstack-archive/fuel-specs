..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Package for nodejs modules for nailgun
==========================================

https://blueprints.launchpad.net/fuel/+spec/package-for-js-modules


--------------------
Problem description
--------------------

For building nailgun package we made about 50 packages with js libraries. 
But every package included about 100 js libraries. 
For latest update nailgun we should rebuild more 20 packages with new js modules. 
This workflow is very long.


----------------
Proposed changes
----------------

Need to prepare 1 package with all JS libraries. 
All js libraries will be automatically downloading when building nailgun package. 
For update all js libraries maintainer should update version of new package in spec file

Web UI
======

None


Nailgun
=======

TODO

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

Rebuilding 50 packages with new js libraries

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

None

------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

Mone


----------------
Developer impact
----------------

Reducing the time required to update the js library for canges in Fuel UI

---------------------
Infrastructure impact
---------------------

Plan fort transition responsibility from MOS-packages team to the Fuel build team:
*Artem prepare the package (new spec file) with new js modules. it will be one package containing all js modules. All modules automatically downloaded in the building process.
*SergeyO will participate in the review of new package
*The Package will be merged

*For update js modules:
*Vitaly will create a new bug in LP
*SergeyO create new change request in gerrit. it will be simple request with increase of package version in spec file. 
*After approval from Vitaly, new package will be merged


--------------------
Documentation impact
--------------------

ToDO


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Artem Silenkov`_

Build-team:
  `Sergey Otpuschennikov_


Mandatory Design Reviewers:
  - `Artem Silenkov`_
  - `Dmitry Burmistrov`_
  - `Roman Vyalov`_
  - `Vladimir Kozhukalov`_



Work Items
==========

Plan for transition responsibility from MOS-packages team to the Fuel build team:
*Artem prepare the package (new spec file) with new js modules. it will be one package containing all js modules. All modules automatically downloaded in the building process.
*SergeyO will participate in the review of new package
*The Package will be merged

*For update js modules:
*Vitaly will create a new bug in LP
*SergeyO create new change request in gerrit. it will be simple request with increase of package version in spec file. 
*After approval from Vitaly, new package will be merged


Dependencies
============




------------
Testing, QA
------------

None


Acceptance criteria
===================




----------
References
----------

.. _`Dmitry Burmistrov`: https://launchpad.net/~dburmistrov
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`Artem Silenkov`: https://launchpad.net/~asilenkov
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Sergey Otpuschennikov`: https://launchpad.net/~sotpuschennikov

