..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Daemon Resource Allocation Control
================================================

https://blueprints.launchpad.net/fuel/+spec/cgroups

Support daemon resource control by means of cgroups kernel feature.


--------------------
Problem description
--------------------

General OS doesn't have any protection against taking all hardware's memory
or CPU. So there is need to allocate resources between competing processes,
e.g. at the peak time CPU computing resources should be distributed by the
specified rules.


Proposed changes
----------------

By using cgroups, cloud operator gain fine-grained control over
allocating, prioritizing, denying, managing, and monitoring system resources.
Hardware resources can be appropriately divided up among tasks and services,
increasing overall efficiency. 
Service set what is supposed to be moved under cgroups control:
  * all OpenStack services
  * middleware
    - rabbitmq
    - mysql/galera
    - mongodb
    - ceph services

It was decided to move all described services above under cgroups resources
control, but cgroups limits will not be activated by default. So cgroups
profiles will be configured for proposed resources without specified limits if
they were not explicitly configured by the user. User will be able to specify
limits via UI/API/CLI (one more field will be introduced into cluster's
settings structure). New puppet task to apply cgroups configuration on target
nodes will be introduced. It will be run on post deploment stage:
    
.. code-block:: yaml

  id: cgroups
  type: puppet
  version: 2.0.0
  groups: ['/.*/']
  requires: [post_deployment_start]
  required_for: [post_deployment_end]
  condition: "settings:cgroups.enabled.value == true"
  parameters:
      puppet_manifest: .../osnailyfacter/modular/cgroups/cgroups.pp
      puppet_modules: /etc/puppet/modules
      timeout: 3600
      cwd: /


Web UI
======

New section to configure cgroups limits for services will be introduced.


Nailgun
=======

None


Data model
----------

Cloud operator could add/update a data to override default cgroups settings.
Example of a new structure(it will be included into openstack.yaml and may
be modified):

.. code-block:: yaml

  cgroups:
    metadata:
        label: "Configure cgroups"
        description: "If selected, Cgroups will be configured"
        weight: 10
    enabled:
        value: false
        type: "checkbox"
    blkio:
      blkio.weight:
        - cinder: 500
    cpu:
      cpu.shares:
        - keystone: 70
    cpuacct:
    cpuset:
    devices:
    freezer:
    memory:
      limit_in_bytes:
        - nova: 5242880
        - neutron: 5242880
      memsw.limit_in_bytes:
        - mysqld: 0
        - rabbitmq: 0
    perf_event:
    net_cls:
    net_prio:
    ns:
    ...


REST API
--------

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

Should be implemented brand new cgroups puppet module which will be used by
main task to configure given limits for services on the cluster nodes.
Module should be able to get input data from hiera structure
then validate and apply it.


------------
Alternatives
------------

Limit CPU utilization by nice(1), for limiting memory allocation rely upon
service configuration/runtime constrains itself.


--------------
Upgrade impact
--------------

From life cycle management perspective, cloud operator will be able to change
cgroups settings for the deployed cluster in following way:
    1. change service's limits in cluster's settings via UI/CLI/API
    2. run 'hiera' and 'cgroups' taks on the cluster via CLI
       (fuel node --node-id ID1, ID2 --tasks hiera,cgroups)


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

User will be able to configure cgroups for set of services using API/CLI/UI.


------------------
Performance impact
------------------

With emploing cgroups kernel feature hardware resources can be appropriately
divided up among tasks and services, increasing overall efficiency.


-----------------
Deployment impact
-----------------

None


----------------
Developer impact
----------------

None


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

This feature should be described in the documentation.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:

Other contributors:

Mandatory design reviewer:


Work Items
==========

* Implement cgroups puppet module

* Introduce new `cgroups` section into openstack.yaml file

* Place openstack/middleware services in cgroups (create task)

* Testing of overall system impact


Dependencies
============

None


------------
Testing, QA
------------

New test should be written which covers this scenario:


Acceptance criteria
===================

The test which described above should pass.


----------
References
----------

None
