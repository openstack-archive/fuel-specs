..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================
Plugins deployment order
========================

https://blueprints.launchpad.net/fuel/+spec/plugins-deployment-order

If environment has two and more plugins, plugin developer should be
able to specify priorities in which plugins will be deployed.

Problem description
===================

Plugins for network configuration should be run before plugins
which install software services. Currently it is not possible
to specify the order of plugins tasks deployment.

Proposed change
===============

For each stage name plugin developer adds a postfix, which defines stage
specific execution order of the task.

Lets take a look at the following example:

tasks.yaml file of Fuel plugin **A**

.. code-block:: yaml

    - role: ['primary-controller', 'controller']
      stage: post_deployment/100
      type: shell
      parameters:
        cmd: ./deploy.sh
        timeout: 42

tasks.yaml file of Fuel plugin **B**

.. code-block:: yaml

    - role: ['primary-controller', 'controller']
      stage: post_deployment/50
      type: shell
      parameters:
        cmd: ./deploy.sh
        timeout: 42

During post_deployment stage execution post task of plugin **B**
will be executed before plugin post task of plugin **A**, because
"post_deployment/50" is lower than "post_deployment/100".

But in some cases plugins don't know about each other, and the best
way to solve the problem is to define as convention the ranges which
plugin developers will be able to use.

Pre and post deployment ranges:

* 0 - 999 - hardware configuration, for example drivers configuration

* 1000 - 1999 - reserved for future uses

* 2000 - 2999 - disks partitioning and volumes configuration

* 3000 - 3999 - reserved for future uses

* 4000 - 4999 - network configuration

* 6000 - 6999 - reserved for future uses

* 5000 - 5999 - software deployment

* 7000 - 7999 - reserved for future uses

* 8000 - 8999 - monitoring services deployment

In this case if one network plugin defines "stage: post_deployment/100"
and another plugin defines "stage: post_deployment/2000", they will be
installed in the right order without knowing about each other.

Also if there are two plugins which implement monitoring, plugin developers
can figure out which plugin should be installed first and tune postfixes
accordingly.

If two tasks have the same priorities, they should be sorted in alphabetic
order by name and the first in the list should be deployed first.

Postfix can be negative or positive, floating or integer number.

Alternatives
------------

Additional stages instead of numerical postfixes
++++++++++++++++++++++++++++++++++++++++++++++++

Additional plugin specific stages can be defined:

* hw_configuration

* disk_partitioning

* network_configuration

* software_installation

And then existing stages

* pre_deployment

* post_deployment

And the last one new stage

* monitoring

In this case plugin developer will be able to work with a single entity
without some additional postfixes.

But, in this case plugin developer won't be able to more granularly define
order, for example if two plugins implement monitoring, it'll be impossible
to define the order.

Another cons is it'll confuse a plugin developer because plugin specific stages
are differ from granular deployment stages. Also it will complicate migration
to the next release when we will implement granular deployment like tasks.

Plugins wide priorities
+++++++++++++++++++++++

Plugins priorities should be defined not for entire plugin,
but for each task, because a single plugin can have drivers
and services, which should be deployed in the right order.

Postfix separator
+++++++++++++++++

It was decided to use "/" instead of ":", or "::" as a separator because in
case of typos like:

.. code-block:: yaml

    stage: post_deployment:: 50

.. code-block:: yaml

    stage: post_deployment: :50

Yaml parasers fails and it's impossible to cursomize error message.

Also people got used to convention that "/" is used to define subdirectories
or subgroups for RPMs and DEBs.


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

None

Performance Impact
------------------

None

Plugin impact
-------------

Numerical postfixes for stages in each task.

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  eli@mirantis.com

Work Items
----------

* Fix fuel plugin builder validator to allow to specify deployment order.

* Nailgun should set the correct order of the plugins with dependencies
  on tasks.

* Docs

Dependencies
============

None

Testing
=======

Acceptance Criteria
-------------------

* If environment has two installed plugins Z with stage
  "pre_deployment/100" and A with stage "pre_deployment/200"
  plugin Z should be started before plugin A scripts.

* If both plugins A and Z have the same stage "pre_deployment/100",
  plugins should be installed in alphabetic order, i.e. A and then Z.

* If stage postfix is not specified, it should be set to 0 by default
  on the backend.

Here is example of order which tasks should be executed in:

Plugin with name "plugin1", and with the next task stages:

.. code-block:: yaml

   stage: pre_deployment
   stage: pre_deployment/100
   stage: pre_deployment/-100
   stage: pre_deployment/-99.9

Plugin with name "plugin2", and with the next task stages:

.. code-block:: yaml

   stage: pre_deployment
   stage: pre_deployment/100.0
   stage: pre_deployment/-101
   stage: pre_deployment/0

Execution order of the tasks for both plugins which is sent to orchestrator:

.. code-block:: yaml

   stage: pre_deployment # plugin1
   stage: pre_deployment # plugin2
   stage: pre_deployment/0 # plugin2

   stage: pre_deployment/-101 # plugin2
   stage: pre_deployment/-100 # plugin1
   stage: pre_deployment/-99.9 # plugin1

   stage: pre_deployment/100 # plugin1
   stage: pre_deployment/100.0 # plugin2

Documentation Impact
====================

* Documentation with description of ranges should be created.

References
==========

None
