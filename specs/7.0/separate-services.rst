..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Separate Controller Services onto Separate Nodes
================================================

https://blueprints.launchpad.net/fuel/+spec/detach-components-from-controllers

Some deployers require flexibility in locating services for a multitude of
reasons. Some of these could be geographic, related to load balancing,
or necessary for scale.

Problem description
===================

Currently all services are bundled into the controller (with a few exceptions).
True granularity will allow a deployer to work around potential issues.

Proposed change
===============

Each controller service needs to be modified so that it can be detached from
the controller role and deployed independently. This includes not only the
supporting services in Fuel, such as Galera and RabbitMQ, but potentially
all OpenStack services. For the scope of this spec, only Keystone and Horizon
are covered.

Corosync/Pacemaker/HAProxy may need to be fragmented if Galera+RabbitMQ are
geographically separated from Neutron+Heat for HA management.

This feature will modify existing tasks and their dependencies, but does not
introduce new deployable roles. Those will only be possible through custom
roles defined by a deployer, usually via a Fuel Plugin.

Alternatives
------------

Complete independence of services should be the ultimate goal, but is likely
out of scope for this feature.

Additionally, full UI granularity to pick and choose controller sub-roles is
not covered in this feature.

Data model impact
-----------------

This feature impacts the data model by redefining deployment tasks to
unhardcode their reliance on the controller role.

REST API impact
---------------

None.

Upgrade impact
--------------

There is an upgrade impact with regards to custom roles for custom
controller-like role definitions because roles are attached to an OS and
particular OpenStack release.

Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

None.

Performance Impact
------------------

None.

Plugin impact
-------------

This feature depends on enhancements in Fuel Plugin framework to support
custom roles defined by a plugin. Plugins are required to enable custom
controller deployment configurations.

Other deployer impact
---------------------

None

Developer impact
----------------

None

Infrastructure impact
---------------------

A Jenkins job will be required to validate separation of controller tasks
works. Without it, a developer could re-introduce hardcoded dependencies.

Implementation
==============

Assignee(s)
-----------

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  Matthew Moseoshn

Other contributors:
  Aleksandr Didenko
  Stanislaw Bogatkin
  Alex Schultz
  Sergii Golovatiuk

Work Items
----------

fuel-library:
* Separate DB/RabbitMQ/Horizon/Keystone from Controller role dependency
* Support separated Galera/RabbitMQ from Neutron/Heat nodes on 
  Corosync/Pacemaker/HAProxy
* Modify task flow to enable each service above to deploy separately

fuel-plugin-builder:
* Add support for custom roles
* Add support for custom pre/post/uninstall scripts

fuel-web:
* Remove hardcoded requirement for minimum 1 controller

Dependencies
============

* Roles from Fuel Plugins
* Task-based deployment framework


Testing
=======

Testing will be unorthodox because of its deployer-driven customization focus.
It will be necessary to define a custom role and task to represent each (or a
group of) separated controller service(s). This will likely be in the form of a
custom Fuel plugin for testing. This deployment schema will require new logic
in fuel-qa to generate the role(s) and task(s) to deploy, then run the usual
set of OSTF tests.

Documentation Impact
====================

New notes in Fuel Developer docs will be necessary to show an example of how to
create a plugin that creates a customized controller role.

References
==========

None
