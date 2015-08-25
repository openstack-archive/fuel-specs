..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================
Supporting IPv6 in Fuel
=======================

Fuel should not depend on IPv4 for provisioning an OpenStack
deployment. This spec documents what Fuel should add support for, and
also links to work in other OpenStack components for supporting IPv6
networking.


--------------------
Problem description
--------------------

It's 2015 - we should support IPv6 in Fuel.

----------------
Proposed changes
----------------


Web UI
======

* Verify that IPv6 is able to be accepted in all networking fields.


Nailgun
=======

* Verify that IPv6 networking information can be passed to
  provisioning.

Data model
----------

* No changes, data model for ip addresses already uses a column type
  that can store IPv6 addresses. 

REST API
--------

* None, only parts of the payload in the API will change 

Orchestration
=============

General changes to the logic of orchestration should be described in details
in this section.


RPC Protocol
------------

* Only payload changes

Fuel Client
===========

* Support IPv6 addresses in all IP address fields (if it does not
  already).

Plugins
=======

* TBD

Fuel Library
============

* Configure all services run through xinetd to use IPv6 networking
* Update Fuel-Library to configure Cobbler using IPv6 networking
* Determine if dnsmasq supports IPv6 extensions for DHCPv6 options
* Swap out dnsmasq for isc-dhcpd (due to lack of `support for IPv6 extensions <https://wiki.ubuntu.com/UEFI/SecureBoot-PXE-IPv6#DHCPv6_.28isc-dhcp-server.29>`_
* Deploy a Neutron plugin that supports IPv6 
     * Determine if Open vSwitch has support for IPv6 as the tunnel
       protocol. It may only support using VLANs.
     * Determine if Linuxbridge has support for IPv6 as the tunnel
       protocol if deploying with VXLAN. It may only support using VLANs.

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

* Upgrades will be impacted dnsamsq is replaced with isc-dhcpd

---------------
Security impact
---------------

* Ensure that firewalling for IPv6 stacks is enabled where apropriate.

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

Users will be able to provision OpenStack clusters in deployments that
do not have IPv4 networking.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

TBD

----------------
Developer impact
----------------

None

--------------------------------
Infrastructure/operations impact
--------------------------------

CI systems within Mirantis for Fuel will require IPv6 networking
configured, in order to test.

--------------------
Documentation impact
--------------------

* Document IPv6 support

--------------------
Expected OSCI impact
--------------------

TODO

--------------
Implementation
--------------

Assignee(s)
===========

* scollins

Work Items
==========

* Enable PXE booting over IPv6

* Change networking provisioning to deploy Neutron with only IPv6
  subnets

* Configure underlay networking to use IPv6 only - for example
  configure open vSwitches to use IPv6 for tunnels between hypervisors
  and controllers.


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

* Requires a lab that has IPv6 networking configured.

Acceptance criteria
===================

TBD


----------
References
----------

* `Open vSwitch - Add support for IPv6 for tunneling <https://www.mail-archive.com/dev%40openvswitch.org/msg46017.html>`_
