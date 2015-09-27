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

  2. User has an ability to enable HugePages for each compute node in
     pending state and select the desired page-size from list of
     available sizes using UI or CLI.

  3. Fuel configures HugePages on selected nodes and creates additional
     Flavor(s) in OpenStack with extra key hw:mem_page_size.

  4. User can use created flavor to start VMs.


Web UI
======

TBA

Nailgun
=======

Collecting the information about available page sizes should be implemented in
nailgun-agent.
Should be added two new tasks:
* Configuration support of HugePages on selected compute nodes
* Creating additional flavor(s) with extra key `hw:mem_page_size=large`.
Also there will be need appropriate changes in validators/serializers/fixtures
according to data model changes.

Data model
----------

Node db model should be extended with new JSON `hugepages_sizes` and
`hugepages_use` fields.

astute.yaml will be extended as

::

  nodes:
  - user_node_name: slave-02_compute
    uid: '2'
    hugepages_use: <SIZE>

where <SIZE> is the size in kB. If `hugepages_use` isn't presented
in astute.yaml it means that hugeapges are disabled for this node.


REST API
--------

There is not need for new API end-points. However, the format of both
request and response data will be changed in the following way:

* GET /api/nodes/<node_id> to read node data.
* PUT /api/nodes/<node_id> to update node Huge Pages settings.
  The data in the requests and responses will be extended with two additional
  fields - `hugepages_sizes` and `hugepages_use`.


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

`fuel node update` command will be modified and used for configuration
HugePages:
There will be added new flag --use-hugepages which will be used to set
size of hugepages or disable this feature, by providing `None` value.
`fuel node show` will be used to show both current and possible page sizes.

Plugins
=======

None


Fuel Library
============

Library will consume data from astute.yaml
Puppet manifests will be adjusted to configure HP and flavors


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

Users won't be able to upgrade their environments to environment with HP.
This feature will be enabled for new environments only.


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
  fzhadaev

Other contributors:
  iponomarev

Mandatory design review:
  ikalnitsky
  kozhukalov
  sgolovatiuk

QA engineer:
  vkrayneva


Work Items
==========

* Nailgun-agent (page sizes discovering)
* Nailgun (change db_models, validators, serializers, add API, tasks, fixtures)
* Library (configuring hugepages in OS, creating new flavor)
* UI/CLI (add work with new API)
* QA part (not known yet)


Dependencies
============

None


-----------
Testing, QA
-----------

* Manual UI testing should be run according to the use cases steps
* Manual CLI testing should be run according to the use cases steps
* System tests should be created for the huge pages


Acceptance criteria
===================

* It should be possible to enable and set huge pages in Fuel
  for each compute node
* Flavors with extra key `hw:mem_page_size=large` are available after enabled
  and we can use created flavor to start VMs.


----------
References
----------

https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt
