..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================
Build Fuel RPM packages for CentOS 7
====================================

https://blueprints.launchpad.net/fuel/+spec/build-fuel-rpm-packages-for-centos7


--------------------
Problem description
--------------------

As an operator I want Fuel RPM packages be available for the latest stable
release of the operating system used on the master node (currently, CentOS 7).
The biggest value for us is that we can consume bug and security fixes directly
from upstream and don't waste resources on support of custom packages
(especially Linux kernel).


----------------
Proposed changes
----------------

Create additional workflow (on packagin-ci) for building fuel [1]_ rpm packages for
CentOS 7:

* stackforge/fuel-agent
* stackforge/fuel-astute
* stackforge/fuel-library
* stackforge/fuel-main
* stackforge/fuel-mirror
* stackforge/fuel-nailgun-agent
* stackforge/fuel-octane
* stackforge/fuel-ostf
* stackforge/fuel-upgrade
* stackforge/fuel-web
* stackforge/python-fuelclient


Web UI
======

None


Nailgun
=======

None


----------
Data model
----------

None


--------
REST API
--------

None


Orchestration
=============

None


------------
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

Developer will be able to use repos with fuel packages built for CentOS 7

--------------------------------
Infrastructure/operations impact
--------------------------------

* Expected jobs workload will be double increased, because of building
  fuel package both for CentOS 6 and CentOS 7


* Will it increase the load on CI infrastructure by making build or test jobs
  consume more CPU, network, or storage capacity? Will it increase the number
  of scheduled jobs?

* Will it require new work-flows or changes in existing work-flows implemented
  in CI, packaging, source code management, code review, or software artifact
  publishing tools?

  * Will it require new or upgraded tools or services to be deployed on project
    infrastructure?

  * Will it require new types of Jenkins jobs?

  * Will it affect git branch management strategies?

  * Will it introduce new release artifacts?

* Will it require changes in build environments of any existing CI jobs? Would
  such changes be backwards compatible with previous Fuel releases currently
  supported by project infrastructure?

--------------------
Documentation impact
--------------------

None


--------------------
Expected OSCI impact
--------------------

Expected and known impact to OSCI should be described here. Please mention
whether:

* There are new packages that should be added to the mirror

* Version for some packages should be changed

* Some changes to the mirror itself are required


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Sergey Kulanov`_

CI-team:
  `Alexander Evseev`_

QA:
  TBD

Mandatory Design Reviewers:
  - `Alexander Evseev`_
  - `Dmitry Burmistrov`_
  - `Roman Vyalov`_
  - `Vladimir Kozhukalov`_
  - `Vitaly Parakhin`_


Work Items
==========

* Implement related changes to zuul-layouts configuration [2]_

* Implement related changes to jenkins-job-builder [3]_


Dependencies
============

* `separate-mos-from-centos`_

------------
Testing, QA
------------


Acceptance criteria
===================

* CI builds Fuel packages for CentOS 7, based on the existing package specs

* Fuel packages available on the public mirrors


----------
References
----------

.. _`Alexander Evseev`: https://launchpad.net/~aevseev-h
.. _`Dmitry Burmistrov`: https://launchpad.net/~dburmistrov
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`Sergey Kulanov`: https://launchpad.net/~skulanov
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Vitaly Parakhin`: https://launchpad.net/~vparakhin

.. _separate-mos-from-centos: https://review.openstack.org/#/c/205109

.. [1] `Fuel stackforge repos <https://github.com/stackforge/>`_
.. [2] `Zuul-layouts <https://review.fuel-infra.org/#/admin/projects/fuel-infra/zuul-layouts>`_
.. [3] `Jenkins job builder <https://github.com/fuel-infra/jenkins-jobs>`_
