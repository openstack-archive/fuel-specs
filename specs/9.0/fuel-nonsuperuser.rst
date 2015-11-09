..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Running Fuel as non-superuser
==========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-nonsuperuser

It should be possible to run the Fuel master node and the slave nodes as a non-superuser (non-root).
Currently, users are required to log into the master node using the root account by default.
This could represent  an enterprise security policy violation for many companies.

--------------------
Problem description
--------------------

Currently, Fuel node uses root account for all operations, including:

* deployment and configuration

* running services (Astute, Nailgun etc)

* user operations (CLI, upgrades etc)

* accessing slave nodes

Many corporate security policies do not allow root access.
Furthermore, compliance with auditing entities like Health Insurance Portability and Accountability
 (HIPAA) and Payment card industry (PCI) may require that better access control is in place.
Consequently, Fuel should operate using non-privileged accounts where it is possible to do so.

----------------
Proposed changes
----------------

The cornerstone of this change is the introduction of an admin user called
'fueladmin' which will be used instead of the root user account to manage the OpenStack
environments via CLI on the master node, to access the slave nodes etc. This account
is going to have sudo privileges with password authentication.

The proposed way to achieve this is to introduce a separate package called 'fuel-admin-user',
whose only job would be to create the 'fueladmin' user and add him to sudoers.d.
This package must be listed as a requirement for all the other fuel-related
RPM packages. This package will be added to the fuel-main spec. All the other
fuel-related packages will also use 'fueladmin' as a default owner for their
files. This approach will allow following:

* easier transition during upgrades as new Fuel packages will automatically
  fetch fuel-admin-user as well

* less worries about file permissions as packages will set correct
  permissions right from the start

Moreover, SSH root login should be disabled on all nodes and allow for users to set up
their own method of user access management not covered here. SSH keys for the fueladmin
user will need to be added to slave nodes placed in it's home directory.

Every service on the Fuel node will run under a non-privileged user (for services
which do not require elevated privileges). E.g. A supervisor is going to run under
'supervisor' user etc.

Default password for 'fueladmin' user would be 'fuel'. Operator will have
an option to change this in fuelmenu.

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

With this change, plugins will require 'fuel-admin-user' package and will
use 'fueladmin' as a default user for their files.

Fuel Library
============

Puppet manifests will be changed to reflect this feature:

* Generic files belonging to Fuel will have correct permissions

* For each service which will be running on the Fuel node:

  * logs will be moved to dedicated directories (since many services currently
    write into /var/log which is owned by root)

  * configuration files of certain services will be moved to dedicated
    directories as well

  * other application data (e.g. pid files) will be moved to dedicated
    directories

  * configuration will be changed to run the service under non-privileged
    account

  * if a service is running inside Docker container, put it under supervisor

* changes to Fuel services' configuration files to reflect new location of SSH keys.

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

When upgrading to a release containing this feature, items, described in the
Library section will have to be taken care of. The reasonable solution would
be to re-run Puppet on master node after the new library is installed.
Please note that this requires Fuel node manifests to be idempotent.
The next step would be to move log files and/or application data to their new
directories (where applicable). This can be easily automated.

---------------
Security impact
---------------

This change will have a security impact as root login over SSH will be
disabled for Fuel and slave nodes.

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

User will have to use 'fueladmin' user account instead of root.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

Fuelmenu will allow to configure a password for 'fueladmin'.

----------------
Developer impact
----------------

New features will need to be designed with consideration that new code will
not be running with superuser privileges.

---------------------
Infrastructure impact
---------------------

As remote root login will be disabled, CI jobs, and scripts which access Fuel
and slaves remotely will have to be adjusted to use 'fueladmin' user account.

--------------------
Documentation impact
--------------------

Documentation will have to be updated to reflect changes (using 'fueladmin'
for access etc)

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  <nikishov-da>

Other contributors:
  <gomarivera>

Mandatory design review:
  <gomarivera>


Work Items
==========

* Indroduce 'fueladmin' user as a part of respective package.
  Include it in dependecies lists of other Fuel packages.
  Fix any problems with file permissions which are not managed,
  but still are used by Fuel packages.

* Change fuelmenu to allow setting custom password for 'fueladmin'.

* Change puppet manifests for Host node to run supervisor (and some other
  services) under it's own non-privileged user.

* Add 'fueladmin' to slave nodes and enable remote login to other nodes for
  this user. Disable root login.

* Run Fuel services under non-privileged users inside Docker containers.

Dependencies
============

None

------------
Testing, QA
------------

Manual testing.

Acceptance criteria
===================

* Fuel uses non-privileged user during installation, configuration, operation
  (where it is possible).

* All Fuel services are running under dedicated non-superuser accounts.

* Anything that requires to remain root is documented.

* Non-privileged user's name is 'fueladmin'.

* Remote SSH root login is disabled for both Fuel and slave nodes.

----------
References
----------

Implementation draft:
https://review.openstack.org/243337
https://review.openstack.org/243313
