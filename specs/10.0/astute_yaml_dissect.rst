..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Puppet noop run for Fuel puppet deployment tasks
================================================

https://blueprints.launchpad.net/fuel/+spec/astute-yaml-dissect


--------------------
Problem description
--------------------

Today we have an astute.yaml as a source of truth when gathering data for
puppet modules. This file has a complex structure, some sections of it can
be met several times. It contains all the data about current cluster and as a
result it leads to following problems:

  * This file generates from DB objects, so when there are many nodes in a
    cluster, it takes too much time to serialize all these entities to a file
  * Astute.yaml has complex structure with too loose logic which leads to badly
    written YAQL queries based on it
  * Some data in this file meets twice or more frequently, which breaks DRY
    principle


----------------
Proposed changes
----------------

Data which serialized from DB should be restructured to better fit current
demands. There are thoughts which we should be guided by for this
restructurization:

  * Common data for all nodes should be splittedi from other data and serialized
    only once. It gives us acceleration when serialize initial data from DB
  * All the data met twice or more in serialized objects must be united to one
  * Sensitive data should be exported to special section to have an opportunity
    to cut it out from diagnostic snapshots
  * Similar data sections should be aggregated to bigget sections

The implementation of this approach requires changes in the Fuel:

  * Puppet manifests should be changed accordingly to changed sections

  * Deployment tasks: should be adapted to new serialized data objects

  * Nailgun: serialization should be changed from one big monilith call to
    separate calls for different sections

  * Diagnostic snapshot gathering tool (timmy): should get an ability to cut
    out sensitive data from diagnostic snapshot by passing special flag for it


Web UI
======

None


Nailgun
=======

* Nailgun should serialize common data only once for cluster and do it
  separately from other serialization tasks


Data model
----------

None


REST API
--------

None


Orchestration
=============

None


Fuel Client
===========

None


Plugins
=======

Plugins for new releases should be rewritten according to the new astute.yaml
structure. Support of old astute.yaml structure will be dropped according to
global Fuel features deprecation policy.


Fuel Library
============

Puppet manifests uses hiera should be rewritten to use new data structure. The
same should be done with noop tests.


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

None


---------------
Security impact
---------------

Sensitive data won't be stored in diagnostic snapshot anymore. It will allow us
to have snapshots from customers tracked by default communication channels,
like Launchpad instead of using non-standard storage places.


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

Performance for big clusters will be significantly improved (speed factor is
clearly depends on cluster size as common data grown based on nodes count).

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

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Stanislaw Bogatkin <sbogatkin@mirantis.com>

Other contributors:
  Bulat Gaifullin <bgaifullin@mirantis.com>

Mandatory design review:
  Vladimir Kuklin <vkuklin@mirantis.com>

QA engineer:
  Alexander Kurenyshev <akurenyshev@mirantis.com>


Work Items
==========

* Change Nailgun to serialize data according to new structure

* Create deployment tasks to copy data to target nodes

* Change fuel-library hiera hierarchy to consume new data

* Change fuel-library puppet modules accordinglyhierarchy to consume new data

* Change fuel-library puppet modules accordingly

* Change fuel-noop-fixtures to reflect new data structure

* Change Timmy to have an ability to cut out sensitive data from diagnostic
  snapshot


Dependencies
============

None

------------
Testing, QA
------------

* Nailgun's unit and integration tests will be extended to test new feature.

* Fuel-library noop tests will be changed accordingly

* Fuel Client's unit and integration tests will be extended to test new feature.

* Timmy test will be extended to test new feature

Acceptance criteria
===================

* Deploy should be successfully ran without old astute.yaml file

* Fuel-library tests should be passed with new data structure

* Diagnostic snapshots shouldn't have sensitive data anymore

----------
References
----------

1. LP Blueprint https://blueprints.launchpad.net/fuel/+spec/astute-yaml-dissect
