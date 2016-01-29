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

Most CPUs support multiple memory page sizes, ranging from 4k through
2MB/4MB upto as large as 1 GB. OpenStack also permit us to use different
memory page sizes in flavors. Fuel should have an ability to provide users
with Huge Page configuration

----------------
Proposed changes
----------------

Huge Pages give a performance boost to applications that intensively deal
with memory allocation/deallocation by decreasing memory fragmentation [1]_. It
improves the performance of guest workloads by improving TLB cache efficiency.
For workloads that require strong guarantees of guest performance,
such as the Network Function Virtualization (NFV) deployments, they should be
able to get advantage of Huge Pages feature by benefiting from
improved libvirt driver [2]_.

Also, Huge Pages configuration can be applied per NUMA node, for more
description about support NUMA node take a look [3]_. Operator will have an
ability to specify configuration for whole compute node. Distribution of Huge Pages
on NUMA nodes will be processed by Nailgun.

Enabling of Huge Pages requires:

  * Collect information about available pages size and RAM per NUMA node [3]_

  * Operator must have an ability to select number of desired pages from list of
    available sizes using UI or CLI for each node. This pages will be
    used by Nova

  * Fuel have to configure Huge Pages on selected nodes and applies
    appropriate Nova configuration

Web UI
======

Nova and DPDK Huge Pages sections will be rendered in "NFV" section of node
details dialog as several fields per page size as described in data model
section.

For more detailed example please take a look at [3]_.

Nailgun
=======

Collecting the information about available page sizes and memory should be
implemented in nailgun-agent. For this purposes will be used `lstopo` and
system files.

Example of collected information can be viewed here [3]_.

Huge Pages configuration should be passed to astute.yaml.

New validation should be added. User can't specify more Huge Pages than
system possesses.

Data model
----------

`numa_topology` section of node.metadata will contain information about available
Huge Pages and RAM per NUMA node [3]_:

Huge Pages User's configuration will be stored in node.attributes as:

.. code-block:: json

  node.attributes = {
    ...
    'nova_hugepages': {
      'weight': 20,
      'description': "Nova Huge Pages configuration",
      'label': "Nova Huge Pages",
      'type': 'custom_hugepages',
      'value': {
        '<size>': <count>,
        '1G': 10
      }
    },
    'dpdk_hugepages': {
      'weight': 20,
      'description': "DPDK Huge Pages per NUMA node in MB",
      'label': "DPDK Huge Pages",
      'type': 'text',
      'value': '128',
      'regex': {
        'source': "^\d+$",
        'error': "Incorrect value"
      }
    ...
   }

Where `<size>` can only be one of the available Huge Pages sizes. For all
remaining memory will be used default 4K page size.
`value` for `nova_hugepages` will be filled within creating of node when
available page sizes are known, default count of pages will be 0.

Nailgun will make huge pages distribution per NUMA node according memory and
User input.

astute.yaml will be extended as

.. code-block:: yaml

  nova:
    ...
    enable_hugepages: true
  dpdk:
    ...
    ovs_socket_mem: 128,128,128,128
  hugepages:
  - {count: 512, numa_id: 0, size: 2M}
  - {count: 8, numa_id: 1, size: 1G}

`ovs_socket_mem` contains information about Huge Pages size in MB per
NUMA node. DPDK driver needs only total amount of memory on each NUMA
node, not exact information about how many pages of each size should
be allocated. It uses lazy logic to allocate needed amount of memory.
I.e. if 1G pages are available - they will be used first, then 2M pages etc.

REST API
--------

API described in [3]_.

Validation should check User configuration whether RAM is enough for specified
Huge Pages.

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

Changes described here [3]_

Plugins
=======

None

Fuel Library
============

Puppet manifests will perform next actions:

 * enable `KVM_HUGEPAGES` for qemu-kvm daemon in
   `/etc/default/qemu-kvm` and notify `qemu-kvm`
 * configure Nova: enable additional scheduler filters on controller nodes
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

Changes described here [3]_

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

It possible that User reserves large amount of memory for Huge Pages.
Thus, there are not enough RAM for OS processes.


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

Mandatory design review:
  Igor Kalnitsky <ikalnitsky>
  Sergii Golovatiuk <sgolovatiuk>
  Dmitry Borodaenko <dborodaenko>
  Vitaly Kramskikh <vkramskikh>

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
* Extend TestRail with Manual CLI cases for the Huge Page configuration
  per compute
* Extend TestRail with Manual CLI cases for the Huge Page configuration
  per numa node
* Extend TestRail with Manual WEB UI cases for the Huge Page
* Lead manual CLI testing for the new test cases
* Performance testing
* Extend TestRail with manual cases for Huge Page functionality in OpenStack


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
