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

    * change fuel-nailgun-agent to send discovered multipath topology in Nailgun

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

Disk configuration reported by fuel-nailgun-agent will be stored, as it works
now, as a part of Node DB instance metadata. Disk configuration will be
displayed in Web UI as is.


Fuel-nailgun-agent
------------------

We propose to extend fuel-nailgun-agent with support for multipath devices.
That means, that fuel-nailgun-agent will be able to handle not only physical
block devices, but also /dev/mapper/* and /dev/mpath/* devices - which
will be populated by multipath service.

For example, a node with two HBAs attached to a storage controller with two
ports via a single unzoned FC HBA switch sees four devices: /dev/sda, /dev/sdb,
/dev/sdc, and /dev/sdd. DM-Multipath creates a single device with a
unique WWID (WWN) that reroutes I/O to those four underlying devices
according to the multipath configuration.

We suggest adding logic in fuel-nailgun-agent to discover and report multipath
topology in following format:

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
nailgun as a separate block device. Metadata for not multipatch devices will
not be changed.

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
devices.

Data model
----------

None

REST API
--------

None

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

Alternative solution is following fuel-nailgun-agent should be extended to
provide parsed output from commands

  .. code-block:: text

    `dmsetup info -c --nameprefixes --noheadings --rows -o name,uuid,blkdevname,blkdevs_used`
    `udevadm info --query=property --export --name=#{device_name}`

as for discovered block devices. It should be enough to determingite the multipath
configuration on server side.

New version of fuel-nailgun-agent report will look this:

  .. code-block:: json

    {
      "meta":{
      ...
        "disks":{
          "blocks":[
            {
              "removable": "0",
              "size": 53687091200,
              "udev_info":{
                "DEVLINKS":"/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_35e53b2cb5114d80b28b /dev/disk/by-path/pci-0000:00:09.0-scsi-0:0:0:0",
                "DEVPATH":"/devices/pci0000:00/0000:00:09.0/host2/target2:0:0/2:0:0:0/block/sda",
                "MAJOR":"8",
                "MINOR":"0",
                "ID_BUS": "scis",
                "ID_MODEL": "Toshiba",
                ...
              },
            },...
          ],
          "dmsetup_info": {
            "DM_NAME":"0QEMU    QEMU HARDDISK   35e53b2cb5114d80b28b",
            "DM_UUID":"mpath-0QEMU    QEMU HARDDISK   35e53b2cb5114d80b28b",
            "DM_BLKDEVS_USED":"sdb,sda"
            "DM_SUBSYSTEM":"mpath"
          }
        }
      }
    }

Reports in new format will be handled by url "/api/v1/nodes/agent/".
To handle new report format API microversion **v1.1** will be pointed in HTTP
handlers, like OpenStack components do. New API handler should be available to
receive and process data about nodes disks from the fuel-nailgun-agent.

Only disk part of report will be changed. Received data will be processed and
stored as part of Node DB instance metadata in the format compatible with
current Nailgun UI. Output of REST API will not be changed.


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

Work Items
==========

- extend fuel-ui to show multipath disks
- add packages related to multipath support into default ubuntu-bootstrap image
- add fuel-nailgun-agent support for correct multipath disk discovery
- add to nailgun support for correct serialization of disks delivered by multipath


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
