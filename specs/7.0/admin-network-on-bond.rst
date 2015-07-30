..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================
Admin network on bond
=====================

https://blueprints.launchpad.net/fuel/+spec/admin-network-on-bond

This blueprint describes a way to bond admin interface using non-lacp
bond modes.

Problem description
===================

In some cases user wants to bond admin interface. It is not possible
for FUEL 6.0 and earlier release using UI. It is possible to bond admin
interface via API and CLI, but in this case there is a problem with
determining admin interface mac address during the provisioning stage.
This is Nailgun provisioning serializer issue. If admin interface was
bonded, serializer returns mac of the bond interface(empty value) and
it breaks provisioning process.

Proposed change
===============

Nailgun provisioning serializer should be fixed to handle case when
admin interface is bonded. Serializer may return first bonded slave
interface mac address instead bond mac address. Lacp modes should
be denied for admin interface via Nailgun API(add validation rules).

Additional `pxe` db field should be added into the nic interfaces db model
to properly track initial admin interface(node's interface what was used for
node's registering in Nailgun API). It necessary for identifying pxe
interface if user decide to disassemble bond which includes admin interface.
This property will be sent in registration request from Nailgun agent.
Nailgun agent will identify `pxe` interface by:

* ip address ( if some of node's interfaces IPs belong to the same network
  as IP for Nailgun API which is taken from configuration file
  "/etc/nailgun-agent/config.yaml")
* mac address ( Nailgun agent does already have an ability to identify
  interface which belongs to network with default gateway; it helps to
  identify admin interface during the bootstrap stage ) in case if we are
  using multiple node groups

This property will be automatically calculated in the Nailgun(on the data from
Nailgun agent) and user will not be able to change it.

Possibility to bond admin interface via UI should be added. Available
bond modes for admin interface in UI should be limited(only non-lacp modes).
This limitation will be described in metadata which describes bonding
settings in following way::

      bonding:
          linux:
            mode:
              - values: ["balance-rr", "active-backup"]
              - values: ["802.3ad"]
                condition: "'experimental' in version:feature_groups or
                            interface:pxe == false"
              - values: ["balance-xor", "broadcast", "balance-tlb",
                         "balance-alb"]
                condition: "'experimental' in version:feature_groups"

"interface:pxe == false" condition indicates interfaces which are able to be
bonded using lacp mode. This flag calculation will be based on interfaces's
property : `pxe`.

It is proposed to use only non-lacp bond modes for admin interface
due to complex and unclear implementation in regarding to following reasons:

* During the pre-provisioning (bootstrap) and provisioning stages the switch
  sees both ports up and may attempt to send traffic on both, depending on
  load balancing algorithms. This behaviour may crush PXE booting and OS
  installing processes.
* It's not clear when lacp bonding should be enabled on the node(before the
  OS installation, after OS installation, etc.)

But, there are several switches models what support fallback to non-bond mode
if LACP session did not established. So, It was decided to allow using of lacp
mode for admin interface in experimental mode. UI condition "'experimental' in
version:feature_groups" describes it.


Alternatives
------------

None

Data model impact
-----------------

Additional `pxe` boolean db field should be added into the node_nic_interfaces
DB model.

REST API impact
---------------

Additional API validation rules should be added to prevent passing of lacp
bond mode for admin interface. Also API will be extended with rules preventing
assignment of admin network to non-pxe interface.

Upgrade impact
--------------

Additional `pxe` field will be injected into nic interfaces db model and set
to True for interfaces which belong to admin network during the database
migration procedure.
Also Nailgun server code will be fixed to properly calculate pxe interface
in case if we have no `pxe` property set for any interface (to support old
Nailgun agent versions). Calculation will be based on 'node.mac' property
which is present in old agent's versions.
Admin interface's bonding is not allowed for old releases, so metadata for
old releases will be updated to not allow any bonding mode for `pxe`
interface.

Updated metadata example::

      bonding:
          linux:
            mode:
              - values: ["balance-rr", "active-backup", "802.3ad"]
                condition: "interface:pxe == false"
              - values: ["balance-xor", "broadcast", "balance-tlb",
                         "balance-alb"]
                condition: "interface:pxe == false and "
                           "'experimental' in version:feature_groups and "

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

User will be able to bond admin interface via UI, API and CLI
using non-lacp modes.

Performance Impact
------------------

None

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Valyavskiy Viacheslav <slava-val-al>

Work Items
----------

* Fix provisioning serializer to proper handle case when admin interface is
  bonded
* Deny lacp modes for admin interface via Nailgun API
* Deny to reassign admin network on non `pxe` interface via Nailgun API
* Add possibility to bond admin interface via UI
* Limit bond modes for admin interface via UI
* Fix Nailgun to stick `pxe` property to admin interface during the bootstrap
  stage
* Fix Nailgun agent to calculate `pxe` property for interfaces

Acceptance criteria
-------------------

User is able to bond admin interface using non-lacp bond modes.
User is able to bond admin interface using lacp bond modes in experimental
mode.

Dependencies
============

None

Testing
=======

It is necessary to improve devops to support tests
with admin interface bonding.


Documentation Impact
====================

Extend Deployment Guide with following items:
* add new possible network topologies
* how to prepare an env for installation with bonded admin interface
* how to deploy OpenStack env with bonded admin interface


References
==========

- https://blueprints.launchpad.net/fuel/+spec/admin-network-on-bond
