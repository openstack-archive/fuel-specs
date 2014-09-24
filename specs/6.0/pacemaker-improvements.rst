..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Improve Corosync and Pacemaker management
==========================================

https://blueprints.launchpad.net/fuel/+spec/pacemaker-improvements [1]_

A next iteration of Corosync & Pacemaker improvements required by scaling
requirements, better Pacemaker management and new OS support.

Problem description
===================

The current Pacemaker implementation has some limitations:

* doesn't allow to deploy a large amount of OpenStack Controllers

* Operations with CIB utilizes almost 100% of CPU on the Controller

* Corosync shutdown process takes a lot of time

* No support of new OSes as CentOS 7 or Ubuntu 14.04

* Current Fuel Architecture is limited to Corosync 1.x and Pacemaker 1.x

* Puppet service provider for pacemaker doesn't disable Upstart or SystemV
  services by default

* At current implementation ordering between resources is not specified

* Diff operations against Corosync CIB require to save data to file rather
  than keep all data in memory

* Debug process of OCF scripts is not unified requires a lot of actions from
  Cloud Operator

** No granular enough

 Openstack services are not managed by Pacemaker

Proposed change
===============

* Support Fuel Controllers with Corosync 2.0 packages

* Get the puppet corosync module from puppetlabs and integrate it

* Rename OCF resources. Remove __old from resource names

* Refactor service provider and include disabling of the same services under
  systemd/upstart/system v

* Refactor provider and remove diff operation from files

* Add wrapper handler for OCF scripts or unify debug handling of OCF scripts

* Move pacemaker & corosync installation to own stage. Create own corosync.pp
  to make it more granular

Permissive change:

* Add all openstack services to pacemaker and make ordering

Alternatives
------------

All changes are not critical and doesn't affect deployment or Cluster
Operation

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Since Resources will be renamed Upgrade process should delete old resources
on upgrade and delete new resource names on roll back.

Security impact
---------------

None

Notifications impact
--------------------

Please specify any changes to notifications. Be that an extra notification,
changes to an existing notification, or removing a notification.

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

Enchanced pacemaker provider requires some refactoring of puppet manifests
in Fuel Library manifests

Implementation
==============

Assignee(s)
-----------

Primary assignee:
* sgolovatiuk@mirantis.com
* bdobrelya@mirantis.com

Other contributors:
* dilyin@mirantis.com
* vkuklin@mirantis.com
* svasilenko@mirantis.com

Work Items
----------

Mandatory items:

* Replace Corosync 1.0 with Corosync 2.0

* Synchronize corosync manifest with puppetlabs.

* Refactor puppet system provider. It should:

  - Disable systemd/upstart/system v when corosync system
    provider is enabled

* Refactor Corosync provider to perfrom diff operation in
  memory rather than files

* Redesing puppet manifests to start all OCF scripts via
  Wrapper

Permissive items:

* Add openstack services to Pacemaker

* Configure ordering between services in Pacemaker

Dependencies
============

Corosync 2.x packages

Testing
=======

Standard swarm testing are required. Manual HA testing is required.
Rally testing is preffered but not mandatory.

Documentation Impact
====================

High Availability guide should be reviewed. CRM related information
should be replaced with pcs based equivivalents

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/pacemaker-improvements
