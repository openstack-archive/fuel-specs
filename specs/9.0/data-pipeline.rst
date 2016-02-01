..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Provisioning and deployment data pipeline
=========================================

https://blueprints.launchpad.net/fuel/+spec/data-pipeline

--------------------
Problem description
--------------------

Together with implementation of Nailgun Extensions [#nailgun_extensions]_
we want to remove all direct calls from Nailgun core to any kind of extension
i.e.: to volume_manager [#volume_manager_import]_ or any other extension using
`node_extension_call` function [#node_extension_call]_.

But extensions must have the ability to change the deployment and provisioning
data. It is required for example by new bareon-fuel-extension
[#bareon_fuel_extension]_ which will be used to integrate Fuel with Bareon-API
[#bareon_api]_.

----------------
Proposed changes
----------------

Once the deployment or provisioning data serialization happens the data will be
passed to all available extensions. Then every extension will be able to make
some data manipulation.

The proposal is to create new Extension attribute which is called
`data_pipelines`.

`data_pipelines` is a list of Pipeline classes. Every Pipeline class should
implement at least one of the following methods:

  * :code:`process_deployment(deployment_data, **kwargs)` - is executed once
    the serialization of deployment data occurs. It receives reference to a
    dict which can be changed.

  * :code:`process_provisioning(provisioning_data, **kwargs)` - is executed
    once the serialization of provisioning data occurs. It receives reference
    to a dict which can be changed.

Both methods don't return anything and both are executed **after** Nailgun data
serialization. Then the data can be changed by User using Fuel CLI as it was
possible so far.

Example implementation:

.. code:: python

  class ExamplePipeline(BasePipeline):

      @classmethod
      def process_deployment(cls, deployment_data, **kwargs):
          deployment_data['new_field'] = external_source.get_new_data()

      @classmethod
      def process_provisioning(cls, provisioning_data, **kwargs):
          provisioning_data['new_field'] = external_source.get_new_data()

  class ExampleExtension(BaseExtension):
      ...
      data_pipelines = (ExamplePipeline,)
      ...





Web UI
======

None

Nailgun
=======

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

None

------------
Alternatives
------------

Instead of introducing new Extension attribute with classes list:

* we could just add these two methods to Extensions class:

  * but it will clash with Expert design [#expert_pattern]_ pattern what can
    lead to blurred responsibilities

* we could implement Pipelines as mixins:

  * but it comes down to the same issue as in the previous example

  * we want to implement Pipeline classes execution custom ordering in the
    future


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

Developer is able to change the deployment/provisioning data directly from
extensions.


---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Pipelines should be described in Extensions docs. Description should include:

* Definition of pipeline

* Minimal working pipeline (required methods etc.)


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee: Sylwester Brzeczkowski <sbrzeczkowski@mirantis.com>

Mandatory design review:

  * Evgeny Li <eli@mirantis.com>
  * Igor Kalnitsky <igor@kalnitsky.org>

Work Items
==========

* Implement BasePipeline class and integrate it with existing
  BaseExtension class and add serialization event triggers to
  the places in Nailgun core where the event occurs.

* Remove all direct calls to extensions from Nailgun core.

* Write functional tests from `Testing, QA`_

Dependencies
============

* Nailgun extensions discovery must be done first [#nailgun_extensions]_


------------
Testing, QA
------------

Cases:

* Install extension with pipeline which changes node volumes on provisioning
  serialization. Run provisioning and check if correct data was sent to Astute.

* Install extension with pipeline which adds some new field in
  provisioning/deployment data. Download this data using Fuel CLI, remove that
  field, upload it back and run deployment. Check if the field was present
  in the message sent to Astute (shouldn't be).

Acceptance criteria
===================

* It is possible to change/add new data to provisioning/deployment serialized
  data.

* User can change deployment/provisioning data (as it was possible so far)
  and make the decision to use the changes introduced by pipelines or not.


----------
References
----------

.. [#nailgun_extensions] https://blueprints.launchpad.net/fuel/+spec/stevedore-extensions-discovery
.. [#volume_manager_import] https://github.com/openstack/fuel-web/blob/stable/8.0/nailgun/nailgun/db/sqlalchemy/models/node.py#L38
.. [#node_extension_call] https://github.com/openstack/fuel-web/blob/stable/8.0/nailgun/nailgun/orchestrator/provisioning_serializers.py#L131
.. [#bareon_fuel_extension] https://github.com/gitfred/bareon-fuel-extension
.. [#bareon_api] https://blueprints.launchpad.net/fuel/+spec/fuel-bareon-api-integration
.. [#expert_pattern] https://en.wikipedia.org/wiki/GRASP_%28object-oriented_design%29#Information_Expert