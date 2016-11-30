..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================
Security Groups support for Neutron/OVS
=======================================

https://blueprints.launchpad.net/fuel/+spec/security-groups-support-for-ovs

It is required to implement a radio button in Fuel to switch a Neutron Firewall
driver. `IPTables-based Firewall Driver` and `Open vSwitch Firewall Driver`
should be able. IPTables functionality should be used by default.

-------------------
Problem description
-------------------

Until now, only one firewall was implemented in OpenStack's Neutron project:
an iptables-based firewall. As long as now there is a second option to natively
utilize OVS for implementing security groups instead of the former
iptables/linux bridge solution we should have an attribute in Fuel for
selecting firewall driver.

----------------
Proposed changes
----------------

We should add a cluster attrubute for selecting firewall driver and apply
appropriate settings in nova and neutron configs.

Web UI
======

None

Nailgun
=======

* Change openstack.yaml as described in the
  :ref:`Data model<security-groups-data-model>` section.
* Add the security_groups attribute to the white list for the installation
  info.

.. _security-groups-data-model:

Data model
----------

* openstack.yaml changes::

    attributes_metadata:
      editable:
        common:
          security_groups:
            value: "iptables_hybrid"
            values:
              - data: "openvswitch"
                label: "Open vSwitch Firewall Driver"
                description: "Choose this driver for OVS based security groups implementation."
              - data: "iptables_hybrid"
                label: "IPTables-based Firewall Driver (No firewall for DPDK case)"
                description: "Choose this driver for iptables/linux bridge based security groups implementation."
            label: "Security Groups"
            group: "security"
            weight: 20
            type: "radio"

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

Fuel-library should apply firewall settings in neutron config.
* neutron/plugins/ml2/openvswitch_agent.ini: set OVS firewall driver in the
`securitygroup` section.
**If IPTables-based Firewall Driver was chosen in dpdk case,**
**security groups should be disabled.**

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

Data migration should be prepared according to the changes in data models.
After upgrade procedure, a Neutron Firewall driver switching is forbidden.
An appropriate warning should be added to release notes.

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

Performance impact is not expected.

-----------------
Deployment impact
-----------------

Rerun the deployment with changing a Neutron Firewall driver is forbidden.
An appropriate warning should be added to release notes.

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

The user guide should be updated according to the described feature.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Anastasia Balobashina <atolochkova@mirantis.com>
  Mikhail Polenchuk <mpolenchuk@mirantis.com>

Mandatory design review:
  Vladimir Eremin <veremin@mirantis.com>

Work Items
==========

* Change openstack.yaml as described in the
  :ref:`Data model <security-groups-data-model>` section.
* Apply firewall settings in neutron and nova configs
* Test manually.
* Verify the :ref:`acceptance criteria <security-groups-acceptance-criteria>`.

Dependencies
============

None

-----------
Testing, QA
-----------

* Test cases for configuring and deployment of environment with the OVS based
  security groups, VLAN/VXLAN segmentation, but without enabled DPDK.
* Test cases for configuring and deployment of environment with the OVS based
  security groups, VLAN/VXLAN segmentation and enabled DPDK.
* Web UI test cases for configuring the OVS based security group.
* Functional testing.
* Performance testing.

.. _security-groups-acceptance-criteria:

Acceptance criteria
===================

* OVS based security group is tested and working with MOS + OVS and MOS +
  OVS/DPDK.
* The OVS performance should be equivalent or better to iptables in kernel at
  1000 VM and 2000 VM scale.
* OVS/DPDK performance should result in no more than 15% performance
  degradation vs no security groups at 1000 VM and 2000 VM scale.
* Scale limit testing: Test the maximum number of flows supported per OVS,
  get a model such that we know when OVS based security groups will fail.
* Default should still utilize iptables as OVS based security groups are new
  and not well tested yet.
* When OVS/DPDK is used on the host OS then we must automatically configure to
  use OVS based security groups. Iptables based security groups do not work
  with OVS/DPDK.
* The radio button in UI to choose a firewall_driver.

----------
References
----------

[0] - http://docs.openstack.org/developer/neutron/devref/openvswitch_firewall.html
