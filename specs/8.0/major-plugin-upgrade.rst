..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================
Major plugin version upgrade
============================

https://blueprints.launchpad.net/fuel/+spec/example

We need a possibility to perform major version plugin upgrade.
By upgrade we understand not only upgrade plugin version on Fuel master, but
also run upgrade path on all nodes in environment.
Upgrade should be possible for each environment independently.

-------------------
Problem description
-------------------

Now you can do only minor plugin upgrades (ex. 1.0.1 -> 1.0.2), this is designed
to support ie. security upgrades.
To do this you can use `Using Fuel CLI <https://docs.mirantis.com/openstack/fuel/fuel-6.1/user-guide.html#using-fuel-cli>`_ command::

        fuel plugins --update <fuel-plugin-file>

But this command upgrades only RPM file on Fuel. It will not execute any task
on already deployed nodes. Only new nodes (in current or in new environment)
will have new code installed.

We need a possibility to run upgrade tasks on already deployed nodes.

Now when you install a plugin, it is assigned to Fuel Master. That means each environment
has the same version of plugin installed (some plugins can be enabled for
some environments).

When we introduce plugin upgrades, we need to support different versions of
the plugin for different environments.
On a single Fuel Master installation Operator can have many environments with
different purposes:

 * Production with stable version of the plugin
 * Testbed with latest version of the plugin

In the above example, Operator might want to update the plugin in testbed env but still
have possibility to manage production environment (deploy nodes with stable
plugin code).

----------------
Proposed changes
----------------

We will extend Fuel API to be able to execute dedicated upgrade plugin path.
This "upgrade plugin path" is a bunch of tasks which should be executed to
perform upgrade.
Each plugin developer should prepare upgrade path for plugin.
Format of upgrade path is available in data impact section.

Upgrade path contains different tasks than standard plugin installation path
(tasks.yaml/deployment_tasks.yaml).

We will assign plugins in given version to environment. This way each
environment can have different versions of the plugin. This will allow operator
to manage environments even with old plugin version.

To support plugin upgrades, we need a possibility to have many versions of a plugin
installed on Fuel Master.
All plugin versions should be available for all environments, and ready to be
installed or/and enabled.
Installation of a newer plugin version should not overwrite previous one.

Web UI
======

When upgrade is possible we should have a button which will assign new version
of the plugin to given environment.
'Deploy changes' should be executed by user after assigning new version of plugin.
We should show which version of the plugin is installed on given environment.
We should show all available plugins (in all available versions) on Fuel master.

Nailgun
=======

Data model
----------

We need to store in DB information which plugin version was assigned for each
environment. During puppet/plugin sync task we should sync only assigned
plugin version.
We need to store in DB information which versions of plugins were installed and
are available for deploy.

We will introduce new file to the plugin structure. This file will store upgrade
path for plugin.
upgrade_tasks.yaml structure will be similiar to deployment_tasks.yaml.
It will introduce only two new parameters:

   - from_version
   - to_version

Example:

.. code-block:: yaml

 ---
 - role: ['primary-controller']
  stage: post_deployment/8100
  from_version: 1.0
  to_version: 1.1
  type: puppet
  parameters:
    puppet_manifest: puppet/manifests/upgrade/1.0-1.1/primary_controller.pp
    puppet_modules: puppet/modules:/etc/puppet/modules
    timeout: 1200
 - role: ['controller']
  stage: post_deployment/8101
  from_version: 1.0
  to_version: 1.1
  type: puppet
  parameters:
    puppet_manifest: puppet/manifests/upgrade/1.0-1.1/controller.pp
    puppet_modules: puppet/modules:/etc/puppet/modules
    timeout: 1200
 - role: ['primary-controller']
  stage: post_deployment/8102
  from_version: 1.1
  to_version: 1.2
  type: puppet
  parameters:
    puppet_manifest: puppet/manifests/upgrade/1.1-1.2/primary_controller.pp
    puppet_modules: puppet/modules:/etc/puppet/modules
    timeout: 600

With that example, if the upgrade of plugin version from 1.0 to 1.1 is to be performed,
first 2 tasks will be run.
If the upgrade from version 1.0 to 1.2 should be performed, all 3 subsequent tasks will be performed.
Order is important here - tasks from 1.0 to 1.1 will be executed first, then
tasks upgrading from 1.1 to 1.2.

