..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================================
Enabling Fernet keys by default during Fuel installation
========================================================

https://blueprints.launchpad.net/fuel/+spec/fernet-tokens-support


Implement Fernet token activation along with generation and installation
of Keystone Fernet keys during Fuel deployment in HA-mode.


-------------------
Problem description
-------------------

Keystone set up to use Fernet token format do not support HA mode, realization
of this task is entrusted on devops. Keystone service itself has no means to
inter-operate in HA mode. But it is critical to have the same keys on all
keystone nodes at the same time to provide proper token validation through all
keystone nodes (controllers). Changes proposed in this spec should solve a
problem of all nodes with keystone (controllers).

----------------
Proposed changes
----------------

Fernet keys generation/installation during deployment process (HA mode)

As Keystone setup with Fernet tokens do not support HA mode installation  we
propose to implement this functionality using puppet manifests of fuel-library.
It will provide a possibility to generate and install fernet keys to all
keystone nodes during deployment process.
To generate keys we should add an additional function to the script:
'osnailyfacter/modular/astute/generate_keys.sh'.
It will use 'openssl' tool for keys generation. Generated keys will be stored
to the following directory on Fuel-Master node:
'/var/lib/fuel/keys/$cluster_id/fernet-keys'.
Astute should be used to copy generated Fernet keys to controller nodes during
deployment process. To do it the following file should be updated:
'osnailyfacter/modular/astute/tasks.yaml'.
Source and destination paths of keys will be added to 'copy_keys' task of
'pre deployment' section.
After copying fernet keys to all controller nodes , they will be installed to
appropriate directory (/etc/keystone/fernet-keys) using puppet.
To configure fernet tokens and use it by default, 'token_provider' keystone
parameter will be set to 'keystone.token.providers.fernet.Provider' in puppet
manifest. And 'revoke_by_id' parameter will be set to 'false' as it is not
needed with Fernet and generates considerable overhead.

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

---------------------
Infrastructure impact
---------------------

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
