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
 * Plugin which uses features executed in pre-deployment stage (ex. reserve
   VIP address).

Web UI
======

Fuel UI should be extended in order to support plugin assignment for
particular environment (plugin installation is avaialable from CLI only).
New Plugins tab should appear in both new and deployed environment.

For not deployed environment, the tab should contain a list of plugins
installed to Fuel Master, that can be assigned to the environment.
Plugins in the list should have 'Not assigned' status and 'Assign' button
to mark plugins as pending deployment.
Plugin item in the list should also contain plugin information such as
authors, releases, authors, versions, etc. (the same information that is
shown on the common Plugins page in Fuel UI).

For already deployed environment, the tab should also contain a list of
all plugins installed to Fuel Master and compatible with particular
environment with their data.
Those plugins that are already deployed to the environment, should have
'Assigned' status and NO some action buttons.
Those plugins that are not deployed to the environment, but can be assigned
to the already deployed environment, should have 'Not assigned' status AND
'Asssign' button to mark plugins as pending deployment. To figure out if
a plugin can be added to already deployed environment, UI should check
`installable_after_deployment` plugin attribute.
Those plugins that are not deployed to the environment and can not be added to
the environment after it has been deployed, should have 'Not available' status
and NO 'Assign' button.

After some plugins are marked as pending deployment, environment Dasboard
should display an information that some plugins need deployment and 'Deploy'
button should be enabled to start plugins deployment.

If plugins deployment successful, the plugins have an appropriate 'Assigned'
status on Plugins tab.
[TBD] If plugins deployment failed, it does not affect environment
'operational'status, BUT Fuel UI should warn user about plugin deployment
failure.

[TBD] List of available plugins for the environment should be provided on UI by
`GET /api/plugins/?cluster_id=<cluster_id>` request.

Plugin entry should include:

* `clusters` attribute with a list of assigned environment ids, to check if
  the plugin already assigned to the environment (already existing attribute).

* `installable_after_deployment` attribute to check if plugin can be added to
  already deployed environment (this attribute should be added to Plugin
  model).

[TBD] When user clicks 'Assign' button for a plugin, API should be provided,
how to mark the plugin as pending deployment to the particular environment.
Should it be a new Cluster model attribute like 'pending_plugins'?

[TBD] When user clicks 'Deploy' button to install new plugins to the already
deployed environment, UI should poll 'deploy' task as a usual deployment
process.

Other UI changes:

* Plugins tab should be always locked and read-only during deployment process.
  No 'Assign' buttons on the tab for deploying environment.

* [TBD] Should the tab be locked in stopped or error environment?

* Existing root-level Plugins page in Fuel UI should be updated with plugins
  version data only. No other changes required here.


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
Plugin developer should put statement into documentation how plugin will
handle installation after deployment.

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

Primary assignee:
  ?

Other contributors:
  ?

Mandatory design review:
  ?
  vkramskikh

QA engineer:
  ?

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

- System tests should be created to verify plugin installation on already
  deployed environments.
- Manual testing should be executed according to the UI use cases steps.
- New environment Plugins tab in Fuel UI should be covered with UI functional
  auto tests.
- Manual testing should be executed according to the CLI use cases steps.

Acceptance criteria
===================
* A property in plugin metadata indicates if the plugin can be installed after
  deployment of an environment.
* When plugin installation process is finished the operator is notified about
  the status (success/ failure).
* Fuel API request to install a plugin is validated to ensure that the target
  environment is deployed.
* Fuel API request to apply a plugin is validated to ensure that the plugin can
  be installed on already deployed environment.
* Plugin installed on already deployed environment.
* Plugin applied on already deployed environment.

----------
References
----------

None
