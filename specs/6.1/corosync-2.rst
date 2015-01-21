..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================================
Update pacemaker and corosync infrastructure (Corosync 2.x)
===========================================================

https://blueprints.launchpad.net/fuel/+spec/corosync-2

A next iteration of Corosync & Pacemaker improvements required by scaling
requirements, better Pacemaker management and new OS support.

Problem description
===================

The current Pacemaker implementation has some limitations:

* Doesn't allow to deploy a large amount of OpenStack Controllers

* Operations with CIB utilizes almost 100% of CPU on the Controller

* Corosync shutdown process takes a lot of time

* No support of new OSes as CentOS 7 or Ubuntu 14.04

* Current Fuel Architecture is limited to Corosync 1.x and Pacemaker 1.x

* Fuel fork of corosync module contains a lots of tunings for parallel
  deployment of controllers which cannot be contributed to the upstream yet
  because of the huge diverge of the code base

Proposed change
===============

* Support Fuel Controllers with Corosync 2.3.3 and Pacemaker 1.1.12 packages
  for Centos 6.5 and Ubuntu 14.04

* Get the puppet corosync module from puppetlabs and integrate it. That would
  allow to install and configure Corosync cluster with Pacemaker without
  additional reosurces for the code maintanance.

* Move all custom Fuel changes for corosync and pacemaker providers to the
  separate pacemaker module. That would allow custom changes to not interfere
  with the upstream code.

Alternatives
------------

* Continue to develop and support Fuel fork of corosync module in order to
  make it compatible with Corosync 2 without help from puppet community

* Leave Corosync 1.x infrastructure as is

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

* Corosync 2.x is NOT compatible with previous versions of Corosync 1.x [0].
  Please make sure to upgrade all nodes at once (full-downtime patching)

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

* Deployment process will be improved and will require less time as CIB
  operations will not require 100% CPU time

* Corosync 2.0 has a lot of improvements that allow to have up to 100
  Controllers. Corosync 1.0 scales up to 10-16 node

Other deployer impact
---------------------

None

Developer impact
----------------

* All changes for custom pacemaker providers should go to the separate
  pacemaker module.

* Any changes not related to the providers should be done for corosync module
  and contributed to the upstream as well

Implementation
==============

Assignee(s)
-----------

Primary assignee:
* sgolovatiuk@mirantis.com
* bdobrelya@mirantis.com

Other contributors:
* dilyin@mirantis.com

Work Items
----------

* Replace Corosync 1.x infrastructure with Corosync 2.3.3 and Pacemaker 1.1.12
  at the staging mirrors

* Adapt puppet modules for corosync and pacemaker for Corosync 2.x

* Synchronize corosync manifest with puppetlabs as well

* Push staging mirrors to the public ones once manifests is ready

Dependencies
============

* Corosync 2.3.3 and Pacemaker 1.1.12 packages with dependency libraries

Testing
=======

* Standard swarm testing are required.

* Manual HA testing is required.

* Rally testing is preffered but not mandatory.

Acceptance criteria
-------------------

* Openstack clouds deployed by Fuel are passing OSTF tests with
  Corosync 2.

Documentation Impact
====================

* High Availability guide should be reviewed. For Ubuntu, crm tool stays
  as is, but documentation should be as well enhanced with pcs
  equivivalents for Centos

* Upgrade/Patching impact should be described - corosync 2.x upgrading
  assumes full downtime for cloud

References
==========

.. [0] http://lists.corosync.org/pipermail/discuss/2012-April/001456.html

