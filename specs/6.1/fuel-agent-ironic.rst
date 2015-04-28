..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================
Deploy Baremetal with Ironic and Fuel Agent
===========================================

https://blueprints.launchpad.net/fuel/+spec/baremetal-deploy-ironic

This blueprint introduces baremetal deploy with Ironic and Fuel Agent.
Fuel Agent will be the one supported deploy agent for Ironic in MOS.
This spec describes changes for Ironic at first.


Problem description
===================

There is custom ramdisk in Fuel, it contains extended set of certified drivers
and Fuel agent inside. Fuel Agent is able to deploy baremetal and supports
features which are needed for customers (extended partitioning, software RAID,
LVM etc.)
Makes sense to use this ramdisk in MOS.


Proposed change
===============

A deploy driver for Fuel Agent should be implemented. This driver should be
packed in a separate package file and installed into Ironic drivers namespace.
Driver will use standard ipmitool mechanism for power and management
interfaces.

**Deploy a node with Fuel Agent driver workflow:**

::

                        DHCP
            Ironic      manager      TFTP        Node      Swift
              +           +           +           +          +
     add node |           |           |           |          |
    +-------> |           |           |           |          |
              |           |           |           |          |
     deploy   |           |           |           |          |
    +-------> | create temp URLs      |           |          |
              +--------------------------------------------->|
              |           |           |           |          |
              | create PXE config     |           |          |
              +-----------+---------> |           |          |
              |           |           |           |          |
              |     power on          |           |          |
              +-----------+---------------------> |          |
              |           |           |           |          |
              |           |           | PXE boot  |          |
              |           |           +---------> |          |
              |           |           |           |          |
              | "I am ready and my IP=a.b.c.d"    |          |
              |  to vendor_passthru               |          |
              | <---+-----+-----------+-----------+          |
              |           |           |           |          |
              | ssh /bin/deploy tmp/data.json     |          |
              +-----------+-----------+---------> |          |
              |           |           |           |          |
              |           |           |     +-----+------+   |
              |           |           |     | deployment |<--+ Image
              |           |           |     +-----+------+   |
              |        power reboot   |           |          |
              +-----------+---------------------> |          |
              +           +           +           +          +


#. Administrator creates a node via Ironic CLI and sets driver properties.

#. Nova send instance data and trigger deploy via Ironic API.

#. The driver creates Swift temp url for Glance instance image.

#. The driver gets disks layout information (partitions, lvm, etc.) stored in
   Glance image meta properties.

#. The driver configures TFTP options for port created by Nova.

#. Node loads ramdisk with Fuel Agent from TFTP server via PXE.

#. Fuel Agent ramdisk calls vendor_passthru API method, sends node's status
   ("ready" or "error" together with an error message) and node's IP address.
   Vendor methods are to be added to public_routes.

#. The driver connects to ramdisk system via SSH. Ramdisk for typical use case
   has ssh credentials defined on build time.

#. The driver merges image url and disks layout information in one json file.

#. The driver puts this file to /tmp directory on deploy ramdisk.

#. The driver starts Fuel Agent executable entry point (e.g. /bin/deploy).

#. Fuel Agent gets an image from Swift and does deploying.

#. The driver waits for the completion of Fuel Agent's process and uses
   exit code and stderr for errors handling. Conductor's worker is blocked
   until deployment is done.

#. The driver does reboot of a node.


Alternatives
------------

* ironic-python-agent

* iSCSI deploy (PXE driver)

Data model impact
-----------------

None for Ironic, Ironic input data driver for Fuel Agent.

REST API impact
---------------
None for Ironic.

Upgrade impact
--------------
None for Ironic.

Security impact
---------------

When a node is deploying it is accessible via defined SSH credentials.

Notifications impact
--------------------
None for Ironic.

Other end user impact
---------------------

User triggers baremetal deploy via Nova Horizon/CLI tools.
User should set disks layout information before deploy in Glance image meta
properties.

Performance Impact
------------------

Fuel Agent does image downloading and deploy of a node independently, therefore
load of conductor node will be insignificant.
One conductor's worker per a node is required. Most of the time a worker waits
in blocking state for the completion of deploy process.

Other deployer impact
---------------------

For Ironic:
These parameters must be provided with driver_info:

  * ``deploy_kernel`` - UUID (from Glance) of the deploy kernel.
  * ``deploy_ramdisk`` - UUID (from Glance) of the deploy ramdisk.
  * ``fuel_deploy_script`` - path to Fuel Agent executable entry point.
  * ``fuel_username`` - SSH username for ramdisk.
  * ``fuel_key_filename`` - name of SSH private key file.
  * ``fuel_ssh_port`` - SSH port.

Developer impact
----------------
None for Ironic

Infrastructure impact
---------------------

Introduces new package: Fuel Agent deploy driver for Ironic.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
    yuriyz (Ironic driver)

Work Items
----------

* Fuel Agent changes for Ironic (input data driver, input data from http url,
  notifications).

* Implement Fuel Agent deploy driver.


Dependencies
============
None for Ironic.


Testing
=======

Hardware servers with IPMI support needed for testing.
Rally test scenarios should be created.

Documentation Impact
====================

Will document the usage of this driver.

References
==========

* Fuel Agent code:
  https://github.com/stackforge/fuel-web/tree/master/fuel_agent

