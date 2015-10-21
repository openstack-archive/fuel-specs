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

Data Model
----------

Database calls will all be moved into the appropriate object classes.
Following that work a new proxy object layer will be created. This layer will
be responsible for making database queries and provide a simple CRUD-like
interface.

This split provides two benefits. The first is that it decouples the networking
data from Nailgun's internal classes (network manager, objects, etc.) which
will allow the use of data sources besides Nailgun's database. The second is
that it makes maintaining some data (like nodegroup information) in Nailgun and
other data (e.g. IP address allocation) somewhere else possible. The
composition of this data would happen in the existing objects layer.

The following objects (and their corresponding Collections) will be proxied:

 * NetworkGroup (objects/network_group.py)
 * IPAddr (objects/ip_address.py)
 * IPAddrRange (objects/ip_address.py)
 * NIC (objects/interface.py)
 * Bond (objects/bond.py)
 * NIC and Bond network assignments (does not exist in current objects layer)

Proxy Interface
---------------

get(id)
 Retrieves the instance matching ``id``

get_all()
 Retrieves all instances

create(data)
 Creates a new instance with values from ``data``

update(instance, data)
 Updates ``instance`` with specified ``data``

delete(instance)
 Deletes the specified ``instance``

bulk_delete(ids)
 Deletes all instances which match the list of ``ids``

filter_delete(data)
 Deletes all instances matching the filter parameters

filter(data)
 Retreives instances matching the specified filter parameters
 ``data`` is a dictionary with the following format:

 * options

   * fields: List of fields to include in the query, defaults to '*'
   * distinct: List of fields to create DISTINCT ON clause for
   * single: If True will return first result only, defaults to False

 * filters

   * Filters can be nested arbitrarily
   * By default a list of filters is joined by an AND clause
   * The boolean filters AND, OR, NOT are supported. These combine multiple SQL
     filters like so: ::

             {'or': [
               {'name': 'field1', 'op': 'gt', 'val': 10},
               {'name': 'field2', 'op': 'is', 'val': None}
             ]}

   * The filter format is: {'name': <field name>, 'op': <op>, 'val': <val>}
     where <field name> is the name of the field, <op> is the SQL operation to
     apply, and <val> is the value used by the operation
   * The following SQL operations are supported:

     * eq: field = val
     * gt: field > val
     * gte: field >= val
     * lt: field < val
     * lte: field <= val
     * in: field IN val
     * is: field IS val
     * isnot: field IS NOT val


Example:

   ::

        {
            'options': {
                'fields': [
                    'ip_addr',
                    'network'
                ]
            },
            'filters': [
                {'name': 'network', 'op': 'eq', 'val': network_id},
                {'or': [
                    {'name': 'node', 'op': 'isnot', 'val': None},
                    {'name': 'vip_type', 'op': 'isnot', 'val': None}
                ]}
            ]
        }


This equates to:

    ::

        SELECT ip_addr, network FROM ipaddr WHERE network=<network_id>
            AND (node IS NOT NULL OR vip_type IS NOT NULL)

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

The initial proxy object implementation should have minimal overhead as it is
only one additional method call. However, there will most likely be a negative
performance impact once the proxy object calls are replaced with HTTP calls.

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
  objects. Work started here: https://review.openstack.org/#/c/256881

Phase 3
  Replace calls to proxy objects with HTTP API. This will result in a
  potentially dramatic drop in performance. Areas in Nailgun which make a large
  number of requests for network data will need to be identified and then
  optimized.

Phase 4
  Extract HTTP API as an external service and develop a client library for use
  by Nailgun.

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

