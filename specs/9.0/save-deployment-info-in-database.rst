..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================================
Save Information about The Deployment in The Database
=====================================================

https://blueprints.launchpad.net/fuel/+spec/save-deployment-info-in-database

As a deployment engineer I would like to be able to leverage deployment
configuration history for my cluster as a base for decision making.

For example, I need to have an opportunity about
what actually change in the cluster since previous (or even earlier) times.

This information is sometimes crucial. E.g. I want to have an ability to
inject tasks into deployment graph based on what actually changed in
graph configuration.

As an example, when I change mysql configuration
(something like max_connections), I need to perform mysql restart one by one
as opposed to parallel installation in order to maintain the cluster operating.
This cannot be done without actual knowledge of what are the new nodes and
what are the old nodes in the cluster or whether this deployment is a new
one or is a redeployment of previously deployed cluster.

This info may also be required for changes such as backend switching for
glance/keystone or may be needed for plugins to alter their behaviour
depending on cluster metadata change.

--------------------
Problem description
--------------------

Currently, such a history does not exist which makes satisfaction of
aforementioned use cases impossible. It should not be a rocket science
to store cluster configuration in the database before sending it to the
nodes being deployed.


----------------
Proposed changes
----------------

Additional fields for 'tasks' model should be added to store serialized data,
unserialized settings and unserialized network configuration associated with
particular Nailgun task.

Web UI
======

None

Nailgun
=======

None

Data model
----------

Add 3 new fields with deployment data into 'tasks' table with type 'JSON'

REST API
--------

There will be a REST API handler allowing to get serialized data,
unserialized settings and unserialized network configuration for specified
Nailgun task

+--------+---------------------------------+-------------------+-------------+
| method | URL                             | action            | auth exempt |
+========+=================================+===================+=============+
|  GET   | /api/transactions/              | get serialized    | false       |
|        | :transaction_id/                | data for a nailgun|             |
|        | deployment_info                 | task              |             |
+--------+---------------------------------+-------------------+-------------+
|  GET   | /api/transactions/              | get settings      | false       |
|        | :transaction_id/                | for a nailgun task|             |
|        | settings                        |                   |             |
+--------+---------------------------------+-------------------+-------------+
|  GET   | /api/transactions/              | get network       | false       |
|        | :transaction_id/                | configuration     |             |
|        | network_configuration           | for a nailgun task|             |
+--------+---------------------------------+-------------------+-------------+

The methods should return the following statuses in case of errors:

* 404 Not found - in case of missing entry
* 405 Not Allowed - for `PUT /api/transactions/:transactions_id/
  deployment_data`, `PUT /api/transactions/:transactions_id/settings`, `PUT
  /api/transactions/:transactions_id/network_configuration`

GET method returns JSON

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

Fuel Client have to show stored information for particular Nailgun task.
New command should be added:

.. code-block:: console

  fuel2 task 1 deployment-info show
  fuel2 task 1 settings show
  fuel2 task 1 network-configuration show

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

Wait for ConfigDB full implementation or Solar integration, which will happen
only with N release

--------------
Upgrade impact
--------------

Should be disabled for pre-9.0 clusters

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

User will be able to get history of all the changes and conduct better
troubleshooting

------------------
Performance impact
------------------

Non-significant overhead for Postgres DB layer

-----------------
Deployment impact
-----------------

Flexible deployment workflow generation and LCM support

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

Only feature-related documentation

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  bgaifullin

Other contributors:
  ikutukov
  vsharshov
  ashtokolov

Mandatory design review:
  ikalnitsky


Work Items
==========

See Proposed Changes section

Dependencies
============

------------
Testing, QA
------------

Simple functional testing for deployment info history storage

Acceptance criteria
===================

Ability to fetch deployment info data for any particular nailgun task being
run

----------
References
----------

