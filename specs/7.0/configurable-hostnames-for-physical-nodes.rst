..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Configurable hostnames for physical nodes
==========================================

https://blueprints.launchpad.net/fuel/+spec/node-naming

Configure the hostnames of the slave nodes that Fuel will deploy based on
custom naming convention or the node's workload in order to have ability to
customize node names and use them to add new node instead of old removed
one.


Problem description
===================

The name that is visible in the UI/CLI/API for the node is NOT what is applied
as the hostname when the node is deployed. The hostname is dynamically
generated (i.e. node-1 .. node-n). The naming convention that is captured
in the Fuel DB should be applied as the hostname during the provisioning
process to enable customers to access the device for updates, security checks,
etc. and prevent confusion.


Proposed change
===============

This spec proposes to extend fuel-cli and nailgun validation API as well in
order to use custom names for generating the hostname prior provisioning stage.
Node name can be changed only before provision stage
Current realization call internal function which change node name in nailgun DB

* Employ visible node name as a target node hostname
* Extend nailgun node validation API
* Modify `nailgun/objects/node.py:make_slave_name()` to use instance name
  in current realization node name generate automatically based on its
  UID(node-$UID). I proposed to extend function to handle node names
  what were changed by user
* API validation should be extended to forbid to rename node after
  provisioned
* Extend fuel-cli to support node re-naming
    for example::

    fuel node --node-id 15 --setname node-3

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

NodeValidator should be extended to handle incorrect node's hostname format and
duplicates of hostnames within a cluster as well.

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

End user gets ``--setname`` additional option via CLI, that not required for
changes. Deployed env can work properly with default values.

Performance Impact
------------------

None

Plugin impact
-------------

None

Other deployer impact
---------------------

Will allow to map node name to hostname of a physical node.

Developer impact
----------------

None

Infrastructure impact
---------------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Ivan Ponomarev

Other contributors:
  <None>

Work Items
----------

* Forbid to rename node after provisioning in API part
* Extend fuel-cli to use ``--setname`` option
* Modify NodeValidation API of Nailgun
* Modify `nailgun/objects/node.py:make_slave_name()` to use instance name
  instead of node-{instance id} template for real target hostname.
* Write a documentation


Dependencies
============

None


Testing
=======

* Nailgun tests should be passed
* Fuel-cli tests should be passed

Set custom node name for a compute via CLI:

1. Set a new name for a compute node via Fuel CLI
2. Provision and deploy the node
3. Run Network check
4. Run OSTF tests set

Set custom node name for a compute via Fuel UI:

1. Set a new name for a compute node via Fuel UI
2. Deploy the changes
3. Run Network check
4. Run OSTF tests set



Documentation Impact
====================

* A note should be added to Fuel Deployment Guide to describe the possibility
  to specify custom node hostname.
* The documentation should warn about using default node-{id} template for
  hostname which will be used in case of incorrect name format.


References
==========

None
