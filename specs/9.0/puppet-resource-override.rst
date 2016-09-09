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

To implement this solution, we need to change the configuration data format
to support any Puppet resource defined by ``fuel-library``. The new data format
should be recognized by the ``override_resources`` Puppet type and should
allow a user to create a new resource of a given type. The new data structure
should have the following format:

.. code-block:: yaml

    configuration:
      <puppet_resource_type>:
        data:
          <puppet_resource_title>:
            <puppet_resource_param1>: value1
            <puppet_resource_param2>: value2
            ...
        create_res: <True|False>

This structure should be transformed into parameters for the
``override_resources`` type.

The ``override_resources`` Puppet type has following logic:

#. It searches for all the resources in the Puppet catalog whose type
   equals ``<puppet_resource_type>``.

#. Among all the resources found in the step 1, it selects resources with
   title equals ``<puppet_resource_title>``.

#. If the result from the step 2 is not empty (if the resource is found),
   it updates the resource parameters with the values from
   ``<puppet_resource_paramX>``.

#. If the result from the step 2 is empty, ``create_res`` defines the
   following behavior:

    a. If ``create_res = True``, the new ``<puppet_resource_type>`` resource
       with the title ``<puppet_resource_title>`` and parameters
       ``<puppet_resource_param1>...<puppet_resource_paramN>`` is created.
    b. If ``create_res = False``, the resource is not be created.

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
        data:
          fontconfig-config:
              ensure: latest
          mc:
              ensure: absent
        create_res: true

will be transformed into the following Puppet resource definition:

.. code-block:: puppet

    override_resources {'package':
      data => { 'fontconfig-config' =>
                    {'ensure' => 'latest'},
                'mc' =>
                    {'ensure' => 'latest'}
              },
      create_res => true,
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

RPC protocol
------------

None

Fuel client
===========

None

Plugins
=======

None

Fuel library
============

The static ``override_recources`` definition in the Fuel library
will be replaced with the dynamic one based on the data in Hiera.
The ``override_resources`` type should be created using the
``create_resources`` function.

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

All data uploaded to an environment by using the old configuration format
should be converted to the new format.

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

Work items
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