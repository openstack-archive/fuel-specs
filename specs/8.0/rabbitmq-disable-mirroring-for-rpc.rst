..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================================================
Disable queue mirroring for RPC queues in RabbitMQ
==================================================

https://blueprints.launchpad.net/fuel/+spec/rabbitmq-disable-mirroring-for-rpc

RabbitMQ restarts caused by too high load impact OpenStack stability.
In order to reduce load on RabbitMQ, it is proposed to disable mirroring
for RPC queues and leave it enabled only for Ceilometer queues.

Note: the feature will be expeimental in 8.0 and will be disabled by
default.

--------------------
Problem description
--------------------

When a significant load is put on OpenStack, it in turn causes high load
on RabbitMQ. As a result, some nodes in RabbitMQ cluster fail and that
causes OpenStack downtime while its services reconnect to the remaining
nodes.

We observe this issue on scale, especially when OpenStack is deployed
with DVR enabled and the boot_and_delete_server_with_secgroups Rally test
is run on 200 nodes.

----------------
Proposed changes
----------------

In order to mitigate the described problem, it is proposed to disable
mirroring for OpenStack RPC queues. That way RPC messages will cause
smaller impact on RabbitMQ as it will not need to replicate them to
all cluster nodes. In case of 3-controller cluster that should reduce
load on each RabbitMQ node by a factor of 3.

Obviously, any failover will cause RPC messages loss (and OpenStack
instability, as a result), but we will gain stability by reducing number
of failovers.

We consider Ceilometer notifications to be important to users and so we do
not want to reduce safety for Ceilometer messages.

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

The whole change will be made in RabbitMQ OCF script, where queue policy is
defined.

------------
Alternatives
------------

Instead of disabling HA completely, we can use ha-mode=exactly with count
set to 2, 3, etc. But that will be much less effecive then disabling HA, since
some replication will still take place.

--------------
Upgrade impact
--------------

The change does not affect OpenStack environment upgrade. Our current
upgrade procedure (for 8.0) keeps 7.0 and 8.0 controllers separate, so
RabbitMQ nodes from 7.0 and 8.0 will not be joined into the same cluster.
As a result, we will not have a RabbitMQ cluster with constantly changing
policies.

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

The change should positively affect OpenStack stability under load.

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

None

--------------------
Documentation impact
--------------------

The change should be noted in the release notes.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  dmitrymex

Other contributors:
  None

Mandatory design review:
  bogdando, sgolovatiuk, vkuklin


Work Items
==========

1. Implement the change in the OCF script.
2. Test it on scale, verify that it significantly reduces CPU and/or memory
   consumption on 200 nodes, DVR, boot_and_delete_server_with_secgroups
   Rally test.
3. Perform destructive testing for messaging / RabbitMQ. Make sure our
   failover time did not get worse. Specific scenario to test:
     * Start up an oslo.messaging client and server.
     * Make client do periodic RPC calls to server each second.
     * Find the node hosting the queue used by the server and kill it.
     * See how many requests fail before client and server reconnect
       and recreate the queue.
4. Merge the change if it helps.

Dependencies
============

None

------------
Testing, QA
------------

As noted in work items, the change needs to be tested on 200 nodes to confirm
that it helps reduce load on RabbitMQ.

Acceptance criteria
===================

* The change considerably reduces load on RabbitMQ in scenario described in
  work item #2. There should be no RPC errors during normal operations
  (with all nodes working correctly).
* In case of failover, the recovery time must not increase. That is measured
  by work item #3.

----------
References
----------

None
