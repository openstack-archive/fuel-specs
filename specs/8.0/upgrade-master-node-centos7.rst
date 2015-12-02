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

  * ``/root/.ssh/identity`` private key used by Fuel Admin node to access
    all target nodes in environments.

  * ``/var/lib/cobbler/config/systems.d`` directory contains configuration
    files for target nodes discovered by the Fuel Admin node.

  * ``/var/lib/fuel/keys/master/nginx/nginx.[crt|key]`` certificate and
    key for SSL/TLS encryption of web UI traffic.

  * ``postgres pg_dumpall`` command dumps all data from configuration
    database for Nailgun into text file.

* Supply file ``astute.yaml`` from backup to the freshly installed Fuel
  Admin node via ``fuel-menu``. ``fuel-menu`` will preserve credentials
  from the supplied ``/etc/fuel/astute.yaml`` file.

* Install the Fuel Admin node as usual.

* After installation of the Fuel Admin node, inject database dump into
  PostgreSQL DB and repeat uploading of ``openstack.yaml`` fixture with
  metadata of the new release.

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

User experience for upgrading Fuel Admin node changes significantly. Instead
of running single shell script ``upgrade.sh``, operator will have to:

* create backup with ``backup`` command from ``fuel-upgrade`` package and
  copy resulting file to external location (e.g. USB drive or another server).

* install new Fuel Admin node using elements of backup in installation
  procedure. Operator have 2 options:

  * install the new Fuel Admin node onto existing physical server or VM,
    replacing the original 7.0 Fuel Admin node.

  * install the Fuel Admin node onto new physical/virtual server in parallel
    with the original 7.0 Fuel Admin node.

* use ``fuel-menu`` to retrieve and extract the backup file and restore
  credentials and other settings of the Admin node from ``astute.yaml``
  from the backup.

* run ``restore`` command from ``fuel-upgrade`` package to inject remaining
  elements of backup into fresh installation of the Fuel Admin node.

Rollback option is available through installing fresh Fuel Admin node of
the original release (7.0) and restoring configuration on that node according
to the procedure outlined above.

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

None.

------------------
Performance impact
------------------

None.

-----------------
Deployment impact
-----------------

Deployment engineer shall be required to provide a path to kickstart file
as a boot parameter during the installation of the new version of Fuel
Admin node.

----------------
Developer impact
----------------

None.

---------------------
Infrastructure impact
---------------------

None.

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

* Implement ``backup`` script to create a backup file from the Fuel Admin
  node

* Implement injection of ``astute.yaml`` file into boostrap process of the
  Fuel Admin node

* Implement injection of DB dump from backup file into PostgreSQL database
  server during the bootstrap

* Implement ``restore`` script to restore Cobbler configuration files and
  key/cert files from backup

* Implement translations for the backup data according to Predictable
  Interfaces Naming feature

* Implement system test to verify new upgrade workflow


Dependencies
============

* Centos7 on the Fuel Admin node

* Enable Predictable Interfaces Naming schema

------------
Testing, QA
------------

* Current test plans must be be updated with new upgrade procedure.

* Rollback-scenarious must be adapted for using restore feature.

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

TBD

----------
References
----------

