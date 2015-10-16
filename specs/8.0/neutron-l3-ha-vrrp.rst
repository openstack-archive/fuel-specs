..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Example Spec - The title of your blueprint
==========================================

https://blueprints.launchpad.net/fuel/+spec/neutron-vrrp-deployment


The aim of this blueprint is to add High Availability Features on virtual
routers.

High availability features will be implemented as extensions and drivers.
A first driver on the agent side will be based on Keepalived.

A new scheduler will be also added in order to be able to spawn multiple
instances of a same router on many agents for the redundancy.


--------------------
Problem description
--------------------

Currently we are able to spawn many l3 agents, however each l3 agent is a SPOF.
If an l3 agent fails, all virtual routers of this agent will be lost, and
consequently all VMs connected to these virtual routers will be isolated from
external networks and possibly from other tenant networks. Existing
rescheduling has one big issue - thousands of routers take hours to finish the
rescheduling and configuration process.


----------------
Proposed changes
----------------

The idea of this blueprint is to schedule a virtual router to at least two
l3 agents, but this limit could be increased by changing a parameter in the
neutron configuration file.

The current router interfaces management in the l3 agent will be abstracted in
order to introduce the possibility to add drivers for that purpose. As a first
implementation of a driver, an HA Keepalived driver will be added. All the IPs
will be converted to VIPs.

In order to hide the HA traffic from the tenant point of view a HA network
will be added and all the virtual router instances will be connected through a
HA port to this network.

Flows::

         +----+                          +----+        
         |    |                          |    |        
 +-------+ QG +------+           +-------+ QG +------+ 
 |       |    |      |           |       |    |      | 
 |       +-+--+      |           |       +-+--+      | 
 |     VIPs|         |           |         |VIPs     | 
 |         |      +--+-+      +--+-+       |         | 
 |         +      |    |      |    |       +         | 
 |  KEEPALIVED+---+ HA +------+ HA +----+KEEPALIVED  | 
 |         +      |    |      |    |       +         | 
 |         |      +--+-+      +--+-+       |         | 
 |     VIPs|         |           |         |VIPs     | 
 |       +-+--+      |           |       +-+--+      | 
 |       |    |      |           |       |    |      | 
 +-------+ QR +------+           +-------+ QR +------+ 
         |    |                          |    |        
         +----+                          +----+ 


Web UI
======

In section Neutron Advanced Configuration we need a checkbox for enabling L3
HA. This checkbox cannot be enabled if DVR is turned on.


Nailgun
=======

General changes to the architecture, tasks and encapsulated business logic
should be described here.

Data model
----------

None

REST API
--------

No FUEL REST API changes.


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

Fuel Client is a tiny but important part of the ecosystem. The most important
is that it is used by other people as a CLI tool and as a library.

This section should describe whether there are any changes to:

* HTTP client and library

* CLI parser, commands and renderer

* Environment

It's important to describe the above-mentioned in details so it can be fit
into both user's and developer's manuals.


Plugins
=======

Plugins are ofter made by third-party teams. Please describe how these changes
will affect the plugin framework. Every new feature should determine how it
interacts with the plugin framework and if it should be exposed to plugins and
how that will work:

* Should plugins be able to interact with the feature?

* How will plugins be able to interact with this feature?

* There is something that should be changed in existing plugins to be
  compatible with the proposed changes

* The proposed changes enable or disable something for new plugins

This section should be also described in details and then be put into the
developer's manual.


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

TODO


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

HA L3 is based on Keepalived(VRRP protocol) which gives the following features:
Configuration determines default, admin can overrule

* Works within tenant networks
* Failover independent from RPC layer
* Expected to be quicker than rescheduling
  (Rescheduling - 1 router - 5 sec, then linear growth with number of routers
   Rough failover time: single router - 7-8 sec, 30 - 10 sec)



-----------------
Deployment impact
-----------------

Since this implementation relies on Keepalived, Keepalived will have to be
installed on each l3 node. The required version of Keepalived is the version
1.2.10 in order to have the IPV6 support. Safe versions:1.2.13,>1.2.16


----------------
Developer impact
----------------

None


--------------------------------
Infrastructure/operations impact
--------------------------------

None

--------------------
Documentation impact
--------------------

Ability to enable L3 HA support in Neutron should be documented in Fuel
Deployment Guide.


--------------------
Expected OSCI impact
--------------------

TODO
Expected and known impact to OSCI should be described here. Please mention
whether:

* There are new packages that should be added to the mirror

* Version for some packages should be changed

* Some changes to the mirror itself are required


--------------
Implementation
--------------

Assignee(s)
===========


Primary assignee:
  Ann Kamyshnikova <akamyshnikova>

Other contributors:
  Sergey Kolekonov <skolekonov> (DE) Kristina Kuznetsova <kkuznetsova> (QA)

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


------------
Testing, QA
------------

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly.

If there are firm reasons not to add any other tests, please indicate them.


Acceptance criteria
===================

Please specify clearly defined acceptance criteria for proposed changes.


----------
References
----------

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
