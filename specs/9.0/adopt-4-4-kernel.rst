..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Example Spec - The title of your blueprint
==========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/adopt-4-4-kernel


--------------------
Problem description
--------------------

As a Cloud Owner I want to be able to deploy MOS 9.x with Linux kernel v4.4 so
that I could use latest models of servers for my cloud.

MOS 9.x is currently shipped with Linux kernel v3.x - this will likely become
an issue in 2017, when customers will want to use newer models of servers for
their cloud capacity. Next to that OVS and KVM may get improvements by
upgrading the Kernel.

Latest Ubuntu 14.04 release, 14.04.5, includes kernel 4.4 oficially
backported from Ubuntu Xenial 16.04 that will be supported until 14.04 EOL:

* `14.04.x Ubuntu Kernel Support`_

* `LTS Kernel Support Schedule`_

This gives us a good opportunity to replace 3.13 kernel with 4.4, to get
the following advantages:

* updated drivers (we even can remove several drivers since stock version
  are good)

* support for more hardware out of the box (e.g. it fixes issue with multiple
  SR-IOV NICs installed in one chasis)

* a kernel with a lot of bug / security fixes


----------------
Proposed changes
----------------


Web UI
======

None

Nailgun
=======


Data model
----------

None

REST API
--------

None

Orchestration
=============


RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

There is a little chance that some plugins are not compatible with 4.4 kernel.
However, since upgrading to 4.4 kernel is a manual operation, this should be
checked before an upgrade.


Fuel Library
============

The following CRs needed:

* https://review.fuel-infra.org/#/c/22955/


------------
Alternatives
------------

There is no alternative way if you want functionality of a new kernel.


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

End user (or support stuff) should manually upgrade their environement in order
to get this feature.


------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

Initial deployment of MOS 9.0 and upgrade to MOS 9.1 is not affected. Upgrade
to 4.4 kernel can be applied manually on MOS 9.1 at any moment. It's much
better to apply it *before* deploying an environment, because it requires less
work.

Upgrading of deployed environment also possible, but requires carefull planning
because cluster nodes must be rebooted after an upgrade.


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

Upgrade procedure should be documented and officially published.


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
  `Nastya Urlapova`_


Work Items
==========

* Prepare documentation describing upgrade steps.

* Prepare minimal set of scripts to automate routing tasks required to perform
  upgrade.

* Verify upgrade procedure, verify cluster after an upgrade in following cases:

  * upgrade master node only and deploy new environment

  * upgrade master node and existing environment


Dependencies
============

None

------------
Testing, QA
------------

Upgrade procedure is not fully automated process and should be applied
and verified manually. No new tests needs to be added.



Acceptance criteria
===================

* Instructions for upgrade of existing MOS 9.0/9.1 environments into kernel
  v4.4 are created and meet the following criteria:

  * Customers/L2 are expected to follow instructions and upgrade the kernel to
    v4.4 on computes, one by one, nothing should be automated by Fuel,
    instructions are provided as is.

  * Any node in a deployment environment that is currently using v3.x should
    stay on v3.x unless customer manually upgrades the kernel to newer version.


----------
References
----------

.. _`14.04.x Ubuntu Kernel Support`: https://wiki.ubuntu.com/Kernel/LTSEnablementStack#Kernel.2FSupport.A14.04.x_Ubuntu_Kernel_Support
.. _`LTS Kernel Support Schedule`: https://wiki.ubuntu.com/Kernel/Support?action=AttachFile&do=view&target=LTS+Kernel+Support+Schedule.svg
.. _`Dmitry Teselkin`: https://launchpad.net/~teselkin-d
.. _`Ivan Suzdal`: https://launchpad.net/~isuzdal
.. _`Nastya Urlapova`: https://launchpad.net/~aurlapova