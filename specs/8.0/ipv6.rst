..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Supporting IPv6 in Fuel and MOS
===============================

Fuel and MOS should not depend on IPv4 for provisioning an OpenStack
deployment. This spec documents what Fuel should add support for, and
also links to work in other OpenStack components for supporting IPv6
networking.

--------------------
Problem description
--------------------

It's 2015 - we should support IPv6 in Fuel.

Fuel should support the following scenario:

A deployer who has a rack of gear that he wants to provision, but does
not want to deploy IPv4 networking *at all*. Instead, the deployer
wants to build an IPv6 only OpenStack installation - and the bare
metal nodes will use DHCPv6 and PXE boot, instead of the normal
DHCPv4 and PXE boot.

MOS will need to support IPv6-enabled tenant and provider networking scenarios.
For tenant networking, customer could either provide pool of prefixes or setup 
prefix delegation DHCPv6 server on their side.

Fuel will also need to provision all storage, control, and tenant
networks as IPv6 only networks.

----------------
Proposed changes
----------------

* Stage 1: Add ability to deploy MOS that provide IPv6 services for OpenStack
  API and instances.
* Stage 2: Add ability to deploy on dualstack or IPv6-only infrastructure,
  including public/floating, admin, management and storage infrastructure.

Limitation
==========

* Floating IPs and SNAT for IPv6 **will not** be implemented in Neutron.
* DVR has no IPv6 support yet.
* Open VSwitch requires IPv4 for GRE/VxLAN tunnels, which is may required in
  multirack deployments.
* Metadata API services requires any IPv4 subnet to be configured in Neutron.
* Horizon has no support for creating IPv6-enabled security group rules.
* Horizon also has no support for prefix delegation and subnet pools, which
  is required to provide smooth UX.

Implementation details
======================

Web UI
======

* Provide IPv4 and/or IPv6 in all networking configuration.
* Choose which prefix source will be used for tenant networks.

Nailgun
=======

* Verify that IPv6 networking information can be passed to provisioning.

Data model
----------

* Store additional IPv6 network configurations.
* Store subnet-pools or prefix delegation settings.

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

Stage 1
-------

* Modify OCF to configure IPv6 public address
* Configure HAproxy to bind on IPv6 public address
* Setup subnet pool if needed and set default_ipv6_subnet_pool config point
* Setup corresponding dibbler-client package

Stage 2
-------

* Configure all services run through xinetd to use IPv6 networking
* Update Fuel-Library to configure Cobbler using IPv6 networking
* Determine if dnsmasq supports IPv6 extensions for DHCPv6 options
* Swap out dnsmasq for isc-dhcpd (due to lack of `support for IPv6 extensions 
  <https://wiki.ubuntu.com/UEFI/SecureBoot-PXE-IPv6#DHCPv6_.28isc-dhcp-server.29>`_
* Deploy a Neutron plugin that supports IPv6. 
   * Open vSwitch has no support for IPv6 as the tunnel protocol. It only 
     support using VLANs.
   * Determine if Linuxbridge has support for IPv6 as the tunnel
     protocol if deploying with VxLAN. It may only support using VLANs.

Horizon
=======

* Add support for creating IPv6-enabled Security Group Rules.
* Add support for creating pooled subnets.

Neutron
=======

* Blueprint and implement RA to end user's infrastructure side.

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

* Upgrades will be impacted dnsmasq is replaced with isc-dhcpd.

---------------
Security impact
---------------

* Ensure that firewalling for IPv6 stacks is enabled where appropriate.
* Turn off IPv6 autoconfiguration for IPv4-only interfaces.

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

Users will be able to provision and operate OpenStack clusters in deployments 
that do not have IPv4 networking.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

Users could not deploy OpenStack Neutron with VxLAN or GRE with IPv6-only
management network.

----------------
Developer impact
----------------

None

--------------------------------
Infrastructure/operations impact
--------------------------------

As current IPv6 implementation has no SNAT, there are routing should be
provided on end user's data center infrastructure. To provide their 
infrastructure with information about which prefixes is used in tenant networks
OpenStack Neutron provided prefix delegation mechanism. This requires special
setup of end user's DHCPv6 server which is providing prefixes and register 
routing information. It could be extended or replaced with IPv6 Router 
Advertisements that provides information about which prefixes are routed.

--------------------
Documentation impact
--------------------

* Document IPv6 support

--------------------
Expected OSCI impact
--------------------

CI systems within Mirantis for Fuel will require IPv6 networking
configured, in order to test.

Provide dibbler-client 1.0.1.

--------------
Implementation
--------------

Assignee(s)
===========

* yottatsa
* scollins

Work Items
==========

Stage 1
-------

* Store and serialize IPv6 information in nailgun (at least 2w)
* Provide IPv6 CIDR in Public Network settings in fuel-web (2d)
* Configure IPv6 for Corosync in fuel-library (at least 1w)
* Configure IPv6 fencing on br-ex in fuel-library (1d)
* Add IPv6 support in OCF (4d)
* Change networking provisioning to deploy Neutron with IPv6 subnets (2d)
* Build dibbler-client (1d)
* Blueprint on Neutron RA (at least 1w, optionally)
* Unittest nailgun that IPv6 could be set (4d)
* Test fuel-library that IPv6 is assigned (2d)
* BVT with IPv6 (2d)
* OSTF fun test with launch instance and ping6 (2d)

Stage 2
-------

* Enable PXE booting over IPv6
* Configure underlay networking to use IPv6 only - for example
  configure open vSwitches to use IPv6 for tunnels between hypervisors
  and controllers.
* Fix RabbitMQ clustering over IPv6

Dependencies
============

* Partially depends on multirack, as IPv6 is a feature for large customers

------------
Testing, QA
------------

* Requires a lab that has IPv6 networking configured.
* Cover IPv6 services with OSTF and bvt.

Acceptance criteria
===================

* For stage 1: IPv6 subnet could be provided for Public interface. Horizon
  and API should be available on IPv6. IPv6 enabled networks and instances
  could be created.
* For stage 2: There is no need to provide IPv4 addresses to provision 
  OpenStack.

----------
References
----------

* `Support floatingip in IPv6
  <https://blueprints.launchpad.net/neutron/+spec/ipv6-floatingip>`_

* `Support IPv6 router and DVR 
  <https://blueprints.launchpad.net/neutron/+spec/ipv6-router-and-dvr>`_

* `Open vSwitch - Add support for IPv6 for tunneling <https://www.mail-archive.com/dev%40openvswitch.org/msg46017.html>`_

* `DHCPv6 Options for Network Boot  <http://tools.ietf.org/html/rfc5970>`_

* `[Dnsmasq-discuss] Support for RFC5970 - DHCPv6 Options for Network Boot <http://lists.thekelleys.org.uk/pipermail/dnsmasq-discuss/2015q3/009802.html>`_

* `Deploying and Operating an IPv6-only Openstack Cloud <http://sched.co/49sH>`_

* `compute port lose fixed_ips on restart l3-agent if subnet is prefix 
  delegated <https://bugs.launchpad.net/neutron/+bug/1505316>`_

* `Support metadata service with IPv6-only tenant network
  <https://bugs.launchpad.net/neutron/+bug/1460177>`_

* `Magic thing to make old Erlang stuff work in IPv6-only networks
  <https://github.com/yandex/inet64_tcp>`_
