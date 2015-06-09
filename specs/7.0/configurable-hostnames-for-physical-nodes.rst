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
Basically, we are using node's name [1] property only for displaying it to
the user. It uses just a label for nodes.
Also, we have dedicated function `make_slave_name` [2] what in charge
of hostname generating process. Right now, this function is not so flexible
and it generates node's hostname based on node's uid.
I propose to extend current `make_slave_name` function to generate node's name
on the basis of its 'name' property. We are not going to replace current
functionality, but to extend existed one. For example, in case if user don't
want to change default node's name, function will generate node's name based
on its 'uid'. So, backward compatibility will not be corrupted.
As we are going to use node's name as a basis of target hostname, validation
API for nodes should be extended to handle improper values for it (incorrect
symbols, length, etc.).
It was decided that it will not be possible to change node's name for
non-bootstrap nodes as it may lead to system's inconsistency (different values
for displayed hostname and real one). This restriction should be handled via
node's API ( name changing requests for non-bootstrap nodes should be
rejected).
Also, it's proposed to extend the functionality of fuel CLI to support node
re-naming, for example::

    fuel node --node-id 15 --setname node-3

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

NodeValidator should be extended to::

  * handle incorrect node's hostname format
  * handle duplicates of hostnames within a cluster
  * prevent attempts to change hostname for non-bootstrap nodes (exception
    should be raised)

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

New cli option ``--setname`` will be introduced to allow user to change
not only displayed node name, but real hostname for the target system.
It's not obligatory for user to change this value, and, user will be able
to deploy environment successfully without modification of this value.

Performance Impact
------------------

None

Plugin impact
-------------

None

Other deployer impact
---------------------

It will be possible to specify hostname for the target system using
CLI/API/UI.

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

Work Items
----------

* Extend `make_slave_name` function to support hostname generating in the
  basis of node's name property
* Extend Nailgun's NodeValidation API to forbid renaming for non-bootstrap
  nodes and to validate node's name property
* Extend fuel-cli to change node's name property using it (to change name for
  the target system)
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
[1] https://github.com/stackforge/fuel-web/blob/stable/6.1/nailgun/nailgun/db/sqlalchemy/models/node.py#L96
[2] https://github.com/stackforge/fuel-web/blob/stable/6.1/nailgun/nailgun/objects/node.py#L728-L729
