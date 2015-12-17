..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Bareon-api integration with Nailgun
==========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/example

In order to externalize nodes volumes management, Nailgun needs some
integration with bareon-api service. The change is a part of fuel
modularization plan.


--------------------
Problem description
--------------------

Currently the Volume Manager is a part of nailgun. All volumes computations
and disks management are being processed there. The problem VM resolves
is generic and reaches broader areas than just fuel. So it's worth to
externalize it which is now happening in bareon project [#bareon-api]_.

Nailgun needs some integration with new tool to use its resources.
It also needs to be replaceable by other tools with such functionality.


----------------
Proposed changes
----------------

Nailgun extensions engine has capability to catch specific events like node
create, update, delete etc. Proposed change considers creating an adapter
for bareon-api, which will update the service about node volumes changes in
cases like assigning new role for node or destroying an environment, so
it should be implemented as an extension.

Current `volume-manager` extension must be completely replaced by
`bareon` extension.


Web UI
======

None


Nailgun
=======

Data model
----------

None


REST API
--------

None


Orchestration
=============


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

* We could write a plugin for nailgun instead of extension, but:
  * it would require making this plugin mandatory for every cluster what
    clushes with plugin definition - None of the plugins should be required,
    for basic actions.


--------------
Upgrade impact
--------------

While upgrading Fuel Master node one should spawn bareon-api daemon to make
extension work.


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

`volume_manager` will be replaced with external bareon-api service with
REST API interface. On every node change like create, update etc. there will
be additional request to this service.


-----------------
Deployment impact
-----------------


There should be new nailgun setting `BAREON_ADDRESS` which value will be set
to `127.0.0.1:9322` by default.


----------------
Developer impact
----------------

While working on nailgun one should spawn bareon-api daemon to make
extension work.

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Documentation should have information about new `BAREON_ADDRESS` setting.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  <sbrzeczkowski@mirantis.com>

Other contributors:
  <eli@mirantis.com>

Mandatory design review:
  <eli@mirantis.com>


Work Items
==========

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.

#. Implement `bareon` extension with adapter for bareon-api


Dependencies
============

#. Bareon-api service [#bareon-api]_


------------
Testing, QA
------------

None


Acceptance criteria
===================

* `bareon` extension should completely replace `volume_manager` extension
  in terms of its functionality and it should be unnoticeable for end user


----------
References
----------
.. [#bareon-api] http://example.com/here/should/be/link/to/bareon/bp