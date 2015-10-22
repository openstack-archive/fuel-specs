..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
Cinder Block Device driver
==========================

https://blueprints.launchpad.net/fuel/+spec/TBD

Problem description
===================

Disk-intensive workloads require the storage layer to be able to provide both
high IOPS and sequential operations capabilities. Apache Hadoop is one of the
most storage-sensitive frameworks which is widely used for Data Processing in
production. Sahara service provides Hadoop installations on top of OpenStack.

The best performance on the virtualized environment can achieved by providing
the direct access from a VM to a block device located on the same compute
host. OpenStack Cinder service has such attachment option implemented in the
BlockDeviceDriver.

The current implementation requires a user to set up the Fuel plugin to have
the BlockDeviceDriver support. Some manual configuration steps are required as
well.

Having a built-in functionality for this use-case will provide a better user
experience without plugin installation and manual configurations.

Proposed changes
================

The implementation requires a new role to be added. The new role should be
available in Fuel Web UI. The proposed name for new role is
*Cinder-Block-Device Storage*.

The main aim of assigning a host to this role is to give a user a choice of
which block devices should be dedicated exclusively to Cinder
BlockDeviceDriver. The chosen block device cannot be shared with any other
role. BlockDeviceDriver is supposed to work with entire device not with its
partitions.

This implies that a host with the Cinder-Block-Device role should be validated
to have at least one extra device for host OS and VM root disks.

The Block-Device-Role is not supposed to be combined with other Cinder roles.
The Block-Device-Role should require to be place on compute hosts only.

The user configuration should be applied in the following flow:

* All information about the chosen disk should be serialized by Nailgun and
passed to nodes in Astute yaml config.

* cinder.conf file should be updated with the volume_driver and
available_devices options.

Example of yaml file:

.. code-block:: yaml

   - cinder-block-devices:
      node-2: /dev/sdb, /dev/sdc
      node-3: /dev/sdb, /dev/sdg
      node-4: /dev/sdy

Example of cinder.conf

.. code-block:: ini

  volume_driver = cinder.volume.drivers.block_device.BlockDeviceDriver
  available_devices = /dev/sdb,/dev/sdc

The Puppet manifests should be updated to be able to handle new configuration
options on the hosts with Cinder-Block-Device role.

No new packages are required for the BlockDeviceDriver, because it is a part
of Cinder codebase.

According to the description above the following implementation steps are
required:

* Add a new node role to the Web UI;
* Add a validation prohibiting to place Cinder-Block-Device role along with
other Cinder roles.
* ADd a validation allowing to place Cinder-Block-Device role only on hosts
which already have compute role.
* Add a validation allowing to allocate only entire disks for the
Cinder-Block-Device role.
* Extend Nailgun API to support device data serialization. The serialized data
should then be passed to Astute
* Add a new Puppet task and manifests to deploy the configurations.


Web UI
======

A new Block-Device-Driver node role should be added.

When the role is applied to the host the host disks should have checkboxes for
Cinder-Block-Device. The checked disks should be passed to the
BlockDeviceDriver.


Nailgun
=======

An ability to serialize the Cinder-Block-Device role data should be added.

The checked disks should be serialized to a yaml which the should be passed
to Astute.

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

None


Fuel Library
============

A new Puppet task should be added.

The task should be responsible for provisioning the cinder.conf changes on
appropriate nodes.

------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

None


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None


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

None


--------------------------------
Infrastructure/operations impact
--------------------------------

Need add one more job and tests, which will cover a new
deployment scheme.


--------------------
Documentation impact
--------------------

All infrastructure changes should be documented.


--------------------
Expected OSCI impact
--------------------

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Denis Egorenko`_


Mandatory Design Reviewers:
  - `Sergey Reschetnyak`_
  - `Nikita Konovalov`_


Work Items
==========

* Implement related changes to Fuel Web UI and Nailgun

* Implement related changes to Fuel Library

* Implement related changes to Fuel OSTF and CI tests;


Dependencies
============

None


-----------
Testing, QA
-----------

Introduced changes should be covered by system tests.

QA engineers:
  `Evgeny Sikachev`_


Acceptance criteria
===================

* Disks attached to VM without LVM

* If VM and disk on the same host then necessary check that libvirt
uses virtio driver instead iSCSI for attached disk.


----------
References
----------

.. _`Denis Egorenko`: https://launchpad.net/~degorenko
.. _`Sergey Reschetnyak`_:
.. _`Nikita Konovalov`:
.. _`Evgeny Sikachev`:
