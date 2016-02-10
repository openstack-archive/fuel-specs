..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Add memcache load balancer to controllers
=========================================

https://blueprints.launchpad.net/fuel/+spec/add-memcache-loadbalancer

--------------------
Problem description
--------------------

Today we have several memcached instances that ran one per each controller.
OpenStack services configuration files have list of those instances in it. But
when one of nodes with memcached is dead, OpenStack service can't process this
fast and reliable, because there is no internal request rescheduling mechanism
from one memcache to another in OpenStack service.

----------------
Proposed changes
----------------

We will propose a new entity - twemproxy, loadbalancer created especially for
memcache. It is reliable and fast, can mantain persistent connections and
reliable find out that node is down. Overall scheme will look next way:

* All controllers will look on localhost for memcached instance
* On each controller localhost there will be a twemproxy instance listening
  for a connection
* Twemproxy instances will subscribe to all memcache instances

It will look like this:

::

  +-------------------+  +-------------------+  +-------------------+
  |   Controller.1    |  |   Controller.2    |  |   Controller.3    |
  +-------------------+  +-------------------+  +-------------------+
  |                   |  |                   |  |                   |
  |    Memcached-1    |  |   Memcached-2     |  |   Memcached-3     |
  |  10.109.1.4:11211 |  | 10.109.1.5:11211  |  | 10.109.1.6:11211  |
  |        ^          |  |         ^         |  |         ^         |
  |        |          |  |         |         |  |         |         |
  |        +----------------------------------------------+         |
  |        |          |  |         |         |  |         |         |
  |        +          |  |         +         |  |         +         |
  |    Twemproxy-1    |  |    Twemproxy-2    |  |    Twemproxy-3    |
  |  127.0.0.1:22122  |  |  127.0.0.1:22122  |  |  127.0.0.1:22122  |
  |        ^          |  |         ^         |  |         ^         |
  |        |          |  |         |         |  |         |         |
  |        +          |  |         +         |  |         +         |
  | OpenStack service |  | OpenStack service |  | OpenStack service |
  |                   |  |                   |  |                   |
  +-------------------+  +-------------------+  +-------------------+


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

New puppet twemproxy module must be added to library side. I believe that we
can get existing one: [0].

------------
Alternatives
------------

* mcrouter - it is more or less pure alternative of twemproxy
* memcached with the repcached patches - it will cost us to support custom
  memcached package

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

This change needs to be reflected in the Fuel documentation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Stanislaw Bogatkon <sbogatkin@mirantis.com>

Mandatory design review:
  Vladimir Kuklin <vkuklin@mirantis.com>

Work Items
==========

Fuel Library:

* Pull new twemproxy module
* Create a new task to install and configure twemproxy
* Point all OpenStack services to localhost for memcache by default

Dependencies
============

None

------------
Testing, QA
------------

Noop tests should be changed accordingly

Acceptance criteria
===================

* All OpenStack service should be point to localhost twemproxy instead of
  real memcached instances
* Twemproxy must balance to real memcaches

----------
References
----------

[0]: https://github.com/sorrowless/puppet-twemproxy
