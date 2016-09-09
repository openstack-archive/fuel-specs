..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Allow user to override puppet resources via hiera
==========================================

https://blueprints.launchpad.net/fuel/+spec/puppet-resource-override

Currently user can provide yaml formatted data to override OpenStack
configuration resources. This is implemented by using specific puppet resource
which allows to override parameters only for openstack config resources
in catalog. This approach should be extended to support all puppet
resources which gives an opportunity to control deployment using hiera.
Implementing this enhancement will allow us to enable INfrastructure as Code
concept for user.


--------------------
Problem description
--------------------

Fuel openstak-config feature introduces a way to update OpenStack configuration files.
User can upload yaml-formatted file using Fuel client. The format of this file is following

configuration:
  <service_key>:
      <config_section>/<config_oprion>:
        <puppet_reousrce_param>: <config_value>

This format transparently transformed into puppet resource respociblr for OpenStack
configuration.

Common Life Cycle Management and Infrastructure as Code approaches imply that user can configure any entity
within environment (configuration file, package version e.t.c). Current solution is
limited by only OpenStack configuration file which leads to significant obstacles in
environment management after it has been deployed.


----------------
Proposed changes
----------------

To solve the problem above we can extend Fuel to support configuration of any entity
within deployed environment. This provides an opportunity to manege environment without
introducing sophisticated deployment procedures like creating a plugins or custom graphs

To achieve that we need to change configuration data format to support any puppet resource
defined with fuel-library. New data format should be recognised by override_resources
Puppet type and should allow user to create new resource of a given type. New data structure should have following format:

configuration:
  <puppet_resiource_name>:
    data:
      <puppet_resource_title>:
        <puppet_resource_param1>: <value1>
        <puppet_resource_param2>: <value2>
        ...
    create_res: <True|False>

This structure should be transformed into parameters for oeverride_rousrces type.
For example following construction

configuration:
  package:
    data:
      fontconfig-config:
          ensure: latest
    create_res: true

should be transformed in following puppet resource definition

override_resources {'package':
  data => { 'fontconfig-config' => {'ensure' => 'latest'}},
  create_res => true

New upproach will allow to override any puppet resource in catalog or create new
defined by user


Web UI
======

None


Nailgun
=======

None


Data model
----------

None


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

Static override_recources definition in Fuel Library
will be replaced with dynamic one based on data in Hiera.
Type override_resources should be created using create_resources
function.


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

All data uploaded to environment by using old configuration format should be
converted to new format


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

None


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

Documentation should be updated with new configuration format examples
and description of new possible options from end-user perspective.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  dukov

Mandatory design review:
  vkuklin


Work Items
==========

Development may be split into two stages.
* Implement new configuration format processing in OpenStack related
  puppet tasks.

* Implement new configuration task for all puppte tasks in deployment graph.


Dependencies
============

None


------------
Testing, QA
------------

Tests for fuel openstakc-config feature should be updated with new configuration
format


Acceptance criteria
===================

This change should provide ability to user to configure any entity within deployed
environment


----------
References
----------

None
