..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================
Fuel Library Modularization
===========================

https://blueprints.launchpad.net/fuel/+spec/fuel-library-modularization

This blueprint is about how we are going to split deployment workflow
into pieces.


Problem description
===================

Currently we have a gigantic monolithic deployment workflow, that takes
almost an hour to complete. This does not allow us to develop quickly
as well as inject pieces into deployment workflow in order to improve
our pluggable architecture. This also does not allow us to do more
granular integration and functional testing.


Proposed change
===============

In order to increase engineering velocity and ability for 3rd party users
and developers to inject pieces into deployment workflow we are going
to split fuel library into set of tasks that are going to be executed
by the engine developed as a part of
https://blueprints.launchpad.net/fuel/+spec/granular-deployment-based-on-tasks
blueprint

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

User will be able to call particular deployment pieces by hand.

Performance Impact
------------------

None

Other deployer impact
---------------------

Fuel Library will contain descriptions of tasks along with their
metadata describing which task depends on which one thus allowing
orchestration engine to create a deployment graph and traverse 
it putting the system into desired state.

Developer impact
----------------

Developer will be able to inject deployment piece anywhere,
snapshot the environment, restart deployment from the particular place

Implementation
==============

Implementation is going to be fairly simple. Each deployment piece
is represented as a task along with its metadata, e.g. which nodes
should run these tasks and which order. Then we rip the resources and
classes created using legacy monolithic catalogue and put them into
corresponding deployment manifest. After that we remove corresponding
calls from legacy role and continue until there is no resources left
for the legacy task.

Assignee(s)
-----------

Primary assignee:
Aleksandr Didenko aka ~adidenko
Dmitry Ilyin aka ~idv1985

Other contributors:
Almost all fuel-library contributors

Work Items
----------

Trello board for the feature is here:
https://trello.com/b/d0bKdE43/fuel-library-modularization

Implementation plan
-------------------

* Step #1:
  Separate hiera, netconfig and other prerquired tasks. Everything else
  should be deployed under 'legacy.pp' puppet manifest (it's based on our
  legacy site.pp manifest). So it's mostly like previous deployment scheme
  where everything was daployed with single puppet apply run.
* Step #2:
  Move top-scope roles (primary-controller, controller, compute, cinder,
  ceph-osd) into separate tasks.
* Step #3:
  Split top-scope roles into smaller tasks. For example: controller should
  be split into cluster, haproxy, galera, rabbitmq, openstack::controller, etc.
* Step #4:
  Continue to split large tasks into smaller ones where possible. Like:
  openstack::controller split into nova::api, cinder::api, cinder::scheduler,
  etc.

Dependencies
============

Granular deployment blueprint needs to be completed at least with the first
implementation that allows to execute the simplest granules.
https://blueprints.launchpad.net/fuel/+spec/granular-deployment-based-on-tasks

Testing
=======

Feature is considered completed as soon as
there is no deployment tests failing. This feature
should be mostly considered as refactoring approach,
e.g. implementation rewriting, thus not affecting
functionality of the deployed cloud at all.


Documentation Impact
====================

Process of development will be significantly improved and this should
be reflected in the development documentation.


References
==========

[1] https://blueprints.launchpad.net/fuel/+spec/granular-deployment-based-on-tasks
[2] Trello board https://trello.com/b/d0bKdE43/fuel-library-modularization
[3] Old doc for modularization https://docs.google.com/a/mirantis.com/document/d/1GJHr4AHw2qA2wYgngoeN2C-6Dhb7wd1Nm1Q9lkhGCag/edit
