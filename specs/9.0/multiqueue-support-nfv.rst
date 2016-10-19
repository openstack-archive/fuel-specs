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

Today's high-end server have more processors, guests running on them tend have
an increasing number of vcpus. The scale of the protocol stack in guest in
restricted because of the single queue virtio-net:

* The network performance does not scale as the number of vcpus increasing:
  Guest can not transmit or retrieve packets in parallel as virtio-net have
  only one TX and RX, virtio-net drivers must be synchronized before sending
  and receiving packets. Even through there's software technology to spread
  the loads into different processor such as RFS, such kind of method is only
  for transmission and is really expensive in guest as they depends on IPI
  which may brings extra overhead in virtualized environment.

* Multiqueue nic were more common used and is well supported by linux kernel,
  but current virtual nic can not utilize the multi queue support: the tap and
  virtio-net backend must serialize the co-current transmission/receiving
  request comes from different cpus.

Support for multiqueue in vhost-user was added not a long time ago, so we need
the following packages together:

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

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

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

No specific testing is required, existing test suite covers all cases.


Acceptance criteria
===================

* The following packages available in 9.2 repository:

  * qemu - 2.5

  * libvirt - 1.3.1

  * openvswitch - 2.5

  * dpdk - 2.2

  * dependencies for the packages above

* MOS 9.2 uses updated packages by default


----------
References
----------

.. _`Dmitry Teselkin`: https://launchpad.net/~teselkin-d
.. _`Ivan Suzdal`: https://launchpad.net/~isuzdal
.. _`Dmitry Klenov`: https://launchpad.net/~dklenov