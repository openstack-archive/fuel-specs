..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
100 nodes support (fuel only)
==========================================

https://blueprints.launchpad.net/fuel/+spec/100-nodes-support

If we want Fuel to be an enterprise tool for deploying OpenStack, it should be
able to deploy large clusters. Fuel also should be fast and responsive.
It does not run any processor consuming tasks, so there is no reason
for it to be slow.

Problem description
===================

* For large number of nodes Fuel(nailgun, astute) is getting slow.
* Probability of failing provisioning is also increasing.
* MySQL DB works only as active/standby which has very poor perfomance.

Proposed change
===============

For nailgun
-----------

In the first step, we should write tests which will show places in code which
are not optimal. Some of slow parts are already known.
Such tests should include(all in fake mode):

* list 100 nodes
* get cluster with 100 nodes
* add 100 nodes to environment
* remove 100 nodes from environment
* run network verification for environment with 100 nodes
* change settings in environment with 100 nodes
* change network configuration in environment with 100 nodes
* run deploy in environment with 100 nodes
* run provision in environment with 100 nodes
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
which can be addressed now. The rest of the problems can be identified after
testing on real hardware.

One known problem is connected with network/storage capabilities of Fuel Master
node. When, during provisioning, 100 nodes simultaneously trying to fetch
images and packages. Master node can not handle that high load. Astute should
detect such situation and handle it.
User should be also able to manually tweak astute work. For example to
configure it to provision 10 nodes at the time. It will increase provisioning
time but will make it more resistant.
There should be configuration option to set number nodes to deploy in one run.

Currently, if provisioning fails on one of the nodes, astute will
stop the whole process. It is not an optimal solution for larger deployments.
Some nodes may fail because of random failures, provisioning should still
continue in this case.
Provision will not be restarted for failed nodes. This nodes will be removed
from cluster. User can re-add this nodes to cluster after successful
deployment.
There should be a configuration option to set number of nodes which can fail
during provisioning.

For UI
------

Our tests show that for 100 nodes UI speed is acceptable. In future, for 1000
nodes, it will require some speed improvements.

For puppet manifests library
----------------------------

Configure HAproxy MySQL backends as active/active.
There is a patch https://review.openstack.org/#/c/124549/ addressing this change,
but it requires additional researching and load testing.

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

If there are failed nodes. User should be informed about this.

Other end user impact
---------------------

None

Performance Impact
------------------

After blueprint is implemented Fuel should be able to deploy 100 nodes.
Active/active load balancing for MySQL connections should improve DB operations.

Other deployer impact
---------------------

Rules will change. Some nodes can fail now.

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
* In next stage all known and discovered bottlenecks will be fixed.
* After this we will run tests in virtual environment which can create
  100 nodes.
* At the end we will test Fuel in lab with 100 physical nodes. This test
  should show us all astute bottlenecks.
* To prevent reintroducing bottlenecks in next releases all test
  will be integrated with our CI infrastructure.
* Additional integration with OSProfiler. It can help find bottleneck
  in production systems
* Additional integration with Rally. It will help to test Fuel in real live
  environment.
* Additional Neutron load testing with Rally in HA for active/active MySQL.
  Even if active/active will fail the testing, at least we could play with
  tuning related params and provide some output to community.

Dependencies
============

None


Testing
=======

When all bottlenecks are fixed, load test will be added to CI infrastructure,
so we can immediately notice non optimal code.

Documentation Impact
====================

Deployment rules will change, it should be documented. New notifications
should be described. Active/active mode for MySQL should be documented.

References
==========

* https://github.com/stackforge/osprofiler
* https://github.com/stackforge/rally
* https://docs.google.com/a/mirantis.com/document/d/1GJHr4AHw2qA2wYgngoeN2C-6Dhb7wd1Nm1Q9lkhGCag
* https://docs.google.com/a/mirantis.com/document/d/1O2G-fTXlEWh0dAbRCtbrFtPVefc5GvEEOhgBIsU_eP0
* http://lists.openstack.org/pipermail/openstack-operators/2014-September/005162.html
