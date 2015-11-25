..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================
Support for selective TLS for OpenStack endpoints
=================================================

https://blueprints.launchpad.net/fuel/+spec/selective-ssl

Fuel should allow user to deploy OpenStack with TLS for every endpoint, not
only for public one.


--------------------
Problem description
--------------------

Current implementation of TLS support for OpenStack endpoints lacks ability to
enable TLS for internal or admin endpoints and disable or enable TLS per
endpoint.


----------------
Proposed changes
----------------

1. Create additional variables for every TLS endpoint in fuel-library. By
default these variables will be unused (fixtures won't have required data).


Web UI
======

None. UI part will be covered by another blueprint.


Nailgun
=======

There are 2 ways of TLS implementation in nailgun.
1. If we implement UI part in main Fuel UI codebase, we need to pass data
from UI to task which will generate keys. In this case nailgun must be changed
accordingly to have an ability to serialize that data.

2. If we implement UI part in Fuel plugin, we have to implement fetching data
from UI by task itself. It seems more reasonable.


Data model
----------

User can add a hash to override default TLS values. It should looks like:

::

  use_ssl:
    horizon: true
    horizon_public: true
    horizon_public_hostname: horizon.fuel.local
    horizon_public_usercert: true
    horizon_public_certdata: <KeyPairStoredHere>
    keystone: true
    keystone_public: true
    keystone_public_ip: <ip of external keystone>
    ...
    keystone_internal: true
    ...
    keystone_admin: true
    ...
    glance: true
    glance_public: true
    ...



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

New variables that are pulled from Hiera and which allow to override existing
TLS data should be added.


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

Previous releases will be upgraded seamlessly, cause we will introduce new
fields to override old ones.
Downgrade from existing release to previous one will be unavailable.


---------------
Security impact
---------------

All data channels between openstack endpoints will be potentially encrypted. By
default TLS for all OpenStack endpoints will be disabled.


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

User will loose ability to look on data channels between endpoints if they will
be encrypted.


------------------
Performance impact
------------------

Depends on service data rate. For extreme cases performance will be downgraded
by 7-10 times (for example, for big images uploading to Glance).

-----------------
Deployment impact
-----------------

None


----------------
Developer impact
----------------

None


--------------------------------
Infrastructure impact
--------------------------------

N/A

--------------------
Documentation impact
--------------------

Documentation should be changed as well to reflect introduced changes


--------------------
Expected OSCI impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee: Stanislaw Bogatkin

Mandatory design review: Vladimir Kuklin


Work Items
==========

- Create additional code in fuel-library to pull new configuration data from
  Hiera

- Write tests


Dependencies
============

N/A

------------
Testing, QA
------------

In order to verify the quality of new features, automatic system tests have to
be expanded.


Acceptance criteria
===================

- While deploying an environment, administrator can choose which services and
  components use SSL for their endpoints, and on which networks.

- Administrator can perform CRUD operations on SSL certificates used for
  services and components.

- Administrator can identify a unique FQDN for each service endpoint.

- Administrator can associate a unique SSL certificate to each service/FQDN.


----------
References
----------

https://blueprints.launchpad.net/fuel/+spec/selective-ssl
