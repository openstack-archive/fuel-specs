..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Provider and Tenant IPv6 Networking
===================================

https://blueprints.launchpad.net/fuel/+spec/provider-tenant-ipv6-networking

Provide end user with documentation how to plan and deploy OpenStack
installation with Fuel that enables IPv6 North-South connectivity using
provider networks, how to setup IPv6-enabled tenant networks for East-West
connectivity between instances. Write tests that covers this functionality in
Fuel and OpenStack.

-------------------
Problem description
-------------------

Delivering IPv6-enabled OpenStack requires to have rigth settings and right
software delivered. At the moment OpenStack installed with Fuel is provided
with next features:

* Working in IPv6-enabled provider networks that routed by end user's
  infrastructure

* Providing end user with tenant IPv6-enabled networks

* Routing between tenant, provider and external IPv6-enabled networks

* Managing IPv6 Security Groups Rules

Then we need to ensure this featureset is covered by our tests.

----------------
Proposed changes
----------------

Documentation should cover next topics:

#. Requirements, planning and deploying steps to setup OpenStack with Fuel with
   provider networks

#. Managing IPv6 subnets, including addressing types comparsion and cases

#. Setting up virtual routers and corresponding changes on end user's
   infrastructure

Cases we have to test:

#. IPv6 Security Groups Rules is working

#. SLAAC and DHCPv6 Stateful addressing modes is working and instances are
   receiving their addresses

#. DHCPv6 advertises IPv6 name server correctly

#. Virtual routers is working between two networks, and instances are receiving
   default routes and reaching each other

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

Additional research on IPv6 support in plugins is needed.

Fuel Library
============

* Provide all needed software to enable IPv6 addressing functionality working.

* Ensure that IPv6 autoconfiguration is disabled on any external interfaces
  does not managed with OpenStack Neutron (br-ex, br-floating).

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

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Specific deployment planning steps to enable provider networks should be
documented. End user's manual should be updated to provide instruction how to
setup IPv6-enabled networks.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vladimir Eremin, yottatsa (veremin@mirantis.com)

QA engineer:
  to be assigned

Mandatory design review:
  Sheena Gregson, sgregson (sgregson@mirantis.com)

Work Items
==========

* Disable IPv6 autoconf in fuel-library

* Extend planning and setup documentations

* Extend end user's manual

* Write new fuel-ostf swarm tests on provided test cases

* Extend smoke bvt_2 test that could check IPv6 functinality

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