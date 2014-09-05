..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
100 nodes support (fuel only)
==========================================

https://blueprints.launchpad.net/fuel/+spec/100-nodes-support

If we want Fuel to be enterprise tool for deploying OpenStack it should be
able to deploy large clusters. Fuel also should be fast and responsive.
It does not run any processor consuming tasks so there is no reason
for it to be slow.

Problem description
===================

For large number of nodes fuel(nailgun, astute) is getting slow.

Proposed change
===============

For nailgun
-----------

In the first step we should write tests which will show places in code which
is not optimal. Some of slow parts are already known.
Such tests should include(all in fake mode):

* list 100 nodes
* get cluster with 100 nodes
* add 100 nodes to environment
* remove 100 nodes from environment
* run network verification for environment with 100 nodes
* change settings in environment with 100 nodes
* change network configuration in environment with 100 nodes
* run deploy in environment with 100 nodes
* ...

For fuelclient
--------------

There should not be any performance bottlenecks in the fuelclient, it
only parses JSON data. There should be tests for fuelclient which performs 
the same test as for nailgun.

For astute
-----------

Testing astute is harder because it includes interaction with hardware 
and other services like cobbler, tftp, dhcp. There is one known problem
which can be addressed now. Rest of the problems can be identified after 
testing on real hardware.

One known problem is connected with network/storage capabilities of Fuel Master
node. When, during provisioning, 100 nodes simultaneously trying to fetch 
images and packages. Master node can not handle that high load.
Solution here is to split provisioning into smaller parts, for example to
provision 10 nodes at the time. It will increase provisioning time but will
make it more resistant.
There should be configuration option to set number nodes to deploy in one run.

Currently, if provisioning will fail on one of the nodes, astute will
stop whole process. It is not optimal solution for larger deployments. Some
nodes may fail because of random failures, provisioning should still
continue in this case. 
There should be configuration option to set number of nodes which can fail
during provisioning.

For UI
------

Our tests shows that for 100 nodes UI speed is acceptable. In future, for 1000
nodes, it will require some speed improvements. 

Alternatives
------------

Leave it as it is.

Data model impact
-----------------

Depends on bottlenecks found, but unlikely.

REST API impact
---------------

No API changes. All optimization have to be backward compatible.

Upgrade impact
--------------

Only if database is changed, but unlikely.

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

After blueprint is implemented Fuel should be able to deploy with 100 nodes.

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  loles@mirantis.com
  ksambor@mirantis.com

Work Items
----------

Blueprint will be implemented in several stages:

* In first stage all tests will be written.
* In next stage all known and discovered bottleneck will be fixed.
* After this we will run tests in virtual environment which can create
  100 nodes.
* At the end we will test Fuel in lab with 100 physical nodes. This test
  should show us all astute bottlenecks.
* To prevent reintroducing bottlenecks in next releases all test 
  will be integrated with our CI infrastructure.
* Additional integration with OSProfiler. It can help find bottleneck 
  in production systems
* Additional integration with Rally. It will help with integrating with
  other performance test done by Scale team.


Dependencies
============

None


Testing
=======

When all bottlenecks are fixed. Load test will be added to CI infrastructure,
so we can immediately notice non optimal code.

Documentation Impact
====================

None

References
==========

* https://github.com/stackforge/osprofiler
* https://github.com/stackforge/rally
* https://docs.google.com/a/mirantis.com/document/d/1GJHr4AHw2qA2wYgngoeN2C-6Dhb7wd1Nm1Q9lkhGCag
* https://docs.google.com/a/mirantis.com/document/d/1O2G-fTXlEWh0dAbRCtbrFtPVefc5GvEEOhgBIsU_eP0
