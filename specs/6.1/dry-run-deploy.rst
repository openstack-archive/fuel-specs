==========================
Dry run deploy
==========================

https://blueprints.launchpad.net/fuel/+spec/fuel-dry-run-deploy

For development and debugging it would be nice if Fuel can perform
all prepared steps for deploy including facts uploading and finish
on this.

Problem description
===================

Deployer typical work flow in case of implementing new feature using CLI:

- provision new cluster;

- download, edit and upload deployment settings;

- go to master node and break manifest;

- do necessary things on nodes;

- run deploy.

Problem is in the step 3rd step:

* not obvious;

* will be difficult in case of granular deployment because it require
  to many changes in different tasks;

* different pre and post deploy hooks can change environment in
  unexpected ways;

* require to many steps in case when deployer needs to perform changes
  on node with multiple roles or with a deployed node;

* block automation for routine tasks.


Proposed change
===============

For nailgun
-----------

* support new api call 'prepare_env' for cluster;

* create new task 'prepare_env' for orchestrator.

For fuelclient
--------------

Create new action for node '--prepare-env' with same syntax as '--deploy'

highlights::

   fuel --env 1 node --prepare-env --node 3,4

For astute
----------

* create new RPC handler 'prepare_env' which will process all tasks
  related to the environment preparation;

* change the facts uploading mechanism: instead of rewriting 'astute.yaml'
  for every node's role we should upload /etc/<role>.yaml and do symbolink
  link from it to /etc/astute.yaml;

* move the facts uploading operation from pre deploy stage to pre
  deployment one.

All actions is known as pre deployment one should executed in case of
'prepare_env' call:

* generate and upload ssh keys;

* update repository sources and package metadata;

* sync time;

* sync puppet manifests;

* sync tasklib tasks;

* enable puppet deploy;

* upload facts.

Alternatives
------------

Leave it as it is.

Data model impact
-----------------

None

REST API impact
---------------

New API call named 'prepare_env' similar to 'deploy'.

.. highlights::

    /clusters/<cluster id>/prepare_env/?nodes={nodes ids}

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  vsharshov@mirantis.com

Work Items
----------

Whole task may be divide into following separate changes:

* new command in Fuel CLI;

* new api call and task in Nailgun;

* new handler in Astute.

Dependencies
============

None

Testing
=======

Main scenario:

* create cluster;

* add nodes with with several role on each one;

* provision nodes;

* change puppet modules;

* call prepare environment API call.

Expecting result:

* nodes should have provisioned state in Nailgun;

* nodes should contain /etc/<role>.yaml for each node role;

* nodes should contain changed modules;

* no OpenStack packages should be installed;

* no puppet or tasklib processes should be running.

Documentation Impact
====================

* Fuelclient;

* Nailgun API.

This interfaces will be changed so it must be
mirrored into corresponding documentation.

References
==========

* initial discussion: https://www.mail-archive.com/fuel-dev%40lists.launchpad.net/msg01515.html;
* initial blueprint: https://blueprints.launchpad.net/fuel/+spec/upload-astute-yaml-only;
* related blueprint: https://blueprints.launchpad.net/fuel/+spec/blank-role-node.

