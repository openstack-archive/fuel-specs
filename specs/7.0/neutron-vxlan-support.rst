..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Neutron VXLAN Tenant Networking Support
==========================================


Problem description
===================

For a customer, we need to provide the best network data plane performance
possible. Multiple tunneling protocols exist to enable an L2 over a L3
overlay network: GRE, STT, and VXLAN. Fuel supports GRE tunneling, but
the performance of GRE overlay networks has been shown to be
deficient. VXLAN tunneling has more promising performance
characteristics, with hardware vendors developing chipsets that can
provide hardware acceleration for the protocol, and the industry is
beginning to settle on the VXLAN protocol as the protocol for SDN
solutions. This engineering proposal outlines steps needed to take in
Fuel to enable VXLAN tunneling for the tenant data plane.


Proposed change
===============

OpenStack Networking (neutron) already supports VXLAN as one of the
tunneling protocols for tenant networks. Most of the work will be
focused on enabling support inside Fuel’s components to select this
tunnel protocol for configuration and deployment, as well as some
UI/UX work to make the option available to the user when configuring
networking.


Alternatives
------------

None

Data model impact
-----------------

Changes to the Nailgun database will be made, to update the supported
segmentation types.


REST API impact
---------------

None

Upgrade impact
--------------

An upgrade script will be written to update the Nailgun database.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Performance Impact
------------------

This change may have positive performance implications on the tenant networking
data plane.

Plugin impact
-------------

Due to the structure of the Networking wizard in the Web UI,
it is not possible to add VXLAN as a fuel plugin, since Fuel plugins
cannot currently modify the Networking wizard, to add new options.

Other deployer impact
---------------------

Developer impact
----------------

None

Infrastructure impact
---------------------

None

Implementation
==============



Assignee(s)
-----------

scollins

Work Items
----------

* Fuel-Web UI changes to present VXLAN (or just TUN instead of GRE) as a
  segmentation type
* Database changes to support VXLAN(TUN) as a segmentation type
* Changes to Nailgun and provisioning layer to deploy and configure
  Neutron with the appropriate settings to support VXLAN
* Fuel-library changes to add vxlan as supported segmentation type. In
  neutron_network type (actually only flat, vlan, local, gre and l3_ext
  are supported)to be able to create a vxlan network
* python-fuelclient changes to add vxlan(tun) as a possible value
  to --net-segment-type argument

Dependencies
============

* https://blueprints.launchpad.net/fuel/+spec/combine-tun-and-vlan-cases

Testing
=======

Tests will be created to exercise the UI interactions for the new
segmentation option, as well as unit tests for the new configuration
deployment.

Documentation Impact
====================

Documentation will be written to document the support for VXLAN in the
new release of Fuel.

References
==========

* http://lists.openstack.org/pipermail/openstack-dev/2015-May/065076.html
