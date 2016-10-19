..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================
Implement Security Groups switch in Fuel
========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-security-groups-switch

It is required to implement a switch in fuel to enable Security Groups.
IPTables functionality should be used by default.

-------------------
Problem description
-------------------

Until now, only one firewall was implemented in OpenStack's Neutron project:
an iptables-based firewall. We want replace the firewall driver for Security
Groups to be deployed as rules for OVS. Therefore, we should have a flag in
Fuel for enabling security groups.

----------------
Proposed changes
----------------

We should add checkbox to Settings Tab by changing of openstack.yaml as
described in the :ref:`Data model <data-model>` section.

Web UI
======

None

Nailgun
=======

* Change openstack.yaml as  described in the :ref:`Data model <data-model>`
  section.

.. _data-model:

Data model
----------

* openstack.yaml changes::

    attributes_metadata:
      editable:
        common:
          security_groups:
            value: "false"
            label: "Enable Security Groups"
            description: "IPTables functionality is used by default"
            group: "security"
            weight: 20
            type: "checkbox"

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

Performance impact is not expected.

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

The user guide should be updated according to the described feature.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Anastasia Balobashina <atolochkova@mirantis.com>

Mandatory design review:
  Vladimir Eremin <veremin@mirantis.com>

Work Items
==========

* Change openstack.yaml as described in the :ref:`Data model <data-model>`
  section.
* Test manually.
* Verify the :ref:`acceptance criteria <acceptance-criteria>`.

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

.. _acceptance-criteria:

Acceptance criteria
===================

Flag in Fuel UI is available to easily enable OVS based security groups.

----------
References
----------

None
