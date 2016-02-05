..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================================================
Support for FC Multipath disk configurations on MOS nodes
=======================================================================

https://blueprints.launchpad.net/fuel/+spec/support-for-multipath-disk

Many of real OpenStack production systems use external devices - which provide
storage solutions. Most part of them provide possibility to connect block
devices using `FC`_ (Fiber Channel) `HBA`_ (Host Based Adapter) with multipath
support.

FC HBA is an useful technology that can enable OpenStack  to run more virtual
machines(due high input\output productivity) and applications per server,
reduce management time and server power draw and protect data from silent data
corruption(usually,external data storage solution take care about data
integrity and safety). FC HBA with multipath architect also increase high
availability and stability of whole system.

-------------------
Problem description
-------------------

*   Fuel currently does not support any multipath solution, which creates all
    sorts of UX issues and blockers for deployment on such nodes.

*   Currently there is no possibility to deploy OpenStack on nodes with
    FC HBA multipath devices, using Fuel. Otherwise, many and many Openstack
    solutions are switching to use FC HBA solutions with multipath.

*   Currently there is no possibility to deploy OpenStack by Fuel on nodes,
    which have only FC HBA storage.

----------------
Proposed changes
----------------

The field analysis shown that FC HBA multipath is more frequent use case
than iSCSI, so this proposal is to implement support for FC HBA multipath
disks in Fuel 9.0, which means at least the following:

    * enable of needed multipath devices support in bootstrap\target system
      (Multipath support will be enabled by default in Fuel.)

    * proper export of disk info into UI (right now Nailgun exports multiple
      records for single multipath drive, which breaks UX)

    * extending Nailgun logic to interpret raw disks data from nailgun-agent
      More details in Nailgun_ section.

    * extending fuel-agent to support disabling udev blacklisting and resolve
      issue with predictable naming of multipath partitions align tooling(utils)
      with multipath needs.

    * change fuel-nailgun-agent from sending interpreted disk data to only parsed
      commands output data.

Web UI
======

Recognized multipath configuration will be available on Web UI , for each node,
in the node information dialog.

Nailgun
=======

We propose to extend Nailgun to determine the multipath configuration from data
which is sent from fuel-nailgun-agent. As a result stored disk
configuration will contain only regular physical devices and multipath
devices. Each multipath device will contain a list with information of
underlying devices in common format.

#. Changes in Node meta validation schema to align with received raw
   dict-like structures from fuel-nailgun-client.

#. Implementing interpretation of raw data which will output disks and
   multipath devices with paths and all necessary information related to block
   devices.



Fuel-nailgun-agent
------------------

We propose to extend fuel-nailgun-agent with support for multipath devices.
That means, that fuel-nailgun-agent will be able to handle not only physical
/dev/*d* devices, but also /dev/mapper/* and /dev/mpath/* devices - which
will be populated by multipath service.

For example, a node with two HBAs attached to a storage controller with two
ports via a single unzoned FC HBA switch sees four devices: /dev/sda, /dev/sdb,
/dev/sdc, and /dev/sdd. DM-Multipath creates a single device with a
unique WWID (WWN) that reroutes I/O to those four underlying devices
according to the multipath configuration.

So, we propose to add logic in fuel-nailgun-agent to provide some additional
metadata for discovered block devices. This metadata should be enough to
determine the multipath configuration.

Fuel-bootstrap
--------------

We propose to extend default fuel-bootstrap build with new packages and
parameters needed for multipath support.

Support for HBA card will be provided by ubuntu distribution or driver
delivered by user to bootstrap during build process. User can manually
rebuild bootstrap with required driver package.

Fuel-agent
----------
We propose to extend fuel-agent to support IBP process with multipath devices.

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

  .. code-block:: text

    udevadm info --query=property --name={}
    dmsetup info -c --nameprefixes --noheadings --rows -o blkdevname,name,uuid,blkdevs_used,subsystem,lv_name


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

We propose to add possibility to attach disk via multipath and FC HBA for nodes.
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
