..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================
Minimal RHEL 7 support in MOS as a compute node
===============================================

https://blueprints.launchpad.net/fuel/+spec/rhel-compute-nodes

--------------------
Problem description
--------------------

* As a Cloud owner I want to introduce pre-provisioned RHEL hosts into my MOS
  cloud as Compute nodes so that I could run my RHEL-certified workloads on it

----------------
Proposed changes
----------------

A Minimal Viable Product is to provide detailed documentation for enabling
minimal RHEL 7 support in MOS as a compute node to work under Ubuntu-based
control plane. This documentation should consist of following parts:

* How to validate that RHEL node is ready to be used as compute node
  (validate network interfaces, disks);

* How to add MOS repositories to this node;

* How to install minimal required set of packages on top of pre-provisioned
  RHEL 7 node to have a possibility to run puppet granular tasks
  from Fuel Library;

* How to prepare configuration in astute.yaml for Fuel Library tasks;

* Desription of the procedure (with automated/scripted steps where it's
  possible) to deploy MOS packages on a pre-provisioned RHEL node and
  configure Compute services using granular puppet tasks from Fuel Library.

RHEL 7 Compute nodes will not be integrated with Fuel (no UI, nailgun and etc
changes are required).

Feature is targeted to Fuel 8.0 release, so each enivonment which was deployed
by Fuel 8.0 version supports adding of RHEL 7 compute node to it.

Upon successfully delivering MVP for this feature in 8.0 we can continue with
this feature in 9.0 - full track of RHEL packages, automate deployment and
support RHEL computes at scale. Also another roles can be supported.


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

Fuel Library may need to be updated to work on RHEL (Fuel common tasks,
l23network, neutron-l2-agent and nova-compute related manifests).
This changes will be RHEL-specific (won't affect Ubuntu deployments).

------------
Alternatives
------------

Implement full support of RHEL compute nodes managed by Fuel:

* Adapt Fuel-related package and source code (mcollective, nailgun-agent
  and etc) for RHEL

* Implement provisioning of RHEL nodes

* Support RHEL subscription (allow user to provide RHEL license)

* Integrate RHEL nodes with Fuel Architecture

* Allow Fuel to deploy environments with multiple operating systems

--------------
Upgrade impact
--------------

If an existing cluster was upgraded to MOS 8.0, then it's possible
to add RHEL computes to it.

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

None

------------------
Performance impact
------------------

None

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

All implementation steps should be fully documented and contain examples
of commands and templates for configuration files.

--------------
Implementation
--------------

The following workflow should be considered:

* User creates base MOS cloud (Fuel Master + Controllers) using standard Fuel
  flow (UI or CLI). The target environment configuration to be considered is:

  * Ubuntu on Controllers
  * Neutron+OVS (VXLAN, VLAN) on networking layer
  * Ceph storage for Nova, Glance, Cinder (managed by Fuel, host OS is Ubuntu)

* User validates base requirements for Compute node (disks, network interfaces)

* User validates connection to MOS repositories and configures them
  on RHEL node

* User installs base packages for Fuel Library granular tasks and adds
  all required puppet modules on RHEL node

* User prepares astute.yaml for puppet tasks based on template
  which is provided in documentation

* User connects pre-provisioned (provisioned and configured without Fuel)
  RHEL node to MOS Management network using Fuel Library 'netconfig' task

* User configures installed MOS packages to have services up and running
  managed by puppet granular tasks from Fuel Library

* User validates RHEL compute functionality using instructions. At least Nova
  compute and Neutron openvswitch services should be run and visible
  from controller nodes. Checking of other services depends on Fuel
  environment configuration and it will be described in documentation as well.


Assignee(s)
===========

Primary assignee:
  Ivan Berezovskiy

Other contributors:
  Sergey Kolekonov
  Mykyta Karpin

Mandatory design review:
  Sergii Golovaiuk
  Vladimir Kuklin
  Evgeny Konstantinov

QA engineer:
  Timur Nurlygayanov

Work Items
==========

* Documentation with instructions which describes how to deploy RHEL compute

Dependencies
============

------------
Testing, QA
------------

* Manual testing of RHEL 7 nodes in a certain lab environment

* Automate testing on CI using RHEL 7 based computes. Some new
  tests will be added to existing SWARM test suite by MOS QA team.

* Perfomance testing on real hardware with RHEL 7


Acceptance criteria
===================

* Cloud Deployment engineer can validate whether RHEL node is ready
  to be introduced into MOS cloud as a compute node:

  * Network interfaces are sufficient and can be configured to operate with
    Neutron+OVS (VXLAN).

  * Disk size and partitioning is sufficient/feasible to enable basic
    MOS services on Compute node.

  * Packages are successfully installed without any conflicts with official
    RHEL packages

* Cloud Deployment engineer can deploy MOS packages on existing RHEL node
  and standup+configure MOS services to operate under control of Ubuntu-based
  control plane

* Cloud Deployment engineer can validate that newly introduced RHEL node
  is operational and can be introduced into an operating MOS cloud

* There is the way to test all changes to OpenStack components (for Nova and
  Neutron projects in 8.0-liberty branch) and their dependencies
  under RHEL as well as Ubuntu (automatically or manually)

----------
References
----------

1. LP Blueprint https://blueprints.launchpad.net/fuel/+spec/rhel-compute-nodes
