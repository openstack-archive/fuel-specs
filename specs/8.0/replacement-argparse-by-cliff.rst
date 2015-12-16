..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Replacement argparse by cliff
================================================

https://blueprints.launchpad.net/fuel/+spec/replacement-argparse-by-cliff

We are going to extend command line interface for fuel-devops and
we have intend to replace argparce by cliff - command line interface
developed by OpanStack community


--------------------
Problem description
--------------------

Fuel-devops is going to be extended in order to support new features like
deployment on real hardware or virtual or mixed. In this case we have to
extend command line interface and add more options, nested options, multiplay
arguments. Cliff which was developed by OpenStack community is good enough
and it is a command line interface #1 for everybody who are contribute to
OpenStack and argparce is going to be replaced by cliff everywhere.

----------------
Proposed changes
----------------

Shell.py shall be kept as is and new clf.py shall be added  and provide
the same functionality like shell.py.  It is first step and
obviously shell.py will be deprecated and removed later but not right now.
We  are going to apply cliff library instead argparce.

Web UI
======

None


Nailgun
=======

None

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

Actually many free python command line libraries are presented on market
but cliff is special developed by OpenStack community in order to
replace argparce and provide more rich functionality.

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

None


----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

This feature should be described in the documentation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Kirill Rozin <krozin@mirantis.com>

Other contributors:
  QA section:Kirill Rozin <krozin@mirantis.com>

Mandatory design reviewer:
  Dennis Dmitriev <@mirantis.com>,
  Anton Studenov <astudenov@mirantis.com>


Work Items
==========

* Clf.py: new file is going to be added in order to support
          the same functionality like shell.py but
          it will utilize cliff OpenStack python library
* Shall.py: Deprecate in next time

Dependencies
============

Cliff python library

------------
Testing, QA
------------

go through list of supported commands and make it manually by using clf.py
like we do the same by using shell.py

Acceptance criteria
===================

clf.py must provide the same fucntionality like shell.py and all commands
must be supported. No any regression or degradation happaning

----------
References
----------

[1] Command Line Interface Formulation Framework
  (http://docs.openstack.org/developer/cliff/)
