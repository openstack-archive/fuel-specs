======================
Virtual IP reservation
======================

https://blueprints.launchpad.net/fuel/+spec/vip-reservation

This document is about additional virtual IP (VIP)
reservation during deployment.

Problem description
===================

Some plugins require additional VIP to proper configuration.
For example Zabbix could be configured in way that it expect SNMP traffic
on dedicated VIP.

In current version VIPs reservation is done based on information from
release field in the database.

So the plugin developer should have a better way to create extra VIPs
as puppet resource in pre-deployment or post-deployment plugin stage.

Proposed change
===============

Give user a possibility to reserve additional VIPs during deployment process.
This should be possible by providing REST API extension to reserve additional
VIPs.

Add support of new REST API calls to the Fuel client.

Plugin developers will use puppet provider for VIPs to manage them
on pre-deployment stage. Puppet provider should call fuel client
and return reserved VIP address.

Deployment flow: None

Migration script flow: None

Alternatives
------------

VIP requirements for particular network role can be placed in plugin into
tasks description. This fits to the current view of flexible networking
implementation. Plugin can have its own tasks description already.
Network role list should be defined in description of each task and each
network role definition there may contain VIP requirements.

Network roles to tasks mapping will be parsed by nailgun and
VIP requirements will be processed so that VIPs will be assigned
before the deployment is started.

  Cons:
   - More difficult implementation
   - API solution gives better ability to manage VIPs

  Pros:
   - Better flexibility in some cases

Data model impact
-----------------

None

REST API impact
---------------

We should introduce new API calls which will allow to reserve
and manage VIPs in the given network. Supported operations
should be add, delete and get VIPs.

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

Other deployer impact
---------------------

Performance Impact
------------------

None

Developer impact
----------------

Developer that works on Fuel plugins can use new API
to reserve VIPs for the plugin.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Alexander Saprykin (cutwater)

Work Items
----------

  - Implement new REST API to manage VIPs.
  - Investigate possibilities to manage VIPs via fuel client.

Dependencies
============

None

Testing
=======

Regression testing is required.

Acceptance criteria:

   - VIPs can be added and recieved using REST API.
   - VIPs can be added via puppet provider.

Documentation Impact
====================

We need to update documentation about VIPs in networks. Plugin documentation
should be updated as well.

References
==========

- https://blueprints.launchpad.net/fuel/+spec/vip-reservation

