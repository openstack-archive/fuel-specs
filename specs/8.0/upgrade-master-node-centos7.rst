..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================
Upgrade Fuel Admin node 7.0 to 8.0 with CentOS7
===============================================

https://blueprints.launchpad.net/fuel/+spec/upgrade-master-node-centos7

Upgrade of the Fuel Admin node is a way to deliver latest version of
Fuel installer and OpenStack to users without breaking their existing
environments. It is necessary to accommodate the upgrade method for
Fuel Admin node to changes made in 8.0 release cycle.

This spec is addressing only the upgrade of the Fuel Admin node up to
the point when it is able to deploy and manage environments with the
new version of OpenStack. Upgrade of the OpenStack environments is out
of scope of this proposal.

--------------------
Problem description
--------------------

In release 8.0, CentOS 7 is introduced as a base operating system for the
Fuel Admin node, replacing CentOS 6.6 in release 7.0.

Due to the level of customization of the basic operating system in release
7.0, it is impossible to upgrade the operating system by standard tools
(e.g. YUM package management system).

Users of Fuel installer should be able to keep their OpenStack environments
managed by Fuel through the upgrade of the Fuel Admin node.

----------------
Proposed changes
----------------

Current approach to the upgrade in release 7.0 assumes that the new version
of docker images are packaged in RPM. Upgrade script installs the package and
rebuilds the containters.

New approach shall be data-driven in a sense that the Fuel Admin node
will be reinstalled from scratch, while configuration data of OpenStack
environments shall be retained and applied to the fresh installation of
Fuel. This allows the Fuel Admin node to manage existing OpenStack
clusters deployed by previous versions of Fuel.

For data-driven upgrade of the Fuel Admin node, the following procedure
must be developed:

* Backup configuration of the Fuel Admin node and all OpenStack clusters
  managed by this node, including the following items:

  * ``/etc/fuel/`` directory that contains configuration files for the
    Fuel Admin node's installation and operation.

  * ``/etc/puppet/`` directory to preserve Puppet modules for former
    release(s) to retain support for old clusters.

  * ``/root/.ssh/`` directory contains private/public keys used to access
    all target nodes in environments.

  * ``/root/.ssh/authorized_keys`` file with public keys authorized to connect
    to the Fuel Admin node.

  * ``/var/lib/cobbler/config/systems.d`` directory contains configuration
    files for target nodes discovered by the Fuel Admin node. File
    ``default.json`` contains definition for bootstraping nodes and must not
    be backed up or restored in the new release version.

  * ``/var/lib/fuel/keys/`` certificates and keys for SSL/TLS
    encryption of web UI traffic.

  * text dump of ``nailgun`` database from Postgres server

  * text dump of ``keystone`` database from Postgres server

  * ``ostf`` database **is not** backed up/restored

* ``fuel-octane`` tool shall be used for backup purposes. The original
  version shall be patched and published as an update to 7.0 release. User
  installs it in the host and uses it to create backup tarball.

* Backup log files separately from the configuration, since they could be
  bulky and will slow down the backup/restore process. Logs backup can
  be done via Nailgun diagnostic snapshot as usual.

* Install the Fuel Admin node as usual.

* Supply file ``astute.yaml`` from backup to the freshly installed Fuel
  Admin node via ``octane fuel-restore`` command. It will restore
  credentials from the supplied ``/etc/fuel/astute.yaml`` file.

* Command ``octane fuel-restore`` shall inject database dump into
  PostgreSQL DB and run migration scripts on the database.

* Command ``octane fuel-restore`` shall upload ``openstack.yaml`` fixture
  with metadata of the new release via Nailgun API.

* After installation of the Fuel Admin node, inject Cobbler configuration
  files, keys and certs in corresponding places and restart appropriate
  services.

Web UI
======

None.

Nailgun
=======

None.

Data model
----------

None.

REST API
--------

None.

Orchestration
=============

None.

RPC Protocol
------------

None.

Fuel Client
===========

None.

Plugins
=======

None.

Fuel Library
============

None.

------------
Alternatives
------------

Alternative way is to backup and restore Docker containers, as per current
version of Fuel Admin node backup. Given the decision to drop containers
support and additional value of the data-based backup/restore for cases when
the master node is reinstalled, we abstain from this approach.

Another path is to upgrade operating system of the Fuel Admin node in-place
with ``centos-upgrade-tool`` provided by CentOS. This path is unstable
considering modifications to base operating system, including changed package
versions and rebuilt packages. It will require modifications to the upgrade
tool and supporting third-party upgrade scripts.

--------------
Upgrade impact
--------------

This proposal covers change of upgrade workflow. The new workflow shall
reuse the database upgrade capabilities provided by Alembic migrations
in Nailgun. Migrations will be applied automatically with the restart of
container ``docker-nailgun``.

---------------
Security impact
---------------

Backup file contains high sensitive data, including SSH private keys and
access credentials to all components in both Fuel and OpenStack environments.
This file must be handled with extreme care. It must not be published to
externally accessible location (e.g. HTTP server). Preferred way to transfer
the file between old and new instance of the Fuel Admin node is removable
storage device.

Backup file shall be encrypted and protected with user-supplied secret.

Root password for the fresh installation of the Fuel 8.0 Admin node must be
changed via fuel-menu or immediately after the installation. ``fuel-octane
backup`` shall not save ``/etc/passwd`` and ``/etc/shadow`` files and thus
won't preserve root password and/or other users credentials from the original
node.

