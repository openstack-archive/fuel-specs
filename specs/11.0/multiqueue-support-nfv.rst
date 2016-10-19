..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Improve NFV workload performance with multiq support
====================================================

https://blueprints.launchpad.net/fuel/+spec/multiqueue-support-nfv


--------------------
Problem description
--------------------

Today’s high-end servers have more processors, and guests running on them
often have an increasing number of vCPUs. In a single virtio-net queue, the
scale of the protocol stack in a guest is restricted, as the network
performance does not scale as the number of vCPUs increases. Guests cannot
transmit or retrieve packets in parallel, as virtio-net has only one TX and
RX queue.

Multiqueue virtio-net provides the greatest performance benefit when:

* Traffic packets are relatively large.

* The guest is active on many connections at the same time, with traffic
  running between guests, guest to host, or guest to an external system.

* The number of queues is equal to the number of vCPUs. This is because
  multi-queue support optimizes RX interrupt affinity and TX queue selection
  in order to make a specific queue private to a specific vCPU.

There is a spec `Libvirt: virtio-net multiqueue`_ implemented that adds
support for mutliqueue feature in OpenStack, now we need to add support
on packages level. To achieve this we need the following packages together:

* qemu 2.5

* libvirt 1.3.1

* openvswitch 2.5

* dpdk 2.2

Unfortunately, those packages are unavailable in Ubuntu 14.04 (which is a base
system in MOS 9.x) and should be backported. The good thing is that packages
were backported as part of optional 'NFV feature support'.

----------------
Proposed changes
----------------

Integrate packages from 'feature/nfv' branch into main 9.0 development branch
and verify that they work as expected.

To enable the feature from OpenStack side additional parameter should be
added to image properties, like shown below:

  ..code-block:: text

    hw_vif_multiqueue_enabled=true|false (default false)

Currently, the number of queues will match the number of vCPUs, defined for
the instance.

..note::  Virtio-net multiqueue should be enabled in the guest OS manually,
          using ethtool. For example:

          ..code-block:: text

            ethtool -L <NIC> combined #num_of_queues


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

Networking-related plugins might face issues with new packages.


Fuel Library
============

None


------------
Alternatives
------------

There is no other way than upgrade to the packages that provide multiqueue
functionality.


--------------
Upgrade impact
--------------

Upgrading QEMU requires every guest VM was stopped and started again (not
rebooted).


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

Improves NFV performance.


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

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Dmitry Teselkin`_

Other contributors:
  `Ivan Suzdal`_

Mandatory design review:
  `Dmitry Klenov`_


Work Items
==========

* Move every package from 'feature/nfv' into 9.0 branch, merge and build
  packages.


Dependencies
============

None


------------
Testing, QA
------------

* Verify that new set of packages doesn't introduce any regressions.

* Verify that vhost-user network works in OpenStack


Acceptance criteria
===================

* The following packages available in 9.2 repository:

  * qemu - 2.5

  * libvirt - 1.3.1

  * openvswitch - 2.5

  * dpdk - 2.2

  * dependencies for the packages above

* MOS 9.2 uses updated packages by default

* Multiqueue support with vhost user in OpenStack


----------
References
----------

.. _`Dmitry Teselkin`: https://launchpad.net/~teselkin-d
.. _`Ivan Suzdal`: https://launchpad.net/~isuzdal
.. _`Dmitry Klenov`: https://launchpad.net/~dklenov
.. _`Vladimir Khlyunev`: https://launchpad.net/~vkhlyunev
.. _`Libvirt: virtio-net multiqueue`: https://specs.openstack.org/openstack/nova-specs/specs/liberty/implemented/libvirt-virtiomq.html
