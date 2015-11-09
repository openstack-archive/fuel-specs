..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Running Fuel as non-superuser
==========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-nonsuperuser

It should be possible to run the Fuel master node and the slave nodes as a
non-superuser (non-root).  Currently, users are required to log into the master
node using the root account by default.  This could represent  an enterprise
security policy violation for many companies.

This specification addresses usage of the root accounts on slave nodes for user
access.

--------------------
Problem description
--------------------

Currently, Fuel node uses root account for all operations, including:

* deployment and configuration

* running services (Astute, Nailgun etc)

* user operations (CLI, upgrades etc)

* accessing slave nodes (addressed in this specification)

Many corporate users of Fuel would be required to meet security compliance
standards in their infrastructure including Fuel. Many of such policies
restrict access to non-root accounts. Consequently, Fuel should operate using
non-privileged accounts where it is possible to do so.

----------------
Proposed changes
----------------

**Disabling remote root SSH access to slave nodes**

   * Console root access will still be allowed.

   * Instead of root SSH access, users will login into slaves with a non-root
     account.

   * The name, password and authorized SSH keys will be configurable via UI.
     The defaults will be fueladmin/fueladmin. User-supplied public SSH keys
     will be included into authorized_keys file as well as the key, generated
     by Fuel.

   * This user account will have sudo privileges, however users will be
     required to input password to do sudo.

   * Optional list of commands, that are allowed to be executed with sudo
     without the need to input password, will be available for customization in
     UI as well.

   * User accounts will be created at the image building stage (in cloud-config
     templates), as well as all the required configuration (sshd, sudoers)

   * Every service that uses SSH to access slave nodes will be modified to use
     an account passed by Nailgun for remote login.

   * Certain OSTF tests will be modified, since these tests access slaves via
     SSH and non-root account might not have required privileges to perform
     required commands (e.g. read /etc/nova/nova.conf)

   * CI infrastructure (fuel-qa/fuel-devops) will be updated to use a non-root
     account for SSH access to slaves. All the commands that are executed on
     slaves and do require elevated privileges will be wrapped into sudo.

Web UI
======

* Add following items to settings tab:

  * User account name (defaults to fueladmin)

  * User account password (defaults to fueladmin)

  * User-supplied public SSH keys (empty by default)

  * List of commands that this user is allowed to run with passwordless sudo
    (empty by default)

Nailgun
=======

* Fuel-agent's cloud-init templates will be extended to:

  * Create user-specified accounts

  * Populate sudoers.d

  * Configure sshd_config to set "PermitRootLogin no" (boothook)

* openstack.yaml fixture will be changed to include slave node user accounts
  configuration

* Extend provisioning serializer to pass OS user account settings to
  Astute/Fuel agent

* Nailgun will pass to other components (e.g. Shotgun) ssh-user parameter along
  with ssh-key for remote SSH access. This username will be taken from the DB.

Data model
----------

None

REST API
--------

None

Orchestration
=============

* Astute will use credentials passed by Nailgun for SSH access to slave nodes.

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

* refactor openstack::auth_file to allow specifying user name and home directory

* put openrc into user-supplied user account home directory

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

When upgrading to the release, containing this feature, user accounts on slave
nodes will have to be taken care of.  This can easily be automated.

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

Users will have to log into slave nodes with accounts, which have been
specified during deployment stage.

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

New features will need to be designed with consideration that root SSH access
to slave nodes will be disabled.

---------------------
Infrastructure impact
---------------------

As remote root login to slave nodes will be disabled, CI jobs, and scripts
which access Fuel and slaves remotely will have to be adjusted to use non-root
user accounts.

--------------------
Documentation impact
--------------------

Documentation will have to be updated to reflect changes (using non-root
accounts for access etc)

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

* Introduce non-root account configuration for slave nodes in UI (fuel-web).

* Move openrc file to a new location on slave nodes (fuel-library)

* Pass non-root account to fuel-agent to configure target OS images (fuel-web,
  fuel-agent).

* Change Astute to use credentials passed by Nailgun for SSH access
  (fuel-astute)

* Fix/change OSTF that rely on SSH user having root-level privileges
  (fuel-ostf).

* Fix CI jobs to use non-root account for slave nodes SSH access (fuel-qa,
  fuel-devops).


Dependencies
============

None

------------
Testing, QA
------------

* Fuel-qa will be extended to try and login to the slave node with default root
  credentials (root/r00tme)

Acceptance criteria
===================

* Remote SSH root login is disabled for slave nodes.

* User can specify settings for the account that should be created during
  initial deployment.


----------
References
----------

None
