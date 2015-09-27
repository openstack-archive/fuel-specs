..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Support for HugePages for improved performance
==============================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/support-hugepages

User should be able to configure and use HugePages on compute nodes for
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

New widget should be added. It should give to user the possibility to enable
HugePages for selected node(s) and select page size from the
list of available sizes for this node(s).


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

Node db model should be extended with new JSON 'available_pagesizes' and
'pagesize' fields.


REST API
--------

No changes are needed


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

CLI will be extended with new commands like:
  * fuel node get-available-pagesizes --node-id ID
  * fuel node set-pagesize --node-id ID --pagesize PAGESIZE


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

TBD


--------------------------------
Infrastructure/operations impact
--------------------------------

TBD

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
  vvalyavskiy

Mandatory design review:
  TBD


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

TBA


Acceptance criteria
===================

TBA


----------
References
----------

None
