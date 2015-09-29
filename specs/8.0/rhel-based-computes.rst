..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
RHEL-based computes support
==========================================

Launchpad blueprint:
https://blueprints.launchpad.net/fuel/+spec/rhel-based-computes

Fuel should be able to work with preinstalled RHEL-based computes
in the next release of Fuel 8.0.
The best way to do that is use fuel plugin architecture.

--------------------
Problem description
--------------------

A detailed description of the problem:

* RHEL OS should be prepared(installed) on fuel slave node.

* ssh key or password should be defined for RHEL prepared node.

* Admin interface should be connected to the fuel admin network
  interface and configured for dhcp.

* Fuel plugins will be used to add new preprovisioned OS.

----------------
Proposed changes
----------------

Fuel RHEL-based-compute plugin should include:

    * Roles (Compute on RHEL)
    * List of supported OS and Realses (RHEL 7.0, RHEL 7.0.1 for example)
    * Install command (yum install <package>)
    * List of default repositories for supported operation system
    * Puppet manifests


Web UI
======

None

Nailgun
=======

None

Data model
----------

None


REST API
--------

None

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

RHEL based computes can be realized as based configuration of fuel.
In this case all changes should be moved to fuel-library upstream.
Fixtures should include new position of supported OS RHEL,CentOS,etc.

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

* Shared access to RHEL installed node (ssh key/password) with fuel

* After removing node from cluster node and data on this node
  will not be erased

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

* User should prepare RHEL OS manually

* Configure admin interface and connect to fuel network

* Create root password or upload fuel pub key to preprovisioned node

* Use dashboard to add node preprovisioned node to pool


------------------
Performance impact
------------------

Provision stage will be skipped

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

None

--------------------------------
Infrastructure/operations impact
--------------------------------

* MOS should support RHEL repositories

--------------------
Documentation impact
--------------------

Documentation should include restriction of adding RHEL
preprovisioned nodes.


--------------------
Expected OSCI impact
--------------------

Expected and known impact to OSCI should be described here. Please mention
whether:

* New RHEL mirror should be added

* Supporting RHEL packages


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  <iponomarev>

Other contributors:
  <asvechnikov>

Mandatory design review:
  <sgolovatiuk>


Work Items
==========


- DEVOPS - installation RHEL on compute node
- Build compute packages for RHEL
- Extend and add puppet modules for RHEL to plugin

Dependencies
============

* https://blueprints.launchpad.net/fuel/+spec/pre-provisioned-nodes-support
  RHEL based computes depends on preprovisioned nodes support

------------
Testing, QA
------------

* Manual UI testing should be run for deployment with Compute on RHEL
* Manual CLI testing should be run for deployment with Compute on RHEL
* System tests should be created for the new deploy
  procedure with Pre-provisioned RHEL node

===================

* Customer can deploy already added to Fuel pre-provisioned RHEL
  node as a Compute node.
* Customer can remove RHEL nodes from their cloud using Fuel
* Customer can return removed node to cluster
* Customer can reinstall RHEL OS on node
* Customer can change or add new RHEL repositories
* Customer can configure network settings
* Customer can use connectivity check for networks


----------
References
----------

None
