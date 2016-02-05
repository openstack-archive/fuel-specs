..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================================================
Support for FC Multipath disk configurations on MOS nodes
=======================================================================

https://blueprints.launchpad.net/fuel/+spec/support-for-multipath-disk

Many of our customers use storage devices, which provide possibility to connect
block devices using `FC`_ `HBA`_ (Fiber Channel Host Based Adapter) with multipath
support. We need to have a possibility to deploy Openstack on nodes with
FC HBA multipath devices. This feature will allow customer to use disk-less
nodes to build Openstack environments, with support storage connected with
multipath(using FC HBA).

-------------------
Problem description
-------------------

Many Mirantis customers have disk-less Compute hardware which is usually
connected to storage system, that provides multipath-enabled disks.
Fuel currently does not support multipath, which creates all sorts of UX issues
and blockers for deployment on such nodes.

This spec intends to enable support for FC HBA multipath disks in Fuel/MOS 9.0.
The field analysis shown that this is more frequent use case than iSCSI.
FC HBA multipath disk support requires few things:

    * enable of needed FC HBA card driver (can be done now with dynamic Ubuntu
      bootstrap and\or with Fuel plugins)

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
   ports via a single unzoned FC HBA switch sees four devices: /dev/sda, /dev/sdb,
   /dev/sdc, and /dev/sdd. DM-Multipath creates a single device with a
   unique WWID (WWN) that reroutes I/O to those four underlying devices
   according to the multipath configuration.

   So, we will add logic in fuel-nailgun-agent to provide some additional
   metadata for discovered block devices. This metadata should be enough to
   determine the multipath configuration.

#. We will extend default fuel-bootstrap build with new packages and parameters
   needed for multipath support.

   Support for HBA card will be provided by ubuntu distribution or driver
   delivered by user to bootstrap during build process. User can manually
   rebuild bootstrap with required driver package.

#. We will extend Naigun to determine the multipath configuration from data
   which is sent from fuel-nailgun-agent. As a result stored disk
   configuration will contain only regular physical devices and multipath
   devices. Each multipath device will contain a list with information of
   underlying devices in common format.

#. We will extend fuel-agent to support IBP process with multipath
   devices.

#. Multipath support will be enable by default in Fuel.

#. We will extend Web UI to view multipath configuration.

Web UI
======

Recognized multipath configuration will be available on Web UI , for each node,
in the node information dialog.

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

Adding new handler in api v2 (/api/v2/nodes/agent/).
New format will have raw data from commands only parsed to dict-like structure.

  .. code-block:: json

     {'disks': {'blocks': [{'udevadm': "output of "udevadm info" command for each
                                        block device parsed to dicts",
                            'size': 0,
                            'removeable': boolean},...],
                'dmsetup': [splited output of "dmsetup info"]}}

In output of dmsetup there is now clear separator from each of multipath
devices. Which means then when key is already in dict we should create next
dict and add it to dmsetup output.
Exact commands lines that will be used:
`udevadm info --query=property --name={}`
`dmsetup info -c --nameprefixes --noheadings --rows
-o blkdevname,name,uuid,blkdevs_used,subsystem,lv_name`


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
(w\o FC HBA multipath system).
All others impact can be related only with FC HBA multipath system itself.

-----------------
Deployment impact
-----------------

We will add possibility to attach disk via multipath and FC HBA for nodes.
Disks will be available on fuel ui, and normally processed like physical disks.
This feature don't have any impact on previous installations, only extend
disks support.

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
  `Szymon Banka`_

Other contributors:
  `Krzysztof Szukielojc`_
  `Sergey Slipushenko`_
  `Aleksey Zvyagintsev`_

QA engineers
  `Alexander Zatserklyany`_

Mandatory design review:
  `Alexander Gordeev`_
  `Vladimir Kozhukalov`_
  `Evgeny Li`_

Work Items
==========

- extend fuel-ui to show multipath disks
- add packages related to multipath support into default ubuntu-bootstrap image
- add fuel-nailgun-agent support for correct multipath disk discovery
- add to nailgun support for correct serialization of disks delivered by multipath
- apply blacklisting for underlying devices handled by multipath


Dependencies
============

None


-----------
Testing, QA
-----------

Proper functional tests should be implemented.


Acceptance criteria
===================

* Multipath devices automatically detected and configured during
  node bootstrap

* Host OS able to boot from FC HBA multipath disk devices

* OpenStack deployed on nodes with multipath devices

* All auto-tests implemented and merged to swarm tests


----------
References
----------

.. _`Alexander Gordeev`: https://launchpad.net/~a-gordeev
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Evgeny Li`: https://launchpad.net/~rustyrobot
.. _`Krzysztof Szukielojc`: https://launchpad.net/~kszukielojc
.. _`Sergey Slipushenko`: https://launchpad.net/~sslypushenko
.. _`Aleksey Zvyagintsev`: https://launchpad.net/~azvyagintsev
.. _`Szymon Banka`: https://launchpad.net/~sbanka
.. _`Alexander Zatserklyany`: https://launchpad.net/~zatserklyany
.. _`HBA`: https://en.wikipedia.org/wiki/Host_Bus_Adapter
.. _`FC`: https://en.wikipedia.org/wiki/Fibre_Channel
