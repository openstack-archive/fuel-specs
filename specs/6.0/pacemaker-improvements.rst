..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Improve Pacemaker Configuration and Management
==========================================

https://blueprints.launchpad.net/fuel/+spec/pacemaker-improvements [1]_


Problem description
===================
The current Pacemaker implementation has some limitations that:

* doesn't allow to to deploy a large amount of OpenStack Controllers by Fuel
* operations with CIB takes almost 100% of CPU
* current implementation is limited to corosync 1.x and pacemaker 1.x which
makes almost impossible to make HA on Ubuntu 14.04 or CentOS 7
* service provider for corosync doesn't disable upstart/system V services
* diff operations over CIB require save to /tmp rather than keep the data in memory
* some resources have really weird names
* not all resources are added to corosync, half or resources are managed by upstart/system V
that doesn't allow to unify an aproach
* Corosync shutdown time is bad. Sometimes shutdown or reboot hangs


Proposed change
===============

Mandatory
* Rename OCF vip.*old resources to proper names
* Sync latest puppetlabs corosync upstream puppet module
* Add wrapper handlers for manual control and/or debugging of ocf services
  (example: http://review.openstack.org/#/c/116825 ) 
  OR just add debug parameter for all pacemaker resources under OCF control plane
* Refactor puppet service provider. It should disable upstart/systemd/system V init
  when we use pacemaker as a service control plane
* Update to Corosync 2.0, Pacemaker 1.1.12

Nice to have:
* Move all Openstack services under pacemaker control plane.

Alternatives
------------

Leave as is

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Then patching Openstack cloud, vip.*old resources in pcs should be deleted due to renaming.

Security impact
---------------

Unknown.
Upgrading corosync and pacemaker packages could be the source of new security issues

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

Enhanced pacemaker provider for service core provider in Puppet will require some
minor refactoring in fuel library manifests as well.

Implementation
==============

Mandatory
* Rename OCF vip.*old resources to proper names
* Sync latest puppetlabs corosync upstream puppet module
* Add wrapper handlers for manual control and/or debugging of ocf services
  (example: http://review.openstack.org/#/c/116825 ) 
  OR just add debug parameter for all pacemaker resources under OCF control plane
* Refactor puppet service provider. It should disable upstart/systemd/system V init
  when we use pacemaker as a service control plane
* Update to Corosync 2.0, Pacemaker 1.1.12

Nice to have:
* Move all Openstack services under pacemaker control plane.

Assignee(s)
-----------

Feature Lead: Sergii Golovatiuk
Mandatory Design Reviewers: Bogdan Dobrelia, Dmitry Ilyin, Vladimir Kuklin
Developers: Dmitry Ilyin, Sergii Golovatiuk, Bogdan Dobrelia
QA: Andrey Sledzinskiy

Primary assignee:
  sgolovatiuk

Other contributors:
  bogdando, idv1985, vkuklin

Work Items
----------

Mandatory
* Rename OCF vip.*old resources to proper names
* Sync latest puppetlabs corosync upstream puppet module
* Add wrapper handlers for manual control and/or debugging of ocf services
  (example: http://review.openstack.org/#/c/116825 )
  OR just add debug parameter for all pacemaker resources under OCF control plane
* Refactor puppet service provider. It should disable upstart/systemd/system V init
  when we use pacemaker as a service control plane
* Update to Corosync 2.0, Pacemaker 1.1.12

Nice to have:
* Move all Openstack services under pacemaker control plane.

Dependencies
============

Update Corosync, Pacemaker packages

Testing
=======

Standard swarm testing jobs we have in CI should handle these changes as well.

Documentation Impact
====================

If Openstack resources will be moved under pcs, that should be reflected in docs as well.

References
==========

None
