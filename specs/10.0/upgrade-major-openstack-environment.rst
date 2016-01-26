..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Upgrade cluster metadata to 9.0
===============================

https://blueprints.launchpad.net/fuel/+spec/upgrade-major-openstack-environment

Current approach to upgrading of OpenStack environment metadata in Fuel
involves creating another instance of environment ('replacement' or 'upgrade
seed'). This replacement environment has its metadata generated with
metadata of the new release.

Creation of second environment to upgrade an existing one is counterintuitive,
unpractical and creates unnecessary complexity. It also requires to duplicate
information which is normally relates to single environment (IP addresses and
ranges, etc).

This proposal enables a single environment approach to the upgrade process
by introducing versioned cluster attributes, node attributes and methods
to create new versions of therefore as a precursor for the upgrade operation.

--------------------
Problem description
--------------------

Current upgrade solution creates a new version of cluster settings by cloning
the existing cluster's attributes. Then we need to manipulate 2 clusters:
change cluster assignment of nodes and migrate the data between clusters
(e.g. state DB contents or configuration data for Ceph).

This breaks data model of Nailgun, reduces velocity of development and
reliability of the upgrade. This solution also creates duplication of code:
DB migrations and Nailgun clone API from Cluster Upgrade extension implement
similar function in two parts of the code.

The problem of metadata update partially covered by DB migrations included
with the source code of Nailgun. However, migrations only affect structured
metadata. They adjust the schema of DB to the changes introduced for the
new release. We also need to handle changes in unstructured data defined
in the new release.

----------------
Proposed changes
----------------

We need to introduce proper support for upgrade of metadata between releases,
including unstructured data stored as BLOBs/JSONs in certain fields in tables
of Nailgun database.

* Alembic migration scripts shall update database schema to the new version.

* Nailgun migration functions must be realized to update the unstructured
  data.

* Special system tests shall be integrated into test system to ensure that
  no changes are introduced in ``openstack.yaml`` fixture without matching
  functions in Nailgun migrations.

Web UI
======

No changes to Web UI introduced in this proposal.

Nailgun
=======

Data model
----------

There is no changes to data model on this stage. In future, Nailgun should
be developed in a fashion that reduces the use of non-structured data in
favor of structured data.

REST API
--------

No changes to REST API introduced in this proposal.

Orchestration
=============

No changes to orchestration.

RPC Protocol
------------

None.

Fuel Client
===========

None.

Plugins
=======

Plugins metadata are stored in separated database structure and can be
upgraded using the same methods as the core metadata.

However, the code that updates the non-structured data for certain plugin
must be provided by the plugin itself.

Fuel Library
============

None.

------------
Alternatives
------------

An alternative approach was implemented in Cluster Upgrade extension in
Nailgun API. It creates a clone of original environment with the same
settings. This approach breaks certain natural constraints in Nailgun
data model. For example, it requires creation of network groups with
with duplicated parameters.

--------------
Upgrade impact
--------------

This change facilitates the upgrade of OpenStack environment by changing
its metadata to values and semantics of the new release version.

Database migration scripts must be applied to Nailgun database upon upgrade
of the Fuel Admin node.

---------------
Security impact
---------------

This change does not introduce new security risks.

--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

None.

------------------
Performance impact
------------------

None.

-----------------
Deployment impact
-----------------

None.

----------------
Developer impact
----------------

This change introduces tests that strictly prohibit changes to database
schema and metadata formats in Nailgun (i.e. in ``openstack.yaml`` and
other fixtures) without corresponding functions for automated update of
the metadata. Developers have to provide these upgrade functions.

---------------------
Infrastructure impact
---------------------

This change introduces new type of checks that might be included in CI
as a separate job. The new check must be used in gating and, if possible,
in verification of changes.

--------------------
Documentation impact
--------------------

None.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  sabramov (Sergey Abramov)

Other contributors:
  gelbuhos (Oleg Gelbukh)
  akscram (Ilya Kharin)

Mandatory design review:
  ikalnitskiy (Igor Kalnitskiy)


Work Items
==========

* Develop test to verify the data model and fixtures consistency for every
  CR to Nailgun code base.

* Implement functions to upgrade non-structured data between releases 8.0
  and 9.0.

Dependencies
============

None.

------------
Testing, QA
------------

Proposed test should keep track of changes in fixtures, including
``openstack.yaml``, and verify that module ``utils/migrations.py`` can
transform data for the old version to the new one.

Acceptance criteria
===================

* DB migration scripts allow to update the schema of ``clusters`` table
  and other connected tables in Nailgun database from version 8.0 to
  version 9.0.

* Data migration scripts allow to update non-structured metadata for the
  cluster and related entities, stored in fields of table ``clusters``
  and others, from version 8.0 to 9.0.

* System test added that fails if changes to fixture format are not
  accompanied by metadata update functions in ``utils/migrations.py`` module.

----------
References
----------

