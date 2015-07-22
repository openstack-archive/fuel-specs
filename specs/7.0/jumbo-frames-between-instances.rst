..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================================================
Jumbo frames between instances using mtu-selection-and-advertisement feature
============================================================================

https://blueprints.launchpad.net/fuel/+spec/jumbo-frames-between-instances

This blueprint describes a way to use Jumbo frames between instances using
mtu-selection-and-advertisement[1] openstack kilo feature.

Problem description
===================

For network providers it may make sense to control(increase) mtu
value in openstack environment. Increasing the frame size makes a
certain large amount of data transferable with less effort, reducing
CPU utilization (mostly due to interrupt reduction) and increasing
throughput by reducing the number of frames needing processing
and reducing the total overhead byte count of all the frames sent.

Currently, we are already supporting Jumbo frames between instances
using 'network_device_mtu' nova & neutron configuration options and
mtu value is based on interface's mtu value what assigned to private
network. This mtu value will be default value for all cluster and private
networks if we have it more then one. mtu-selection-and-advertisement
feature implementation is supposed to support separate mtu configuration
for each private network. Fuel doesn't support multiple private networks
right now and we are not going to implement it in scope of 7.0 release,
but, I'm thinking that this feature may be in the scope of 8.0 and later
release. So, it may be useful to switch our Jumbo frames between instances
approach from current implementation to implementation using
mtu-selection-and-advertisement preliminarily.

Proposed change
===============

I propose to replace our current Jumbo frames between instances implementation
with implementation using mtu-selection-and-advertisement. These changes
will touch only puppet part and do not require any changes in nailgun side.
Currently, we have way to calculate mtu value for private network in case if
we have gre traffic. These calculations are not obligatory when we switch to
mtu-selection-and-advertisement solution, cause neutron performing it itself.
But, we should not wide out these calculations cause we should use it to
control mtu of dhcp/l3 neutron agents tap interfaces (cause current feature
implementation do not allow to do it). Also, we should extend current
calculation process to properly calculate mtu for `vxlan` environments.
Remaining to move mtu value for private network (mtu value of interface what
assigned to private network) to the appropriated configuration files.

Implementation will be include following steps:

* fix mtu calculations to support `vxlan` environments
* to enable mtu-selection-and-advertisement feature
  set in neutron.conf file on controller nodes:
  advertise_mtu = True
* to advertise proper mtu using neutron's L2 mechanism drivers(VLAN)
  to VMs set in ml2_conf.ini file on all nodes:
  physical_network_mtus = physnetX:private_net_mtu
* to advertise proper mtu using neutron's L3 mechanism drivers(GRE)
  set in ml2_conf.ini file on all nodes:
  path_mtu = private_net_mtu
* keep 'network_device_mtu = 65000' in nova.conf configuration
  files on compute nodes to set appropriated mtu for veth devices
* keep 'network_device_mtu = $calculated_mtu' option in neutron.conf file on
  controller nodes to avoid traffic's fragmentation on virtual interfaces
  what are placed in namespaces ( dhcp/l3 agents tap interfaces)

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

None

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

None

Performance Impact
------------------

Network bandwidth between instances will be significantly increased.

Plugin impact
-------------

None

Other deployer impact
---------------------

Openstack Kilo feature will be used.

Developer impact
----------------

Feature may require additional bugfixing and improvements during testing
procedure.

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

* Fix puppet to configure mtu between instances using
  mtu-selection-and-advertisement feature

Acceptance criteria
-------------------

User is able to use mtu-selection-and-advertisement feature(in clusters where
network provider is neutron). Feature will be switched on automatically during
the deployment process and its parameters will be based on node's private
interface mtu value.

Dependencies
============

* https://blueprints.launchpad.net/neutron/+spec/mtu-selection-and-advertisement

Testing
=======

Devops tool should be extended to prepare test environment with custom
mtu values for the virtual bridges to test passing of jumbo frames between
instances.

Documentation Impact
====================

Ability to change mtu values between instances should be documented in
Fuel Deployment Guide.

References
==========

1. https://blueprints.launchpad.net/neutron/+spec/mtu-selection-and-advertisement