REST API
--------

API should allow to get/set information about which plugin (including version)
was enabled on given environment.

API should allow to get information about which versions of plugins are
available on Fuel Master.

API should allow to execute upgrade plugin path.
This API call should be available per environment (upgrade plugin on given
environment, not all environments).
API should do some validation for each call:

   - Check if there is a need of upgrade for the given environment.
     Ex. plugin is already present in latest version.
   - Check if plugin have proper upgrade path available.


Orchestration
=============

RPC Protocol
------------

None

Fuel Client
===========

Command for assigning plugin to environment:

   fuel plugins --assign --env <env_id> <plugin_name>==<plugin_version>

Flow of upgrading and deploying plugin:

#. install new version plugin:

   fuel plugins --install <plugin_name>-<new_version>.rpm

#. assign plugin:

   fuel plugins --assign --env <env_id> <plugin_name>==<new_version>

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

1) Support only the latest version of a plugin for environment.

In that case if operator installs new version of the plugin, he also should update
all environments.
Otherwise he will loose a possibility to manage environments with previous
versions of the plugin. This is because Fuel will sync only the latest version of the plugin
code which is not always compatible with previous versions.

   Cons:
      - All environments have the same version of the plugin installed.
            Operator doesn't have possibility to test plugins in different versions.

   Pros:
      - Some part of this spec can be abandoned.

2) Upgrade will only change version on Fuel master.

We will handle major upgrades the same way as minor upgrades.
Operator will be responsible for running manually all necessary steps to perform
upgrade.

   Cons:
      - Operator should manually execute appropriate tasks to perform full
            upgrade.

   Pros:
      - Some part of this spec can be abandoned.

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

When upgrade process ends we should inform operator about status
(success/failure).
We should inform which version have been installed.

---------------
End user impact
---------------

In some cases, upgrade can lead to service disruption. Ex. new version of a daemon
delivered by plugin is not compatible with old clients. In that case the service
will be unavailable until upgrade is finished.
In some cases upgrade of the plugin can lead to data loss (e.g. overwrite of data).
Plugin developer should put statement into documentation how the plugin will handle
upgrades and what are the potential onward caveats.

------------------
Performance impact
------------------

In most cases none. But sometimes plugin upgrade path can run some "heavy"
tasks.
Ex. Ceph upgrade can run some kind of index rebuilding which will lead to high
IO on node.

Different versions of the plugin can lead to hard to debug performance problems.
Ex. daemon in version X installed by plugin in version Y on environment Z have
performance problems.

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

Plugin developer should prepare upgrade path for plugins.
Plugin developer should test the plugin. The testing should especially show if
the upgraded version of the plugin will not have a negative impact on the existing deployments
such as increased load or data loss.
Plugin developer should update documentation of the plugin (how the plugin handles
upgrades).

--------------------------------
Infrastructure/operations impact
--------------------------------

None

--------------------
Documentation impact
--------------------

We need to prepare documenation which will describe this design change.

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

 * Modify nailgun to assign plugin in given version to environment.
 * Modify API to set/get plugin version assigned to environment.
 * Show in UI/CLI which plugin in which version was assigned to environment.
 * Modify nailgun to build granular task tree for plugin upgrade.
 * Modify API to execute plugin upgrade path for given environment.
 * Modify CLI/UI to support new API call.
 * Modify API to store plugin in multiple versions.

Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?

-----------
Testing, QA
-----------

* System tests should be created to verify installing multiple plugin versions
  on Fuel Master node
* System tests should be created to verify upgrading of a major plugin version
  on environments
* Manual testing should be executed according to the UI use cases steps
* Manual testing should be executed according to the CLI use cases steps

Acceptance criteria
===================

* There is a possibility to install multiple plugin versions on Fuel Master
  node via Fuel API/ CLI
* There is a possibility to apply a major version to a live plugin on an
  existing environment via Fuel API/ CLI/ UI
* Upgrade is possible for each environment independently
* Fuel API request for upgrading plugin version is validated to ensure that
  there is a need for upgrade, i.e. to skip upgrade if the latest version is
  already present on the given environment
* When upgrade process is finished the operator is notified about the status
  (success/ failure)
* When upgrade process is finished successfully the operator is notified about
  the version which is installed

----------
References
----------
