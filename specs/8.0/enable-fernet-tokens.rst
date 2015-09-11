..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================================
Enabling Fernet tokens by default during Fuel installation
==========================================================

https://blueprints.launchpad.net/fuel/+spec/fernet-tokens-support


Implement Fernet tokens as default authentication method, including initial
generation and propagation of keys to all controllers.


-------------------
Problem description
-------------------

The default Keystone configuration for Fernet tokens does not support multiple
controllers (HA mode). As a result, the current state requires Operators that
are interested in using Fernet tokens to manually generate and sync the Fernet
token key across controllers. Keystone itself does not have any knowledge of
multiple key locations and does not provide any syncing capabilities natively.
However, it is critical to have the keys synced between all Keystone nodes in
order to provide proper token validation.
The goal of this spec is to provide a mechanism by which Fernet token keys can
be easily generated, propagated during initial cluster environmnet setup to
all keystone nodes and enabled by default.

----------------
Proposed changes
----------------

Keystone with Fernet tokens does not natively support multiple controllers
(HA mode), we propose to implement this functionality using astute and puppet
manifests in fuel-library.
This will enable the user to generate and install Fernet keys to all Keystone
nodes seamlessly during the deployment process.
To generate keys, a new 'GenerateFernetKeys’ class will be added to
'pre-deployment actions' of astute. It will use the openssl tool for key
generation. The generated keys will be stored in the following directory on the
Fuel-Master node:

'/var/lib/fuel/keys/“${deployment_id}"/fernet-keys'

To copy the generated Fernet keys to all controllers, a new 'UploadFernetKeys'
class will be added to 'pre-deployment actions' of astute. It will copy Fernet
keys to the following destination:

'/var/lib/astute/fernet-keys'

After copying Fernet keys to all controller nodes, they will be installed to
the appropriate directory using puppets facilities:

'/etc/keystone/fernet-keys'

In order to use configure the Fernet token selection and use Fernet tokens as
the default authentication mechanism, the 'token_provider' Keystone parameter
will be set to 'keystone.token.providers.fernet.Provider' in the associated
puppet manifest.

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

It is not expected that upgrade impact on Fuel Master and new environment
deploying will be significant. But in case when upgrade is performed on
existing environment some keystone service unavailability can be observed until
all controllers are updated.



---------------
Security impact
---------------

It is expected to have the same security level as for ssh keys of mysql,
nova and etc.

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

The fact that Fernet tokens algorithm perform reading off of fernet keys every
time when issuing or validating tokens may be the cause of performance
degradation.

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

Switching to Fernet tokens and manual Fernet keys rotation procedure should be
documented in Fuel Deployment Guide.

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

QA engineers:
  Oleksandr Petrov <apetrov>

Mandatory design review:
  Sergii Golovatiuk <sgolovatiuk>
  Vladimir Kuklin <vkuklin>

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

* Token verification after controller failure
  * issue a token
  * stop a controller this token was issued
  * make sure token works

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
