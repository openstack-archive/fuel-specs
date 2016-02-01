..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Support to start,stop,reset node via IPMI
================================================

https://blueprints.launchpad.net/fuel/+spec/ipmi-driver

Driver should be able to start/stop/reset node(via IPMI)


--------------------
Problem description
--------------------

Baremetal nodes are not supported now but we have to do real testing
for those type of nodes. We have to extend fule-devops
in order to add new driver and provide similar interface
like for libvirt nodes.

As a developer I want to run system tests on baremetal nodes
to check some hardware-related issues, run performance tests and so on.
As a QA engineer I want to perform system tests on baremetal nodes
on a regular basis in an automated way, increasing test cases coverage
by getting much more test results from different environmets
and sharing the results on CI instead of doing the same by hands.

----------------
Proposed changes
----------------

Fuel-devops tool should be able to use the IPMI driver
with specified access parameters for each baremetal node,
getting environments with kvm or/and baremetal types of nodes.

Fuel-devops is going to be extended in order to support new features like
 - start/stop/reset node(via IPMI)
 - set boot device
 - get power info
 - get usefull info via IPMI
 - TODO: mount iso image(via PXE for example)

New driver shall be inherited from DriverBase.
New Node class shall be inherited from NodeBase.
Yaml config shall be provided as well. Example is shown below:

template:
    groups:
      name: rack-01
        driver:
          name: devops.driver.baremetal.ipmi_driver

        nodes:
          name: admin        # Custom name of baremetal for Fuel admin node
            role: fuel_master  # Fixed role for Fuel master node properties
            params:
              ipmi_user: mosqa
              ipmi_password: password
              ipmi_previlegies: OPERATOR
              ipmi_host: c1-kvm.host-test.com
              ipmi_lan_interface: lanplus
              ipmi_port: 623
              impi_cmd: ipmitool

Web UI
======

None


Nailgun
=======

None

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

None

------------
Alternatives
------------

We dont have alternatives now untill manual management.

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

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

This feature should be described in the documentation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Kirill Rozin <krozin@mirantis.com>

Other contributors:
  QA section: Kirill Rozin <krozin@mirantis.com>

Mandatory design reviewer:
  Dennis Dmitriev <@mirantis.com>,
  Anton Studenov <astudenov@mirantis.com>
  Nastya Urlapova <aurlapova@mirantis.com>
  Timur Nurlygayanov <tnurlygayanov@mirantis.com>


Work Items
==========

* baremetal/ipmi_driver.py: new file is going to be added in order to support
          IPMI functionality desribed above.
* ipmi/: This folder is going to be deprecated in next time

Dependencies
============

ipmitool shall be installed upfront

------------
Testing, QA
------------

Actually need a real testing on different IPMI.
Note: Shall be tested on IPMI SuperMicro at least.

1. Fuel environment is created by fuel-qa tests
   using the devops template with baremetal nodes.
2. Power off by using IPMI driver
3. Power on by using IPMI driver
4. Power reset by using IPMI driver
5. Set PXE boot device


Acceptance criteria
===================
1. Fuel environment has been created by using the devops
   template with baremetal nodes.
2. start/stop/reset node by using IPMI driver
3. Set boot device by using IPMI driver

----------
References
----------

[1] Early Blueprint request:
  (https://blueprints.launchpad.net/fuel/+spec/devops-bare-metal-driver)
