..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================================
Support for NUMA/CPU pinning for improved guests performance
============================================================

https://blueprints.launchpad.net/fuel/+spec/support-numa-cpu-pinning

User should be able to deploy compute nodes which can utilize libvirt driver
handling of the NUMA (Non-Uniform Memory Access) topology and CPU pinning
features

--------------------
Problem description
--------------------

The nature of virtualization means that processes typically use whatever vCPU
is available, but the memory access time depends on the memory location
relative to the processor. NUMA means that memory is broken up into pools with
each vCPU working with the closest one, so the memory access time is the
shortest. To achieve optimal performance also an ability to establish a mapping
between virtual CPU to the physical core is required, and it's covered by CPU
pinning.

----------------
Proposed changes
----------------

Enabling NUMA/CPU pinning requires:

* Collect information about NUMA topology from discovered nodes

* Possibility to configure CPU pinning via API/CLI/UI

* Configure OS (Operation System) compute nodes according User configuration
  to tell which cores should be used only by OS

* Configure nova on controller/compute nodes to set which cores can be used
  for virtual machines and enable appropriate filter for Nova Scheduler

Web UI
======

On Settings tab, to Compute settings dialog add:

* A checkbox to enable NUMA/CPU pinning

* A field to let a user set the CPUs which should be available for an Operating
  System

Nailgun
=======

Nailgun-agent have to collect information about NUMA topology and CPUs

Nailgun changes:

* Additional validation should be added for CPU pinning in Node Handlers.

* CPU pinning options should be added to kernel parameters in provision
  information for each node.

Data model
----------

Node meta will store the next data:

::
  {'numa_nodes': [{'node_number': 0,
                   'cpus': [0, 1, ..., 5, 12, 13, ..., 17]
                  },
                  {'node_number': 1,
                   'cpus': [6, 7, ..., 11, 18, 19, ..., 23]
                  }],
   'isolated_cpus': [0, 1, 18, 19]}

where isolated_cpus is the CPUs which is prohibited for OS utilization

astute.yaml will be extended as

::
  numa:
    enabled: true
    isolated_cpus: [0, 1, 18, 19]


REST API
--------

Only payload changes.

Orchestration
=============

For each node with enabled CPU pinning the custom kernel parameters should be
passed to isolate cores for virtual machines

RPC Protocol
------------

Only payload changes.

Fuel Client
===========

New commands should be added for download/upload NUMA/CPU pinning
configuration

.. code-block:: bash

  fuel node --node-id 1 --numa --download
  fuel node --node-id 1 --numa --upload

Where will be stored information about current NUMA topology
and will be possible to configure isolated_cpus

::
  isolated_cpus: [0, 1, 18, 19]
  numa_nodes:
  - cpus: [0, 1, 5, 12, 13, 17]
    node_number: 0
  - cpus: [6, 7, 11, 18, 19, 23]
    node_number: 1


Plugins
=======

None

Fuel Library
============

Library will consume data from astute.yaml.

* `scheduler_default_filters` will be configured for nova-scheduler

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

User Web UI/CLI impact described in appropriate sections.

------------------
Performance impact
------------------

* Performance of virtual machines using NUMA/CPU pinning will be higher
  relatively to virtual machines are not using these features

* It possible that node will have low performance if User allocate not enough
  CPUs for OS

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
