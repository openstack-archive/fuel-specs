..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Replacement argparse by click
================================================

https://blueprints.launchpad.net/fuel/+spec/replacement-argparse-by-click

Argparse is not flexible like click. We are going to extend command line
interface for fule-devops with command groups and nested sub commands.
To avoid complexity solution we will use click lib instead of argparse.


--------------------
Problem description
--------------------

Fuel-devops is going to be extended in order to support new features like
deployment on real hardware or virtual or mixed. In this case we have to
extend command line interface and add more options, nested options, multiplay
arguments. Argparse currently does not support disabling of interspersed
arguments. It is root cause.

----------------
Proposed changes
----------------

Shell.py shall be kept as is and new cli.py shall be added  and provide
the same functionality like shell.py.  It is first step and
obviously shell.py will be deprecated and removed later but not right now.
We  are going to apply click library here which is using decorators and
cli.py will provide general command line interface.

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
but click still is supporting and have appropriated license
(Click is licensed under a three-clause BSD License).

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

* Cli.py: new file is going to be added in order to support
          the same functionality like shell.py but
          it will utilize click python library
* Shall.py: Deprecate in next time

Dependencies
============

Click python library

------------
Testing, QA
------------

go through list of supported commands and make it manually by using cli.py
like we do the same by using shell.py

Acceptance criteria
===================

cli.py must provide the same fucntionality like shell.py and all commands
must be supported. No any regression or degradation happaning

----------
References
----------

[1] Python Click licence
  (http://click.pocoo.org/6/license/#license-text)
