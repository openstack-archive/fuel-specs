..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Integration of Aodh alarming service with Fuel
==============================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/fuel-aodh-integration

Fuel has to deploy Aodh alarming in the environments with Ceilometer.


-------------------
Problem description
-------------------

Aodh is the alarm engine of the Ceilometer project. This project has been
founded based on the alarming services code of Ceilometer since Liberty.
All alarm relative code has been deleted from the Ceilometer project in Mitaka.
So, for the alarm supporting Aodh has to be deployed by Fuel. [1]_

----------------
Proposed changes
----------------

Aodh provides alarm functional on the Ceilometer database.
The main idea of this proposal is deploy Aodh as a separate project
with Ceilometer.

Aodh has 4 services which should be started:

* aodh-api
* aodh-evaluator
* aodh-listener
* aodh-notifier

Service `aodh-api` provides an access to alarms for the user.
This service runs under HAProxy with mod_wsgi or eventlet.
Endpoint for this service should be registered in keystone service catalog,
because Ceilometer API uses this endpoint for proxying alarm related requests
from Ceilometer client. It means that it's better to install and run `aodh-api`
before running `ceilometer-api` service.
Service 'aodh-api' uses a Keystone for the authenticating requests.
API described in [2]_.

Service `aodh-evaluator` evaluates alarms on a periodic basis.
The default interval is 1 minute. This service runs as current
`ceilometer-alarm-evaluator` service under the pacemaker with one active and
other passive services. It caused by fact what coordination needed for the
several instances of `aodh-evaluator`.

Service `aodh-listener` provides evaluating for the event alarms.
It listens to the queue and evaluates alarms if event for this alarm
is received. This service doesn't need a coordination and can be started
on every controller as service with respawn.
This service uses an oslo.messaging listeners for the receiving messages from
the queue.

Service `aodh-notifier` effects notification actions that is described in
alarm for the state transition of individual alarm
(to ok, alarm, insufficient data).
This service doesn't need a coordination and
can be started on every controller as service with respawn.
This service need a connection to the AMQP.

The default database for aodh is MySQL and connection url should be defined
in configuration file. Binary `aodh-dbsync` running is required
before the first Aodh services starting.

All alarms should be moved from the Ceilometer database to the Aodh db.
According to the fact of default Ceilometer db is MongoDB and default
Aodh db is MySQL we should have a migration code between these databases.
This code will be implemented on Ceilometer side and should be run during
the deploying. Now it's in progress in upstream part of Aodh.

Fuel modular manifests for described services deployment should be created.


Web UI
======

We need to make two minor modifications in the cluster creation wizard and
on the `Settings` -> `OpenStack` services tab. On the both we should tell
that Ceilometer and Aodh will be installed.
In other respects it will be same as current Ceilometer installation.

Nailgun
=======

It supports current business logic and don't need any changes.

Data model
----------

No changes in the data Nailgun data model.


REST API
--------

No changes in Nailgun API.

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

No changes in the Fuel client.

Plugins
=======

None

Fuel Library
============

Puppet manifests will perform next actions before Ceilometer deploying:

 * install Aodh packages
 * configure Aodh
 * sync database
 * configure Keystone endpoint for the `aodh-api`
 * run `aodh-evaluator` under `pacemaker`
 * start other Aodh services

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

There is no impact of master node upgrade.
Upgrading Ceilometer to MOS 9.0 will include an alarm migration
from the MongoDB Ceilometer db to MySQL Aodh database.

Script for this action will be delivered in upstream Aodh.

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

API for the end users will be the same as current Ceilometer API.
All alarm request will be redirected automatically to the Aodh API.


------------------
Performance impact
------------------

Aodh performance is the same as current performance level of
Ceilometer alarm services.

-----------------
Deployment impact
-----------------

Everything was already mentioned.

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

New services have a documentation space in Openstack wiki. [3]_
So, note about fact of Aodh installation should be added in Fuel docs
associated with Ceilometer installations.

--------------------
Expected OSCI impact
--------------------

Packages for the AODH services and code should be prepared:
* aodh-api
* aodh-common
* aodh-doc
* aodh-evaluator
* aodh-expirer
* aodh-listener
* aodh-notifier
* python-aodh

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Dmitry Burmistrov

Other contributors:
  * Ivan Berezovsky
  * Ilya Tyaptin

QA engineer:
  Artem Minasyan

Mandatory design review:
  * Ivan Berezovsky
  * Nadya Shakhat


Work Items
==========

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Work Items
==========

* Prepare Aodh packages
* Implement fuel modular manifests to deploy the Aodh services
* Implement migration script for migrating alarms from Ceilometer to Aodh storage.

Dependencies
============

No additional dependencies

-----------
Testing, QA
-----------

* Create OSTF tests for event alarms
* Create system tests for event alarms
* Create Tempest tests for event alarms

Acceptance criteria
===================

* Aodh is deployed to the environment with Ceilometer installation successfully
* It is possible to migrate alarm data from Ceilometer to Aodh DB
* Old and new OSTF tests pass
* System tests pass
* Tempest and acceptance tests passed
* New test scenarios and their results are documented

----------
References
----------

.. [1] https://blueprints.launchpad.net/ceilometer/+spec/split-ceilometer-alarming
.. [2] http://docs.openstack.org/developer/aodh/webapi/v2.html#alarms-api
.. [3] https://wiki.openstack.org/wiki/Telemetry#Aodh
.. [4] https://github.com/openstack/aodh