..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Fernet keys rotation in HA mode
============================================

https://blueprints.launchpad.net/fuel/+spec/fernet-tokens-support

Implement Fernet token activation and generation of Keystone fernet keys
and their installation during Fuel deployment in HA-mode.

Problem description
===================

Fernet tokens don't support HA mode, realization of this task is entrusted on
devops. Fernet tokens don't have mechanisms that allow to generate, synchronize
keys during deployment process with HA mode.
Its critical to have the same keys on all keystone nodes at the same time to
provide proper token validation through all controllers. Changes proposed in
this spec should solve a problem of all nodes with keystone (controllers).

Proposed change
===============

Fernet keys generation/installation during deployment process (HA mode)

As Fernet tokens don't support HA mode installation for keystone we propose to
implement this functionality using puppet manifests of fuel-library. It will
provide a possibility to generate and install fernet keys to all keystone nodes
during deployment process.
To generate keys we should add an aditional function to the script:
'osnailyfacter/modular/astute/generate_keys.sh' , it will use 'openssl' tool for
keys generation.
Generated keys will be stored to /var/lib/fuel/keys/$cluster_id/fernet-keys
directory on Fuel-Master node. To copy generated fernet keys to controller nodes
during deployment process should be used astute. To do it the following file
should be updated:  osnailyfacter/modular/astute/tasks.yaml , source and
destination  paths of keys will be added to 'copy_keys' task of 'pre deployment'
section.
After copying fernet keys to all controller nodes , they will be installed to
appropriate directory (/etc/keystone/fernet-keys) using puppet.
To configure fernet tokens and use it by default, 'token_provider' keystone
parameter will be set to 'keystone.token.providers.fernet.Provider' in puppet
manifest, and 'revoke_by_id' parameter will be added and set to 'false'.

Alternatives
------------

None.

Data model impact
-----------------

None.

REST API impact
---------------

None.

Upgrade impact
--------------

None.

Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

None.

Performance Impact
------------------

None.

Plugin impact
-------------

None.

Other deployer impact
---------------------

None.

Developer impact
----------------

None.

Infrastructure impact
---------------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  myatsenko

Mandatory design reviewers:
  sgolovatiuk
  vkuklin
  iberezovskiy

Work Items
----------

* Implement enabling Fernet tokens, fernet keys generating and copying to all keystone nodes during deploymnet process.
* Scale testing.

Dependencies
============

None.

Testing
=======

Acceptance criteria
-------------------

After successfull deployment all keystone nodes contain fernet keys, Keystone functions properly.

Documentation Impact
====================

Switching to Fernet tokens should be documented.

References
==========

https://blueprints.launchpad.net/fuel/+spec/fernet-tokens-support
