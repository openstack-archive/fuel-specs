..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Environment Snapshot
==========================================

https://blueprints.launchpad.net/fuel/+spec/environment-snapshot

We use system test framework for many deployment tests. Those tests
are executed on jenkins slaves used by CI.
In case of test failure developer or QA engineer need to revert
environment with broken test and analyse the failure reason. This
is possible only on the same system on which test was executed.
We want to create a solution which allow QA engineers and developers
to revert broken test on different server or local station.

--------------------
Problem description
--------------------

With actual system test framework we create libvirt snapshot at the
end of failed test. This solution allow developers to revert broken environment
on the same server. Developers and QA engineers needs some time to start
work on broken test and analyse it. This require to leave broken test on
slave server for at least 12-24h.

Created solution should allow to:

* import/export environments created in libvirt:

 * virtual machine configuration
 * virtual machine disk content
 * network configuration

* design and create solution for manage exported environments:

 * copy environments over network to and from storage servers
 * manage lists of environments
 * delete old environments

* store exported environments for at least 48h:

 * design and create storage solution which allow to store all required data

----------------
Proposed changes
----------------

System tests generates 30-50 TB of data daily, 5-20TB come from failed tests.
This sizes could be reduces by using external snapshots, it will allow to use
common base image and copy only required snapshots. This requires to update
fuel-devops framework to support external snapshots.

Storage server - TODO

Import/Export system - TODO

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

None

Fuel Library
============

None

------------
Alternatives
------------

We could try to use openstack as a source of virtual machines for environment
tests. But at this moment it is not possible to execute environment tests with
VLAN segmentation, standard openstack not allow to pass tagged VLAN frames
between instances. This is also not supported by fuel-devops and fuel-qa
frameworks.

--------------
Upgrade impact
--------------

None

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

None

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

* Requires additional hardware to store exported snapshots
* Higher network traffic between slaves and servers dedicated to store
  exported data
* Depends of used solution for snapshots store it could reduce disk usage
  on slaves
* Potential speedup of tests execution by reusing exported snapshots as
  starting point for other tests, this will require additional changes
  in fuel-qa
* Requires implementation of external snapshots in fuel-devops

--------------------
Documentation impact
--------------------

Requires to create documentation with description of usage and installation
procedures for storage servers.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  TODO

Work Items
==========

* Implement external snapshots for fuel-devops
* Design storage system for exported data
* Design import/export solution for libvirt environments
* Create PoC system
* Implement storage system
* Implement import/export system on slave servers

Dependencies
============

* External snapshots for fuel-devops
  https://blueprints.launchpad.net/fuel/+spec/system-test-external-snapshots

------------
Testing, QA
------------

TODO

Acceptance criteria
===================

* There is possibility to export system test to storage server
* There is possibility to import system test from storage server
* There is possibility to list system tests possible to download

----------
References
----------

None