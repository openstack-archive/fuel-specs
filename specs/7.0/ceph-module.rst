..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================
Extended ceph support
=====================

https://blueprints.launchpad.net/fuel/+spec/ceph-module [1]_

The goal is to improve ceph support in next ways:

	* Fix issues with current deploument code
	* Provide external ceph cluster support
	* Prepare ceph code to be moved to a plugin in next releases
	* Make FUEL to be ready to integrate with external ceph deployment tool
	* Update ceph code to simplify switching to different deployment manifests
	* Evaluate external ceph deploument manifests

Problem description
===================

* Ceph code embedded into many places in Nailgun, which makes it
  maintenance hard
* It's hard to provide external cluster support
* It's hard to deploy ceph with external tool
* Ceph partitioning logic is located in several places

Proposed change
===============

Move most of ceph-related code into package inside FUEL. 
Package should provide a set of tasks classes for ceph deployment
(granular deployment tasks) and factory function, which
obtains user settings and returns set of tasks instances to
be executed.

One more function to be provided to update default partitioning scheme
in case if ceph used.

Volume manager and fuel-agent to be updated to move all ceph partitioning logic
to nailgun. Each time, when nailgun get from UI partitioning scheme for node
it would split cephjournal on separated partitions and store results in DB.
Each time when UI ask for partitioning all cephjournal partiotion on same
drive would be merged.

openstack.yaml would be updated to allow user to pass external cluster auth data.


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