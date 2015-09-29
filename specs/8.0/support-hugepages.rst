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

Huge pages give a performance boost to applications that are memory and
compute intensive. It improves the performance of guest workloads by improving
TLB cache efficiency.
For workloads that require strong guarantees of guest performance,
such as the Network Function Virtualization (NFV) deployments, they should be
able to get advantage of Huge page feature by benefiting from
improved libvirt driver.

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

Node details pop-up of compute nodes should be updated to give End User
an ability to manage HugePages settings.
User should be able to enable/disable HugePages for a particular node.
If HugePages is active for the node, then user should be able to select
a particular page size for the node from a list of available sizes
(`available_pagesizes` attribute of Node model provides the list of sizes).

Page size for the node should be set to `hugepages_size` attribute of
Node model (`Null` value means that HugePages is not active for the node).


Nailgun
=======

Collecting the information about available page sizes should be implemented in
nailgun-agent.
Should be added two new tasks:
* Configuration support of HugePages on selected nodes
* Creating additional flavor(s) with extra key `hw:mem_page_size=large`.
Also there will be need appropriate changes in validators/serializers/fixtures
according to data model changes.

Data model
----------

Node db model should be extended with new JSON `available_pagesizes` and
`hugepages_size` fields.


REST API
--------

There is not need for new API end-points. However, the format of both
request and response data will be changed in the following way:

* GET /api/nodes/<node_id> to read node data.
* PUT /api/nodes/<node_id> to update node Huge Pages settings.
  The data in the requests and responses will be extended with two additional
  fields - `available_pagesizes` and `hugepages_size`.


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
There will be added new flag --hugepages-size which will be used to set
size of hugepages or disable this feature, by providing `None` value.
`fuel node show` will be used to show both current and possible page sizes.

Plugins
=======

None


Fuel Library
============

Functionality of configuring HugePages.
Functionality of creating new flavor(s) in OpenStack.


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

HugePages usage will result in VMs' performance boosting.


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
  sgolovatiuk
  vkramskikh

QA engineer:
  vkrayneva


Work Items
==========

* Nailgun (change db_models, validators, serializers, add API, tasks, fixtures)
* Nailgun-agent (page sizes discovering)
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
* Existing UI functional test of node component should cover the change
* Manual CLI testing should be run according to the use cases steps
* System tests should be created for the huge pages


Acceptance criteria
===================

* It should be possible to manage huge pages settings in Fuel for each compute
  node via API/CLI/UI.
* Flavors with extra key `hw:mem_page_size=large` are available after enabled
  and we can use created flavor to start VMs.


----------
References
----------

None
