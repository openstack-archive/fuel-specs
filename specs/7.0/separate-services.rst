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

Corosync/Pacemaker/HAProxy will be fragmented per-role if any of the following
tasks are on separate roles:
* OpenStack services
* RabbitMQ
* Galera

A recommended deployment consists of 3 nodes to a custom role for full HA.

This feature will modify existing tasks and their dependencies, but does not
introduce new deployable roles. Those will only be possible through custom
roles defined by a deployer, usually via a Fuel Plugin.

Another goal of this spec is to deliver a set of examples and tools to enable a
plugin developer to create his or her own custom roles and split up the tasks
as desired, but ensure that all requirements for a complete deployment are met.

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

If other tasks are combined with the nova-compute task, it may expose
security risks.

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

Primary assignee:
  Matthew Moseoshn

Mandatory Design Reviewers:
  Andrew Maksimov
  Nathan Trueblood

Other contributors:
  Stanislaw Bogatkin
  Alex Schultz
  Sergii Golovatiuk
  Bartlomiej Piotrowski

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
* Add additional VIPs from plugin

fuel-ostf:
* Support for testing custom roles

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

- Manual functional testing of custom roles will be conducted
- Separating DB/RabbitMQ/Horizon/Keystone from Controller role will
  be covered with regression testing - mainly with fuel-qa automation tests
  and manual checks of base cases and some corner cases like failover
- System tests will be augmented to cover testing of custom roles deployment

Acceptance Criteria
-------------------

Must be able to deploy a custom role with database task. All components
dependent on the database will connect to it via a database VIP on management
network.
Must be able to deploy a custom role with keystone task. All components
dependent on Keystone will connect to it via a keystone service_endpoint VIP on
management network.
Must be able to deploy a custom role with rabbitmq task. All components
dependent on RabbitMQ will connect to each as a list of nodes with rabbitmq
role.
Must be able to deploy controller role without keystone, database, or
rabbitmq task. All roles dependent on these tasks must be able to consume a
field in hiera for these endpoints.
Should have backward compatibility. In the absence of custom defined
rabbitmq_nodes, database_endpoint, keystone_service_endpoint, use
primary_controller IP or management_vip as before in 6.1.
Should create databases from OpenStack service tasks(nova, neutron, glance,
etc), not from database task.
Should create keystone users/endpoints from OpenStack service tasks(nova,
neutron, glance, etc), not from database task.
Custom tests should be developed to create controller_minus_$SERVICE and
$SERVICE custom roles to ensure granular deployment passes

Documentation Impact
====================

New notes in Fuel Developer docs will be necessary to show an example of how to
create a plugin that creates a customized controller role. For example, any
role containing heat, neutron, Galera or RabbitMQ task also requires corosync.
Similarly, any role containing an OpenStack service or Galera requires a VIP.

References
==========

None
