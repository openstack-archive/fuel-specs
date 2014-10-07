==========================
Dry run deploy
==========================

https://blueprints.launchpad.net/fuel/+spec/fuel-dry-run-deploy

For development and debugging propose it would be nice if Fuel can 
perform all prepared steps for deploy including facts uploading and
and finish on this.

Problem description
===================

Deployer typical workflow in case of implementing new feature using CLI:

- provision new cluster;

- download, edit and upload deployment settings;

- go to master node and break manifest;

- do necessary things on nodes;

- run deploy.

Problem is in the step № 3:

* not obvious;

* will not work in case of granular deployment because it will require 
  to many changes;

* diffirents pre and post deploy hooks can change enviroment in 
  unexpected ways;
  
* require to many steps in case when deployer needs to perform changes
  on a multirole node or with a deployed node;
  
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
  related to the enviroment preparation;

* change the facts uploading mechanism: insted of rewriting 'astute.yaml'
  for every node's role we should upload /etc/<role>.yaml and do symbolink
  link from it to /etc/astute.yaml.

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

* call prepare env API call.

Expecting result:

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

