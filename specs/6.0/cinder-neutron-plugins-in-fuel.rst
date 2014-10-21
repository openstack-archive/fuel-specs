..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Cinder/Neutron plugins in fuel
==========================================

https://blueprints.launchpad.net/fuel/+spec/cinder-neutron-plugins-in-fuel

Cloud operators want to extend and change behavior of Fuel in order to
do that, Fuel should provide plugin mechanism.

Problem description
===================

Sometimes Fuel user wants to extend Fuel to install Cinder/Neutron
plugin. Right now user changes the code of Fuel services rebuilds
and adds repositories manually.

The current approach causes a lot of problems:

* user has to support all the patches
* also he has to apply all the patches manually after Fuel upgrade

Proposed change
================

List of terms
-------------

* `plugin` - archive which contains all required data, like
  repositories for ubuntu, centos, metadata file with description
  of plugin, scripts, etc
* `fpb` - is fuel plugin builder, command line tool which helps user to
  develop plugin, the code will be in fuel-web repository

Requirements
------------

* user should be able to install simple Cinder/Neutron
  plugins, "simple" means that plugin doesn't require
  additional business logic, user can configure only
  static data for settings tab
* plugin developer in the most cases should know nothing
  about python/js/css/html
* plugin developer should have easy way to test his plugin
  (he shouldn't reinstall his master node again and again to
  test his plugin)
* plugin should be environment specific, it means that user
  should be able to enable or disable plugins for specific
  environment, plugin should be disabled for deployed environments
  without possibility to enable it

Plugins constraints
-------------------

For the current release we have the next constraints:

* plugin cannot change business logic and should not contain
  any python code
* plugin can provide additional attributes for environment, it cannot
  remove or change existing information which we provide for orchestrator
* plugin cannot add new kernel
* plugin cannot change provisioning data
* user will not be able to enable plugin on deployed environment
* plugin cannot change or add new bootstrap image
* plugin cannot be uninstalled in the first feature release
* plugin cannot change existing database schema
* plugins will work on openstack releases after 6.0 Fuel release,
  plugins won't work on 5.X openstack releases. This constraint
  is related to changes in MCollective plugins

Plugins examples
----------------

* Neutron

  * LBaaS https://wiki.openstack.org/wiki/Neutron/LBaaS

* Cinder

  * GlusterFS http://bit.ly/1BDheDc , we are **not** going
    to deploy GLusterFS nodes, the plugin will allow user
    to configure cinder backend to use existed GlusterFS
    cluster

Plugin development process
--------------------------

Plugin developer will be able to develop plugin on his machine,
we will specify all requirements for environment, like version
of OS and additional dependencies.

* plugin developer installs all of the dependencies which are mentioned
  in development document to prepare his env, like python, rpm, createrepo,
  dpkg-dev
* plugin developer installs `fpb` command line tool
  `pip install fpb`
* plugin developer runs `fpb --create plugin-name`
* fpb creates new directory `plugin-name`, where he can see
  the a basic structure of the plugin with in place documentation
* plugin developer adds his packages with all required dependencies
  for ubuntu and centos
* sets the metadata, like version of the plugin, its description,
  and versions of openstack releases
* then he runs `fpb --build plugin-name` from the plugin directory,
  fpb checks, that all required fields are valid and all
  required files are there, builds the repositories and generates
  tar-ball

Note, `fpb` should provide `--debug` key to turn on debug information.

Checks and validation
^^^^^^^^^^^^^^^^^^^^^

`fpb` should perform checks during the plugin build

* check that metadata is correct
* deploymetn_scripts_path is exists for each release
* repositories_path is exists for each release
* tasks.yaml, check the structure

Plugin installation process
---------------------------

From user point of view:

* user downloads a fuel plugin
* unarchives it in temporary directory
  TODO(eli): maybe it will be implemented in fuelclient
  see http://bit.ly/1sH6GBa
* runs install script which was in the archive, user should provide
  nailgun credentials (user/password) for the script
* after plugin is installed user should **create a new cluster**
  new plugin will not be available for created clusters, even
  if they are not deployed

Install script workflow:

