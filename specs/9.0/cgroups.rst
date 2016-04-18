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

General OS doesn't activate any protection by default against taking all
hardware's memory or CPU. So there is a necessity to allocate resources
between competing processes, e.g. at the peak time CPU computing resources
should be distributed by the specified rules.


----------------
Proposed changes
----------------

By using cgroups, cloud operator gains fine-grained control over
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

User will be able to move all services described above under cgroups resources
control(we specified only openstack related set of services in provided list,
but, user is able to move any service what he want under the cgroup control).
User should prepare special configuration JSON string for each service
what supposed to be moved under the cgroups control(cgroups utils will be
installed even if no cgroup's settings are specified).

User will be able to specify limits via API/CLI (one more field will be brought
into yaml with cluster's settings structure by user). New puppet task to apply
cgroups configuration on target nodes will be added as well.

As there is one source of limits for all cluster nodes we should support
relative values for specific resources(like RAM). Format of proposed relative
expressions is (user should put it into respective resource's field):

`%percentage_value, minimal_value, maximum_value`

It means that:

    * percentage value(% of total memory) will be calculated and
      then clamped to keep value within the range( percentage value
      will be used if total node's RAM lower than minimal range value)
    * minimal value will be taken if node's RAM lower than minimal
      value
    * maximum value will be taken if node's RAM upper than maximum
      value

Example: `%20, 2G, 20G`

For other limits (e.g. disk I/O, share of CPU time) the native relative
values will be accepted.

User will be able to extend list of limits using cluster settings yaml
file(download/upload via CLI).

Base list of limits:
    * blkio.weight
    * cpu.shares
    * memory.soft_limit_in_bytes
    * memory.limit_in_bytes
    * memory.swappiness

Web UI
======

None


Nailgun
=======

None

Data model
----------

New hidden section `cgroups` should be added into openstack.yaml file under
'general' group to make cgroups settings configurable after the cluster is
deployed. User will be able to download/upload cluster's settings file to
override default cgroups settings(add new services and settings).

Example of a new structure what's supposed to be added into openstack.yaml
file by (the nesting level - ['editable']['additional_components']):

.. code-block:: yaml

  cgroups:
    metadata:
      group: general
      label: Cgroups configuration
      always_editable: true
      weight: 90
      restrictions:
        - condition: "true"
          action: "hide"
    ...

Example of services what should be added under cgroups control:

.. code-block:: yaml

    mysqld:
      label: mysqld
      type:  text
      value: '{"memory":{"memory.swappiness":0, "memory.soft_limit_in_bytes":"%5, 10, 20"}}}'
    rabbitmq:
      label: rabbitmq
      type:  text
      value: '{"memory":{"memory.swappiness":0}}'
    cinder:
      label: cinder
      type:  text
      value: '{"blkio":{"blkio.weight":500}}'
    keystone:
      label: keystone
      type:  text
      value: '{"cpu":{"cpu.shares":70}}'
    neutron:
      label: neutron
      type:  text
      value: '{"memory":{"memory.soft_limit_in_bytes":"%total, min, max"}}'
    ...

Cgroups limits per service will be described in json format into 'text' fields.
Format will be explicitly described in feature's documentation.


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

Cloud operator should add services that are supposed to be moved under cgroups
control into cluster's settings file via CLI(into cgroups section), data from
corresponding section will be included into node's astute yaml file
automatically during the serialization process.

A new cgroups puppet module should be implemented which will be used by
main task to configure given limits for services on the cluster nodes.
Module should be able to get input data from hiera structure
then validate and apply it.

Task will be run on post deploment stage:

.. code-block:: yaml

  id: cgroups
  type: puppet
  version: 2.0.0
  role: '*'
  requires: [post_deployment_start]
  required_for: [post_deployment_end]
  parameters:
      puppet_manifest: .../osnailyfacter/modular/cgroups/cgroups.pp
      puppet_modules: /etc/puppet/modules
      timeout: 3600
      cwd: /

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

    1. change service's limits in cluster's settings via CLI/API
    2. run 'hiera' and 'cgroups' tasks on the cluster via CLI
         `(fuel node --node-id ID1, ID2 --tasks hiera,cgroups)`


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

User will be able to configure cgroups for set of services using:
    * API - PUT api call -
      http://FUEL_IP:8000/api/v1/clusters/CLUSTER_ID/attributes
    * CLI - download, introduce `cgroups` section and upload cluster's
      settings via `fuel --env CLUSTER_ID settings -d/-u` command


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
  Michael Polenchuk <mpolenchuk>

Other contributors:
  Slava Valyavskiy <slava-val-al>
  Valeriy Saharov <vsakharov>
  Ivan Ponomarev <ivanzipfer>

QA engineers:
  Dmitry Kalashnik <dkalashnik@mirantis.com>

Mandatory design reviewers:
  Sergii Golovatiuk <sgolovatiuk>
  Vladimir Kuklin <vkuklin>


Work Items
==========

* Introduce cgroups section into openstack.yaml file
* Implement cgroups puppet module
* Place openstack/middleware services in cgroups (create task)
* Testing of overall system impact


Dependencies
============

None


------------
Testing, QA
------------

In order to verify the quality of new feature, automatic system tests will be
expanded by the cases listed below:

1. Test ability to apply, reconfigure and disable cgroups limits to services
2. Test relative limits applying with and without border conditions
3. Test absolute limits applying


Acceptance criteria
===================

The tests that are described above should pass.


----------
References
----------

`Control Groups Doc <https://www.kernel.org/doc/Documentation/cgroup-v1/cgroups.txt>`_
