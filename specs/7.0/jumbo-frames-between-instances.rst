..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
Jumbo frames between instances
==============================

Include the URL of your launchpad blueprint:
https://blueprints.launchpad.net/fuel/+spec/jumbo-frames-between-instances

This blueprint describes a way to use Jumbo frames between instances.

Problem description
===================

For network providers it may make sence to control(increase) mtu
value in openstack environment. Increasing the frame size makes a
certain large amount of data transferable with less effort, reducing
CPU utilization (mostly due to interrupt reduction) and increasing
throughput by reducing the number of frames needing processing
and reducing the total overhead byte count of all the frames sent.

Proposed change
===============

As mtu selection and advertisement neutron blueprint[1] was implemented
it is possible to control MTU value using options in neutron configuration
file. It means that it will be enough to pass MTU value from UI/CLI to
neutron configuration file.
It will be necessary to add extra UI option to cluster network settings
tab to configure MTU value. This option will be availiable only for neutron
network provider. Network configuration validator should be extended to
check that passed MTU value is not higher than mtu value of physical
interface/bond which tenant network(mgmt, private) is assigned to.
Nailgun deployment serializer should be fixed to include MTU value option
to neutron serialized data. Fuel-library should be extended to set passed
MTU option as neutron mtu option in neutron configuration file.

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

Extend neutron network configuration validator to handle MTU value.

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

User will be able to change mtu value between instances via API and CLI.

Performance Impact
------------------

Network throughput in high performance networks will be increased.

Plugin impact
-------------

None

Other deployer impact
---------------------

Extra cluster network option will be introduced to configure MTU value
if neutron network provider was choosen. This option will be empty
by default and it will not be configured if it was not specified by
user.

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

* Add option to UI to configure MTU between openstack
  instances (availiable for neutron only)
* Fix neutron network configuration validator to check
  MTU value
* Fix nailgun serializer to include this option in neutron
  serialized data
* Fix puppet to set passed option as neutron mtu option in
  neutron configuration file

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
