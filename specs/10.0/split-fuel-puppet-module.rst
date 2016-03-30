..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================
Split Fuel puppet module
========================

https://blueprints.launchpad.net/fuel/+spec/split-fuel-puppet-module

--------------------
Problem description
--------------------

Currently we use Fuel puppet module [1]_ to deploy the Fuel master node.
Common puppet practices assume different services are deployed by different
puppet modules. Fuel itself is not just a single service but a set of services
and we need to split Fuel puppet module into a set of modules.

Since Fuel is an official OpenStack project we'd better put Fuel related
puppet modules to upstream puppet project.

Fuel puppet module also contains manifests for deployment not only Fuel services
like Nailgun, OSTF, Astute but also database, AMQP, identity, so we'd better
re-use respective manifests that we use for OpenStack deployment.

We run all master node manifests one by one using `deploy.sh` [2]_ script, but
this approach is not flexible.

The motivation behind this proposal is as follows:

* ability to deploy Fuel over several nodes

* ability to upgrade Fuel

* ability to deploy Fuel HA cluster

* ability to deploy not all Fuel services but some of them

* ability to deploy some of OpenStack services on the same nodes as Fuel serivces
  (e.g. database)

* since some of Fuel components are, in fact, OpenStack components
  (Keystone, potentially Ironic, potentially Glance), we need to be able
  to re-use existent deployment tasks both for Fuel deployment and for
  OpenStack deployment


----------------
Proposed changes
----------------

Our suggestion is to use the same approach that we use when deploy OpenStack.
In case of OpenStack we have a set of tasks that describe not only
the deployment of particular services like Nova or Keystone, but also
dependencies that allow to orginize orchestration of the whole multiservice
deployment over multiple nodes environments.

We could use the same approach for Fuel deployment. Fuel module must be split
into a set of moudules (one module per Fuel service). Those manifests that
use third party modules like nginx.pp or postgresql.pp should be put to a
directory, let's say, `fuel_tasks` and respective `tasks.yaml` files should be
created. Once it is ready we then need to have a kind of bootstrap task
manager and task runner (i.e. rudimentary Nailgun and Astute) to be able to
run all Fuel deployment tasks on a single node (a.k.a Fuel master node).

Particular implementation of such rudimentary task manager could be either
a python script (for simplest case) or any existent solution like Ansible
for deployments over several nodes. In the future we could also provide
Fuel LiveCD that will run real Nailgun and Astute to deploy Fuel.
Besides, LiveCD could provide web based Fuel configuration
interface instead of Urwid based Fuelmenu.

New per-service Fuel modules should be written following upstream common
practices, so we can contribute them to openstack/puppet project.

The new set of puppet modules must include at least the following:

* fuel-nailgun (Nailgun and Nailgun client (a.k.a python-fuelclient))
* fuel-astute (Astute)
* fuel-ostf (OSTF)


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

Nonw

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

Fuel puppet module will be split into multiple puppet modules and
these modules will then be moved to upstream. Fuel deployment
procedure will be re-written in terms of tasks and rudimentary
orchestrator will be written (python script) to run these tasks
on a single node (Fuel master node).

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

Upgrade procedure should be re-written so it uses Fuel tasks to
upgrade (re-configure) Fuel services.


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

Fuel deployment procedure is going to change slightly. It will be more
modular and fuel deployment expefience will become the same as for
any other openstack services. For example, it will be possible to
deploy Fuel over multiple node environment.

----------------
Developer impact
----------------

Potentially deployment engineers will be able to deploy Fuel over
several nodes and even deploy Fuel HA cluster.

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

New Fuel deployment procedure should be described in details.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>

Mandatory design review:
  Oleg Gelbukh <ogelbukh@mirantis.com>
  Vladimir Kuklin <vkuklin@mirantis.com>
  Evgeny Li <eli@mirantis.com>
  Alexey Shtokolov <ashtokolov@mirantis.com>
  Alex Schultz <aschultz@mirantis.com>

Work Items
==========

* Split Fuel puppet module into a set of independent modules. One module
  per Fuel service and contribute them to the OpenStack puppet project.
* Create a set of Fuel deployment tasks (similar to OpenStack tasks)
* Create rudimentary orchestrator (python script) to run Fuel deployment
  tasks on a single node (Fuel master node)

Dependencies
============

None

------------
Testing, QA
------------

Current Fuel deployment tests deploy Fuel master node, so it partly covers
the feature. Besides, we need to add necessary tests to public
puppet-openstack CI.

Acceptance criteria
===================

* Fuel puppet module should be split into a set of independent modules.
* Fuel puppet modules should be moved in a set of openstack/puppet-*
  repositories.
* It should be possible to deploy Fuel master node using task based
  approach.

----------
References
----------

.. [1] `Fuel puppet module <https://github.com/openstack/fuel-library/tree/master/deployment/puppet/fuel>`_
.. [2] `Fuel deploy script <https://github.com/openstack/fuel-library/blob/master/deployment/puppet/fuel/examples/deploy.sh>`_
