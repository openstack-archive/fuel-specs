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

--------------------
Problem description
--------------------

Currently, Fuel node uses root account for all operations, including:

* deployment and configuration

* running services (Astute, Nailgun etc)

* user operations (CLI, upgrades etc)

* accessing slave nodes

Many corporate users of Fuel would be required to meet security compliance
standards in their infrastructure including Fuel. Many of such policies
restrict access to non-root accounts. Consequently, Fuel should operate using
non-privileged accounts where it is possible to do so.

----------------
Proposed changes
----------------

Items in this change (in the order they're going to be implemented):

1. **Disabling remote root SSH access to slave nodes**

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

   * User account will be created at the image building stage (in cloud-config
     templates), as well as all the required configuration (sshd, sudoers)

   * Every service that uses SSH to access slave nodes will be modified to use
     an account passed by Nailgun for remote login.

   * Certain OSTF tests will be modified, since these tests access slaves via
     SSH and non-root account might not have required privileges to perform
     required commands (e.g. read /etc/nova/nova.conf)

   * CI infrastructure (fuel-qa/fuel-devops) will be updated to use a non-root
     account for SSH access to slaves. All the commands that are executed on
     slaves and do require elevated privileges will be wrapped into sudo.

2. **Disabling remote root SSH access to the master node**

   * Console root access will still be allowed

   * Instead of root SSH access, users will log into fuel node with a non-root
     account

   * This user will be created by any fuel-* package (created in pre-install
     script). fuel-* packages' files ownership will be changed to fueladmin for
     packages it makes sense to do so (e.g. fuel-bootstrap-image since it's
     spec is hardcoded to copy SSH key to \/root\/.ssh).

   * The name for this account will be static: fueladmin; the default password
     will be "fueladmin". It'll also be possible to set the password from
     kernel command line.

   * Users will be able to change fueladmin password (along with the root
     password) in fuelmenu the same way it is implemented for root user right
     now.

   * This user will have sudo privileges that will require password.

   * <More details to be added>

3. **Fuel services running under non-privileged users**

   * Every Fuel service (Nailgun, Astute etc) as well as non-Fuel services
     (e.g. dnsmasq) will be running under a non-privileged user account.

   * User accounts will be created during package installation (pre-install
     script) for Fuel services. For non-Fuel services this will be managed by
     host-only Puppet manifest during initial Fuel node configuration.

   * Files ownership will be changed to per-service users.

   * If a service requires elevated privileges, these privileges will be
     managed via Linux capabilities feature. The capabilities will be granted
     by systemd.

   * <More items to be added>

4. **Run mcollective as non-root**

   * Mcollective will be running as non-privileged user 'mcollective'.

   * All commands that require root privileges, will be wrapped into
     oslo-rootwrap.

   * oslo-rootwrap is going to be installed on slave nodes during image build.

   * Nailgun will compile a command whitelist for oslo-rootwrap for each node
     based on tasks, scheduled for execution on each node.

   * This whitelist will be uploaded to the slave nodes during pre-deployment
     stage via rsync.

   * <more details to be added>

Web UI
======

* There will be an additional tab in the UI to configure a non-root user
  account (name, password, authorized SSH keys).

Nailgun
=======

* Fuelmenu will have option to configure fueladmin password as well.

* Fuel-agent's cloud-init templates will be extended to create 'fueladmin' user
  on the slave nodes, configure sshd, install oslo-rootwrap.

* Nailgun will pass to other components (e.g. Shotgun) ssh-user parameter along
  with ssh-key for remote SSH access. This username will be taken from the DB.

* Nailgun will compile a list of commands to be included into oslo-rootwrap
  whitelist.

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

* With this change, plugins will create 'fueladmin' user upon installation and
  will use 'fueladmin' as a default user for their files.

Fuel Library
============

* openrc file will be put to the home directory of a non-root user.

* <More items to be added>

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
and slaves remotely will have to be adjusted to use non-root user accounts.

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

* Pass non-root account to fuel-agent to configure target OS images (fuel-web, fuel-agent).

* Change Astute to use credentials passed by Nailgun for SSH access (fuel-astute)

* Fix/change OSTF that rely on SSH user having root-level privileges (fuel-ostf).

* Fix CI jobs to use non-root account for slave nodes SSH access (fuel-qa, fuel-devops).

* Research further work items and update or split the specification.


Dependencies
============

* CentOS 7

* Fuel services running under systemd

------------
Testing, QA
------------

Manual testing.

Acceptance criteria
===================

* Fuel uses non-privileged user during installation, configuration, operation
  (where it is possible, e.g. puppet should be executed with superuser
  privileges).

* All Fuel services are running under dedicated non-superuser accounts.

* Anything that requires to remain root is documented.

* Non-privileged user's name is 'fueladmin'.

* Remote SSH root login is disabled for both Fuel and slave nodes.

----------
References
----------

None
