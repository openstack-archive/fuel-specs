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

Huge Pages give a performance boost to applications which are intensively deal
with memory allocation/deallocation by decreasing memory fragmentation. It
improves the performance of guest workloads by improving TLB cache efficiency.
For workloads that require strong guarantees of guest performance,
such as the Network Function Virtualization (NFV) deployments, they should be
able to get advantage of Huge Pages feature by benefiting from
improved libvirt driver [1].

[1] https://blueprints.launchpad.net/nova/+spec/virt-driver-large-pages

Also, Huge Pages configuration can be applied per NUMA node, for more
description about support NUMA node take a look [2].

[2] https://blueprints.launchpad.net/fuel/+spec/support-numa-cpu-pinning

----------------
Proposed changes
----------------

The flow of actions is:

  1. Due discovery state nailgun-agent collects information about available
     page sizes for each node.

  2. Also nailgun-agent collects information about amount of RAM for node and
     each NUMA node.

  3. User has an ability to enable Huge Pages and select number of desired pages
     for each page-size from list of available sizes using UI or CLI. This
     configuration can be applied per compute node or per compute NUMA node in
     pre-deployment.

  4. Fuel configures Huge Pages on selected nodes.

  5. User can create flavor with Huge Pages extra key.

Web UI
======

TBA

Nailgun
=======

Collecting the information about available page sizes should be implemented in
nailgun-agent. For this purposes will be used <TBD>.
Information about memory should be done at [2].


Huge Pages configuration should be passed to node kernel parameters and
astute.yaml.

New validation should be added.

Data model
----------

Node meta will store information about available Huge Pages:

.. code-block:: json

  'topology': {
    'available_hgpgs': ['2M', '1G']
    'numa_nodes': {
      ...
    }
  }

Huge Pages user's configuration will be stored in node.attributes as:

.. code-block:: json

  {
    'description': "Huge Pages configuration per compute or per NUMA node",
    'label': 'Huge Pages',
    'restrictions': [],
    'type': 'hgpgs',
    'value': {
      'node': [
        {'size': '2M',
         'count': 512},
        {'size': '1G',
         'count': 8},
      ],
      'numa_nodes': [
        {'numa_id': 0,
         'size': '2M',
         'count': 512}
        {'numa_id': 1,
         'size': '1G',
         'count': 8}
      ]
    },
    'weight': 20,
    'regex': {
      'source': "",
      'error': ""
    }
   }

User can specify configuration per `node` or per `numa_node`

astute.yaml will be extended as

.. code-block:: yaml

  nfv:
    node-1:
      huge_pages:
        enabled: true
        node:
        - {count: 512, size: 2M}
        - {count: 8, size: 1G}
        numa_nodes:
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

User will have an ability to download topology

.. code-block:: bash

  fuel node --node-id 1 --topology

and configure Huge Pages by using

.. code-block:: bash

  fuel node --node-id 1 --attributes --download/-d
  fuel node --node-id 1 --attributes --upload/-d

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
  asvechnikov
  skolekonov

Mandatory design review:
  TBA

QA engineer:
  TBA


Work Items
==========

* Enable Huge Pages configuration in Fuel
* Support Huge Pages configuration via fuel API
* Support Huge Pages configuration via fuel CLI
* Support Huge Pages configuration on UI
* Manual testing
* Create a system test for Huge Pages


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/support-numa-cpu-pinning


-----------
Testing, QA
-----------

* Manual UI testing should be run according to the use cases steps
* Manual CLI testing should be run according to the use cases steps
* System tests should be created for the huge pages


Acceptance criteria
===================

* It should be possible to enable and set huge pages in Fuel
  per compute node or compute NUMA node via Web UI/CLI/API


----------
References
----------

https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt
