..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Bareon-API integration with Nailgun
===================================

https://blueprints.launchpad.net/fuel/+spec/fuel-bareon-api-integration

In order to externalize nodes volumes management, Nailgun needs some
integration with Bareon-API service. The change is a part of Fuel
modularization plan.


--------------------
Problem description
--------------------

Currently the Volume Manager is a part of Nailgun. All volumes computations
and disks management are being processed there. The problem VM resolves
is generic and reaches broader areas than just fuel. So it's worth to
externalize it which is now happening in Bareon project [#bareon-api]_.

Nailgun needs some integration with new tool to use its resources.
It also needs to be replaceable by other tools with such functionality.


----------------
Proposed changes
----------------

Nailgun extensions engine has capability to receive specific events like node
create, update, delete etc. Proposed change considers creating an adapter
for Bareon-API, which will update the service about node volumes changes in
cases like assigning new role for node or destroying an environment, so
it should be implemented as an extension.

Implementation of extensions engine should be changed. There
should be more methods i.e. `process_deployment_data` and
`process_provisioning_data` which could be overwritten by any extension.
It will make Nailgun more extensible.

Current `volume_manager` extension must be completely replaceable by
`bareon` extension which will have the following capabilities:

* `process_provisioning_data` - for fetching Bareon (old Fuel-agent) ready
  serialized provisioning data for a single node from Bareon-API.

* `on_node_create` - if the node does not have role assigned, extension will
  create the node with no default schema, otherwise the schema will
  be provided.

* `on_node_update` - update default volume schema for the node and available
  disks.

* `on_node_delete` - delete node representation and all related data
  from Bareon-API.

* `on_node_reset` - delete node representation and all related data
  from Bareon-API.

* `on_node_collection_delete` - delete all nodes representation in collection
  and all related data from Bareon-API.

* there will be no additional database models defined since they're not
  needed. All volumes data will be stored in Bareon-API.

* there will be no additional API handlers defined since they're not needed.
  Bareon-API will have it's own REST API interface so end User could edit
  volumes directly using python-bareonclient.


Web UI
======

UI will have to support new API for clusters which has `bareon` extension
enabled.


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

Remove hardcoded definition of task from Astute so it can be passed
from Nailgun. Extension should be able to replace this task with another one
which runs `bareon-provision --data-driver=nailgun_simple ...` instead of
fuel_agent's `provision ...`. Nailgun simple driver is prepared to receive
data which will be used as actual partitioning schema


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

* The implementation may be done in Nailgun directly but it clashes with the
  modularization plan.
* Leave all related logic in extension (not in separate service), but in this
  case we will not be able to use it separately so it also clashes with the
  modularization plan.


--------------
Upgrade impact
--------------

For old versions of Clusters old "volume_manager" extension will be used.
During upgrade Bareon-API service has to be installed and configured.


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

Huge performance impact is not expected, bunch of operations on Bareon-API
side has to be implemented.


-----------------
Deployment impact
-----------------


There should be new Nailgun setting `BAREON_ADDRESS` which value will be set
to `127.0.0.1:9322` by default.


----------------
Developer impact
----------------

While working on Nailgun one should spawn Bareon-API daemon to make
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

Primary assignee: Sylwester Brzeczkowski <sbrzeczkowski@mirantis.com>

Other contributors:

  * Evgeny Li <eli@mirantis.com>

Mandatory design review:

  * Evgeny Li <eli@mirantis.com>


Work Items
==========

* Make extension to be able to change provisioning/deployment info, which is
  sent to Astute (required to provide partitioning schema in separate field
  for SimpleDriver).
* Add `process_deployment_data` and `process_provisioning_data` methods
  to BaseExtension
* Fix discovery mechanism, so extension can be installed as separate package.


Dependencies
============

* Bareon-API service [#bareon-api]_


------------
Testing, QA
------------

None


Acceptance criteria
===================

* `volume_manager` extension should completely replaceable by `bareon`
  extension in terms of its functionality and should be unnoticeable
  for end user.


----------
References
----------
.. [#bareon-api] http://example.com/here/should/be/link/to/bareon/bp