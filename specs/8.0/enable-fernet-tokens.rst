..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Fernet keys rotation in HA mode
============================================

https://blueprints.launchpad.net/fuel/+spec/fernet-tokens-support

Implement generation of Keystone fernet keys and their installation during Fuel
deployment in HA-mode, determine a mechanism of fernet keys rotation and
synchronization.

Problem description
===================

Fernet tokens don't support HA mode, realization of this task is entrusted on
devops. Fernet tokens store keys on local file system and can be periodically
rotated by using "keystone-manage" tool. Such approach works only in single
mode (with one controller).
It means that fernet tokens don't have mechanisms that allow to generate,
synchronize keys during deployment process with HA mode and don't have built-in
tools to rotate in HA mode, synchronize fernet keys between all keystone nodes
working in HA mode.
Its critical to have the same keys on all keystone nodes at the same time to
provide proper token validation through all controllers. Changes proposed in
this spec should solve a problem of all nodes with keystone (controllers).

Proposed change
===============

Task of HA mode support for Fernet tokens can be devided into two parts: 

* provide Fernet encryption keys generation/installation during
  deployment process;
* provide automatic scheduled Fernet enctyption keys rotation between
  all keystone nodes;

1. Fernet keys generation/installation during deployment process (HA mode)

As Fernet tokens don't support HA mode installation for keystone we propose to
implement this functionality using puppet manifests of fuel-library. It will
provide a possibility to generate and install fernet keys to all keystone nodes
during deployment process.
To generate keys we should add an aditional function to the script:
"osnailyfacter/modular/astute/generate_keys.sh" , it will use "openssl" tool for
keys generation. 
Generated keys will be stored to /var/lib/fuel/keys/$cluster_id/fernet-keys
directory on Fuel-Master node. To copy generated fernet keys to controller nodes
during deployment process should be used astute. To do it the following file
should be updated:  osnailyfacter/modular/astute/tasks.yaml , source and
destination  paths of keys will be added to "copy_keys" task of "pre deployment"
section. 
After copying fernet keys to all controller nodes , they will be installed to
appropriate directory (/etc/keystone/fernet-keys) using puppet.
To configure fernet tokens and use it by default, 'token_provider' keystone
parameter will be set to 'keystone.token.providers.fernet.Provider' in puppet
manifest, and 'revoke_by_id' parameter will be added and set to 'false'.



2. Fernet keys rotation/synchronization between all keystone nodes

As fernet tokens don't support keys rotation and synchronization between keystone
nodes during operation in HA mode we will use the algorithm that allows to solve
this problem. To realize this algorithm a script running on all keystone nodes
will be used and it will be run by "cron".

Algorithm steps:

* create a new key that planning be a "staged" (or "0") key. It will have the
following name structure: <staged key designation >.<random numeric value>  .
The key will be saved to /etc/keystone/fernet-keys/ directory

* generated in a controller node key will be copied/synced with others controllers of a cluster. For 
these needs "rsync" tool will be used.

* when a keystone node gets all keys (from all keysone nodes) after mutual synchronization locally in  /etc/keystone/fernet-keys/ directory,
it will sort generated key and a key with the largest value will be selected and renamed to "0" key and another keys will be rotated. 





Alternatives
------------

Data model impact
-----------------

REST API impact
---------------

Upgrade impact
--------------

Security impact
---------------

Notifications impact
--------------------

Other end user impact
---------------------

Performance Impact
------------------

Plugin impact
-------------

Other deployer impact
---------------------

Developer impact
----------------

Infrastructure impact
---------------------

Implementation
==============

Assignee(s)
-----------

Work Items
----------

Dependencies
============

Testing
=======

Acceptance criteria
-------------------


Documentation Impact
====================

References
==========

