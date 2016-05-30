..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Create a client module for fuel-devops3.0
=========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-devops-client-as-a-module

Fuel-devops should have an API class to provide a complete interface for
interacting with the environment.


--------------------
Problem description
--------------------

In current implementation there is a list of functions to interact
with environments:

    * devops/helpers/helpers.py:
        * get_nodes
        * get_slave_ip
        * get_admin_ip
        * get_node_remote
        * get_admin_remote
        * get_private_keys
    * devops/helpers/ntp.py:
        * sync_time

These main functions are written in procedural style. It makes it hard to
extend or add a new one.

Also some of these functions are duplicated in fuel-qa
fuelweb_test/models/environment.py

----------------
Proposed changes
----------------

To reduce dependency issues and allow to re-use management layer of
virtual/baremetal labs:

- separate all the code that manage environments nodes/networks
  into a 'devops' module
- separate all the code that provide a logical layer (ssh manager,
  filters for specific node roles, accessing to the services
  that are started on the environment nodes) into a fuel-devops client module.

Fuel-devops client module should provide a complete interface for interacting
with the environment: manage nodes, mapping devops and nailgun nodes into a
single object, accessing nodes via SSH, snapshot/revert nodes, bootstrap admin
node and so on.
It should encapsulate some of methods from fuel-devops Environment object and
fuel-qa EnvironmentModel object (then deprecate it later).


Schema of DevopsClient usage::

    +---------+                 +----------+
    |         |                 |          |
    | fuel-qa |                 | shell.py |
    |         |                 |          |
    +-----+---+                 +-----+----+
          |                           |
          +--------+     +------------+
                   |     |
                   v     v
              +--------------+
              |              |
              | DevopsClient |
              |              |
              +----+-----+---+
                   |     |
                   |     +----------+------------------+
                   |                |                  |
                   v                v                  v
    +--------------------+    +---------------+   +----------+
    |                    |    |               |   |          |
    | devops.Environment |    | NailgunClient |   | NtpGroup |
    |                    |    |               |   |          |
    +--------------------+    +---------------+   +----------+


NailgunClient should be added to replace get_nodes method.
NtpGroup should be added to replace sync_time method.



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

No FUEL REST API changes.

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

N/A


--------------
Upgrade impact
--------------

N/A


---------------
Security impact
---------------

N/A


--------------------
Notifications impact
--------------------

N/A


---------------
End user impact
---------------

N/A


------------------
Performance impact
------------------

N/A


-----------------
Deployment impact
-----------------

N/A


----------------
Developer impact
----------------

N/A


---------------------
Infrastructure impact
---------------------

N/A


--------------------
Documentation impact
--------------------

* fuel-qa

* fuel-devops


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  * Anton Studenov (astudenov): astudenov@mirantis.com

Other contributors:
  * Dennis Dmitriev (ddmitriev): ddmitriev@mirantis.com

Mandatory design review:
  Anastasiia Urlapova, Denys Dmytriiev


Work Items
==========

* Implement DevopsClient and move get_admin_ip/get_node_remote/etc
  to this class
* Change Shell to use DevopsClient instead of direct access to
  Environment
* Refactor ntp.py to be independent of get_admin/get_slave_remote functions
* Deprecate get_admin_ip/get_node_remote/etc functions


Dependencies
============

None


------------
Testing, QA
------------

None

Acceptance criteria
===================

DevopsClient provides all necessary methods to interact with devops
environment.


----------
References
----------

None
