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
a set of separable modules/plugins.

1. Discovery

   This step is when we try to find out which hard drives are available on a
   node. Anaconda and debian-installer do the same at the very beginning of
   provisioning process. In our case this step is implemented as a separate
   service which is called Nailgun Agent.

2. Allocation

   On this step the default partitioning scheme is generated. This allocation
   step can be data driven when, for example, a user of a provisioning agent
   defines which file systems she needs to be created and their priorities but
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
This spec is totally about step 2. So, the suggestion is to implement
volume management (volume allocation) totally in terms of Fuel Agent.

Fuel Agent already implements partitioning object model
``fuel_agent/objects/partition.py``. What we need to add there is the ability
to dynamically allocate volumes over existent hard drives on a node and add
serialization/de-serialization methods.

Implementing dynamic volume allocation code as a part of Fuel Agent will allow
us to easily move this piece of functionality into Fuel plugin. So, there are
two possible cases:

1. Volume manager plugin is NOT installed

   In this case there is no corresponding disk management tab on UI and
   Nailgun does not pass any specific data to Fuel Agent about partitions,
   logical volumes, raids, etc. leaving this stuff completely up to
   Fuel Agent logic. As far as Fuel Agent has its own disk discovery
   mechanism and this dynamic volume allocation code will be
   a part of Fuel Agent, it is obviously be possible for Fuel Agent
   to generate default volume allocation. The default allocation should be
   configurable via allocation metadata which can be passed to Fuel Agent as
   input data. Some default allocation metadata can be hard coded in
   Fuel Agent.

::

  +---------+    +--------------------------------------------+
  |Nailgun  |    |                                            |
  |w/o vol. |    | Fuel Agent                                 |
  |plugin   |    |                                            |
  +---------+    +--------------------------------------------+
  +---------+    +----------+    +-----------+    +-----------+
  |         |    |          |    |           |    |           |
  |discovery+--> |allocation+--> |OS building+--> |OS copying |
  |         |    |          |    |           |    |           |
  +---------+    +----------+    +-----------+    +-----------+


2. Volume manager plugin is installed

   Being installed volume manager plugin imports Fuel Agent code in order
   to generate default allocation. The default allocation should be
   configurable via allocation metadata. A user then can modify this default
   allocation on the disk management tab on UI which is going to appear when
   volume manager plugin is installed. If other plugins need to modify somehow
   volume allocation scheme they need to use volume manager plugin for this
   and they need to interact with it only via its API (they must not modify
   volume manager plugin data directly).

::

  +-------------------------+    +----------------------------+
  |Nailgun with vol. plugin |    | Fuel Agent                 |
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
    type: "lv"
    vg: 9
    minsize: "20G"
    name: "mysql"

  - id: 8
    type: "vg"
    name: "os"
    minsize: __auto__
    pvs: __auto__

  - id: 9
    type: "vg"
    name: "mysql"
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
   That metadata is flat makes it easily scalable. Any plugin
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
size of a logical volume. The field ``priority`` is going to be used for
sharing the volume group space over all logical volumes in this group.
Allocation algorithm for logical volumes should look like the following:

a) allocating minimal size for each logical volume (fail if not enough space)
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
   volumes identifiers which constitute the volume group. If this field is
   equal to ``__auto__`` then it means we should define physical volumes
   dynamically during allocation. For example, we need to allocate 100G for
   the volume group, and there are two disks on the node partly allocated for
   other volume groups and partitions. Let's say there is 50G of free space on
   the first disk and 50G of free space on the second disk. So, two physical
   volumes (50G each) will be allocated for the volume group.

4. TODO Plain partition

5. TODO MD device

Another important thing is that currently Fuel Agent objects are
often initalized with actual block device names (e.g. /dev/sda). But in case
of dynamic allocation the actual device names are unknown when an object is
instantiated. The correct way how to deal with this is to modify objects
so as to make it possible to postpone actual device evaluation
(e.g. ``fuel_agent/objects/device.py:Loop``).


Alternatives
------------

We could implement volume management mechanism from scratch and fully
independently from Fuel Agent. But it looks irrational avoiding using existent
code and ignoring beautiful architectural concept.

Data model impact
-----------------

Currently, generated and modified partitioning data is stored as json string
in one of the fields of the Node model. As far as we are going to switch
on using Fuel Agent object model the format of partitioning data
will be changed.

REST API impact
---------------

That part of REST API which deals with volume data is going to be moved into
volume manager plugin.

Upgrade impact
--------------

As far as Fuel Agent is installed into bootstrap ramdisk, nodes which are
booted with this ramdisk must be forced to be rebooted to make sure the newest
version of Fuel Agent is available on slave nodes.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Volume allocation mechanism is going to become much more flexible. UI disk
management part needs to be modified in order to be able to handle new volume
allocation format.

Performance Impact
------------------

None

Plugin impact
-------------

Volume manager should be implemented as Fuel plugin. Other plugins which
need to modify volume allocation need to depend on volume manager plugin and
use its API.

Other deployer impact
---------------------

TODO

Developer impact
----------------

None

Infrastructure impact
---------------------

TODO

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

TODO

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
