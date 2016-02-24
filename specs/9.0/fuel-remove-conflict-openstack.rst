..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Remove conflicting openstack module parts
==========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-remove-conflict-openstack

The openstack module `deployment/puppet/openstack` has been obsolete for a
long time in puppet-openstack, and with the migration to the tasks
composition layer in fuel, it is obsolete, making only more work for people
who need to maintain manifests that intersect with it.

Portions of the openstack module conflict with supporting detached OpenStack
version (proper, not the module) as defined in `fuel-openstack-tasks`_



--------------------
Problem description
--------------------

Some of the tasks make indirect calls to puppet-openstack modules via the
openstack module. In these cases, overloading the tasks as described in
`fuel-openstack-tasks`_ will not result in success as it depends on being able
change the calls between the task and puppet-openstack to support a specific
version of the puppet-openstack modules.

In these cases the declaration of classes and resources from the
puppet-openstack modules must be moved to the task itself and may not proxy
through openstack module anymore

In this way we would change:

  cinder task => openstack::cinder => ::cinder
  swift  task => openstack::swift  => ::swift
  ...

It would become:

  cinder task => ::cinder
  swift task  => ::swift


----------------
Proposed changes
----------------

As described in Problem description, we will move the declaration of
puppet-openstack classes and resources from the openstack module to its
corresponding granular puppet task

Web UI
======

None

Nailgun
=======

None

Data model
----------

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

At a minimum the following openstack module manifests have to be moved up
to their corresponding task::

  deployment/puppet/openstack/manifests/auth_file.pp
  deployment/puppet/openstack/manifests/ceilometer.pp
  deployment/puppet/openstack/manifests/cinder.pp
  deployment/puppet/openstack/manifests/compute.pp
  deployment/puppet/openstack/manifests/glance.pp
  deployment/puppet/openstack/manifests/heat.pp
  deployment/puppet/openstack/manifests/horizon.pp
  deployment/puppet/openstack/manifests/keystone.pp
  deployment/puppet/openstack/manifests/nova/controller.pp
  deployment/puppet/openstack/manifests/swift/proxy.pp

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

This will further reduce the tech debt around the openstack module by
removing more code out of it. This will simplify the interaction between the
task and the module it calls making it easier for new developers to work on
fuel-library



---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  Andrew Woodward (xarses)

Other contributors:
  <launchpad-id or None>

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

* Further identify any additional of the openstack manifests that need to be
  worked on for 9.0

* remove impacted openstack manifests by moving their calls into their
  respective tasks.


Dependencies
============

Related to `fuel-openstack-tasks`_


------------
Testing, QA
------------

Existing testing coverage should be sufficient to ensure that there are no
regressions introduced by these changes. In some cases, it may be necessary
to extend the NOOP coverage to cover changes.

Acceptance criteria
===================

* Impacted openstack manifests previously identified no longer exist

* puppet-openstack classes and resource should be declared in granular puppet
  tasks directly, not via the indirection in the openstack module.


----------
References
----------

https://blueprints.launchpad.net/fuel/+spec/fuel-openstack-tasks

Spec for `fuel-openstack-tasks`_

.. _`fuel-openstack-tasks`: https://review.openstack.org/#/c/281557/
