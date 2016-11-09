..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================================
Allow a user to override the Puppet resources through Hiera
===========================================================

https://blueprints.launchpad.net/fuel/+spec/puppet-resource-override

Currently, a user can provide the YAML-formatted data to override the
OpenStack configuration resources. This is implemented by using a specific
Puppet resource which allows overriding parameters only for the OpenStack
configuration resources in the catalog. This approach should be extended to
support all the Puppet resources what gives an opportunity to control a
deployment using Hiera. Implementing this enhancement allows us to enable
the Infrastructure as Code concept for a user.

-------------------
Problem description
-------------------

The Fuel OpenStack configuration feature introduces a way to update the
OpenStack configuration files. A user can upload the YAML-formatted file
using the Fuel CLI. The format of this file is as follows:

.. code-block:: yaml

    configuration:
      <service_key>:
        <config_section>/<config_option>:
          <puppet_reousrce_param>: <config_value>

This format being transparently transformed into the Puppet resource is
responsible for the OpenStack configuration.

The common Lifecycle Management and Infrastructure as Code approaches imply
that a user can configure any entity within environment (configuration file,
package version, and so on). The current solution is limited by the OpenStack
configuration file only. It leads to the significant obstacles in an
environment management after it has been deployed.

----------------
Proposed changes
----------------

To solve the problem above, we can extend Fuel to support configuration of any
entity within a deployed environment. This provides an opportunity to manage
an environment without introducing the sophisticated deployment procedures
such as creating plugins or custom graphs.

To implement this solution, we need to extend ``override_resources`` Puppet
type implementation to support any Puppet resource defined by ``fuel-library``.
``override_resources`` Puppet type should allow a user to create a new
resource of a given type or just modify resources' parameters. The new data
structure should have the following format:

.. code-block:: yaml

    configuration:
      <puppet_resource_type>:
        <puppet_resource_title>:
          <puppet_resource_param1>: value1
          <puppet_resource_param2>: value2
          ...
    configuration_options:
        create: <True|False>
        types_filter:
          - <type1>
          - <type2>
          ...
        titles_filter:
          - <title1>
          - <title2>
          ...
        types_create_exception:
          - <type1>
          - <type2>
          ...
        titles_create_exception:
          - <title1>
          - <title2>
          ...

``configuration_options`` hash is optional and is intended to be used by
advancedusers only. This structure should be transformed into parameters
for the ``override_resources`` type.

The ``override_resources`` Puppet type has following logic:

#. It searches for all the resources in the Puppet catalog whose type
   equals ``<puppet_resource_type>``.

#. Among all the resources found in the step 1, it selects resources with
   title equals ``<puppet_resource_title>``.

#. If the result from the step 2 is not empty (if the resource is found),
   it updates the resource parameters with the values from
   ``<puppet_resource_paramX>``.

#. If the result from the step 2 is empty, it creates resource in catalog.

Logic described above can be overridden by ``configuration_options`` hash
using following set of parameters

.. code-block:: yaml

   types_filter: []
   titles_filter: []

These two options allow to provide a list of resource types and/or resource
titles which should be processed by this override_resources instance.
If the lists are missing or empty no filtering will be used and all resources
types and titles will be processed.

Default values ``[]``

.. code-block:: yaml

    create: true/false

Enable the creation of all resources. New instances will be added to the
catalog if no instances of this resource have been found there.

Default value ``True``

.. code-block:: yaml

    types_create_exception: []
    titles_create_exception: []

These two options allow to set the exception lists for the new resource
creation. If "create" option is set to true, these lists of types and
titles are used as the list of resources that should not be created.
If "create" option is set to false, these lists of types and titles are
used as the list of resources that should be created.

Default values ``[]``

.. code-block:: yaml

    defaults:
      <type>:
        <parameter>: <value>

This structure allows to set the default parameters for every Puppet
type (e.g. ensure: present). The value will be added to every updated or
created resource of this type unless the other value is provided for a
resource in the configuration data.

The resource generator raises an error if the resource defined in data
structure is not found within ``modulepath``.

Such data structures can be created using standard Nailgun API which
was introduced for the *Advanced Configurations* feature or through the
Nailgun extension which modify deployment data prior to sending them to
a particular node.

For example, the following construction:

.. code-block:: yaml

    configuration:
      package:
        fontconfig-config:
            ensure: latest
        mc:
            ensure: absent

will be used in the following block of ``fuel-library``:

.. code-block:: puppet

    override_resources {'package':
      configuration => {
                         'fontconfig-config' =>
                           {'ensure' => 'latest'},
                         'mc' =>
                           {'ensure' => 'latest'}
                       },
    }

The new approach allows overriding any Puppet resource in a catalog or add
any resource in ``modulepath`` to the catalog.

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

Execution of ``override_resources`` will be added for each task in
deployment graph. Parameters for will be taken from ``hiera``

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

All data uploaded to an environment by using the old configuration format
may be extended with nesessary configuration options.

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

Documentation should be updated with the new configuration format examples
and description of new possible options from an end-user perspective.

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

The development may be split into two stages:

* Implement a new configuration format processing in the OpenStack-related
  puppet tasks.
* Implement a new configuration task for all the Puppet tasks in the
  deployment graph.

Dependencies
============

None

------------
Testing, QA
------------

Tests for the Fuel OpenStack configuration feature should be updated with
the new configuration format.

Acceptance criteria
===================

This change should provide an ability for a user to configure any entity
within a deployed environment.

----------
References
----------

None
