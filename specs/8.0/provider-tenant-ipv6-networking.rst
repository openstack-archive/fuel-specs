..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Provider and Tenant IPv6 Networking
===================================

https://blueprints.launchpad.net/fuel/+spec/provider-tenant-ipv6-networking

Provide end users with documentation how to plan and deploy OpenStack
installation with Fuel that enables IPv6 North-South connectivity using
provider networks, how to setup IPv6-enabled tenant networks for East-West
connectivity between instances. Write tests that covers this functionality in
Fuel and OpenStack.

-------------------
Problem description
-------------------

Delivering IPv6-enabled OpenStack requires from us that right software is
installed, properly configured and product is tested. At the moment
Fuel-deployed OpenStack is provided with next features:

* Working in IPv6-enabled provider networks that routed by end user's
  infrastructure

* Providing end users with IPv6-enabled tenant networks

* Routing between tenant, provider and external IPv6-enabled networks

* Managing IPv6 Security Groups Rules

We need to ensure this featureset is covered by our tests.

----------------
Proposed changes
----------------

Documentation should provide end users with list of IPv6 features that Fuel 8.0
is supporting.

Documentation may either cover next topics that already covered by OpenStack
Networking Guide, or refers to it:

#. Requirements, planning and deploying steps to setup OpenStack with Fuel with
   provider networks

#. Managing IPv6 subnets, including addressing types comparsion and cases

#. Setting up virtual routers and corresponding changes on end user's
   infrastructure

Almost all functionality is already tested with Tempest on Neutron gates, and
then Fuel ISO is re-tested with Tempest again. Build Verification Test (Smoke)
should be extended to test that IPv6 subnet could be created and address is
received.

Cases we have to do either in Tempest or OSTF:

#. IPv6 Security Groups Rules is working, because Tempest is verifying only
   IPv4 ones.

#. DHCPv6 Stateful addressing modes is working and instances are receiving
   their addresses.

#. Virtual routers is working between two networks, and instances are receiving
   default routes and reaching each other.

Cases we need to test, but have no infrastructure for it:

#. Having IPv6-enabled Public network on deployment stage may broke the process
   in case if any software components don't work properly in dualstack
   environment.

Web UI
======

None

Nailgun
=======

None

Data model
----------

None

REST API
--------

None

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

Additional research on IPv6 support in plugins is needed and should be
documented as well.

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

None

---------------
Security impact
---------------

IPv6 does not provide SNAT and Floating IPs, this should be covered in docs.

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

End users will be able to launch IPv6-enabled instances.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

* IPv6-enabled infrastructure is required to use provider networks.

* Routing setup on end user's infrastructure is required to connect virtual
  router to end user's public network.

* DVR is working with IPv6, but all the traffic will be forwarded through the
  central router.

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

Although many of features could be tested without IPv6 connectivity provided by
CI infrastructure, having proper connectivity required to test that it does not
affect Fuel deployment.

--------------------
Documentation impact
--------------------

OpenStack Networking Guide is already provided with documentation on IPv6
addressing, tenant and provider networks setup. Knowledge Base article that
listing all supported IPv6 cases should be provided. How-to plan and deploy
IPv6-enabled provider networks may be provided.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vladimir Eremin, yottatsa (veremin@mirantis.com)

QA engineer:
  Alexey Stepanov (astepanov@mirantis.com)

Mandatory design review:
  Sean M. Collins (scollins@mirantis.com)
  Michele Fagan (mfagan@mirantis.com)

Work Items
==========

* Write KB article to list all supported cases in 8.0

* Write How-to on setup provider networking in Fuel

* Write new fuel-ostf tests on provided test cases

* Extend smoke test that could check IPv6 functinality

Dependencies
============

None

------------
Testing, QA
------------

* fuel-ostf should be extended to be able to create IPv6 subnets.

Acceptance criteria
===================

End user is provided with documentation on IPv6 and able to design, deploy and
create provider and tenant IPv6 networks. All documented features is covered by
tests.

----------
References
----------

None