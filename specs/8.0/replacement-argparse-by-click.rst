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
extend command line interface and add more options. Argparse has built-in
magic behavior to guess if something is an argument or an option.
This becomes a problem when dealing with incomplete command lines as it’s
not possible to know without having a full understanding of the command line
how the parser is going to behave.
Moreover argparse currently does not support disabling of interspersed
arguments. It is root cause.

There are so many libraries out there for writing command line utilities
like argparse, why does Click exist? This question is easy to answer:
because there is not a single command line utility for Python out
there which ticks the following boxes:
- is lazily composable without restrictions
- fully follows the Unix command line conventions
- supports loading values from environment variables out of the box
- supports for prompting of custom values
- is fully nestable and composable
- works the same in Python 2 and 3
- supports file handling out of the box
- comes with useful common helpers (getting terminal dimensions, ANSI colors,
fetching direct keyboard input, screen clearing, finding config paths,
launching apps and editors, etc.)

The obvious ones are optparse and argparse from the standard library.
Click is actually implemented as a wrapper around a mild fork of optparse and
does not implement any parsing itself. The reason it’s not based on argparse
is that argparse does not allow proper nesting of commands by design and
has some deficiencies when it comes to POSIX compliant argument handling.

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