* check if current fuel version is compatible with the plugin
* copy all the files in `/var/www/plugins/plugin_name-plugin_version`
* via rest api create plugin in nailgun

Plugin archive structure
------------------------

This structure should be generated by `fpb` script.

.. code-block:: text

    .
    |-- deployment_scripts
    |   `-- deploy.sh
    |-- environment_config.yaml
    |-- fuel-simple-service.py
    |-- LICENSE
    |-- metadata.yaml
    |-- pre_build_hook
    |-- README.md
    |-- repositories
    |   |-- centos
    |   |   `-- fuel-simple-service-1.0.0-1.x86_64.rpm
    |   `-- ubuntu
    |       `-- fuel-simple-service_1.0.0_amd64.deb
    `-- tasks.yaml

Here is detailed description of some of the files:

**metadata.yaml file**

.. code-block:: yaml

    # Plugin name
    name: fuel_awesome_plugin
    # Plugin version
    version: 0.1.0
    # Description
    description: Enable to use plugin X for Neutron
    # Required fuel version
    fuel_version: 6.0

    # The plugin is compatible with releases in the list
    releases:
      - os: ubuntu
        version: 2014.2-6.0
        # User can specify if his plugin is ha compatible or not
        mode: ['ha', 'multinode']
        deployment_scripts_path: deployment_scripts/
        repository_path: repositories/ubuntu
      - os: centos
        version: 2014.2-6.0
        mode: ['ha', 'multinode']
        deployment_scripts_path: deployment_scripts/
        repository_path: repositories/centos
        # If plugin can work with several openstack releases
        # user can define different directories with packages
        # and deployment scripts, at the same time he can specify
        # the same directory for all of the versions, it depends
        # on plugin implementation
      - os: centos
        version: 2014.2-7.0
        mode: ['multinode']
        deployment_scripts_path: p7.0/deployment_scripts/
        repository_path: 7.0/repositories/centos

    # Plugin types are required to determine what this plugins
    # extends and how to install them
    types:
      - nailgun
      - repository
      - deployment_scripts

    # Version of package format
    package_version: '1'

**environment_config.yaml**

.. code-block:: yaml

  attributes:
    fuel_simple_port:
      value: 2333
      label: 'Port'
      description: 'Port which be used for service binding'
      weight: 25
      type: "text"

    fuel_simple_host:
      value: 0.0.0.0
      label: 'Host'
      description: 'Host which be used for service binding'
      weight: 10
      type: "text"


**tasks format description**

.. code-block:: yaml

   # Roles which the task should be applied on
   - role: ['controller', 'cinder']
     stage: pre_deployment
     type: shell
     priority: 10
     parameters:
       cmd: configure_glusterfs.sh
       timeout: 42
   # Task is applied for all roles
   - role: "*"
     stage: post_deployment
     type: puppet
     priority: 20
     parameters:
       puppet_manifest: cinder_glusterfs.pp
       puppet_modules: modules
       timeout: 42

Directories structure on the master node
----------------------------------------

Directory `/var/www/plugins` which contains all
of the plugins, should be mounted to the next containers.

* rsync - for puppet manifests
* nailgun - to extend nailgun
* nginx - is required for repositories

Plugins upgrade
---------------

User wants to be able to upgrade his plugin, if there will be some new
plugin with updated version of package or other bug fixes.

NOTE(eli): Details to be researched

Alternatives
------------

There are a lot of alternatives, the best of them are described
in `Future improvements` section and will be implemented later.

Future improvements (not for 6.0)
---------------------------------

Plugin manager
^^^^^^^^^^^^^^

Separate services which keeps information about all of the plugins
in the system, it should know how to install or delete plugins.
We will use this service instead of install script to install the
plugins.

Plugins which change business logic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nailgun drivers and hooks which will provide a way to change
deployment/provisioning data for orchestrator.
Also it will be possible to add new role.

UI plugins
^^^^^^^^^^

Add new step in wizard, add new tab, for cluster env, add new settings
window for node configuration.

Plugins which implement separate service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

User will be able to install any service on the master node,
the good example of such kind of plugins is OSTF.

Users requirements for Fuel plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

General use cases:

* ability to execute custom puppet code during deployment state
  (ideally on any stage not only as a post deployment step)
* ability to execute custom python code in Nailgun

  * Define custom roles and node priorities
  * Provisioning serialization
  * Deployment serialization
  * Post deployment orchestration

* ability to execute custom java script code
* ability to modify UI
* ability to add custom deb/rpm packages
* ability to change and extend node specific parameters

More specific use cases:

* Swift standalone installation: custom roles, priorities, UI changes
* Add neutron plugin: custom puppet modules, UI changes
* Custom monitoring schema: UI, priorities, puppet
* Custom Cinder driver: UI, puppet
* Cinder multibackend: UI, puppet
* Add package that require reboot: provisioning customization

Plugins distribution and management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* user should be able to define dependencies between plugins,
  it means that one plugin can require another to be installed
* user should be able to define conflicts between plugins,
  it means that particular plugin cannot be installed on
  the same master node with another plugin
* plugin system should be able recursively retrieve all of
  the dependency and check that all of the subplugins
  are compatibele with each other and with the current
  version of master node

Nodes management hooks
^^^^^^^^^^^^^^^^^^^^^^

* post_node_deletion - execute after node is deleted
* pre_node_deletion - execute before node is deleted


fpb command line interface
^^^^^^^^^^^^^^^^^^^^^^^^^^

* before build check that packages dependencies are
  compatibele with openstack releases dependencies,
  in order to do that, `fpb` should have access to
  all of the repositories

Data model impact
-----------------

There will be new model in nailgun, `Plugins` with many to many
relation to `Cluster` model.
Model for many to many relation `ClustersPlugins` will be used in
order to disable or enable plugin for specific environment.

**Plugins**

* `id` - unique identificator
* `name` - plugin name
* `version` - plugin version
* `description` - plugin description
* `fuel_version` - requires specified fuel version
* `openstack_releases` - is a list of strings with releases

**ClustersPlugins**

* `id` - record id
* `plugins.id` - plugin id
* `clusters.id` - cluster id

REST API impact
---------------

**GET /api/v1/plugins/**

Returns the list of plugins

.. code-block:: json

    [
        {
            "id": 1,
            "name": "plugin_name",
            "version": "1.0",
            "description": "Enable to add X plugin to Neutron",
            "fuel_version": "6.0",
            "package_version": 1,
            "releases": [
                {
                    "os": "ubuntu",
                    "version": "2014.2-6.0"
                },
                {
                    "os": "centos",
                    "version": "2014.2-6.0"
                }
            ]
        }
    ]

**POST /api/v1/plugins/**

.. code-block:: json

    {
        "id": 1,
        "name": "plugin_name",
        "version": "1.0",
        "description": "Enable to add X plugin to Neutron",
        "fuel_version": "6.0",
        "releases": [
            {
                "os": "ubuntu",
                "version": "2014.2-6.0"
            },
            {
                "os": "centos",
                "version": "2014.2-6.0"
            }
        ]
    }


**GET /api/v1/plugins/1/**

Get the information about specific plugin, where 1 is id of the plugin

.. code-block:: json

    {
        "id": 1,
        "name": "plugin_name",
        "version": "1.0",
        "description": "Enable to add X plugin to Neutron",
        "fuel_version": "6.0",
        "releases": [
            {
                "os": "ubuntu",
                "version": "2014.2-6.0"
            },
            {
                "os": "centos",
                "version": "2014.2-6.0"
            }
        ]
    }

**PATCH /api/v1/plugins/1/**

Update specified attributes for plugin

Accepts the same format as response from `GET` request.

**PUT /api/v1/plugins/1/**

Update all of the attributes

Accepts the same format as response from `GET` request.

**DELETE /api/v1/plugins/1/**

Remove a plugin from DB, should have validation which
returns the error, if plugin is used by some environment.

Validation should be disabled if plugin deletion is performed
with `force` parameter in url. It will be required for development.

Orchestration (astute) RPC format
---------------------------------

As it was described above, user specifies the structure like this

.. code-block:: yaml

   - role: ['controller', 'cinder']
     stage: pre_deployment
     type: shell
     priority: 10
     parameters:
       cmd: configure_glusterfs.sh
       timeout: 42
   - role: *
     stage: post_deployment
     type: puppet
     priority: 20
     parameters:
       puppet_manifest: cinder_glusterfs.pp
       puppet_modules: modules
       timeout: 42

Then nailgun configures this data in the next format

TODO(eli): Describe how dry-run can be performed
in case if plugin defines pre hooks

.. code-block:: yaml

      # This stages should be run after astute yaml for role
      # and repositories are on the slaves
      pre_deployment:
        # Add new repo
        - # This task will be autogenerated by nailgun
          type: upload_file
          uids: [1, 2, 3]
          priority: 0
          parameters:
            path: /etc/apt/sources.list.d/plugin_name-1.0
            data: the file data
            # Overwrite already existed file?
            overwrite: true
            # Create intermediate directories as required
            parents: true
            # File permission
            permissions: '0644'
            # User owner
            user_owner: 'root'
            # Group owner
            group_owner: 'root'
            # What permissions should be set for folder
            dir_permissions: '0644'
        - # This task will be autogenerated by nailgun
          type: sync
          uids: [1, 2, 3]
          priority: 1
          parameters:
            src: rsync:///var/www/nailgun/plugins/plugin_name-1.0/scripts
            dst: /etc/fuel/plugins/plugin_name-1.0/scripts
        - type: shell
          uids: [1, 2, 3]
          priority: 10
          parameters:
            cmd: configure_glusterfs.sh
            timeout: 42
            # This parameter should be autogenerated by nailgun
            cwd: /etc/fuel/plugins/plugin_name-1.0
      post_deployment:
        - type: puppet
          uids: [1, 2, 3, 4, 5, 6]
          priority: 20
          parameters:
            puppet_manifest: cinder_glusterfs.pp
            puppet_modules: modules
            timeout: 42
            # This parameter should be autogenerated by nailgun
            cwd: /etc/fuel/plugins/plugin_name-1.0
      deployment_info:
        # Here is deployment information in the same format
        # as it is now

Deployment scripts
------------------

Plugin developer can use any bash scripts or
puppet manifests in order to perform plugin
installation, here is a list of requirements
for the scripts

* if user wants the script to be executed it
  should has right permission and executable
  flag
* if user uses puppet for plugins installation
  he should provide puppet manifests and modules
  in his plugin
* scripts should not brake anything if they were
  run several times

Hooks in nailgun
^^^^^^^^^^^^^^^^

Nailgun should provide the next hooks, where we will be able to change
the default data:

* cluster attributes
* we should be able to add repository with plugin's packages
* nailgun should extend default deployment/patching tasks with tasks
  for pre and post deployment hooks, where should be specified paths
  to scripts directory on the master node

UI implementation
^^^^^^^^^^^^^^^^^

It is not required to add new logic on UI tab, nailgun generates
checkbox for each plugin on settings tab, so user can enable or
disable particular plugin and configure it.

Upgrade impact
--------------

Current release
^^^^^^^^^^^^^^^

Because we don't have any python code in our plugins, plugin will depend on
openstack release, we don't delete releases, as result it's not necessary
to check if plugin is compatible with the current version of fuel.
Also plugin is stored on shared volume which we mount to nailgun container.

Future releases
^^^^^^^^^^^^^^^

When we get plugins with python code, in upgrade script we will have to
check if plugins are compatible with the new version of fuel, if they
aren't compatible, upgrade script should show the message with the list
of incompatible plugins and it should fail the upgrade.
If user wants to perform upgrade, he should provide the directory with
new plugins, which will be updated during the upgrade, or user should
delete plugins which he doesn't use.

Security impact
---------------

This feature has a huge security impact because the user will be able
to execute any command on slave nodes.
Security is included in acceptance criteria of plugins certification,
see `Plugins certification` section.

Notifications impact
--------------------

Installation script will create notification after plugin is installed.

Other end user impact
---------------------

User should be able to disable or enable plugin for specific environment.

Performance Impact
------------------

**Deployment**

* there will not be any impacts if user doesn't have enabled plugins
* if user has enabled plugins for environment, there will be performance
  impact, the time of deployment will be increased, the increasing time
  depends on the way how plugin is written

**Nailgun**

* we assume that there will not be any notable performance impact, in hooks
  we will have to enable merging of custom attributes in case if plugin is
  enabled for environment, the list of the plugins can be gotten within a
  single database query

Also performance is added as acceptance criteria for core plugins,
see `Plugins certification` section.

Other deployer impact
---------------------

Plugin developer will be able to execute pre/post deployment hooks for
the environment.

Changes which are required in astute:

* add several repositories (should be ready, testing is required)
* add posibility to rsync specific directories from master to slave
* add hooks execution before and after puppet run

Plugins certification
---------------------

NOTE(eli): plugin certification is to be discussed topic

Items which should be reviewed during plugin certification:

* Security review
* Performance review
* Compatibility with other plugins in core
* Plugins upgrade
* Check that plugin works fine in case of openstack patching

After plugin is certified user should be able to add plugin in our
plugins repository.

Cerified plugin code repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

User should not follow fuel's workflow in development, as result they
can have their own repositories with code

Cerified plugin repository
^^^^^^^^^^^^^^^^^^^^^^^^^^

We should provide repository with built plugins where user will be able to
download plugin.

Core plugins
------------

Core plugin is a plugin which is developed and supported by fuel team.
They can or cannot be included in an iso. Build system should has
config with a list of built-in plugins.

Fuel CI
^^^^^^^

NOTE(eli): to be discussed with devops and QA team

The main idea is, plugin developer should be able to test his plugins
with our infrastructure.

Developer impact
----------------

Features design impacts:

* any new feature should be considered to be a plugin
* features should be designed to be extendable

Development impacts:

* we should try not to break compatibility with plugins, it should be
  very easy for plugins developer to make migration from previous
  version of Fuel to new one

Implementation
==============

Assignee(s)
-----------

Primary assignee:

* eli@mirantis.com - developer, feature lead
* nmarkov@mirantis.com - python developer

Other contributors:

* sbogatkin@mirantis.com - deployment engineer
* vsharshov@mirantis.com - orchestrator developer
* aurlapova@mirantis.com, tleontovich@mirantis.com - QA engineers
* skulanov@mirantis.com - devops engineer (plugins distribution)

Work Items
----------

* Plugin creation tools - creates plugin skeleton, builds the plugin,
  also it should provide installation script

* Nailgun - should provide ability to enable/disable plugins
  for specific environments, also it should read plugin's attributes
  and merge them on the fly

* Nailgun/Orchestrator - nailgun should provide post/pre deploy tasks
  for orchestrator, orchestrator should provide post/pre deploy hooks

* UI - ability to enable/disable plugin for specific environment

* Fuel CLI - list/enable/disable/configure plugins for environment

Dependencies
============

Nailgun dependencies which should be added within implementation
of Ceph plugin:

* SQLAlchemy==0.9.4
* stevedore==0.15

Testing
=======

There will be several core plugins, which QA team will be able
to install and test.

For neutron it will be LBaaS plugin, for Cinder it will be GlusterFS backend.

Also it will be required to have infrastructure, where plugin developer
will be able to test his plugins. He should have ability to specify plugin
url and the set of plugins, which he would like to run tests with.

Also we can have core plugins, which should be included in our testing cycle,
it means that we should run system tests with plugins, and also run plugins
specific tests.

Documentation Impact
====================

* how to create a plugin
* how to test a plugin
* how to debug a plugin
* how to add a plugin in core repository and how to perform testing
* documentation for plugin user, where will be the information where to take
  a plugin
* how to install a plugin

References
==========

* Nailgun, Ceph as a plugin - https://review.openstack.org/#/c/123840/
* Fuel design summit 2014 -
  https://etherpad.openstack.org/p/fuel-meetup-2014-pluggable-architecture
* User customization requests -
  https://etherpad.openstack.org/p/fuel-plugins-cloud-operators-feedback
* Users complaints about fuel customization - http://bit.ly/1rz4X2B
* Neutron plugins - https://wiki.openstack.org/wiki/Neutron#Plugins
* Cinder plugins - https://wiki.openstack.org/wiki/CinderSupportMatrix
* Plugins certification meeting -
  https://etherpad.openstack.org/p/cinder-neutron-plugins-certification
