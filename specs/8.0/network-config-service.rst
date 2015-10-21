..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Fuel network modularization
=========================================


--------------------
Problem description
--------------------

Networking configuration data and the methods that work with this data are
spread throughout the existing code base.

----------------
Proposed changes
----------------

All database access will be moved into a "proxy" layer. This proxy layer will
consist of objects with a CRUD-like interface that perform database queries.
Because the proxy objects have a simple interface they could easily be
implemented to manage data in an external service.


Web UI
======

No changes should be required. All changes are to the internal representation
of network configuration objects.

Nailgun
=======

Database calls will all be moved into the appropriate object classes.
Following that work a new proxy object layer will be created. This layer will
be responsible for making database queries and provide a simple CRUD-like
interface.

This split provides two benefits. The first is that it decouples the networking
data from Nailgun's internal classes (network manager, objects, etc.) which
will allow the use of data sources besides PostgreSQL. The second is that
it makes maintaing some data (like nodegroup information) in Nailgun and other
data (e.g. IP address allocation) somewhere else possible. The composition
of this data would happen in the existing objects layer.


REST API
--------

TBD

Orchestration
=============

RPC Protocol
------------

None

Fuel Client
===========

No changes should be required to Fuel Client. The APIs with which it interacts
will remain unchanged.

Plugins
=======

TBD

Fuel Library
============

This change will be transparent to Fuel Library. The network information will
be serialized by Nailgun in the same format as it is now.

------------
Alternatives
------------

Leave it the same.

--------------
Upgrade impact
--------------

This is a huge change in Nailgun's data model and network management. The
upgrade impact will probably be significant.

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

A user will be more easily able to consume Nailgun's network configuration
data. This will make it easier for third-parties to interact with Nailgun's
configuration.

------------------
Performance impact
------------------

Serialization will require retrieving network data from an external REST API
instead of a local database.

-----------------
Deployment impact
-----------------

The external service will have to be deployed on the master node.

----------------
Developer impact
----------------

TBD

--------------------------------
Infrastructure/operations impact
--------------------------------

TBD

--------------------
Documentation impact
--------------------

The new service will need to documented.

--------------------
Expected OSCI impact
--------------------

TBD

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Ryan Moe <rmoe>

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

Phase 1
  All database calls will be moved to the objects layer. This has been started
  here: https://review.openstack.org/#/c/240568/

Phase 2
  Proxy object layer will be created with a CRUD-like interface. All database
  calls from the objects will be moved here. Objects will now call these proxy
  objects.

Phase 3
  Replace calls to proxy objects with HTTP API.

Phase 4
  Extract HTTP API as an external service.

Dependencies
============

Nailgun will depend on the client library for interacting with the external
service.

------------
Testing, QA
------------


Acceptance criteria
===================

Please specify clearly defined acceptance criteria for proposed changes.


----------
References
----------

