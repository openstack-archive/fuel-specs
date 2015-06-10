..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================
Extended ceph support
=====================

https://blueprints.launchpad.net/fuel/+spec/ceph-module [1]_

The goal is to improve ceph support and make code cleanup in next ways:

	* Update deployment code:
	  fix placement group calculation, get rid of ceph-deploy.
	* Provide external ceph cluster support
	* Prepare ceph code to be moved to a plugin in next releases - 
	  extract all ceph-related code into functions.
	* Make FUEL to be ready to integrate with external ceph deployment tool -
	  update ceph deployment task to define external deployment tool integration
	  points. External tool would act as drop-in replacement for ceph deploy code.
	* Update ceph code to simplify switching to different deployment manifests.
	* Evaluate defaul puppet ceph manifests. Switch to them, if they works ok.

Problem description
===================

* Ceph code is embedded into many places in Nailgun, which makes it
  maintenance hard
* It's hard to provide external cluster support
* It's hard to deploy ceph with external tool
* Ceph partitioning logic is located in several places
* Defaul partitiong scheme can be improved - propose to user to use
  SSD as a journals, etc.

Proposed change
===============

Move most of ceph-related code into a module inside FUEL

Update UI to allow user to provide external cluster credentials.
When user select "external ceph cluster" fields for root node ip
and key file became awailable, role 'ceph-osd' became disabled.

When external cluster selected next action would take a place:

 * Deployment of ceph-mon is skipped
 * cinder-volume is deployed on controller, as now
 * User-provided ceph credentials is used for OS services
 * Radosgw might not be installed, depending on user settings

This would be done by updating puppet manifests and by adding
puppet tasks for ceph-gateway.

Volume manager and fuel-agent to be updated to move all ceph partitioning logic
to nailgun. Each time, when nailgun get from UI partitioning scheme for node
it would split cephjournal on separated partitions and store results in DB.
Each time when UI ask for partitioning all cephjournal partiotion on same
drive would be merged.

Alternatives
------------

Data model impact
-----------------

External clusters info would need to be stored in DB. cephjournal 
would be stored in DB as set of partitions.

REST API impact
---------------

Upgrade impact
--------------

Security impact
---------------

Notifications impact
--------------------

Other end user impact
---------------------

UI changes would be required to allow user to provide 
ceph cluster connection info and select ceph management tool.
Changes can be made by modifing openstack.yaml and would requires no
JS/HTML code to be changed.

Performance Impact
------------------

Plugin impact
-------------

Other deployer impact
---------------------

Developer impact
----------------

Infrastructure impact
---------------------

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  kdanylov

Other contributors:
  diurchenko, akiselyova, yportnova, gstepanov,rzarzynski

Work Items
----------

Dependencies
============

Testing
=======

UI should allows to enter external ceph cluster creds and FUEL should connect
OS to provided OS cluster

Documentation Impact
====================


References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/ceph-module
.. [2] https://mirantis.jira.com/wiki/display/MOL/Ceph+API+for+FUEL
.. [3] https://github.com/01org/virtual-storage-manager