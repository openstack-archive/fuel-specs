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

  * ``/etc/fuel/astute.yaml`` configuration file, used by Puppet to install
    the Fuel Admin node and containers within it.

  * ``/etc/fuel/fuel-uuid`` file which identifies the installation of Fuel.

  * ``/etc/fuel/version.yaml`` file which identifies the former version of
    Fuel and used to verify version of backup data.

  * ``/root/.ssh/identity`` private key used by Fuel Admin node to access
    all target nodes in environments.

  * ``/var/lib/cobbler/config/systems.d`` directory contains configuration
    files for target nodes discovered by the Fuel Admin node.

  * ``/var/lib/fuel/keys/`` certificates and keys for SSL/TLS
    encryption of web UI traffic.

  * text dump of ``nailgun`` database from Postgres server

  * text dump of ``keystone`` database from Postgres server

  * ``ostf`` database **is not** backed up/restored

* Backup log files separately from the configuration, since they could be
  bulky and will slow down the backup/restore process. Logs backup can
  be done via Nailgun diagnostic snapshot as usual.

* Supply file ``astute.yaml`` from backup to the freshly installed Fuel
  Admin node via ``fuel-menu``. ``fuel-menu`` will preserve credentials
  from the supplied ``/etc/fuel/astute.yaml`` file.

* Install the Fuel Admin node as usual.

* After installation of the Fuel Admin node, inject database dump into
  PostgreSQL DB and run migration scripts on the database.

* Upload of ``openstack.yaml`` fixture with metadata of the new release
  via Nailgun API.

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

Fuel Library provides manifests used by ``bootstrap_admin_node.sh`` script
to install and configure Fuel components in Docker containers. Installation
of the Fuel Admin node is managed by ``nailgun`` module.

We need to do the following modifications to the ``nailgun`` module to
support restore of configuration and state data in Docker containers and
Postgres database.

* Add new value for ``PRODUCTION`` flag that defines new type of environment
  the ``nailgun`` module is working in: ``restore-docker``, and define the
  following behavior for manifests.

* ``manifests/venv.pp`` manifest must ensure that data from backup are
  uploaded to the database before the ``nailgun_sync`` script is executed.

* ``manifests/cobbler.pp`` manifest shall copy Cobbler systems configuration
  from backup to the volume mounted in ``cobbler`` container. It must preserve
  the ``default.json`` configuration file from release 8.0.

* ``example/keystone-only.pp`` manifest must upload data from backup dump to
  database before running ``keystone db_sync``.

* ``manifests/systemd.pp`` manifest shall handle ``restore-docker`` value
  of flag ``production`` just like ``docker`` value of the same flag.

------------
Alternatives
------------

Alternative way is to backup and restore Docker containers, as per current
version of Fuel Admin node backup. Given the decision to drop containers
support and additional value of the data-based backup/restore for cases when
the master node is reinstalled, we abstain from this approach.

Fuel's ``shotgun``` tool might be used or backup purposes. The original
version shall be patched and published as an update to 7.0 release. User
installs it in the host and uses it to create backup tarball from CLI.

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
in Nailgun. See `Fuel Library` section for the details.

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


--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

User experience for upgrading Fuel Admin node changes significantly. Instead
of running single shell script ``upgrade.sh``, operator will have to:

* install new version of ``fuel-upgrade`` package from ``mos-updates``
  repository onto Fuel Admin node version 7.0.

* create backup with ``backup`` command from ``fuel-upgrade`` package and
  copy resulting file to external location (e.g. USB drive or another server).

* install new Fuel Admin node with version 8.0 using elements of backup in
  installation procedure. Operator have 2 options:

  * install the new 8.0 Fuel Admin node onto existing physical server or VM,
    replacing the original 7.0 Fuel Admin node.

  * install the Fuel Admin node onto new physical/virtual server in parallel
    with the original 7.0 Fuel Admin node.

* use ``fuel-menu`` to retrieve and extract the backup file and restore
  credentials and other settings of the Admin node from ``astute.yaml``
  from the backup.

* run ``restore`` command from ``fuel-upgrade`` package to inject remaining
  elements of backup into fresh installation of the Fuel Admin node.

Rollback option is available through installing fresh 7.0 Fuel Admin node and
restoring configuration on that node according to the procedure outlined
above.

------------------
Performance impact
------------------

None.

-----------------
Deployment impact
-----------------

Deployment engineer shall be required to provide a path to backup file
through the ``fuel-menu`` during the installation of the new version of
Fuel Admin node.

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

* Implement ``fuel-upgrade backup`` command to create a backup file from 
  the Fuel Admin node

* Implement injection of ``astute.yaml`` file into boostrap process of the
  Fuel Admin node in ``fuel-menu`` utility

* Implement injection of DB dump from backup file into PostgreSQL database
  server during the bootstrap in ``fuel-library``

* Implement restore of Cobbler configuration files and key/cert files from
  backup in ``fuel-library``

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

* Backup created by ``fuel-upgrade backup`` command is a tarball that
  contains all files and data according to this specification on the
  Fuel Admin node of version 7.0.

* On fresh installation of Fuel Admin node with version 8.0 ``fuel-menu``
  includes tab with 'Restore' title that allows to specify a path on local
  file system or removable storage that leads to the file with backup data.

* ``fuel-menu`` restores contents of ``/etc/fuel/astute.yaml`` file in
  the following sections from values in backup ``astute.yaml`` file:

  * ``HOSTNAME``, DNS and NTP settings

  * ``ADMIN_NETWORK``

  * ``FUEL_ACCESS``

  * ``FEATURE_GROUPS``

  * ``keystone`` credentials

  * ``postgres`` credentials

* During setup, data from the backup are uploaded to ``nailgun`` and
  ``keystone`` databases at Fuel 8.0 Admin node.

* Configuration files in ``systems.d`` directory of Cobbler configuration
  directory restored from backup and match the actual nodes in the test
  environment.

* Proper access credentials are restored across the system, including DB
  accounts, SSH keys and certificates for Cobbler and Nginx.

* Changes implementing the functions listed above are properly submitted,
  reviewed and merged into source code of corresponding Fuel components.

* Documentation describing the new upgrade workflow submitted and merged'
  in the main Fuel documentation.

----------
References
----------

