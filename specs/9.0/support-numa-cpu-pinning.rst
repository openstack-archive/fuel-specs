..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================================
Support for NUMA/CPU pinning for improved guests performance
============================================================

https://blueprints.launchpad.net/fuel/+spec/support-numa-cpu-pinning

User should be able to deploy compute nodes which can utilize libvirt driver’s
handling of the NUMA placement and CPU pinning features

--------------------
Problem description
--------------------

The nature of virtualization means that processes typically use whatever vCPU
is available, but the memory access time depends on the memory location
relative to the processor. NUMA means that memory is broken up into pools with
each vCPU working with the closest one, so the memory access time is the
shortest. To achieve optimal performance also an ability to establish
a mapping between virtual CPU to the physical core is required, and it's
covered by CPU pinning.

----------------
Proposed changes
----------------

Enabling NUMA/CPU pinning requires:

* Configure OS on compute nodes to tell which cores should be used only by
  virtual machines and not OS itself

* Configure nova on controller/compute nodes to set which cores can be used
  for virtual machines and enable appropriate filter for Nova Scheduler

Web UI
======

On Settings tab, to Compute settings dialog add:

* A checkbox to enable NUMA/CPU pinning

* A field to let a user set the number of CPU threads which should be available
  for an operating system

Nailgun
=======

TBD

Data model
----------

Next data should be stored for every node for every SR-IOV interface:

* Status of NUMA/CPU pinning feature (enabled/disabled)

* Number of cores available for host OS

astute.yaml will be extended as

::

  numa:
    enabled: true
    available_cores: N

where <N> is a number

REST API
--------

Only payload changes.

Orchestration
=============

Custom kernel boot line should be passed to isolate cores for virtual machines

RPC Protocol
------------

Only payload changes.

Fuel Client
===========

TBD

Plugins
=======

None

Fuel Library
============

Library will consume data from astute.yaml.

* `scheduler_default_filters` will be configured for nova-scheduler.

* `vcpu_pin_set` will be configured for nova-compute

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

None

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

User interface impact described in Web UI section.

------------------
Performance impact
------------------

* Performance of virtual machines using NUMA/CPU pinning will be higher
  relatively to virtual machines are not using these features

-----------------
Deployment impact
-----------------

* The feature requires appropriate changes in Nailgun/Fuel Library described in
  corresponding sections

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

TBD

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  asvechnikov
  skolekonov

Mandatory design review:
  TBA

Work Items
==========

* Enable NUMA/CPU pinning configuration in Fuel
* Support of configuring NUMA/CPU pinning via fuel API
* Support of configuring NUMA/CPU pinning via fuel CLI
* Support of NUMA/CPU pinning on UI
* Manual testing
* Create a system test for NUMA/CPU pinning

Dependencies
============

None

------------
Testing, QA
------------

TBD

Acceptance criteria
===================

User should be able to deploy compute nodes which can utilize NUMA/CPU pinning
for virtual machines

----------
References
----------

None
