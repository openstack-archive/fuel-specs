..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================================
Support for FC Multipath disk configurations on MOS nodes
=========================================================

https://blueprints.launchpad.net/fuel/+spec/support-for-multipath-disk

Many of our customers use FC disk for Fuel nodes.
We need to have possibility to attach SAN multipath-enabled disks on MOS nodes.


-------------------
Problem description
-------------------

Many Mirantis customers have diskless Compute hardware which is usually
connected to SAN that provides multipath-enabled disks.
Fuel currently does not support multipath, which creates all sorts of UX issues
and blockers for deployment on such nodes.

This spec intends to enable support for FC multipath in Fuel/MOS 9.0. The field
analysis shown that this is more frequent use case than iSCSI.
FC multipath support requires few things:

    * enable of needed FC card driver (can be done now with dynamic Ubuntu
      bootstrap and Fuel plugins)

    * proper export of disk info into UI (right now Nailgun exports multiple
      records for single multipath drive, which breaks UX)

    * Extending Nailgun logic


----------------
Proposed changes
----------------


#. We will extend fuel-nailgun-agent with support for multipath devices.
   That means, that fuel-nailgun-agent will be able to handle not only physical
   /dev/*d* devices, but also /dev/mapper/* and /dev/mpath/* devices - which
   will be populated by multipath service.

   For example, a node with two HBAs attached to a storage controller with two
   ports via a single unzoned FC switch sees four devices: /dev/sda, /dev/sdb,
   /dev/sdc, and /dev/sdd. DM-Multipath creates a single device with a
   unique WWID (WWN) that reroutes I/O to those four underlying devices
   according to the multipath configuration

   So, we will add logic in fuel-nailgun-agent to provide some additional
   metadata for discovered block devices. This metadata should be enough to
   determine the multipath configuration.

#. We will extend default fuel-bootstrap build with new packages and parameters
   needed for multipath support.

   Support for HBA card will be provided by ubuntu distribution or driver
   delivered by user to bootstrap during    build process. User can manually
   rebuild bootstrap with required driver package.

#. We will extend Naigun to determine the multipath configuration from data
   which is sent from fuel-nailgun-agent. As a result in stored disk
   configuration will contain only regular physical devices and multipath
   devices. Each multipath device will contain a list with information of
   underlying devices if common format.

#. We will extend fuel-agent to support IBP process with multipath
   devices.

#. Multipath support will be enable by default in Fuel.

#. We will extend Web UI to view multipath configuration.

Web UI
======

Recognized multipath configuration will be available on Web UI , for each node,
on tab: 'Hardware Configuration'.


Nailgun
=======

Changes in Node meta validation schema. Implementing processing of raw data
related to block devices received from fuel-nailgun-agent.
Changing the default partitioning schema.

Data model
----------

None

REST API
--------


Extend format of metadata reported by fuel-nailgun-agent.
Adding 'udev_raw' field with content of `udevadm info --query=all --name={}`
Removing fields like name, extra and disk. As this info will be parsed in
nailgun from 'udev_raw'.


Orchestration
=============

None


Fuel Client
===========

None

Plugins
=======

None


Fuel Library
============

None


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

We are not expecting any problems related with default installation
(w\o FC multipath system).
All others impact can be related only with FC multipath system itself.

-----------------
Deployment impact
-----------------

We will add possibility to attach disk via multipath and FC protocol for nodes.
Disks will be available on fuel ui, and normally processed like physical disks.
This feature don't have any impact on previous installations, only
extend disks support.

----------------
Developer impact
----------------

None


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

User will be informed that:
    - functionality is available in Fuel

    - how to generate bootstrap with user HBA card driver
      (custom driver, not delivered with Ubuntu-kernel)


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>


QA engineers
  <launchpad-id or None>

Mandatory design review:
    <launchpad-id or None>

Work Items
==========

- extend fuel-ui to show multipath disks
- add packages related to multipath support into default ubuntu-bootstrap image
- nailgun-agent support for correct multipath disk discovery
- add to nailgun support for correct serialize disks delivered by multipath
- blacklisting underlying devices handled by multipath


Dependencies
============

None


-----------
Testing, QA
-----------

Proper functional tests should be implemented.


Acceptance criteria
===================

* Multi-path devices have to be automatically detected and configured during node bootstrap

* Multi-path devices have to be configured in Host OS

* Deploy OpenStack on nodes with multi-path devices

* Supported protocol for multipath is FC

* Auto-tests implemented



----------
References
----------

