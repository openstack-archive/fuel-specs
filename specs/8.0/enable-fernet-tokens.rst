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


-------------------
Problem description
-------------------

Fernet tokens don't support HA mode, realization of this task is entrusted on
devops. Fernet tokens don't have mechanisms that allow to generate, synchronize
keys during deployment process with HA mode.
Its critical to have the same keys on all keystone nodes at the same time to
provide proper token validation through all controllers. Changes proposed in
this spec should solve a problem of all nodes with keystone (controllers).


----------------
Proposed changes
----------------

Fernet keys generation/installation during deployment process (HA mode)

As Fernet tokens don't support HA mode installation for keystone we propose to
implement this functionality using puppet manifests of fuel-library. It will
provide a possibility to generate and install fernet keys to all keystone nodes
during deployment process.
To generate keys we should add an aditional function to the script:
'osnailyfacter/modular/astute/generate_keys.sh', it will use 'openssl' tool for
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

Web UI
======

None

Nailgun
=======

None

Data model
----------

None

REST API
--------

No FUEL REST API changes.

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

The following option should be passed to ::keystone class in order to
enable Fernet tokens:
* token_provider =  keystone.token.providers.fernet.Provider

remove token revocation:

* revoke_by_id = False

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

None

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

None

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

None

--------------------------------
Infrastructure/operations impact
--------------------------------

None

--------------------
Documentation impact
--------------------

Switching to Fernet tokens should be documented in Fuel Deployment Guide.

--------------------
Expected OSCI impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
	  Maksym Yatsenko <myatsenko>

Mandatory design review:
	  Sergii Golovatiuk <sgolovatiuk> Vladimir Kuklin <vkuklin>

Work Items
==========

* Implement enabling Fernet tokens, fernet keys generating and copying to all
  keystone nodes during deploymnet process
* Scale testing

Dependencies
============

None

------------
Testing, QA
------------

Manual Acceptance Tests
=======================

* Deploy HA-mode configuration
* All keystone nodes should contain identical fernet keys

HA/Destructive Tests
====================

None

Scale
=====

Environment with L3 HA enabled should pass all tests currently run on Scale Lab
with no significant performance degradation.

Acceptance criteria
===================

After successfull deployment all keystone nodes contain identical fernet keys,
Keystone functions properly.

----------
References
----------

`Blueprint <https://blueprints.launchpad.net/fuel/+spec/fernet-tokens-support>`_
