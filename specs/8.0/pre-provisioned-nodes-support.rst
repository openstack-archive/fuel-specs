..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Example Spec - The title of your blueprint
==========================================

launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/pre-provisioned-nodes-support

Sometime user want to have possibility to use node with already istalled OS.
So ability of adding pre-provision nodes is needed.


--------------------
Problem description
--------------------

Nodes which were provisioned without Fuel can't be added to fuel nodes array
(if user install all required packages and configure it properly). Also, nodes
which were provisioned with Fuel in one cluster can't be moved to other fuel
cluster without reprovision proccess.


----------------
Proposed changes
----------------

The flow of actions is:

1. User installs plain OS. Node is configured to not boot from PXE.
   Node installed with ssh and without 3d party repos configured with apt.

2. User has possibility to add pre-provisioned node to cluster through
   UI/CLI through API call like discover-provisioned-node. This API
   call should take ip of the node and (login/password or ssh key).

3. Fuel goes to node and discover it OS by ssh. If OS cann't be supported
   error will be throw. In other case Fuel run pre0provision task like
   installing of base Fuel services (nailgun-agent, mcollective, puppet,
   etc.) by copying package to the node.

4. Node appears in Fuel with pre-provisioned status (this is new status) and
   user can add it to the cluster. there Fuel has role restrictions according
   to OS of this node.

5. All configuration is available for pre-provisioned node, exclude disks.

6. Pre-provisioned node can be deployed.

We assuming that node is not added to cobbler because of user responsible
for node provision and cobbler shouldn't send node to bootstrap or something.

Web UI
======

New widget should be added for node discovering. It should contain ip,
login/password, ssh fields. User can choose login/password or ssh
authentification.


Nailgun
======


Support for new OS may be added through fixtures. For OS should be determined
which roles is support. Tasks for node provision/deploy/delete will be
changed according to node status. All nailgun parts which use node status
should be changed.

Data model
----------

Node db model should be extended with new boolean 'pre-provisioned' field

REST API
--------

API request will be added:
    * URL: /nodes/discover_pre_provisioned
    * Method POST
    * HTTP errors:
      - 400 node with specified IP is not found
      - 409 node OS is not supported
    * JSON parameters:
      { 'ip': node ip,
        'login': login,
        'password': password,
        'ssh_key': ssh_key}


Orchestration
=============

Logic of deploying node with pre-provision status is the same as for
provisioned node. On cluster deletion and reset another logic should
be applied for pre-provisioned nodes. It cann't be rebooted because
it is not added to cobbler. So on delete node will cut off from networks
by removing all bridges, enabling only admin network.


RPC Protocol
------------

None

Fuel Client
===========

CLI will be extended with new command like:
  `fuel node discover-pre-provisioned --ip <IP> 
                                      --login <LOGIN> 
                                      --password <PASS>`

Plugins
=======

None


Fuel Library
============

Functional of node OS discovering by ssh.
Functional of installing base Fuel services.


------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

Pre-provisioned node cann't be upgraded because of no possibility to
reinstall such node.

---------------
Security impact
---------------

Due to specific deletion user should reinstall/clean node OS by himself
because of data will not wiped from node.

--------------------
Notifications impact
--------------------

Notification about discovering preprovisioned node should be added.


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

For support specific OS developer should add function in fuel-library for
installing base Fuel services package, add OS to nailgun fixtures.

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
  asvechnikov

Other contributors:
  iponomarev

Mandatory design review:
  TBD


Work Items
==========

* Nailgun (change db_models, validators, add API, add tasks, fixtures)
* Nailgun-agent (volume disks discovering)
* Astute (OS discovering, installation of base Fuel services)
* UI/CLI (add work with new API)
* QA part (not known yet)


Dependencies
============

Depend on hybrid-os feature[0]


------------
Testing, QA
------------

TBA

Acceptance criteria
===================

TBA


----------
References
----------

[0] link to hybrid-os feature
