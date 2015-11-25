..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Support for multi-rack deployment with static routes
====================================================

https://blueprints.launchpad.net/fuel/+spec/selective-ssl

Fuel should allow to user deploy OpenStack with TLS for every endpoint, not
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
default these variables will be unused (fixtures won't have according data).

2. Create appropriate code to generate keys and copying them to nodes. Create
new tasks to update DNS.

3. Create UI to give user ability to use those data we created in article 1.


Web UI
======

UI needs to be changed accordingly to proposed changes:
1. Have fields for enable/disable TLS for every service.

2. Have fields for enable/disable TLS for every service endpoint.

3. Have fields for user certificates

4. Have fields for DNS hostnames


Nailgun
=======

There are 2 ways of TLS implementation in nailgun.
1. If we will implement UI part in main Fuel UI codebase, we need to pass data
from UI to task which will generate keys. In this case nailgun must be changed
accordingly to have an ability to serialize that data.

2. If we will implement UI part in Fuel plugin, we have to implement fetch data
from UI by task itself. It seems more reasonable.


Data model
----------

New editable attributes will be added to be shown on Settings tab.


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

New fields which allow to override existing TLS data should be added.


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

Depend on service data rate. For extreme cases performance will downgrade by
7-10 times.

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

Documentation should be change to reflect introcuced changes


--------------------
Expected OSCI impact
--------------------

OSCI code should be TLS-aware to have ability for run tests.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee: Stanislaw Bogatkin

Mandatory design review: Vladimir Kuklin


Work Items
==========

- Create additional code in fuel-library to reflect new fields from fixtures

- Create UI part

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

- Administrator can identify a unique FQDN for each service.

- Administrator can associate a unique SSL certificate to each service/FQDN.


----------
References
----------

https://blueprints.launchpad.net/fuel/+spec/selective-ssl
