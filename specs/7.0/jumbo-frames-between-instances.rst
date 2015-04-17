..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
Jumbo frames between instances
==============================

Include the URL of your launchpad blueprint:
https://blueprints.launchpad.net/fuel/+spec/jumbo-frames-between-instances

This blueprint describes a way to use Jumbo frames between instances using
mtu-selection-and-advertisement[1] openstack kilo feature.

Problem description
===================

For network providers it may make sense to control(increase) mtu
value in openstack environment. Increasing the frame size makes a
certain large amount of data transferable with less effort, reducing
CPU utilisation (mostly due to interrupt reduction) and increasing
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
We already have way to calculate mtu value for private network, and, remaining
work here is to move this mtu value to the other configuration files.

Implementation will be include following steps:

* in neutron.conf file on controller nodes set:
  advertise_mtu = True
* in ml2_conf.ini file on all nodes set:
  segment_mtu = private_net_mtu
  physical_network_mtus = physnetX:private_net_mtu
* get rid of 'network_device_mtu' option in neutron & nova
  configuration files

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

None

Plugin impact
-------------

None

Other deployer impact
---------------------

Openstack Kilo feature will be used.

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

Primary assignee:
  Valyavskiy Viacheslav <slava-val-al>

Work Items
----------

* Fix puppet to configure mtu between instances using
  mtu-selection-and-advertisement feature

Dependencies
============

* https://blueprints.launchpad.net/neutron/+spec/mtu-selection-and-advertisement

Testing
=======

Devops tool should be extended to prepare test environment with custom
mtu values for the virtual bridges.

Documentation Impact
====================

Ability to change mtu values between instances should be documented in
Fuel Deployment Guide.

References
==========

1. https://blueprints.launchpad.net/neutron/+spec/mtu-selection-and-advertisement
