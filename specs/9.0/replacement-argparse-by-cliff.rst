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

Current implementation is using argparse where all possiable params 
has been added to "get_params" function. List of supported commands
is kept under "commands" global dict. Actually list of commands and
params are not mapped together and if we need to add new connamd then
we have to add new one to "commands" global dict and
add params to "get_params" function. Finnaly implementation of each
command is done in specific fucntion of "Shell" class where specific
params are getting by using "get_params" function despite unuseable
params can be passed and we have to specify what params is actual for
this specific command. We don't see directly what params are applicable
for each command and we have to go to "get_params" fucntion is order
to see specific of each param applicable for this command.

Moreover cliff is going to be used as default CLI framework and it
is reasonable to replace existing argparce by cliff in order to
follow to latest requirements around of CLI.

Cliff which was developed by OpenStack community is good enough
and it is a command line interface #1 for everybody who are contribute to
OpenStack.

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
