..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
Selectable offloading type
==========================

Include the URL of your launchpad blueprint:
https://blueprints.launchpad.net/fuel/+spec/selectable-offloading-type

This blueprint describes a way to control offloading types what is
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
availiable offloading  types for each node's interfaces during
the provisioning stage. Currently we use ruby rethtool gem to
collect node's interfaces data. We can extend current approach
to collect non-fixed node's interfaces offloading types and sent
those data to the Nailgun server.
Nailgun's NodeNICInterface data model should be extended with
Json field containing array of supported offloading types to properly
receive nailgun's agent data.
Extra checkbox should be added to node's interfaces UI tab to
configure offloading types for physical interfaces/bonds.
Fix frontend to calculate availiable modes for bond interfaces
properly. In case if we want to set offloading type for bond
interface, availiable mode set should be equal with
intersection of availiable physical interfaces offloading types
what were combined to current bond interface.
Currently, selectable offloading types are already supported by puppet manifests. It will
be enough to generate proper Hash field via Nailgun and deliver
it to the puppet manifests as it is.

Alternatives
------------

None

Data model impact
-----------------

Nailgun's NodeNICInterface data model should be extended with
Json field containing array of supported offloading types. This
field will be empty initially, and it's supposed to be filled
using nailgun agent data during the provisioning stage.

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

* Extend nailgun agent to collect availiable offloading
  types for each node's interface during the provisioning
  stage
* Extend Nailgun's NodeNICInterface data model to add
  one more Json field containing array of supported offloading
  types
* Add checkbox to node's interfaces UI tab to configure
  offloading types for physical interfaces/bonds
* Fix frontend to calculate availiable modes for bond
  interfaces properly
* Fix puppet manifests to support selective offloading
  type for interfaces

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
