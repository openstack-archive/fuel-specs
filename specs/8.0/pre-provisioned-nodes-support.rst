..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
Pre-proviosioned nodes support
==============================

launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/pre-provisioned-nodes-support

Sometime user want to have possibility to use node with already installed OS.
So ability of adding pre-provision nodes is needed.

-------------------
Problem description
-------------------

Nodes which were provisioned without Fuel can't be added to fuel nodes array
(if user install all required packages and configure it properly). Also, nodes
which were provisioned with Fuel in one cluster can't be moved to other fuel
cluster without reprovision proccess.

----------------
Proposed changes
----------------

The main idea is create mechanism to grant possibility add pre-provisioned
node to the cluster by using plugins.

Pre-provisioned plugin should contains the next:
    * roles (for example Compute on RHEL, etc.)
    * list of supported OS and Realses (for exmpale RHEL 7.0, RHEL 7.0.1)
    * install command (yum install <package>, apt-get install <package>)
    * list of default repositories for supported operation system
    * puppet manifests

Use case:
    1. User installs plugin which supports required OS

        1.1. Configure repositories represented by the plugin on separate
        plugin page

    2. User obtains a node with vanilla OS installed and disk layout
    configured

    3. User uses WebUI/CLI/API of Fuel Master to request "discovery" the node
    from step 2

        3.1. User provides node’s IP and ssh login+pass OR ssh key

        3.2. Fuel master tries to access the node via provided credentials and
        if successful

            3.2.1. Performs basic OS verification according to installed
            plugins

            3.2.2. Install base Fuel services using corresponding plugin
            settings

    4. Node appears in Fuel with “Pre-provisioned” status

    5. User adds node to an Environment

        5.1.  The list of applicable roles is provided by plugin

    6. User can use default node’s NICs and hostname or apply custom settings
    for them

    7. User runs "Deploy"

User responsible for node provisioning and disks configuration because of this
fact node will not be added to the cobbler and another deletion task should be
runned, instead of usual one.

Also there some restriction will be applied to pre-provisioned nodes:
    * Disks configuration can't be changed
    * This kind of node can't be reprovisioned by Fuel
    * Standard list of roles can't be applied to this node

As node was provisioned without Fuel we can't send node to bootstrap. Node
should be deleted from Fuel db and it should be disconnected from all
networks exclude admin.

Web UI
======

* New widget should be added for node discovering. It should contain ip,
  login/password, ssh fields. User can choose login+password or ssh
  authentification.
* There should be a possibility to configure plugin's repositories on
  plugin's settings page like standard repositories.

Nailgun
=======

Many things should be changed to provide support to plugins:
    * New pre-provisioned status
    * Handle/Validator for discover node
    * Discover mechanism
        ** GetNodeOSVersionTask - operates with plugins when corresponding
           plugin is found node should be associated with plugin
        ** InstallBaseFuelServicesTask - take command from plugin to install
           base Fuel services package
    * Pre-provisioned node should be associated with some plugin
    * Deployment and similiar tasks no longer should use cluster operation
      system
    * Plugins settings should live in dedicated db table
    * Delete/Reset/Deploy tasks should know how to work with pre-provisioned
      node
    * Fuel have to validate disk layout: does it suitable for node’s role
    * Code where status or operation system are used should be checked and
      changed if it's needed

Data model
----------

Plugins settings should be moved to dedicated table.
Node should have field for association it with plugin

REST API
--------

API request will be added:
    * URL: /nodes/discover_pre_provisioned
    * Method POST
    * HTTP errors:
      - 404 node with specified IP is not found
      - 409 node OS is not supported or plugin is not enabled
    * JSON parameters: {
        'ip': <node IP>,
        'login': <login>,
        'password': <password>,
        'ssh_key': <ssh_key>}

Orchestration
=============

* Logic of deploying node with pre-provision status is the same as for
  provisioned node.
* On node deletion or reset another logic should be applied for
  pre-provisioned nodes. It can't be rebooted because it is not added
  to cobbler. Logic already was mentioned.

RPC Protocol
------------

None

Fuel Client
===========

CLI will be extended with new command like:

usage: fuel node discover-pre-provisioned [--ip][--login][--password]
[--ssh-key]

arguments:
    --ip        IP of node discover to
    --login     node login
    --password  node passowrd
    --ssh-key   ssh key for node access

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

We can refuse of pluggable idea. But in this case all data from plugin
should be stored in fixtures and there should be an ability to configure
repositories for different operation system. These required another impact to
DB model and for add support of other OS need to change fixtures and all
puppet manifests.

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

Due to specific deletion user should reinstall/clean node OS by himself
because of data will not wiped from node.

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

User will be able to add pre-provisioned node to Fuel through UI/CLI.

------------------
Performance impact
------------------

Provision stage can be skipped.

-----------------
Deployment impact
-----------------

All was already mentioned.

----------------
Developer impact
----------------

None

--------------------------------
Infrastructure/operations impact
--------------------------------

Some test should be added which can install OS, seems it should be done
by some job.

--------------------
Documentation impact
--------------------

New feature should be documented, namely changes in API/UI/CLI.

--------------------
Expected OSCI impact
--------------------

Base Fuel services package should be added.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  <asvechnikov@mirantis.com>

Other contributors:
  <iponomarev@mirantis.com

Mandatory design review:
  <bdobrelia@mirantis.com>

Work Items
==========

* Nailgun (change db_models, validators, add API, add tasks, fixtures)
* Nailgun-agent (volume disks discovering)
* Astute (OS discovering, installation of base Fuel services)
* UI/CLI (add work with new API)
* QA part (not known yet)

Dependencies
============

None

------------
Testing, QA
------------

* Manual testing should be run according to the UI use cases steps
* Manual testing should be run according to the CLI use cases steps
* System tests should be created for the new plugin
* System tests should be created for the new deploy procedure with Pre-provisioned node

Acceptance criteria
===================	

* There is a possibility to add pre-provisioned node via CLI, UI and API
* List of roles that can be applied to a pre-provisioned node is limited
* There is a possibility to deploy cluster with pre-provisioned node

----------
References
----------

None
