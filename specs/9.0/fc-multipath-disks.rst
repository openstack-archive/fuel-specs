..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================================
Support for FC Multipath disk configurations on OpenStack nodes
===============================================================

https://blueprints.launchpad.net/fuel/+spec/support-for-multipath-disk

Many of real OpenStack production systems use external devices - which provide
storage solutions. Most of them provide possibility to connect block
devices using `FC`_ (Fiber Channel) `HBA`_ (Host Based Adapter) with multipath
support.

FC HBA is an useful technology that can enable OpenStack  to run more virtual
machines (due high input\output productivity) and applications per server,
reduce management time and server power draw and protect data from silent data
corruption (usually, external data storage solution take care about data
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

The field analysis showed that FC HBA multipath is more frequent use case
than iSCSI, so this proposal is to implement support for FC HBA multipath
disks in Fuel 9.0, which means at least the following:

    * enable of FC HBA multipath devices support in bootstrap\target system.
      Multipath support should be enabled in Fuel by default

    * change fuel-nailgun-agent from sending interpreted disk data to sending
      only parsed commands output data.

    * extend Nailgun logic to interpret raw disks data from nailgun-agent
      More details in Nailgun_ section.

    * export of multipath device info into UI as a single block device

    * extend fuel-agent to enable provisioning nodes with multipath devices.
      It requires to fix issue with naming of partitions on multipath devices.

Web UI
======

Recognized multipath configuration will be available on Web UI, for each node,
in the node information dialog. Each multipath device will be exported as a
single block device.

Nailgun
=======

We propose to extend Nailgun to determine the multipath configuration from data
which is sent from fuel-nailgun-agent. As a result stored disk
configuration will contain only regular physical devices and multipath
devices. Each multipath device will contain a list with information of
underlying devices in common format.

#. Changes in Node meta validation schema to align with received raw
   dict-like structures from fuel-nailgun-agent.

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

To make the following things we have 2 options:

Option 1:

Add add logic in fuel-nailgun-agent to discover and report multipath topology
in following format:

  .. code-block:: json

    {'disks':
     [{'name': 'dm-42',
       'model': '',
       'removable': '0',
       'size': 53687091200,
       'extra': ['disk/by-id/dm-uuid-mpath-42']
       'multipaths':['sda', 'sdb']},...
    ]}

Underlying devices (in current sample - sda and sdb) will not be reported into
nailgun as a separate block device. Metadat for not multipatch devices will not
be changed.

Option 2:

Add logic in fuel-nailgun-agent to provide some additional
metadata for discovered block devices. Parsed output from command
`dmsetup info -c --nameprefixes --noheadings --rows -o name,uuid,blkdevname,blkdevs_used`
will be used as this metadata. It should be enough to determine the multipath
configuration on server side.

Fuel-bootstrap
--------------

We propose to extend default fuel-bootstrap build with new packages and
parameters needed for multipath support.

Support for HBA card will be provided by Ubuntu distribution or driver
delivered by user to bootstrap during build process. User can manually
rebuild bootstrap with required driver package.

Fuel-agent
----------
We propose to extend fuel-agent to enable provisioning nodes with multipath
devices. It requires to fix issue with naming of partitions on multipath
devices. Solution of this issue requires to whitelist some udev rules, which
all are blacklisted now. We will add an option in fuel-agent configuration to
whitelist required udev rules.

Data model
----------

None

REST API
--------

Option 1:

No changes in API required.

Option 2:

Reports with data from the updated fuel-nailgun-agent will be handled by url
"/api/v1/nodes/agent/". New API microversion **v1.1** will be pointed in HTTP
handlers, like OpenStack components do.

New API handler should be available to receive raw data about nodes disks from
the fuel-nailgun-agent. New version of report will look this:

  .. code-block:: json

    {
      "meta":{
      ...
        "disks":{[
          {
            "name": "dm-0",
            "removable": "0",
            "size": 53687091200,
            "model": "",
            "dm_properties": {
              "DM_SUBSYSTEM": "mpath",
              "DM_NAME": "0QEMU    QEMU HARDDISK   35e53b2cb5114d80b28b",
              "DM_UUID": "mpath-0QEMU    QEMU HARDDISK   35e53b2cb5114d80b28b",
              "DM_BLKDEVS_USED": ["sdb", "sda"]
            }
          },...]
        },...
      }
    }

Only disk part of report will be changed. Raw data will be processed and stored
in 'metadata' field of Node DB instance in current format to keep compatibility
with Nailgun UI.

Output of REST API will not be changed.

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

* Auto-tests implemented


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
