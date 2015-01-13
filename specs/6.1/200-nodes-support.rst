..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
200 nodes support
==========================================

https://blueprints.launchpad.net/fuel/+spec/200-nodes-support

This blueprint is a continuation of the blueprint "100 nodes support"[1] from
release 6.0.

Problem description
===================

For large number of nodes some parts of the Fuel are getting slow. Probability
of failing during provision and deploy stages is also increasing. If nodes
fail to provision deployment can not continue.

Proposed change
===============

For nailgun
-----------

In the previous release some performance tests[2] were added to nailgun to show
bottlenecks and the biggest issues were fixed. During this release more test
will be added. For example:

Integration tests:

* add 100 nodes, deploy, add 100 nodes, deploy
* add 100 nodes, deploy cluster, stop deployment, deploy cluster

Unit tests:

* Tests for handler ProvisionSelectedNodes
* Tests for handler NodeGroupCollectionHandler
* Tests for handler NodeCollectionNICsDefaultHandler
* Check how NotificationCollectionHandler works with big number of
  notifications

Execution of handler ClusterChangeHandler which takes to much time will be
moved to background as it is hard to optimize it.

Graphs will be added to CI job to show how performance changed between
commits.

For astute
-----------

One known problem is connected with network/storage capabilities of Fuel Master
node. When, during provisioning, 200 nodes simultaneously trying to fetch
images and packages. Master node can not handle that high load. Astute should
detect such situation and handle it.
User should be also able to manually tweak astute work. For example to
configure it to provision 50 nodes at the time. It will increase provisioning
time but will make it more resistant.
There should be a configuration option to set number nodes to deploy in one
run.

Some nodes may fail because of random failures, provisioning should still
continue in this case.
Provision will not be restarted for failed nodes. This nodes will have
status set to error. User can re-provision this nodes after successful
deployment.
There should be a configuration option to set percent of nodes which can fail
during provisioning.
In case when for example all controllers failed to provision, provisioning
should be stopped.
User should be notified about each failure.
The same applies for deploy stage.

Another problem is connected with network verification which for 100 nodes
takes a lot of time. Currently connectivity between node is checked on one
node at time. It should be parallelized to make it faster but also
it should be backward compatible.

Alternatives
------------

None

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

After blueprint is implemented Fuel should be able to deploy 200 nodes.

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

Work Items
----------

Blueprint will be implemented in several stages:

* Allow to run provision in chunks
* Improve network verification performance
* Allow some nodes to fail during provisioning and deployment
* Write new nailgun performance tests

Dependencies
============

None

Testing
=======

More load test will be added to CI infrastructure,
so non optimal code can immediately be noticed.

Documentation Impact
====================

Changes about provision and deployment should be documented.

References
==========

1. https://blueprints.launchpad.net/fuel/+spec/100-nodes-support
2. https://github.com/stackforge/fuel-web/tree/master/nailgun/nailgun/test/performance
