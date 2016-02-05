..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================================
Support for FC Multipath disk configurations on MOS nodes
=========================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/example

Many of our customers use FC disk for Fuel nodes.
We need to have possibility to attach SAN multipath-enabled disks on MOS nodes.


--------------------
Problem description
--------------------

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

   So, we will add logic, which allow nailgun-agent to *mark** multipath
   devices.

#. We will extend default fuel-bootstrap build with new packages and parameters
   needed for multipath support.

   Support for HBA card will be provided by ubuntu distribution or driver
   delivered by user to bootstrap during    build process. User can manually
   rebuild bootstrap with required driver package.

#. We will extend Naigun to serilize and work with multipath devices

#. We will extend fuel-agent to support IBP process with multipath
   devices.

#. Multipath-device support will be enable by default in Fuel.

#. We will patch web-UI to support multipath device view.

Web UI
======

Recognized disk will be available on fuel-ui, for each node, on tab: 'Nodes'
under option 'Configure disks'.


Nailgun
=======

Changes in Node meta validation schema. Implementing processing of raw data
recived from udevadm info for block devices.
Chaning the default partitioning schema.

Data model
----------

None

REST API
--------


Diffrent interface between fuel-nailgun-agent and nodes handler.
Adding 'udev_raw' field with content of `udevadm info --query=all --name={}`
Removing fields like name, extra and disk. As this info will be parsed in
nailgun from 'udev_raw'.


Orchestration
=============

Sending more information to fuel-agent to recognize the multipath disk and
information.
Idea is that mpath object should have list of disk which are under multipath.


Fuel Client
===========

Should be able to recognize new mpath disk objects and display it accordingly.

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


------------
Testing, QA
------------

TBF

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly.

This should include changes / enhancements to any of the integration
testing. Most often you need to indicate how you will test so that you can
prove that you did not adversely effect any of impacts sections above.

If there are firm reasons not to add any other tests, please indicate them.

After reading this section, it should be clear how you intend to confirm that
you change was implemented successfully and meets it's acceptance criteria
with minimal regressions.

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

