==========================================
Enforce access control for Fuel UI
==========================================

https://blueprints.launchpad.net/fuel/+spec/access-control-master-node

Currently, there is no enforced access control to the Fuel UI.

Problem description
===================

Anyone with access to network can create, change and delete environment.

At a minimum, this requirement could be fulfilled by a login/password when
connecting to the Fuel UI.  If implemented in this manner,
additional requirements will be needed:

 * Ability for a user to set / change their own password

  * Default admin/admin
  * Should be configurable in fuelmenu

More advanced options:

 * Secure/Encrypted storage of passwords (potentially on the Fuel Master Node)

  * A more advanced feature would be integration with an external
    authentication source (e.g. Active Directory, LDAP)

 * A "super user" account that can create additional accounts - but these
   additional accounts cannot create more users
 * A better implementation would be to have Role Based Access Control and
   have "super user" as a role that can be assigned to one or more users

  * This may lead, in the future, to a more granular RBAC - e.g. ability
    to view but not take actions, restriction to specific environments, etc.

 * Ability for a "super user" to change a user's password and/or disable/remove
   an account

 * Read only mode

Proposed change
===============

Use Keystone as authorization tool.

Advantages:

 * it can be used with LDAP or AD
 * supports authorization via tokens
 * support scopes, and groups of users
 * has good written api with many functions like geting accessible
   endpoints for user
 * has api easy for consumption
 * has implemented events system that we can use in future
   for additional monitoring
 * has implemented multifactor authentication
   (can be used with external systems)
 * all apis that we need for future managing groups, roles,
   users and project are created
 * for UI we can base our solution on horizon solution
 * keystone will be also used by Ironic project

Disadvantages:

 * need to run in separate container/process
 * next external dependency
 * may be overkill

We tested keystone with postgresql, it's working.
We tested it via console: create (user, role, tenant, endpoint) add role,
get token, list(role, user, tenant)
and also we used api to: get user info, get token, operations via v3 api

Blueprint will be implemented in several stages:
------------------------------------------------

Stage I
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Keystone installation

 * install in nailgun container
 * run script for creating separate db in postgresql container
 * make available ports for keystone
 * create base configuration
 * in nginx allow connection to keystone

2. GUI

 * login page
 * logout button

3. After installation set password via fuelmenu
   (it will be stored in astute.yaml)

Stage II(API protection)
^^^^^^^^^^^^^^^^^^^^^^^^^

1. Keystone

 * create new container for keystone
 * create service user for OSTF
 * create backup script for db

2. Nailgun

 * Try to use `keystone middleware <https://github.com/openstack/python-keystoneclient/tree/master/keystoneclient/middleware>`_,
   for api and api v1
 * for node agent we should run separate webpy app without middleware

3. GUI

 * Add authorization credentials to all requests

   * use keystone token in auth header
   * add handling of 401

4. Change OSTF and Fuel-client and Fuel CLI to use authorization
5. Make authorization optional(flag to enable/disable authorization)

Stage III(all public services protection)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Change password (only for admin user) for cobbler and RabbitMQ

 * extend basic keystone plugin for changing password

2. Node agent authorization

3.GUI

 * change password page

4. Add read only mode.

Stage IV(in unknown future)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Many users, groups/roles and api access based on groups/roles
   (ie. read-only, network-admin)
2. External authentication (LDAP, AD)

Alternatives
------------

**Write everything by yourself or use some existing components:**

we need to write user model and apis for creating and managing: user,
groups etc
oauth, in this case we can reuse some existing libs like oauth2 for creating
and consuming tokens. Oauth will be easy to use with clients and node
authorization
Maybe we can also use sessions for UI to persistence user token

Advantages:

 * full control
 * possibilities to write good oauth2 authorization easy to use
   also with nodes

Disadvantages:

* a lot of work on stuff that is already implemented in keystone

**Use basic auth in nginx**

Advantages:

* really simple to implement, requires only changes in nginx configuration

Disadvantages:

* It shows login page from browser.
  On every browser it will look little different.
* We can not create custom login page.
* It is still required to implement handlers and tab for password change.
* It's not extensible. If we want to implement non minimal
  requirements we need to start from begining.

Data model impact
-----------------

New database for keystone is required

REST API impact
---------------

Keystone API will be used

Security impact
---------------

Fuel will be safer now. It will protect users against unauthorized access.
All actions will require authorization.


Notifications impact
--------------------

Keystone can log all requests to log file.

Other end user impact
---------------------

* before performing any actions user have to login.
* python-fuelclient should be adjusted to use authorization
* fuel cli should be adjusted to use authorization
  Password file for fuel-cli? (like .openrc but .fuelrc)

Performance Impact
------------------

None

Other deployer impact
---------------------

Password for postgresql should be generated and access from remote
locations should be blocked.

External connections to cobbler and rabbitmq should be allowed.
But passwords should be changed to the same as for API even
in first version, if possible. In future versions we'll be able
to transfer options for bootstrap node. So we should generate bootstrap
ssh key during master node installation. And use password-protected API
for nailgun agents


Developer impact
----------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  loles@mirantis.com ksambor@mirantis.com


Work Items
----------



Dependencies
============

None

Testing
=======

Unit tests and functional tests are required

Documentation Impact
====================

It should be described how to change password and where it's required.

References
==========

None
