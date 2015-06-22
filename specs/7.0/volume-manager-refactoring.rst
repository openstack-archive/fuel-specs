..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
Volume manager refactoring
==========================

https://blueprints.launchpad.net/fuel/+spec/volume-manager-refactoring

Currently nailgun volume manager is not flexible and customizable enough
to address many needs of users. For example, some users want some volumes
to be untouched during OS provisioning, some users want it to be possible
to deploy software RAIDs or configure FS mount options, etc.

Problem description
===================

There are use cases which aren't covered with the fuctionality of current
implementation of volume manager.

These use cases include at least the following:

* Volume preservation

  Sometimes when a node is going to be re-provisioned there could be
  volumes (partitions, logical volumes, MD devices) which user wants
  to remain untouched.

* FS mount options

  Sometimes user needs to mount some file systems using specific options, like
  noatime or ro, etc.

* Bootable disks

  Currently we install bootloader on all hard drives, but it is not always
  correspond to what user wants.

* Flexible partitioning scheme

  Currently we have predefined partition scheme which assumes, for example,
  that we put root file system on logical volume and that we don't create
  separate file system for /var. These assumptions limit users in their
  abilities to create a partition scheme they might want.

* Pluggable partitioning scheme

  Some Fuel plugins assume we need to have additional partitions on node.
  Currently, plugin partitions can conflict with existent partitions and
  we need to resolve these potential conflicts.

Proposed change
===============

Provisioning process in general can be considered as the following
set of steps:

::

  +---------+    +----------+    +-----------+    +-----------+
  |         |    |          |    |           |    |           |
  |discovery+--> |allocation+--> |OS building+--> |OS copying |
  |         |    |          |    |           |    |           |
  +---------+    +----------+    +-----------+    +-----------+

All those main steps can be implemented in a monolithic manner or they can be
a set of separable modules/plugins/extensions.

1. Discovery

   This step is when we try to find out which hard drives are available on a
   node. Anaconda and debian-installer do the same at the very beginning of
   provisioning process. In our case this step is implemented as a separate
   service which is called Nailgun Agent.

2. Allocation

   On this step the default partitioning scheme is generated. This allocation
   step can be data driven when, for example, a user of a provisioning agent
   defines which file systems she needs to create and their priorities but
   not their exact sizes. Again anaconda and debian-installer do the same
   using some default hard coded or user difined (kickstart/preseed)
   partitioning metadata. In our case it is implemented as the
   ``volume manager`` module in Nailgun.

3. OS building

   On this step OS is built from scratch using packages repositories or any
   other available mechanisms. Anaconda builds OS using rpm packages and yum.
   Debian-installer uses deb packages and debootstrap. In terms of Fuel this
   step is exactly what we call OS image building. In contrast to anaconda
   and debian-installer we build OS just once somewhere on the master node or
   on a developer node during ISO building. We then just copy this pre-built
   OS image on all provisioned nodes. This step indirectly depends on the
   previous step (step 2) because a user might be potentially
   interested in assigning some specific options for a particular file system.
   Step 2 (allocation) is exactly the place where we define which partitions
   and file systems we need. OS building (or equivalently OS image building)
   being implemented in terms of Fuel Agent can be potentially run on the
   slave node if, for example, this node requires specific file system options.

4. OS copying

   This step makes sense only for image based approach when we build OS
   remotely. For example, anaconda and debian-installer build OS right on the
   file system where it is going to live on a node.

