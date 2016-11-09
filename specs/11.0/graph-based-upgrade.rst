..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Graph Based Upgrades
==========================================

https://blueprints.launchpad.net/fuel/+spec/graph-based-upgrade

This spec aims to improve Octane by making use of Fuel's graph execution engine
to run upgrade-related commands and procedures.

--------------------
Problem description
--------------------

Currently, Octane executes upgrade-related commands on cluster nodes
via SSH. This is not the best way to handle upgrades, given the
capability to execute custom graphs on both new and old environments.
This will allow to enhance upgrade experience in following ways:
- More consistent with Fuel way of logging of upgrade commands
- Utilization of existing graph execution framework for upgrades
- Puppet usage for upgrade tasks (where it is possible to do so)

----------------
Proposed changes
----------------

For each upgrade action, there will be one optional CLI argument:
--with-graph, which will enforce graph-based approach to said
operation.

Graphs and puppet manifests will be stored in the same repository,
in "deployment/" directory (similar to fuel-library).

There will be two types of graphs: "seed" and "orig" for new and old
environments respectively.

Graphs will be uploaded during upgrade action execution.

Graphs will be uploaded to concrete environments (similar to
fuel2 graph upload --env <id> execution)


Web UI
======

None


Nailgun
=======

This change depends on `converted serializers`_ extension.

.. _converted serializers: https://github.com/openstack/fuel-nailgun-extension-converted-serializers


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

None

------------
Alternatives
------------

Stick with current Octane implementation based on existing Python code.

--------------
Upgrade impact
--------------

All the changes will be introduced into fuel-octane repo.
To make use of this feature, the user will have to
run all upgrade actions with "--with-graph" flag.


---------------
Security impact
---------------

Graph-based upgrades require that master node has additional directories
configured for rsync remote access:

- (Read only) /var/www/nailgun/octane_code (contains Puppet-related Octane
  files)
- (Read/write) /var/www/nailgun/octane_data (will hold temporary/backup data
  from other nodes)

Note: due to the nature of upgrade process, the second directory may contain
sensitive data. Contents of this directory are not to be cleaned automatically.
It will be operator's responsibility to remove files with sensitive information
from this directory.

E.g. during upgrade-db step, OpenStack database's contents will be dumped to a
file on the original environment's node, synced to /var/www/nailgun/octane_data
on the master node and then synced to the seed environment's node.



--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

During upgrade process, user will have an option to
execute upgrades with graphs.

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

Documentation will have to be adjusted to mention new
"--with-graph" approach to upgrades.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  rsokolkov

Other contributors:
  nikishov-da
  paulche

Mandatory design review:
  akscram
  vkuklin


Work Items
==========

Implement following commands with graph support:

- upgrade-db
- upgrade-ceph
- upgrade-control
- preugrade-compute
- osd-upgrade


Dependencies
============

None

------------
Testing, QA
------------

Existing test cases will adopt graph-based CLI workflow.

Acceptance criteria
===================

It is possible to successfully execute the upgrade process using task graphs.


----------
References
----------

None
