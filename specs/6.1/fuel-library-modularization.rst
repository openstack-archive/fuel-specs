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
because testing takes far to much time. This also does not allow us to
do more granular integration and functional testing.

Proposed change
===============

In order to increase engineering velocity and ability for 3rd party users
and developers to inject pieces into deployment workflow we We are going
to change the architecture of the Fuel Library and make it more modular.
The idea behind the modular architecture is the separation
of our legacy monolithic manifest into a group of small manifests. Each of
them will be designed to do only a limited part of the deployment. These
manifests can be applied by Puppet in the same way as the monolithic manifest
was applied before by the engine developed as a part of
https://blueprints.launchpad.net/fuel/+spec/granular-deployment-based-on-tasks
blueprint. The deployment process will be the sequential application
of small manifests in the defined order.

Moving from a large manifests to small pieces has several important advantages:

*   **Independent development.** Each developer can work only with those Fuel
    components he is currently interested in. The separate manifest can be
    dedicated wholly to a single task without interfering with components and
    developers. Every ask may require the system to be in a defined state
    before the deployment can be started and the task may require some
    input data be available. Other than these each task is on it’s own.
*   **Granular testing.** Previously testing have been far too time consuming
    because any change required the whole deployment to be started from the
    scratch and there was no way to test only a part of the deployment which is
    related to the changes made. With granular deployment any finished task can
    be tested independently. Testing can be even automated with autotests and
    with environment snapshotting and reverting as well and being run manually
    by the developer on his test sysem.
*   **Encapsulation.** Puppet is known to be to very good at code reuse.
    Usually you cannot just take any third party module or manifests and hope
    that it will work as designed within your Puppet infrastructure without
    neither modifications nor unexpectedly breaking something. These problems
    mostly come from the basic design of Puppet, the way it deems all resources
    unique within the catalog and the way it works with dependencies and
    ordering. There are techniques and methods to overcome these limitation,
    but they are not absolutely effective, and usually problems still persist.
    Using modular manifests bypasses these problems, because every single task
    will use its own catalog and will not directly mess with other tasks.
*   **Self-Testing.** Granular architecture allows us to make test for every
    deployment task. These tests can be run either after the task to check
    if it have successfuly finished or before the task to check if the system
    is in the required state. Pre and post tests can be used either by the
    developer as acceptance tests or by the CI system to determine if the
    changes can be merged or during the real deployment to control the
    deployment process and to raise an alarm if something went wrong.
*   **Using multiple tools.** Sometimes there can be a task that is very hard
    to be done using Puppet and some other methods or tools would be able to
    do it much easier or better. Granular deployment allows us to use any tools
    we see fit for the task, from shell scripts to Python or Ruby or even
    binary executables. Taks, tests and pre/post hooks can be implemented
    using anything the developer knows best. *For the first release only
    pre/post hooks can use non-Puppet tasks.*

Granular deployment is implemented using the Nailgun plugin system that was
merged some time ago and was rather successful. Nailgun uses the deployment
graph data to determine what tasks on which nodes should be run. This data
graph is traversed and sent to the Astute as an ordered list of tasks to be
executed with information on which nodes they should be run.

Astute receives this data structure and begins to run tasks one by one. First,
it doest the pre-deploy actions, then, the main deployment tasks, and, finally,
the post-deploy actions. Each tasks reports back if it was successful and
Astute stops deployment on any failed task.

 .. image:: ../../images/6.1/fuel-library-modularization/granular_scheme.png
    :scale: 75 %

Task graph is a yaml file that can be found at **deployment/puppet/
osnailyfacter/modular/tasks.yaml** in the fuel-library repository. It contains
the array of tasks and their properties.

.. code-block:: yaml

    - id: netconfig
      type: puppet
      groups: [primary-controller, controller, cinder, compute, ceph-osd,
      zabbix-server, primary-mongo, mongo]
      required_for: [deploy]
      requires: [hiera]
      parameters:
        puppet_manifest: /etc/puppet/modules/osnailyfacter/modular/netconfig.pp
        puppet_modules: /etc/puppet/modules
        timeout: 3600




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

User will be able to call particular deployment pieces by hand if this feature
is implemented on the Nailgun side.

Performance Impact
------------------

Testing only small pieces at time will greatly improve the performance of the
CI infrastructure. But neither the deployment speed nor the performance of the
OpenStack are going to be affected.

Other deployer impact
---------------------

Fuel Library will contain descriptions of tasks along with their metadata
describing which task depends on which one thus allowing orchestration
engine to create a deployment graph and traverse it putting the system
into desired state.

Developer impact
----------------

Developer will be able to inject a deployment piece anywhere,
snapshot the environment, restart deployment from the particular place
if these features are supported by the orchestration or just apply
any task manually on the local system without any orchestration.

Implementation
==============

Implementation is going to be fairly simple. Each deployment piece
is represented as a task along with its metadata, e.g. which nodes
should run these tasks and in which order. Then we can rip the resources
and classes created using legacy monolithic catalogue and put them into
corresponding deployment manifest. After that we remove corresponding
calls from legacy role and continue until there is no resources left
for the legacy task.

Nailgun will use the deployment graph generated from the tasks metadata.
This data graph will be traversed and sent to the Astute as an ordered
list of tasks to be executed with information on which nodes they should
be run. Astute receives this data structure and begins to run the tasks
one by one. First, it doest the pre-deploy actions, then, the main
deployment tasks, and, finally, the post-deploy actions. Each task
reports back if it was successful and Astute stops deployment on any task
that have failed.

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
