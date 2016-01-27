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
relative to the processor. NUMA is a computer memory design used in
multiprocessing, where the memory access time depends on the memory location
relative to the processor. Thus, memory computer may contain several NUMA nodes
with local memory and CPUs.
To achieve optimal performance also an ability to establish a mapping between
virtual CPU to the physical core is required, and it's covered by CPU pinning.

NUMA topology can be displayed as:

.. code-block:: console

  available: 2 nodes (0-1)
  node 0 cpus: 0 1 2 3 4 5 12 13 14 15 16 17
  node 0 size: 128910 MB
  node 0 free: 669 MB
  node 1 cpus: 6 7 8 9 10 11 18 19 20 21 22 23
  node 1 size: 129022 MB
  node 1 free: 4014 MB
  node distances:
  node   0   1
    0:  10  21
    1:  21  10

Here we can see that NUMA topology contains 2 NUMA node with 12 CPU each.

Additional information about NUMA/CPU pinning support in OpenStack can
be found here:

https://specs.openstack.org/openstack/nova-specs/specs/juno/implemented/virt-driver-numa-placement.html

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

TBA

Nailgun
=======

Nailgun-agent have to collect information about NUMA topology and CPUs.
Information will be collected by using TBD

Collected information should be passed to nailgun in the next format

.. code-block:: json

  'topology': {
   'numa_nodes': [
      {'id': 0,
      'cpus': [0, 1, ..., 5, 12, 13, ..., 17]},
      {'id': 1,
       'cpus': [6, 7, ..., 11, 18, 19, ..., 23]}]
   ]
  }

Nailgun changes:

* New handlers and validators
* Extend node db model
* Deployment serializer must take into account CPU pinning information

Data model
----------

Nailgun-agent will send information about node NUMA topology.
This information will be stored in node metadata

.. code-block:: json

 node.metadata = {
  ...
  'topology': { ... }
  ...
 }

User can specify which CPUs should be isolated (e.g. not used by OS).
In current implementation all isolated CPUs will be passed to Nova.
Node will be extended with attribute column

.. code-block:: python

 class Node(Base):
     ...
     attributes = Column(MutableDict.as_mutable(JSON), default={})
     ...

where user's cpu configuration will be stored as

.. code-block:: json

 {
  'description': ("Comma separated list of CPUs indexes which should be"
                  " isolated from Operation System"),
  'label': "Isolated CPUs",
  'restrictions': [],
  'type': 'text',
  'value': '',
  'weight': 10,
  'regex': {
   'source': "^$|^\d+(\s*,\s*\d+)$",
   'error': "Incorrect value"
  }
 }


astute.yaml will be extended as

.. code-block:: yaml

  nvf:
  - node-1:
    - isolated_cpus: [0, 1, 18, 19]

Perhaps in the future Fuel will support many possible NFV features.

REST API
--------

New handlers should be added

.. code-block:: python

 GET /nodes/(?P<node_id>\d+)/attributes
    returns node attributes

    :http: * 200 (successful)
           * 404 (node not found in db)
           * 500 (node has no attributes)

 PUT /nodes/(?P<node_id>\d+)/attributes
    update node attributes

    :http: * 200 (attributes are successfuly updated)
           * 400 (wrong attributes data specified)
           * 404 (node not found in db)
           * 500 (node has no attributes)


Orchestration
=============

For each node with enabled CPU pinning the custom kernel parameters should be
passed to isolate cores for virtual machines

`isolcpu=0,1,18,19`

RPC Protocol
------------

Only payload changes.

Fuel Client
===========

Fuel Client have to show node NUMA topology. New command should be added:

.. code-block:: console

  fuel node --node-id 1 --topology --download

User can use next commands to configure node attributes

.. code-block:: console

  fuel node --node-id 1 --attributes --download/-d
  fuel node --node-id 1 --attributes --upload/-u


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
for virtual machines via Web UI/CLI/API

----------
References
----------

None