Anaconda and debian-installer implement these four steps in a monolithic
manner. For example, we can not separate OS building step from the whole
provisioning process. In case of Fuel all these steps implemented as separate
components. Currently, Fuel Agent implements steps 3 and 4, but it looks like
Fuel Agent is the right place where to implement also steps 1 and 2
[#discovery]_.
This spec does not concern step 1. Re-implementing the functionality
of Nailgun Agent in terms of Fuel Agent is a deal of a separate feature.
This spec is totally about step 2.

The suggestion is to implement dynamic volume allocation totally in
terms of Fuel Agent and use this functionality in Nailgun importing
necessary modules from Fuel Agent. The motivation behind is:

* Dynamic volume allocation is tightly connected to the whole
  provisioning process. Fuel Agent already has quite detailed partitioning
  object model ``fuel_agent/objects/partition.py`` which just needs to
  be developed so as to support dynamic allocation over existent hard drives
  on a node.
* Allocation scheme can influence steps 3 and 4. So, it is much easier to
  deal with the whole provisioning process when it is totally implemeted in
  terms of one modular component.
* Being quite independent Fuel Agent can be used w/o Fuel. And it would be
  great to make it able to dynamically allocate volumes when it is used
  out of Fuel.
* In the future we will need to allocate volumes not only basing on their
  size but also taking into account disk types and other parameters. And it
  is going to be much easier to introduce those parameters in terms of
  Fuel Agent object model.

On the other hand we are moving towards modular Fuel architecture, so, it
looks like it is the place where we can start putting our efforts towards
modularisation. The suggestion is to implement current volume manager
in nailgun as extension. Being installed this volume manager extension
imports Fuel Agent code in order to generate volume allocation
(metadata/UI driven). The default volume allocation should be
configurable via allocation metadata. A user then can modify this default
allocation on the disk management tab on UI. If other extensions
(ceph or mongo, etc.) need to modify volume allocation scheme they need
to use volume manager extension for this and they need to interact
with it only via its API.

So, the feature can be considered as two independent tasks

1. Convert Nailgun volume manager into Nailgun volume manager extension
2. Implement dynamic volume allocation procedure in terms of Fuel Agent
   and introduce this functionality into Nailgun volume manager extension
   importing necessary modules from Fuel Agent.

Coverage scheme then will be as follows:

::

  +-------------------------+    +----------------------------+
  |Nailgun & vol. extension |    | Fuel Agent                 |
  +-------------------------+    +----------------------------+
  +---------+    +----------+    +-----------+    +-----------+
  |         |    |          |    |           |    |           |
  |discovery+--> |allocation+--> |OS building+--> |OS copying |
  |         |    |          |    |           |    |           |
  +---------+    +----------+    +-----------+    +-----------+


Dynamic allocation
------------------

Dynamic allocation metadata could look like (exact format will be found
during actual implementation):

::

  - id: 1
    type: "fs"
    mount: "/boot"
    device: 10
    fs_type: "ext2"

  - id: 2
    type: "fs"
    mount: "/"
    device: 5
    fs_type: "ext4"

  - id: 3
    type: "fs"
    mount: "swap"
    device: 6
    fs_type: "swap"

  - id: 4
    type: "fs"
    device: 7
    mount: "/var/lib/mysql"
    fs_type: "ext4"
    block_size: "4K"

  - id: 5
    type: "lv"
    vg: 8
    name: "root"
    minsize: "10G"
    bestsize: "15G"
    priority: 1000

  - id: 6
    type: "lv"
    vg: 8
    minsize: "1G"
    maxsize: "8G"
    priority: 200
    name: "swap"

  - id: 7
    type: "partition"
    minsize: "20G"
    device: __auto__

  - id: 8
    type: "vg"
    name: "os"
    minsize: __auto__
    pvs: __auto__

  - id: 10
    type: "md"
    level: "mirror"
    minsize: "200M"
    maxsize: "400M"
    bestsize: "200M"
    numactive: 2
    numspares: 1
    devices: __auto__
    spares: __auto__

The format of these metadata should be as close to the format of Fuel Agent
objects as possible. It can make it easier to serialize/de-serialize
objects.

Let's go through these metadata step by step.

1. Each item has id field which is used to connect objects wherever they need
   to be connected avoiding at the same time non-trivial data hierarchies.
   That metadata is flat makes it easily scalable. Any plugin/extension
   can append or remove items. For example, the following item means we need
   to allocate ``ext2`` file system with ``/boot`` mount point
   on device with ``id`` equal to 10.

::

  - id: 1
    type: "fs"
    mount: "/boot"
    device: 10
    fs_type: "ext2"

2. Logical volume items have ``vg`` field which identifies volume group where
   a logical volume is to be placed.

::

  - id: 5
    type: "lv"
    vg: 8
    name: "root"
    minsize: "10G"
    bestsize: "15G"
    maxsize: "50G"
    priority: 1000

The fields ``minsize``, ``maxsize``
and ``bestsize`` are used to set limits and give recommendations about the
size of the logical volume. The field ``priority`` is going to be used for
sharing the volume group space over all logical volumes in this group.
Allocation algorithm for logical volumes should look like the following:

a) allocating minimal size for each logical volume (fail if there is no
   enough space)
b) allocating remaining space up to recommended size for each logical volume
   taking into account their priorities
