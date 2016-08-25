..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================================
Upgrade Fuel Admin node 8.0 to 9.x
==================================

https://blueprints.launchpad.net/fuel/+spec/upgrade-fuel-admin-node

The data-driven upgrade of a Fuel Master node is a way how to deliver latest
version of Fuel installer and OpenStack to users without breaking their
existing environments.

This spec covers changes in the current approach to make it useful to upgrade
a Fuel Master node from 8.0 to 9.x releases.

--------------------
Problem description
--------------------

In contrast with previous releases when services were contaniarized, in the 9.0
release services run on the host system level. Due to that it is impossible to
perform upgrade of a Fuel Master node using standard tools (e.g. YUM package
management system).

The data-driven upgrade of a Fuel Master node that was developed to upgrade
from 7.0 to 8.0 assumes that services on both source and destination Fuel
Master nodes are ran in containers. This means that it can not be applied for
upgrades to 9.x as is.

----------------
Proposed changes
----------------

Current approach assumes that all services ran in Docker containers, they
are managed by ``dockerctl`` and ``docker`` toolsets. Also, new versions of
services can be delivered through destroy and build processes of respective
containers. This can be achieved by a sequence of commands
``dockerctl destroy`` and ``dockerctl build```.

The new approach shall modify current handlers that are used in commands
``octane fuel-backup`` and ``octane fuel-restore`` to perform all
manipulations on the host system level instead of container level and
and shall conform the requirements:

  * services are managed by Puppet tasks located on a Fuel Master node in
    ``/etc/puppet/modules/fuel/examples/``

  * services are controlled by the ``systemctl`` command as other
    ordinary services on the host system

  * ``/var/lib/cobbler/config/systems.d`` is placed in the host filesystem and
    contains configuration of already deployment nodes

This minimal set of modifications shall not change a format and a content of
an upgrade tarball. It means that all data set shall be compatible with
data-driven upgrade that was developed earlier.

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

After the upgrade all installed plugins will have the same version they had
before the upgrade, so Fuel Operator will have to install the compatible
version onto the Fuel Admin node after the restore is done.

Fuel Library
============

None.

------------
Alternatives
------------

None.

--------------
Upgrade impact
--------------

This proposal covers modifications of technical aspects of the upgrade
workflow. Backup/restore now work for non-containerized services and
the restore part re-uses puppet tasks to reconfigure and manage services in
a consistent way.

---------------
Security impact
---------------

None.

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

The requirements enforced by the data-driven upgrade remain. The new Fuel
Master node must have the same IP addresses and the admin password as the old
one.

This proposal doesn't impact the deployment of new OpenStack environments.

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

None.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  akscram

Other contributors:
  sabramov

Mandatory design review:
  vkozhukalov
  ashtokolov
  ikalnitskiy


Work Items
==========

* Implement support of non-containairized services in backup/restore handlers
  of ``octane``.

* Implement system test to verify the new upgrade workflow.

* Prepare documentation on the new upgrade workflow.


Dependencies
============

* Apply 9.x MU for a Fuel Master node

------------
Testing, QA
------------

* Current test plans must be be updated with new upgrade procedure.

* New tests must be written for covering disastery recovery cases to handle
  backup/restore of Fuel Master node.

* New tests must be written for covering 7.0->8.0->9.x chain-upgrade scenarious
  of a Fuel Master node.


Acceptance criteria
===================

* Backups created by ``octane fuel-backup`` and ``octane fuel-repo-backup``
  commands are tarballs that contain all files and data according to
  the data-driven upgrade approach.

* On fresh installation of the 9.x Fuel Master node, ``octane fuel-restore``
  and ``octane fuel-repo-restore`` restore an ability to manage already
  deployed environments and create new ones with new versions provided by
  the 9.x releases, including:

  * command ``octane fuel-restore`` uploads data from the backup to ``nailgun``
    and ``keystone`` databases at Fuel 8.0 Admin node

  * configuration files in ``systems.d`` directory of Cobbler configuration
    directory restored from backup and match the actual nodes in the test
    environment.

  * proper access credentials are restored across the system, including DB
    accounts, SSH keys and certificates for Cobbler and Nginx.

* Changes implementing the functions listed above are properly submitted,
  reviewed and merged into ``fuel-octane`` repository.

* Documentation describing the upgrade workflow republished for the 9.x
  releases.

----------
References
----------

* https://github.com/openstack/fuel-octane - the toolset for upgrading
  Fuel Admin node and OpenStack environments

* https://specs.openstack.org/openstack/fuel-specs/specs/8.0/upgrade-master-node-centos7.html
  - the data-driven upgrade of a Fuel Master node from 7.0 to 8.0
