..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Support for HugePages for improved performance
==============================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/support-hugepages

User should be able to configure Huge Pages on compute nodes for
improving performance.


-------------------
Problem description
-------------------

When a process uses some memory, the CPU is marking the RAM as used by
that process. For efficiency, the CPU allocate RAM by chunks of 4K bytes
(it's the default value on many platforms). Those chunks are named pages.
Those pages can be swapped to disk, etc.

Since the process address space are virtual, the CPU and the operating
system have to remember which page belong to which process, and where it
is stored. Obviously, the more pages you have, the more time it takes to
find where the memory is mapped. When a process uses 1GB of memory, that's
262144 entries to look up (1GB / 4K). If one Page Table Entry consume 8bytes,
that's 2MB (262144 * 8) to look-up.

----------------
Proposed changes
----------------

Huge Pages give a performance boost to applications which are intensively deal
with memory allocation/deallocation by decreasing memory fragmentation [1]_. It
improves the performance of guest workloads by improving TLB cache efficiency.
For workloads that require strong guarantees of guest performance,
such as the Network Function Virtualization (NFV) deployments, they should be
able to get advantage of Huge Pages feature by benefiting from
improved libvirt driver [2]_.

Also, Huge Pages configuration can be applied per NUMA node, for more
description about support NUMA node take a look [3]_. User will have an
ability to specify configuration for whole node. Distribution of Huge Pages
on NUMA nodes will be processed by Nailgun.

Enabling of Huge Pages is required:

  * Collect information about abailable pages size and RAM per NUMA node

  * User has an ability to select number of desired pages from list of
    available sizes using UI or CLI for each node. This pages will be
    used by Nova

  * Fuel configures Huge Pages on selected nodes and applies
    appropriate Nova configuration

Web UI
======

Nova Huge Pages section will be rendered in "NFV" section as several
fields per page size as described in data model section.

Nailgun
=======

Collecting the information about available page sizes and memory should be
implemented in nailgun-agent. For this purposes will be used `lstopo` and
system files.

Huge Pages configuration should be passed to astute.yaml.

New validation should be added.

Data model
----------

Node metadata topology will be extented with information about available
Huge Pages and RAM per NUMA node:

.. code-block:: json

  node.metadata = {
    ...
    'topology': {
      'available_hugepages': ['2M', '1G']
      'numa_nodes': [
         {'id': 0,
          'cpus': ...,
          'memory: 135171932160},
         {'id': 1,
          'cpus': ...,
          'memory': 135289372672}]
      ]
      'distances': [
        [...],
        [...]
      ]
    }
    ...
  }

Collecting cpus information should be covered in NUMA/CPU pinning
part.

Huge Pages user's configuration will be stored in node.attributes as:

.. code-block:: json

  node.attributes = {
    ...
    'nova_hugepages':{
      'weight': 20,
      'description': "Nova Huge Pages configuration",
      'label': "Nova Huge Pages",
      'type': 'custom_hugepages',
      'value': {
        '<size>': <count>,
        '1G': 10
      }
    },
    ...
   }

Where `<size>` can be only available Huge Pages sizes. For all remaining memory
will be used default 4K page size.

Nailgun makes Huge Pages distribution per NUMA node

astute.yaml will be extended as

.. code-block:: yaml

  nova:
    ...
    enable_hugepages: true
  system_configuration:
    ...
    hugepages:
    - {count: 512, numa_id: 0, size: 2M}
    - {count: 8, numa_id: 1, size: 1G}


REST API
--------

There is not need for new API end-points.

Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

User will have an ability to look at topology

.. code-block:: bash

  fuel node --node-id 1 --numa-topology

and configure Huge Pages by using

.. code-block:: bash

  fuel node --node-id 1 --attributes --download/-d
  fuel node --node-id 1 --attributes --upload/-u

or by using fuel2 client

.. code-block:: bash

  fuel2 node show-numa-topology 1

  fuel2 node download-attributes 1
  fuel2 node upload-attributes 1

Plugins
=======

None


Fuel Library
============

Library will consume data from astute.yaml
Puppet manifests will perform next actions:

 * enable `KVM_HUGEPAGES`
 * configure nova: change config file
 * reboot appropriate services

In case of configuration is applied per NUMA node, this configuration
will be passed to

   `/sys/devices/system/node/node0/hugepages/hugepages-<SIZE>kB/nr_hugepages`


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

User will be able to configure Huge Pages usage on computes using CLI/UI
or with API request.


------------------
Performance impact
------------------

It will not impact on Fuel performance.


-----------------
Deployment impact
-----------------

All was already mentioned.

----------------
Developer impact
----------------

None


--------------------------------
Infrastructure/operations impact
--------------------------------

None

--------------------
Documentation impact
--------------------

New feature should be documented, namely changes in API/Web UI/CLI.


--------------------
Expected OSCI impact
--------------------

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Artur Svechnikov <asvechnikov>
  Sergey Kolekonov <skolekonov>

Other contributors:
  Alexander Saprykin <cutwater>
  Ivan Ponomarev <ivanzipfer>

QA engineer:
  Ksenia Demina <kdemina>
  Veronica Krayneva <vkrayneva>
  Sergey Novikov <snovikov>


Work Items
==========

* Modify Nailgun-agent to collect available Huge Pages sizes and
  NUMA nodes RAM
* Modify Nailgun part for Huge Pages configuration processing
* Modify Fuel Library part for Huge Pages configuration processing
* Support Huge Pages configuration via Fuel API
* Support Huge Pages configuration via Fuel CLI
* Support Huge Pages configuration on UI
* Manual testing


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/support-numa-cpu-pinning


-----------
Testing, QA
-----------

* Extend TestRail with Manual CLI cases for the topology information
* Extend TestRail with Manual CLI cases for the Huge Page configuration per compute
* Extend TestRail with Manual CLI cases for the Huge Page configuration per numa node
* Extend TestRail with Manual WEB UI cases for the Huge Page
* Lead manual CLI testing for the new test cases


Acceptance criteria
===================

* User is provided with interface (Web UI/CLI/API) to enable and set Huge Pages in Fuel
  per compute node or compute NUMA node
* New test cases are executed succesfully

----------
References
----------

.. [1] https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt
.. [2] https://blueprints.launchpad.net/nova/+spec/virt-driver-large-pages
.. [3] https://blueprints.launchpad.net/fuel/+spec/support-numa-cpu-pinning