c) allocating remaining space up to maximal size for each logical volume
   taking into account their priorities

Those size limitation/recommendation/priority fields are optional.
If they are not set we can use some default
priority and allocate remaining space for the logical volume taking into
account this default priority value.

3. Volume group can also have ``minsize``, ``maxsize``, ``bestsize`` and
   ``priority`` fields which are to be used exactly the same way as in case
   of logical volumes. If ``minsize`` is equal to ``__auto__`` then it means
   it should be calculated as a sum of minimal sizes of all logical volumes
   in the volume group. The field ``pvs`` should define a set of physical
   volume identifiers which constitute the volume group. If this field is
   equal to ``__auto__`` then it means we should define physical volumes
   dynamically during allocation. For example, we need to allocate 100G for
   the volume group, and there are two disks on the node partly allocated for
   other volume groups and partitions. Let's say there is 50G of free space on
   the first disk and 50G of free space on the second disk. So, two physical
   volumes (50G each) will be allocated for the volume group.

4. Plain partition can have the same limitation/recommendation fields
   ``minsize``, ``maxsize``, ``bestsize``, ``priority`` and these fields have
   the same meaning. It is necessary to note that unlike volume groups,
   plain partitions can not be split into parts (physical volumes).
   So, plain partitions should be allocated before volume groups and then
   the remaining free space can be flexibly used for volume groups.

5. MD device has the same dynamic allocation fields, but the trick here is
   that need to allocate several partitions for one MD device and these
   partitions are to be located on different hard drives.

Ideally, dynamic allocation process must take into account many other
parameters apart from just size of a volume. For example, we'd better avoid
using SSD and HDD disks together for one volume group. Another example is
we need to set file system block sized taking into account the type of hard
drive, otherwise we can encounter some serious performance issues.
But due to tight deadline for 7.0 let's implement ONLY size driven allocation.
Other metadata can be easily introduced later in terms of another spec.

Another important thing is that currently Fuel Agent objects are
often initalized with actual block device names (e.g. /dev/sda). But in case
of dynamic allocation the actual device names are unknown when an object is
instantiated. Actual block device name makes sense not earlier than the
command parted is run. The correct way how to deal with this is to
modify objects so as to make it possible to postpone actual device evaluation
(e.g. ``fuel_agent/objects/device.py:Loop``). In partition scheme there
should not be names like ``/dev/sda3`` until it is evaluated and actualized.


Alternatives
------------

We could implement volume management mechanism from scratch and fully
independently from Fuel Agent. But it looks irrational avoiding using existent
code and ignoring beautiful architectural concept.

Data model impact
-----------------

Fuel Agent object model is going to be changed so as to include dynamic
allocation methods and data.

Volume data in Nailgun are stored as plain json in the Node data model. As far
as Nailgun volume manager will re-implemented as an extension, these volume
data will be moved into extension table with foreign key to the Node.

REST API impact
---------------

That part of REST API which deals with volume data is going to be moved into
volume manager extension.

Upgrade impact
--------------

As far as Fuel Agent is installed into bootstrap ramdisk, nodes which are
booted with this ramdisk must be forced to be rebooted to make sure the newest
version of Fuel Agent is available on slave nodes.

Also Fuel Agent package should be updated on the master node because Nailgun
volume manager extension is going to use Fuel Agent modules.

Besides, we need to write a database migration which should create
the new volume manager table and move volume data there.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Plugin impact
-------------

Volume manager should be implemented as Fuel extension. Other
plugins/extensions which need to modify volume allocation, should use
volume manager extension API.

Other deployer impact
---------------------

If deployer need specific allocation mechanism she just needs to write her
own volume manager extension implementing corresponding API.

Developer impact
----------------

None

Infrastructure impact
---------------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <skalinowski@mirantis.com>

Other contributors:
  <vkozhukalov@mirantis.com>

Work Items
----------

1. Implement Nailgun volume manager extension
2. Implement dynamic volume allocation in terms of Fuel Agnent

Dependencies
============

TODO


Testing
=======

TODO


Documentation Impact
====================

TODO

References
==========

.. [#discovery] In fact, Fuel Agent currently implements discovery
   functionality but only for block devices (hard drives) and it is not
   compatible with Nailgun. So, if it is necessary, Fuel Agent is able
   to get the information about available hard drives on a node
   totally on its own.
