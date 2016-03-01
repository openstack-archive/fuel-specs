..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================
Fuel CI for Puppet OpenStack modules
====================================

https://blueprints.launchpad.net/fuel/+spec/deployment-tests-for-puppet-openstack

--------------------
Problem description
--------------------

Fuel Library heavily depends on external puppet modules and upsteam
puppet-openstack modules in particular. External dependencies are handled by
librarian-puppet-simple and are listed in Fuel Library Puppetfile [1]_. To
keep Fuel Library in sync with upstream puppet-openstack modules Puppetfile
references for those modules were set to 'master' of corresponding repositories.
This effectively means that changes merged to upstream pupppet-openstack
repositories can affect the state of Fuel Library code.

To properly estimate the impact of upstream changes we need a way to test them
against Fuel using Fuel CI.

**List 1.** The list of Puppet OpenStack modules used in Fuel Library

 * puppet-aodh
 * puppet-ceilometer
 * puppet-cinder
 * puppet-glance
 * puppet-ironic
 * puppet-heat
 * puppet-horizon
 * puppet-keystone
 * puppet-murano
 * puppet-neutron
 * puppet-nova
 * puppet-openstacklib
 * puppet-sahara
 * puppet-swift


----------------
Proposed changes
----------------

The easiest way to estimate the impact of upstream changes on Fuel Library is
to replicate the existing Fuel CI tests for Fuel Library and run them against
changes to upstream puppet-openstack modules.

We can see the impact of upstream changes using Fuel Library noop tests and
Fuel deployment tests (using Fuel QA and Fuel Devops).

Noop tests workflow
===================

Proposed workflow for the Fuel Library noop tests with upstream
puppet-openstack modules is following:

* Checkout master of Fuel Library
* Checkout the proposed change to puppet-openstack module and put
  it to 'deployment/puppet/$modulename' directory (relative to
  Fuel Library repo root)
* Run Fuel Library noop tests, which will use librarian-puppet-simple
  to fetch remaining external dependencies

Deployment tests workflow
=========================

Proposed workflow for the Fuel deployment tests with upstream
puppet-openstack modules is following:

* Checkout master of Fuel Library
* Use fixed revisions of Fuel QA and Fuel Devops, the same revisions that is
  currently used for Fuel Library deployment tests
* Checkout the proposed change to puppet-openstack module and put
  it to 'deployment/puppet/$modulename' directory (relative to
  Fuel Library repo root)
* Use librarian-puppet-simple to fetch remaining external dependencies
* Create upstream_modules.tar.gz archive containing the contents of
  'deployment/puppet' directory, including all external dependencies fetched
  by librarian-puppet-simple and the proposed change to puppet-openstack
  module
* Provide upstream_modules.tar.gz archive to Fuel Library package building
  process (using Fuel Mirror scripts)
* Get the latest build of Fuel Community ISO which passed BVT
* Start deployment tests using following Fuel QA test cases:
    1) neutron_vlan_ha
    2) smoke_neutron

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

Fuel Library developers will need to watch the results of these CI jobs,
since Fuel CI as a Thrid Party Testing system doesn't have a way to
technicallyi affect the merge process to upstream puppet-openstack modules
evenin case of failures.

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

* Fuel CI workload will increase significantly. Watching for the changes
  in upstream puppet-openstack module results in ~80 deployment tests daily
  (based on current statistics).

* We already have additional HW resources dedicated for this task, HW nodes
  are configured and connected to Fuel CI and ready to run tests.

--------------------
Documentation impact
--------------------

All infrastructure changes should be documented


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Igor Belikov`_

Mandatory Design Reviewers:
  - `Dmitry Borodaenko`_
  - `Ivan Berezovskiy`_


Work Items
==========

* Implement related changes in jenkins-jobs [2]_


Dependencies
============

None

------------
Testing, QA
------------


Acceptance criteria
===================

* Fuel CI runs noop and deployment tests for puppet-openstack modules

* Fuel CI posts test results to OpenStack Gerrit [3]_ and fits
  Third Party Testing requierements [4]_


----------
References
----------

.. _`Dmitry Borodaenko`: https://launchpad.net/~dburmistrov
.. _`Ivan Berezovskiy`: https://launchpad.net/~r0mikiam
.. _`Igor Belikov`: https://launchpad.net/~skulanov

.. [1] `Fuel Library Puppetfile <https://github.com/openstack/fuel-library/blob/master/deployment/Puppetfile>`_
.. [2] `Jenkins job builder <https://github.com/fuel-infra/jenkins-jobs>`_
.. [3] `OpenStack Gerrit <https://review.openstack.org>`_
.. [4] `Third Party Testing requirements <http://docs.openstack.org/infra/system-config/third_party.html>`_
