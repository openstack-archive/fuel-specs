..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Example Spec - The title of your blueprint
==========================================

https://blueprints.launchpad.net/fuel/+spec/split-fuel-puppet-module

--------------------
Problem description
--------------------

Common puppet practices assume different services are deployed by different
puppet modules. Fuel itself is not just a single service but a set of services
and we need to split Fuel puppet module [1]_ into a set of modules.

----------------
Proposed changes
----------------

Currently Fuel puppet module is set of independent puppet manifests. We deploy
Fuel services one by one in a series using `deploy.sh` script [2]_. So, it is not
so hard to split this module into a set of modules. The new set of Fuel modules
should be written following upstream common practices, so it is possible to
move these modules to openstack/puppet-* projects. Fuel deploy script should
be moved to fuel-setup package [3]_.


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
these modules will then be moved to upstream.

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

New set of puppet modules will be available as RPM package(s), so
the upgrade procedure should not be affected.

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

None

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Fuel deployment should be described in details.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>

Mandatory design review:
  Sergii Golovatiuk <sgolovatiuk@mirantis.com>


Work Items
==========

* Split Fuel puppet module into a set of independent modules. One module
  per Fuel service.
* Move Fuel modules to upstream.

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

* Fuel puppet module should be splited into a set of independent modules.
* Fuel puppet modules should be moved in a set of openstack/puppet-*
  repositories.
* It should be possible to deploy Fuel services independently on a single
  node or over multiple nodes env.

----------
References
----------

.. [1] `Fuel puppet module <https://github.com/openstack/fuel-library/tree/master/deployment/puppet/fuel>`_
.. [2] `Fuel deploy script <https://github.com/openstack/fuel-library/blob/master/deployment/puppet/fuel/examples/deploy.sh>`_
.. [3] `Fuel-setup package <https://github.com/openstack/fuel-main/specs/fuel.spec>`_
