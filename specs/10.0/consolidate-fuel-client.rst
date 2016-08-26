..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================================
Consolidate fuel CLI client capabilities in single version
==========================================================

This change is a follow up on the original feature described in the following
blueprint:
https://blueprints.launchpad.net/fuel/+spec/re-thinking-fuel-client

This blueprint describes replacing the old fuel client with the new fuel
client.


--------------------
Problem description
--------------------

There are two versions of fuelclient which are respectively available with fuel
and fuel2 commands. There is no feature parity between them and it is often
quite confusing which version of client a user needs to run. It is necessary to
leave only one version.


----------------
Proposed changes
----------------


Web UI
======

N/A


Nailgun
=======

N/A


Data model
----------

N/A


REST API
--------

N/A


Orchestration
=============

N/A


RPC Protocol
------------

N/A


Fuel Client
===========

* Implement all commands that are missing in the new fuel client.

* Delete old fuel client from the package.

* Add a deprecation warning about deleting fuel2 entry point in the next
  release.

* Set fuel entry point to start the new CLI.

* Make sure old fuel client is installable from PyPi.


The table bellow describes new CLI interfaces in comparision to the old one.

+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| Command                             | Description                                                          | Old alternative                        |
+=====================================+======================================================================+========================================+
| complete                            | print bash completion command                                        | None                                   |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| help                                | print detailed help for another command                              | fuel <cmd> --help                      |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env add nodes                       | Adds nodes to an environment with the specified roles.               | fuel node --set                        |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env create                          | Creates environment with given attributes.                           | fuel env --create                      |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env delete                          | Delete environment with given id.                                    | fuel env --delete                      |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env deploy                          | Deploys changes on the specified environment.                        | fuel deploy-changes                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env deployment-facts delete         | Delete current deployment facts.                                     | fuel deployment --delete               |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env deployment-facts download       | Download the user-defined deployment facts.                          | fuel deployment --download             |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env deployment-facts get-default    | Download the default deployment facts.                               | fuel deployment --default              |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env deployment-facts upload         | Upload deployment facts.                                             | fuel deployment --upload               |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env list                            | Show list of all available environments.                             | fuel env                               |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env network download                | Download and store network configuration of an environment.          | fuel network --download                |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env network upload                  | Upload network configuration and apply it to an environment.         | fuel network --upload                  |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env network verify                  | Run network verification for specified environment.                  | fuel network --verify                  |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env nodes deploy                    | Deploy specified nodes for a specified environment.                  | fuel node --deploy                     |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env nodes provision                 | Provision specified nodes for a specified environment.               | fuel node --provision                  |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env provisioning-facts delete       | Delete current provisioning facts.                                   | fuel provisioning --delete             |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env provisioning-facts download     | Download the user-defined provisioning facts.                        | fuel provisioning --download           |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env provisioning-facts get-default  | Download the default provisioning facts.                             | fuel provisioning --default            |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env provisioning-facts upload       | Upload provisioning facts.                                           | fuel provisioning --upload             |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env redeploy                        | Redeploys changes on the specified environment.                      | fuel redeploy-changes                  |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env remove nodes                    | Removes nodes from an environment.                                   | fuel node remove                       |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env reset                           | Reset deployed environment.                                          | fuel reset                             |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env settings download               | Download and store environment settings.                             | fuel settings --download               |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env settings upload                 | Upload and apply environment settings.                               | fuel settings --upload                 |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env show                            | Show info about environment with given id.                           | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env spawn-vms                       | Provision specified environment.                                     | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env stop-deployment                 | Stop deployment process for a specific environment.                  | fuel stop                              |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| env update                          | Change given attributes for an environment.                          | fuel env --set                         |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| fuel-version                        | Show the version of Fuel.                                            | fuel --fuel-version                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| graph download                      | Download deployment graph configuration.                             | fuel graph --download                  |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| graph execute                       | Start deployment with given graph type.                              | fuel graph --execute                   |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| graph list                          | List deployment graphs.                                              | fuel graph                             |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| graph upload                        | Upload deployment graph configuration.                               | fuel graph --upload                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| network-group create                | Create a new network group.                                          | fuel network-group --create            |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| network-group delete                | Delete specified network group.                                      | fuel network-group --delete            |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| network-group                       | list  List all network groups.                                       | fuel network-group                     |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| network-group show                  | Show network group.                                                  | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| network-group update                | Set parameters for the specified network group.                      | fuel network-group --set               |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| network-template delete             | Delete the network template of the specified environment.            | fuel network-template --delete         |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| network-template download           | Download network configuration for specified environment.            | fuel network-template --download       |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| network-template upload             | Upload network configuration for specified environment.              | fuel network-template --upload         |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node ansible-inventory              | Generate ansible inventory file based on the nodes list.             | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node attributes-download            | Download node attributes.                                            | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node attributes-upload              | Upload node attributes.                                              | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node create-vms-conf                | Create vms config in metadata for selected node.                     | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node disks download                 | Download and store configuration of disks for a node to a file.      | fuel node --disk --download            |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node disks get-default              | Download default configuration of disks for a node to a file.        | fuel node --disk --default             |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node disks upload                   | Upload stored configuration of disks for a node from a file.         | fuel node --disk --upload              |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node interfaces download            | Download and store configuration of interfaces for a node to a file. | fuel node --network --download         |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node interfaces get-default         | Download default configuration of interfaces for a node to a file.   | fuel node --network --default          |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node interfaces upload              | Upload stored configuration of interfaces for a node from a file.    | fuel node --network --download         |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node label delete                   | Delete specific labels on nodes.                                     | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node label list                     | Show list of all labels.                                             | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node label set                      | Create or update specifc labels on nodes.                            | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node list                           | Show list of all available nodes.                                    | fuel node                              |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node list-vms-conf                  | Show list vms for node.                                              | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node show                           | Show info about node with given id.                                  | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node undiscover                     | Remove nodes from database.                                          | fuel node delete-from-db               |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| node update                         | Change given attributes for a node.                                  | fuel node --set                        |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| openstack-config delete             | Delete OpenStack configuration with given id.                        | fuel openstack-config --delete         |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| openstack-config download           | Download specified configuration file.                               | fuel openstack-config --download       |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| openstack-config execute            | Execute OpenStack configuration deployment.                          | fuel openstack-config --execute        |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| openstack-config list               | List all OpenStack configurations.                                   | fuel openstack-config                  |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| openstack-config upload             | Upload new OpenStack configuration from file.                        | fuel openstack-config --upload         |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| plugins list                        | Show list of all available plugins.                                  | fuel plugins --list                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| plugins sync                        | Synchronise plugins on file system with plugins in API service.      | fuel plugins --sync                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| release component list              | Show list of components for a given release.                         | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| release list                        | Show list of all available releases.                                 | fuel release                           |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| release repos list                  | Show repos for a given release.                                      | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| release repos update                | Update repos for a given release.                                    | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| role create                         | Create a role from file description.                                 | fuel role --rel 1 --create             |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| role delete                         | Delete a role from release.                                          | fuel role --delete                     |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| role download                       | Download full role description to file.                              | fuel role --file                       |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| role list                           | Show list of all available roles for release.                        | fuel role                              |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| role update                         | Update role description from file.                                   | fuel role --update                     |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| snapshot create                     | Generate diagnostic snapshot.                                        | fuel snapshot                          |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| snapshot create -c/--config         | Generate diagnostic snapshot with a custom configuration.            | fuel snapshot < config_file.yml        |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| snapshot get-default-config         | Download default config to generate custom diagnostic snapshot.      | fuel snapshot --conf > config_file.yml |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| snapshot get-link                   | Show link to download diagnostic snapshot.                           | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| task delete                         | Delete task with given id.                                           | fuel task                              |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| task deployment-info download       | Save task deployment info to a file.                                 | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| task history show                   | Show deployment history about task with given ID.                    | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| task list                           | Show list of all available tasks.                                    | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| task network-configuration download | Save task network configuration to a file.                           | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| task settings                       | download  Save task settings to a file.                              | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| task show                           | Show info about task with given id.                                  | N/A                                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| vip create                          | Create VIP                                                           | fuel vip --create                      |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| vip download                        | Download VIPs configuration.                                         | fuel vip --download                    |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+
| vip upload                          | Upload new VIPs configuration from file.                             | fuel vip --upload                      |
+-------------------------------------+----------------------------------------------------------------------+----------------------------------------+



