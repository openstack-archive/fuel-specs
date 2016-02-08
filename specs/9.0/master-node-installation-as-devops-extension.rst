..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================================
fuel-devops: Support master node installation as node extension
===============================================================

https://blueprints.launchpad.net/fuel/+spec/master-node-installation-as-devops-extension

In scope of [1] node role extensions were introduced. This spec offers to use
them for bootstrapping of Fuel master node.


--------------------
Problem description
--------------------

There are 2 places in code where installation of Fuel master node is done:

* fuel-qa/fuelweb_test/models/environment.py::EnvironmentModel::setup_environment

* fuel-devops/devops/shell.py::Shell::do_admin_setup

These two places do the same thing but also they have different implementation.
It is not optimal from development and architecture points of view.


----------------
Proposed changes
----------------

Unify methods fuel-qa and fuel-devops, to get in fuel-devops a single method
for setup master node, accessed with Node.ext.setup() instead of dependencies
on unsuitable get_admin_remote() methods.

Example of required steps to bootstrap admin node::

    master_node = env.get_node(name='fuel_master')
    master_node.start()
    master_node.ext.setup()


Web UI
======

None


Nailgun
=======

None

Data model
----------

None


REST API
--------

None


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

None


Fuel Library
============

None


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

None


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None


------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

None


----------------
Developer impact
----------------

None


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  * Anton Studenov (astudenov): astudenov@mirantis.com

Other contributors:
  * Dennis Dmitriev (ddmitriev): ddmitriev@mirantis.com
  * Dmitry Tyzhnenko (dtyzhnenko): dtyzhnenko@mirantis.com
  * Kirill Rozin (krozin): krozin@mirantis.com

Mandatory design review:
  None


Work Items
==========

- Investigate the existing code
- Move/Rewrite fuel-devops/helpers/node_manager.py to extension files
- Update fuel-qa/fuelweb_test/models/environment.py to use node extension


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/template-based-virtual-devops-environments


------------
Testing, QA
------------

None


Acceptance criteria
===================

- Setup of fuel master node is done inside of ``setup`` method of
  node_extension for 5.0, 6.1 and 7.0 versions of Fuel.

- API remains back-compatible to previous versions.


----------
References
----------

[1] - https://blueprints.launchpad.net/fuel/+spec/template-based-virtual-devops-environments
