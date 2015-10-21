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
elements.

Web UI
======

No changes should be required. All changes are to the internal representation
of network configuration objects.

Nailgun
=======

The network manager will now manage objects in the external service. This will
require changes in Nailgun's database models, objects, network manager and
serializers.

Data model
----------

This new service will have a fairly simple data model.

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

Nailgun will no longer have database tables dedicated to keeping track of
networks, IP addresses, or interfaces.


Nailgun's data model will change in the following ways:

NodeNICInterface, NodeBondInterface, IPAddrRange, and IPAddr models will be
removed as this data is provided in full by the external service.

NetworkNICAssignment and NetworkBondAssignment will be combined into a single
model. Because this new service represents interfaces and bonds in the same way
there is no need for a separate model for each type.

New models will be created for:
 * Managing network<->release information
 * Managing network<->nodegroup information

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

The external service will have to be deployed in a container on the master
node.

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

Other contributors:
  Vladimir Kuklin <aglarendil>

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

TBD

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

