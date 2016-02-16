..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================
Support for SR-IOV
==================

https://blueprints.launchpad.net/fuel/+spec/support-qos

Administrator should be able to enable Network QoS for OVS and SR-IOV ML2
drivers. Also administrator should be able to assign policy creation rights to
a user or set up the policies on user behalf. Policy should effectively control
the network traffic on per virtual interface basis.

--------------------
Problem description
--------------------

QoS is defined as the ability to guarantee certain network requirements like
bandwidth, latency, jitter, and reliability in order to satisfy a SLA between
an application provider and end users. This feature is already implemented in
OpenStack Liberty, but requires simple changes in puppets to make it enabled
by default in MOS 9.0.

This feature has several restrictions at the moment:

* Compatible only with two ML2 backends: OVS and SR-IOV

* Only egress bandwidth limit rules are supported

----------------
Proposed changes
----------------

Enabling QoS requires changes in Neutron configuration files:

On server side:

* Enable qos service in service_plugins.
* Set the ‘message_queue‘ driver for ‘notification_drivers‘ in [qos] section.
* For ml2, add ‘qos’ to extension_drivers in [ml2] section.

On agent side (OVS):

* Add ‘qos’ to extensions in [agent] section.

Web UI
======

None

Nailgun
=======

Nailgun-agent
-------------

None

Bootstrap
---------

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

Only payload changes

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

See items in Proposed changes section.

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

By default QoS policies and rules will be managed by the cloud administrator,
that makes the tenant unable to create specific qos rules, or attaching
specific ports to policies.

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

Additional Neutron CLI commands will be enabled as it's described here:
http://specs.openstack.org/openstack/neutron-specs/specs/liberty/qos-api-extension.html#other-end-user-impact

------------------
Performance impact
------------------

Minimal. Additional messaging calls will be created during updating and
creating Neutron networks and ports.

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

TBD

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  skolekonov

Mandatory design review:
  yottatsa

Work Items
==========

* Enable QoS configuration in fuel-library
* Manual testing

Dependencies
============

None

------------
Testing, QA
------------

* Manual API/CLI cases for the configuring QoS rules and polices
* Manually test that QoS rules are applicable to OVS and SR-IOV backends
* Performance testing

Acceptance criteria
===================

User should be able to create, update delete QoS rules for OvS and SR-IOV
ML2 drivers.

----------
References
----------

* `Using QoS functionality
  <http://docs.openstack.org/liberty/networking-guide/adv-config-qos.html>`_
