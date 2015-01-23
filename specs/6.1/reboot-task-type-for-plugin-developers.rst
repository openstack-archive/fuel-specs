..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Reboot task type for plugin developers
==========================================

https://blueprints.launchpad.net/fuel/+spec/reboot-action-for-plugin

For plugins developers it would be nice if Fuel can perform reboot
operation and wait until nodes return to online state before run
another tasks.

Problem description
===================

It now moment any operation or series of operation which requires
reboot do not available for fuel plugin developers using standart
actions, e.g.: it is very hard to change kernel on custom nodes.

Proposed change
===============

Add new task type for plugins: 'reboot'. It will send selected nodes
to reboot and wait until they return back online or time is
run out.

It should acts as other type tasks actions:

* support timeout for whole operation. Mark task as failed if timeout
  is reached;

* support 'fail_if_error' behavior. If this parameter set to true and
  task failed, we should prevent execution additional tasks and mark
  whole deployment as failed;

* the fact of the operation and its result should be logged in Astute
  log, e.g.:

.. code-block:: none

    Run hook
    ---
    uids:
      - '1'
      - '3'
      - '2'
      - '4'
    parameters:
      timeout: <timeout>
    priority: <priority order>
    fail_on_error: true
    type: reboot
    diagnostic_name: <plugin name>

.. code-block:: none

  Reboot command failed for nodes ["<node id>"]. Check debug output
  for details

.. code-block:: none

  Time detection (<timeout> sec) for node reboot has expired

Alternatives
------------

There are no decent alternatives:

* developers can try to use shell task type with command 'reboot' as last
  task type for the plugin. It can potencialy work if it use it as last
  task of last plugin in 'post_deployment' section. Of course, it is very
  limited and unreliable way;

* also they can try to run 'reboot' command by hands. Also this action
  require deliberate mistake in plugin hook to stop deployment then we
  need 'reboot' command. After it we should fix command and run another steps.

Data model impact
-----------------

None

REST API impact
---------------

None

Orchestration (astute) RPC format
---------------------------------

User specifies the structure like this

.. code-block:: yaml

   - role: ['controller', 'cinder']
     stage: pre_deployment
     type: reboot
     parameters:
       timeout: 60
   - role: *
     stage: post_deployment
     type: reboot
     parameters:
       timeout: 120

Then nailgun configures this data in the next format

.. code-block:: yaml

      # This stages should be run after astute yaml for role
      # and repositories are on the slaves
      pre_deployment:
        - type: reboot
          uids: [1, 2, 3]
          priority: 60
          parameters:
            timeout: 42
      post_deployment:
        - type: reboot
          uids: [1, 2, 3, 4, 5, 6]
          priority: 30
          parameters:
            timeout: 53
      deployment_info:
        # Here is deployment information in the same format
        # as it is now

In the current release orchestrator should **fail deployment** if
one of the reboot tasks is not executed successfully.

Upgrade impact
--------------

Current release
^^^^^^^^^^^^^^^

None, because we only extend amount of operation available for plugin
developer.

Future releases
^^^^^^^^^^^^^^^

None, same reason as above

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Plugins which used 'reboot' plugin type, could not be run for enviroments
below 6.1.

Performance Impact
------------------

**Deployment**

* if user has enabled plugin with 'reboot' task type, time there will be
  performance impact, the time of deployment will be increased, the increasing
  time depends on speed of reboot operation on the slowest node.


Other deployer impact
---------------------

None

Developer impact
----------------

* plugins which used 'reboot' task type, could not be run for enviroments
  below 6.1

Implementation
==============

Assignee(s)
-----------

Primary assignee:

* vsharshov@mirantis.com - developer, feature lead

Other contributors:

* eli@mirantis.com - consultant about plugin system, main reviewer

Work Items
----------

* Fuel plugin builder - plugin version validation:

  * increase package version from 1.0.0 to 2.0.0;

  * ability to build plugin for both 1.0.0 and for 2.0.0 versions;

  * validation invalid combination of fuel_version and plugin package
    version, e.g. fuel_version is ['6.0'] and plugin package
    version is '2.0.0';

* Nailgun - support 'reboot' task type for plugins;

* Nailgun/Orchestrator - support 'reboot' task type for plugins;

* Fuel CLI - plugin version validation.

Dependencies
============

None

Testing
=======

Unit tests and functional tests are required.

Acceptance Criteria
-------------------

Fuel plugin builder part:

* should be able to create plugin with package version 2.0;

* still should be able to create plugin with package version 1.0;

* should be able to validate plugin with 'reboot' task type;

* should be able to build plugin with 'reboot' task type;

* should not be able to use 'reboot' task type for package
  version 1.0;

* should not be able to use 'reboot' task type for fuel
  version 6.0;

* should be able to use several 'reboot' type tasks at one
  plugin.

System part:

* should reboot node and wait until it back online;

* should be able to use several 'reboot' type tasks at one plugin;

* should run tasks after 'reboot' only when node back online;

* should mark deployment as failed if one of nodes did not reboot
  or reboot timeout is reached;

* should add into Astute's log a warning if timeout is reached;

* the fact of the operation and its result should be logged in
  Astute log.


Documentation Impact
====================

* how to use 'reboot' task type;
* connection and limitation between current fuel release and plugins.

References
==========

* https://blueprints.launchpad.net/fuel/+spec/reboot-action-for-plugin
* Astute part: https://review.openstack.org/#/c/148355/
* Nailgun part: https://review.openstack.org/#/c/149297/
* Fuel plugin builder part: https://review.openstack.org/#/c/150316/