..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
Selectable offloading type
==========================

Include the URL of your launchpad blueprint:
https://blueprints.launchpad.net/fuel/+spec/selectable-offloading-type

This blueprint describes a way to select offloading types what are
supposed to be disabled instead of to disable offloading for
physical interface at all.

Problem description
===================

In current implementation it is not possible to control offloading
type for physical interface. We can only disable offloading for
physical interface at all. But, for some reasons it may be important
to choose specific type of offloading. Also, it provides more
flexibility for nodes network configuration.

Proposed change
===============

Firstly, it will be necessary to extend nailgun agent to collect
available offloading types for each node's interfaces during
the bootstrap stage. Currently we use ruby rethtool gem to
collect node's interfaces data. But, for some reasons, this library
doesn't provide offloading related interface information. So,
we can collect necessary information by parsing cli output of
ethtool for dedicated interface.

For example, ethtool provides following cli output for interface's
features::

  udp-fragmentation-offload: off [fixed]
  generic-segmentation-offload: on
  generic-receive-offload: on
  large-receive-offload: off [fixed]
  rx-vlan-offload: on
  tx-vlan-offload: on
  ntuple-filters: off [fixed]

In this case we should collect all offloading types what have not
'fixed' attribute during the bootstrap stage, alter on/off offloading
options to true/false to get suitable format for puppet handling on
the deployment stage, and then transform formatted data to Hash object
and sent it to the Nailgun server.
Nailgun's NodeNICInterface and NodeBondInterface data models should be
extended with Json field containing array of supported offloading types
to properly receive nailgun's agent data.
Extra 3-state checkbox for each incoming offloading type
should be added to node's interfaces UI tab to
configure offloading types for physical interfaces/bonds.
It may be hidden by default, and will be invoke in case if user
touch specific button.
Fix frontend to calculate available modes for bond interfaces
properly. UI should calculate intersection (or union) of offloading
types available when setup is being performed for a set of nodes
(every of which could have different offloading types supported for
the NICs with same names).
Currently, selectable offloading types are already supported by
puppet manifests. It will be enough to generate proper Hash field
via Nailgun and deliver it to the puppet manifests as it is.

Also, I want to add several examples regarding to changes in
node's yaml file and how to nailgun should serialise data to make
it handled properly via puppet.
We have two types of interfaces from the API/CLI/UI side of view:
physical interfaces and bond interfaces ( if we are not going to hack
transformations section using CLI ). The offloading types tuning is
similar for physical and bond interfaces in the fact that we have the
identical ethtool injection format for both cases.

For example::

  ethtool:
    offload:
        rx-checksumming:              true (or false)
        tx-checksumming:              true (or false)
        tcp-segmentation-offload:     true (or false)
        udp-fragmentation-offload:    true (or false)
        generic-segmentation-offload: true (or false)
        ....

In case if we are going to change offloading configuration for
physical interface we should add corresponding offload option
as the additional property of the interface object:

For example::
  ['network_scheme']['interfaces']['#interface_name'][ethtool]

In case if we are going to change offloading configuration for
bond interface we should add corresponding offload option
as the additional property of the bond interface object:

For example::
  ['network_scheme']['transformations'][#action_id]\
    ['#interface_properties'][ethtool]

It means that you should find needful #action_id using bond name
if you want to change it's offloading configuration. This change
will be applied for all bonded physical interfaces.

Alternatives
------------

None

Data model impact
-----------------

Nailgun's NodeNICInterface and NodeBondInterface data models should
be extended with Json field containing array of supported offloading
types. This field will be empty initially, and it's supposed to be filled
using nailgun agent data during the bootstrap stage for physical interfaces.
In case of bond interface this property will be filled during the environment
configuration process.

REST API impact
---------------

NodeValidator should be extended to handle incorrect node's offloading
types data.

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

User will be able to select physical interfaces offloading type via UI and CLI.

Performance Impact
------------------

Network performance may be increased due to more flexible offloading
types configuration.

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

Nailgun's NodeNICInterface data model will be extended with
new Json field.

Infrastructure impact
---------------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Valyavskiy Viacheslav <slava-val-al>

Work Items
----------

* Extend nailgun agent to collect available offloading
  types for each node's interface during the bootstrap
  stage
* Extend Nailgun's NodeNICInterface data model to add
  one more Json field containing array of supported offloading
  types
* Add 3-state checkbox for each incoming offloading type
  should be added to node's interfaces UI tab to
  configure offloading types for physical interfaces/bonds
* Fix frontend to calculate available modes for bond
  interfaces properly

Dependencies
============

None

Testing
=======

Devops tool should be extended to deploy environment with custom
offloading type values for the virtual interfaces.

Documentation Impact
====================

Ability to control physical interface's offloading type should be
documented in Fuel Deployment Guide.

References
==========

None
