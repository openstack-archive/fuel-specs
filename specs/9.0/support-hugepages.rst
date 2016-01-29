..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Support for HugePages for improved performance
==============================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/support-hugepages

User should be able to configure HugePages on compute nodes for
improving performance.


-------------------
Problem description
-------------------

Huge pages give a performance boost to applications which are intensively deal
with memory allocation/deallocation by decreasing memory fragmentation. It
improves the performance of guest workloads by improving TLB cache efficiency.
For workloads that require strong guarantees of guest performance,
such as the Network Function Virtualization (NFV) deployments, they should be
able to get advantage of Huge page feature by benefiting from
improved libvirt driver [1].

[1] https://blueprints.launchpad.net/nova/+spec/virt-driver-large-pages

----------------
Proposed changes
----------------

The flow of actions is:

  1. Due discovery state nailgun-agent collects information about available
     page sizes for each node.

  2. Also nailgun-agent collects information about amount of RAM for node and
     each NUMA node.

  3. User has an ability to enable HugePages and select number of desired pages
     for each page-size from list of available sizes using UI or CLI. This
     configuration can be applied per compute node or per compute NUMA node in
     pre-deployment.

  4. Fuel configures HugePages on selected nodes.

  5. User can create flavor with Huge Pages extra key.

Web UI
======

On node configuration page should be possible to set amount and size of
huge pages per node or per NUMA node.

Nailgun
=======

Collecting the information about available page sizes should be implemented in
nailgun-agent.

HugePages configuration should pass to node kernel parameters.
Also all this information will passed to deployment info.

Node Handlers will process information about HugePages and appropriate
changes should be for the validators

Data model
----------

Node meta will store information about HugePages:

::
  {'numa_nodes': [

    {'numa_number'..., 'cpus'...,

     'memory': 128910,

     'huge_pages': [

       {'size': '2M',
       'count': 500},

       {'size': '1G',
       'count': 20}]

    ...

  }

  'memory': 257032,

  'huge_pages': [
    {'size': '2M',
     'count': 1000},

    ...

  ]

astute.yaml will be extended as

::

  nodes:
  - user_node_name: slave-02_compute
    uid: '2'
    hugepages:
    - enabled: true
      hgpg_config:
      - size: 2M
        count: 1000
      ...
      numa_nodes:
      - node_number: 0
        hgpg_config:
        - size: 2M
          count: 500
        - size: 1G
          count: 20
      ...


if `numa_nodes` isn't presented in `hugepages` it means that
there are no configuration per NUMA node


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

Ability to configure hugepages per node or per NUMA node will be added
to commands:

.. code-block:: bash

  fuel node --node-id 1 --numa --download
  fuel node --node-id 1 --numa --upload

Plugins
=======

None


Fuel Library
============

Library will consume data from astute.yaml
Puppet manifests will perform next actions:

 * enable `KVM_HUGEPAGES`
 * configure nova: change configs
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

User will be able to configure HugePages usage on computes using CLI/UI
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

New feature should be documented, namely changes in API/UI/CLI.


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

* Enable HugePages configuration in Fuel
* Support HugePages configuration via fuel API
* Support HugePages configuration via fuel CLI
* Support HugePages configuration on UI
* Manual testing
* Create a system test for HugePages


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
  per compute node or compute NUMA node


----------
References
----------

https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt
