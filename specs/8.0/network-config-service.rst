..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Independent network configuration service
=========================================


--------------------
Problem description
--------------------

Extracting network configuration to a generic service will allow increased
flexibility. Furthermore, other applications or services can interact with
Nailgun's network configuration.

----------------
Proposed changes
----------------

A new service will be created to store and manage network configuration
elements. This service will be integrated with Nailgun by way of a driver
layer added to Nailgun.

Web UI
======

No changes should be required. All changes are to the internal representation
of network configuration objects.

Nailgun
=======

The network manager will now manage objects in the external service. This will
require changes in Nailgun's objects, network manager and serializers.

Data model
----------

This new service will have the following data model.

::


                        +--------------------+
                        |                    |
                 +------+  interface_slaves  |
                 |      |                    |
                 |      +--------------------+
                 |
        +--------v--------+                  +---------------+
        |                 |                  |               |
        |    Interface    <------------------+     Route     |
        |                 |                  |               |
        +--------^--------+                  +---------------+
                 |                     +---------------+
                 |                     |               |
                 |                     |    Network    |
                 |                     |               |
                 |                     +-------^-------+
                 |                             |
                 |                             |
                 |                             |
        +--------+--------+            +-------+-------+
        |                 |            |               |
        |    IPAddress    +------------>    IPRange    |
        |                 |            |               |
        +-----------------+            +---------------+



Ethernet interfaces, bonds, and bridges are all stored in one table
(differentiated by a 'type' field). Slave interfaces are kept track of
with a self-referential many-to-many relationship (interface_slaves).

IPs are associated with an interface (or bond or bridge). Network-to-nic
mapping is not done in this service. It is assumed the user application will
keep track of that.

Networks keep track of information related to L3 networks (cidr,
gateway, ip ranges, etc).

Route information is stored per-interface.

Nailgun's data model will be left unchanged as the existing implementation
will be one of the driver options.


Nailgun Integration
-------------------

All access to the network configuration should go through the objects layer.
The existing objects that are backed by SQLAlchemy will remain as a driver.
Additional drivers can be implemented by creating modules in the 
nailgun.objects namespace.

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

This is a big change in the way Nailgun manages network configuration data.
The upgrade impact will probably be significant.

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

The external service will have to be deployed in a container on the master
node.

----------------
Developer impact
----------------

The existing objects implementation will be turned into a driver layer. There
will also be interaction with an external service to consider.

--------------------------------
Infrastructure impact
--------------------------------

TBD

--------------------
Documentation impact
--------------------

The new service will need to documented. The new driver interface will also
need to be documented.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Ryan Moe <rmoe>

Other contributors:
  Vladimir Kuklin <aglarendil>

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

* Move all database access in network manager to the appropriate objects. [0]
* Create core driver that uses the current SQLAlchemy objects.
* Create new driver to store configuration in external service.


Dependencies
============

Nailgun will depend on the client library for interacting with the external
service.

------------
Testing, QA
------------

* Unit and functional tets for new external service.
* Additional tests for Nailgun to validate new driver.


Acceptance criteria
===================

* All tests pass with new driver.

----------
References
----------
[0] https://review.openstack.org/#/c/240568/
