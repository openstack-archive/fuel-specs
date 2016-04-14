..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Fuel network manager refactoring
=========================================


--------------------
Problem description
--------------------

Networking configuration data and the methods that work with this data are
spread throughout the existing code base. As a consequence there is some code
duplication. This makes it harder to understand and extend this functionality
than it should.

----------------
Proposed changes
----------------

All database queries will be moved from NetworkManager to the appropriate
objects.


Web UI
======

No changes should be required. All changes are to the internal representation
of network configuration objects.

Nailgun
=======

Data model
----------

Database calls will all be moved into the appropriate object classes.

The following objects (and their corresponding Collections) will be modified:

 * NetworkGroup (objects/network_group.py)
 * IPAddr (objects/ip_address.py)
 * IPAddrRange (objects/ip_address.py)
 * NIC (objects/interface.py)
 * Bond (objects/bond.py)
 * NIC and Bond network assignments (does not exist in current objects layer)

REST API
--------

No changes to the REST API are required.

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

None

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

None.

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

In NetworkManager developers must use object methods instead of direct
database queries.

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Developer documentation describing how the proxy interface works will need
to be written.

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
  Aleksey Kasatkin


Work Items
==========

  * All database calls will be moved to the objects layer. This has been done
    here: https://review.openstack.org/#/c/240568/ and here:
    https://review.openstack.org/#/c/268367/


Dependencies
============

None

------------
Testing, QA
------------

None

Acceptance criteria
===================

  * NetworkManager and its subclasses contains no database queries

----------
References
----------

None
