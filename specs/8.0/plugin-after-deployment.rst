This work is licensed under a Creative Commons Attribution 3.0 Unported License
http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Install plugin on already deployed environment
==============================================

https://blueprints.launchpad.net/fuel/+spec/plugin-after-deployment

We need to have possibility to install plugin on already deployed
environment.

-------------------
Problem description
-------------------

Now to deploy plugin code on already deployed environment, you need to install
plugin and redeploy environment. This will lead to environment downtime and
possibly to data loss.

We want to have possibility to install some plugins on already deployed
environments.

---------------
Proposed change
---------------

We will extend Fuel API to be able to execute installation tasks for given
plugin in any point in time (after environment is successfully deployed).

This API call will execute tasks defined inside tasks.yaml (plugin format
version <= 2) or deployment_tasks.yaml (plugin format version > 2).

We will introduce new property in plugin metadata.yaml named
`installable_after_deployment`.
This property will describe if plugin can be installed after environment
deployment.

It's plugin developer responsibility to have knowledge if plugin can be
installed after deployment.
In some cases it will not be possible:

 * Plugin which have pre-deployment tasks defined.
 * Plugin which uses features executed in pre-deployment stage (ex. reserve VIP
address).

Web UI
======

To support install and use plugin on previously deployed environment,
we need extend CLI and UI to control plugin management on Fuel Master.
Plugins should be installed on Fuel Master, and will available for all
environments.
When plugin is installed, you should assign plugin in given version
to environment. After that plugin can be deployed using "Deploy changes".

Each environment should have added 'plugins' tab, which will provide an
information about installed plugins on Fuel Master, with available versions.
Each entry should contain information, about:

   - plugin is installed, or is available to be installed

That information should be related to button 'Assign'.
If there is possibility to assign plugin, button should be available for use,
if not it should be disabled.

Nailgun
=======

Data model impact
-----------------

metadata.yaml file will contain additional field called
`installable_after_deployment`.
This field will store boolean value true/false (1/0).

REST API impact
---------------

API should allow to execute all tasks needed to install plugin.
This API call should be available per environment (install plugin on given
environment).
API should do some validation for each call:

   - Check if for environment was successfully deployed.
   - Check if parameter which defines if plugin can be installed after
     deployment has value true/1.

Orchestration
=============

RPC Protocol
------------

None

Fuel Client
===========

Fuel client should support flow to assign plugin to given environment.

#. command for assigning plugin to environment:

   fuel plugins --assign --env <env_id> <plugin_name>==<plugin_version>

Flow of installing and deploying plugin:

#. install plugin:

   fuel plugins --install <plugin_name>.rpm

#. assign plugin:

   fuel plugins --assign --env <env_id> <plugin_name>==<plugin_version>

#. deploy changes:

   fuel deploy-changes --env <env_id>

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

Instead of providing the `installable_after_deployment` parameter, there
could be a mechanism which would guess based on existence (or lack) of
pre-deployment tasks in the plugin, whether plugin can be installed on already
deployed environment.

   Cons:
      - We need to implement some kind of logic in API/nailgun to decide
        if plugin can be installed.
      - This logic always will provide worse results than plugin developer.

   Pros:
      - Plugin developer doesn't have to change anything inside plugin.

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

New API should have standard Fuel API authentication enabled.

--------------------
Notifications impact
--------------------

When installation process ends we should inform operator about status
(success/failure).

---------------
End user impact
---------------

In some cases, installation can lead to service disruption.
Ex. plugin requires to restart some core services.
Plugin developer should put statement into documentation how plugin will handle
installation after deployment.

------------------
Performance impact
------------------

In most cases none. But sometimes plugin installation can run some "heavy"
tasks.
Ex. Ceph installation can run some kind of index rebuilding which will lead to
high IO on node.

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

Plugin developer should decide if plugin can be installed after deployment.
Plugin developer should update documentation of plugin (how plugin handle
installation after deployment).

--------------------------------
Infrastructure/operations impact
--------------------------------

It will be possible to install plugin on already deployed environment.

--------------------
Documentation impact
--------------------

We need to prepare documentation which will describe this design change.

--------------------
Expected OSCI impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Work Items
==========

 * Modify API to execute plugin installation if possible.
 * Modify CLI/UI to support new API call.

Dependencies
============

None

-----------
Testing, QA
-----------

We need to prepare test scenarios, to check if plugins can be installed after
deployment.

- System tests should be created to verify plugin installation on already
deployed environments
- Manual testing should be executed according to the UI use cases steps
- Manual testing should be executed according to the CLI use cases steps

Acceptance criteria
===================
* There is a possibility to apply a plugin on an already deployed environment

----------
References
----------
