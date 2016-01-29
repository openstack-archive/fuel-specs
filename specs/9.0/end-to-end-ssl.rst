..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================
Add end-to-end encryption to OpenStack services
===============================================

https://blueprints.launchpad.net/fuel/+spec/end-to-end-ssl

We need to imlement end-to-end encryption for OpenStack services.

--------------------
Problem description
--------------------

Today all encrypted traffic destined to OpenStack services unwraps on
HAProxy which listen on VIPs. Then unencrypted request goes to service
it was originally created. As usually we have HA enabled for OpenStack
service, that request can be forwarded by network to other node and,
as a result, can be intercepted.

----------------
Proposed changes
----------------

We propose to avoid encryption on VIP and instead forward encrypted request
to node with OpenStack service itself, hereby provide encrypted line at all
request network path. Steps which needed to achieve this behavior, are:

1. Move HAProxy that listen on VIPs for OpenStack services to TCP mode. It will
   allow to transparenly proxying requests without TLS unwrapping.

2. On every node where OpenStack service (Keystone, Nova, Glance, etc.)
   listens, spawn new HAProxy that will listen on corresponding IP address.
   This HAProxy will work like old one that listened on VIP. It will unwrap TLS
   but will not work as load-balancer - unencrypted request will be forwarded
   only to service on node with this HAProxy itself.

3. To avoid opportunity of using unencrypted communication with OpenStack
   services directly, bind them only to localhost address. This way only
   HAProxy on this node will have an ability to talk with service.

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

New task that will add HAProxy to every node should be implemented.

------------
Alternatives
------------

Terminate TLS without HAProxy on services directly. Unfortunately, it will
lead to perfomance degradation.

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

Communication between HAProxy on VIP and target clients will be encrypted.

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

Complete criteria:
   <sbogatkin@mirantis.com> - Need to create documentation

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Stanislaw Bogatkin <sbogatkin@mirantis.com>

Mandatory design review:
  Stanislaw Bogatkin <sbogatkin@mirantis.com>
  Vladimir Kuklin <vkuklin@mirantis.com>

Work Items
==========

* Implement task for creating HAProxy instance on nodes itself

* Bind services to localhost

* Move VIP HAProxy to TCP mode

------------
Testing, QA
------------

None

Acceptance criteria
===================

* Fuel-library noop tests should be enough for test implementation

* The documentation should be created.

----------
References
----------

None