--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

User experience for upgrading Fuel Admin node changes significantly. Instead
of running single shell script ``upgrade.sh``, operator will have to:

* install new version of ``fuel-octane`` package from ``mos-updates``
  repository onto Fuel Admin node version 7.0.

* create backup with ``octane fuel-backup`` command from ``fuel-octane``
  package and copy resulting file to external location (e.g. USB drive or
  another server).

* install new Fuel Admin node with version 8.0 using elements of backup in
  installation procedure. Operator have 2 options:

  * install the new 8.0 Fuel Admin node onto existing physical server or VM,
    replacing the original 7.0 Fuel Admin node.

  * install the Fuel Admin node onto new physical/virtual server in parallel
    with the original 7.0 Fuel Admin node.

* use ``octane fuel-restore`` to extract the backup file and restore
  credentials and other settings of the Admin node from ``astute.yaml``
  from the backup and inject remaining elements of backup into
  fresh installation of the Fuel Admin node.

Rollback option is available through installing fresh 7.0 Fuel Admin node and
restoring configuration on that node according to the procedure outlined
in Operations Documentation (see Documentation Impact section for details).
The rollback procedure shall be based on ``dockerctl restore`` command.

------------------
Performance impact
------------------

None.

-----------------
Deployment impact
-----------------

Fuel 8.0 Admin node is installed as usual. The restoration procedure must
be applied immediately afterwards, before any changes to settings of the
new Admin node.

This proposal doesn't impact the deployment of OpenStack environments.

----------------
Developer impact
----------------

None.

---------------------
Infrastructure impact
---------------------

To accommodate to this change, an extra virtual machine has to be used in the
testing environment when testing this function and the upgrade of an OpenStack
environment following the upgrade of the Fuel Admin node.

--------------------
Documentation impact
--------------------

New upgrade workflow shall be documented in respective section of Operations
Guide.

New rollback workflow based on ``dockerctl backup/restore`` shall be described
in Operations Guide:

* Before upgrading Fuel Admin 7.0, run ``dockerctl backup`` and save resulting
  backup file in external store.

* To rollback the Fuel Admin installation, deploy fresh Fuel 7.0 Admin nod,
  retrieve backup of Doclker containers from external store and use command
  ``dockerctl restore`` to restore configuration and data of containers.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  sryabin

Other contributors:
  gelbuhos

Mandatory design review:
  vkozhukalov
  sgolovatyuk
  ikalnitskiy
  dborodaenko


Work Items
==========

* Implement ``octane fuel-backup`` command to create a backup file from
  the Fuel Admin node

* Implement injection of ``astute.yaml`` file into boostrap process of the
  Fuel Admin node in ``octane fuel-restore`` utility

* Implement injection of DB dump from backup file into PostgreSQL database
  server during the bootstrap in ``octane fuel-restore`` command

* Implement restore of Cobbler configuration files and key/cert files from
  backup in ``octane fuel-restore`` command

* Implement rebuild of Docker containers with the restored data in
  ``octane fuel-restore`` command

* Implement upload of openstack.yaml fixtures for 8.0 release using
  ``octane fuel-restore`` command

* Implement translations for the backup data according to Predictable
  Interfaces Naming feature in ``fuel-web`` DB migration scripts

* Implement system test to verify the new upgrade workflow

* Prepare documentation on the new upgrade workflow


Dependencies
============

* Centos7 on the Fuel Admin node

* Enable Predictable Interfaces Naming schema

------------
Testing, QA
------------

* Current test plans must be be updated with new upgrade procedure.

* Rollback-scenarios must be adapted for using restore feature.

* New tests must be written for covering upgrading cluster with new features
  introduced in 7.0:

  * Network templates

  * Node groups

  * Separate services

  * Node reinstallation

* Chain-upgrade scenarious for upgrading fuel master node 6.1->7.0->8.0
  must be written to ensure the ability to manage Kilo cluster with
  deprecated or removed features:

  * nova-network FlatDHCP

  * Neutron GRE network

  * CentOS as base OS for cluster

  * Classic provisioning

Acceptance criteria
===================

* Backup created by ``octane fuel-backup`` command is a tarball that
  contains all files and data according to this specification on the
  Fuel Admin node of version 7.0.

* On fresh installation of Fuel 8.0 Admin node, ``octane fuel-restore``
  command restores contents of ``/etc/fuel/astute.yaml`` file in the
  following sections from values in backup ``astute.yaml`` file:

  * ``HOSTNAME``, DNS and NTP settings

  * ``ADMIN_NETWORK``

  * ``FUEL_ACCESS``

  * ``FEATURE_GROUPS``

  * ``keystone`` credentials

  * ``postgres`` credentials

* Command ``octane fuel-restore`` uploads data from the backup to ``nailgun``
  and ``keystone`` databases at Fuel 8.0 Admin node.

* Configuration files in ``systems.d`` directory of Cobbler configuration
  directory restored from backup and match the actual nodes in the test
  environment.

* Proper access credentials are restored across the system, including DB
  accounts, SSH keys and certificates for Cobbler and Nginx.

* Changes implementing the functions listed above are properly submitted,
  reviewed and merged into ``fuel-octane`` repository.

* Documentation describing the new upgrade workflow submitted and merged
  in the main Fuel documentation.

----------
References
----------

* https://github.com/openstack/fuel-octane - the toolset for upgrading
  Fuel Admin node and OpenStack environments
