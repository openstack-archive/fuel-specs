..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Fernet keys rotation in HA mode
============================================

https://blueprints.launchpad.net/fuel/+spec/fernet-tokens-support

Implement generation and copying(installing) fernet keys during openstack
deployment process (HA-mode), determine a mechanism of fernet keys rotation
and synchronization.

Problem description
===================

Fernet tokens don't support HA mode, realization of this task was entrusted on devops.
Fernet tokens store keys on local file system and can be periodically rotated by using
"keystone-manage" tool. Such approach works only in single controller mode.
 
It means that fernet tokens don't have mechanisms that allow to generate, synchronize keys
during deployment process with HA mode and don't have built-in tools to rotate,
synchronize fernet keys between all keystone nodes working in HA mode.

Its critical to have the same keys on all keystone nodes at the same time to provide proper
token validation through all controllers. Changes proposed in this spec should solve a problem
with supporting HA mode for fernet tokens.

Proposed change
===============

Task of HA mode support for Fernet tokens can be devided into two parts: 

* provide Fernet encryption keys generation/installation during deployment process;
* provide automatic scheduled Fernet enctyption keys rotation between all keystone nodes;

1. Fernet keys generation/installation during deployment process (HA mode)

As Fernet tokens don't support HA mode installation for keystone we propose to implement this
functionality using puppet manifests of fuel-library. 
It will provide a possibility to generate and install fernet keys to all keystone nodes
during deployment process.

To generate keys we should add an aditional function to  "osnailyfacter/modular/astute/generate_keys.sh"
script, it will use "openssl" tool for keys generation. Function realization example:

.. code-block:: function generate_fernet_keys {
                  for i in $fernet_keys
                    do
                      local dir_path=${BASE_PATH}fernet-keys/
                      local key_path=$dir_path$i
                      mkdir -p $dir_path
                      if [ ! -f $key_path ]; then
                      openssl rand -base64 32 -out $key_path 2>&1
                      else
                      echo "Key $key_path already exists"
                      fi
                    done
                }

Generated keys will be stored to /var/lib/fuel/keys/$cluster_id/fernet-keys directory on Fuel-Master node.
To copy generated fernet keys to controller nodes during deployment process should be used astute. To do it
osnailyfacter/modular/astute/tasks.yaml file will be updated, source and destination paths of keys will be
added to "copy_keys" task of "pre deployment" section, example:

.. code-block:: src: /var/lib/fuel/keys/{CLUSTER_ID}/fernet-keys/0
                dst: /var/lib/astute/keystone/0

After copying fernet keys to all controller nodes , they will be installed to appropriate directory
(/etc/keystone/fernet-keys) using puppet, example of realization:

.. code-block:: if $token_provider == 'keystone.token.providers.fernet.Provider' {
                  file { "$fernet_key_repository":
                    source  => $fernet_src_repository,
                    mode    => '0600',
                    owner   => 'keystone',
                    group   => 'keystone',
                    recurse => true,
                    require => Class['::keystone'],
                    notify  => Service['keystone'],
                   }
                 }

To configure fernet tokens and use it by default, 'token_provider' keystone parameter will be set
to 'keystone.token.providers.fernet.Provider' in puppet manifest, and 'revoke_by_id' parameter will
be added and set to 'false'. 



2. Fernet keys rotation/synchronization between all keystone nodes

As fernet tokens don't support keys rotation and synchronization between keystone nodes during operation
in HA mode we will use the algorithm that allows to solve this problem. To realize this algorithm a script
running on all keystone nodes will be used and it will be run by "cron".

Algorithm steps:


* create a new key that planning be a "staged" (or "0") key. It will have the following name structure:
<staged key designation >.<random numeric value>.
    Example:
    0.3781143626814230

The key will be saved to /etc/keystone/fernet-keys/ directory and we will have the following list of keys in 
this directory, example:

    0.3781143626814230
    0
    1

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