Plugins
=======

N/A


Fuel Library
============

N/A


------------
Alternatives
------------

Basically this change is about resolving an old technical debt so there are
no alternatives.


--------------
Upgrade impact
--------------

Upgrade scripts mostly use python-fuelclient as a library. However, some parts
rely on the CLI thus minor modifications may be required.

Upgrading python-fuelclient itself is going to be a usual routine for a
package upgrade.


---------------
Security impact
---------------

Removing old fuel client will also remove a lot of self-written code and
replace it with 3rd party libraries. This will make it easier to control
published CVEs and execute required actions.


--------------------
Notifications impact
--------------------

N/A


---------------
End user impact
---------------

Users will gain the following advantages of the new CLI:

* One unified CLI for all operations

* Possibility to use interactive mode

* Better compliance with OpenStack traditions of making command line clients.


The following problems are expected:

* Users will have to learn the new CLI

* Users may need to adapt their scripts


------------------
Performance impact
------------------

N/A


-----------------
Deployment impact
-----------------

* Deployment engineers will have to use new CLI.

* Automaded deployment tools will be able to use convenient Python API wrapper.

----------------
Developer impact
----------------

* No impact for fuel developers

* 3rd party developers will be able to use conveniend API wrapper to operate
  Fuel.


---------------------
Infrastructure impact
---------------------

CI scripts will have to be adapted to use new CLI before the old one is
deleted.


--------------------
Documentation impact
--------------------

* Release notes must be updated

* A comparision table of the old CLI and the new CLI must be included


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  romcheg

Other contributors:
  akalashnikov

Mandatory design review:
  dpyzhov


Work Items
==========

* Implement all missing commands in the new CLI.

* Adapt CI scripts to use fuel2 instead of fuel command.

* Delete the old fuel client.

* Make old fuel client available on PyPi.


Dependencies
============

N/A


------------
Testing, QA
------------

fuel-devops, fuel-qa and some tests need to be updated to use the new CLI
or the API wrapper instead of the old CLI.

Acceptance criteria
===================

* All capabilities of the old CLI are present in new CLI.

* Modules, tests and data files related to the old CLI are deleted from the
  package.

* Both fuel and fuel2 entry points start the new CLI.

* fuel2 entry point shows a deprecation warning saying it is going to be
  removed in the next release.

* The old CLI is installable from PyPi but not maintained.


----------
References
----------

# https://blueprints.launchpad.net/fuel/+spec/re-thinking-fuel-client
