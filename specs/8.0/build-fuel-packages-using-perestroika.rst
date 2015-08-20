..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================
Building Fuel packages using Perestroika
========================================

https://blueprints.launchpad.net/fuel/+spec/build-fuel-packages-using-perestroika

--------------------
Problem description
--------------------

We have a number of DEB and RPM fuel packages that one builds during ISO build
process. All these packages reside on stackforge [1]_:

.. _table:

+--------------------+-----------------------------+---------------------+
|    Repo-name       |       RPM packages          |   DEB packages      |
+====================+=============================+=====================+
| fuel-agent         | - fuel-agent                | - fuel-agent        |
+--------------------+-----------------------------+---------------------+
| fuel-astute        | - ruby21-rubygem-astute     | - nailgun-mcagents  |
|                    | - ruby21-nailgun-mcagents   |                     |
|                    | - nailgun-mcagents          |                     |
+--------------------+-----------------------------+---------------------+
| fuel-library       | - fuel-dockerctl            | - fuel-ha-utils     |
|                    | - fuel-ha-utils             | - fuel-misc         |
|                    | - fuel-library8.0           | - fuel-rabbit-fence |
|                    | - fuel-migrate              |                     |
|                    | - fuel-misc                 |                     |
|                    | - fuel-notify               |                     |
|                    | - fuel-rabbit-fence         |                     |
+--------------------+-----------------------------+---------------------+
| fuel-main          | - fuel                      |                     |
+--------------------+-----------------------------+---------------------+
| fuel-nailgun-agent | - nailgun-agent             | - nailgun-agent     |
+--------------------+-----------------------------+---------------------+
| fuel-ostf          | - fuel-ostf                 |                     |
+--------------------+-----------------------------+---------------------+
| fuel-web           | - fencing-agent             | - fencing-agent     |
|                    | - fuel-package-updates      | - nailgun-net-check |
|                    | - fuel-provisioning-scripts |                     |
|                    | - fuelmenu                  |                     |
|                    | - nailgun                   |                     |
|                    | - nailgun-net-check         |                     |
|                    | - shotgun                   |                     |
+--------------------+-----------------------------+---------------------+
| python-fuelclient  | - python-fuelclient         |                     |
+--------------------+-----------------------------+---------------------+


Such workflow has the following pros/cons:

Pros:

#. Developer (in custom ISO build job [2]_) can explicitly provide a number
   of patchsets to different fuel packages' repos.

Cons:

#. There might be the situation, when fuel packages on release ISO and
   release mirror are different

#. Breaks packages signing workflow (link to public PROD-1029)

#. Needs to update/support local chroot build system (from fuel-main [3]_)
   each time when fuel packages changed: added/removed/changed in specs, etc

#. No checks for RPM, DEB packages specs

#. Additional sudo requirements for jenkins user (link to public PROD-420,
   LP-Bug: 1348599)

#. Additional time required for building packages locally, which is 50% of
   all build ISO process


----------------
Proposed changes
----------------

Here is where you cover the change you propose to make in detail. How do you
propose to solve this problem?

If this is one part of a larger effort make it clear where this piece ends. In
other words, what's the scope of this effort?

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

CI changes


------------
Alternatives
------------

What are other ways of achieving the same results? Why aren't they followed?
This doesn't have to be a full literature review, but it should demonstrate
that thought has been put into why the proposed solution is an appropriate one.


--------------
Upgrade impact
--------------

If this change set concerns any kind of upgrade process, describe how it is
supposed to deal with that stuff. For example, Fuel currently supports
upgrading of master node, so it is necessary to describe whether this patch
set contradicts upgrade process itself or any supported working feature that.


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

Discuss things that will affect how you deploy and configure Fuel
that have not already been mentioned, such as:

* What configuration options are being added? Should they be more generic than
  proposed? Are the default values ones which will work well in
  real deployments?

* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

* If this change is a new binary, how would it be deployed?

* Please state anything that those doing continuous deployment, or those
  upgrading from the previous release, need to be aware of. Also describe
  any plans to deprecate configuration values or features.  For example, if a
  directory with instances changes its name, how are instance directories
  created before the change handled?  Are they get moved them? Is there
  a special case in the code? Is it assumed that operators will
  recreate all the instances in their cloud?


----------------
Developer impact
----------------

Discuss things that will affect other developers working on Fuel,
such as:

* If the blueprint proposes a change to the driver API, discussion of how
  drivers would implement the feature is required.


--------------------------------
Infrastructure/operations impact
--------------------------------

Explain what changes in project infrastructure will be required to support the
proposed change. Consider the following:

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
  `Alexandra Fedorova`_

QA:
  TBD

Mandatory Design Reviewers:
  - `Roman Vyalov`_
  - `Vladimir Kozhukalov`_
  - `Vladimir Kuklin`_


Work Items
==========

* Move all packages build process to Perestroika

* Set build packages jobs in voting mode (blocker PROD-81), but can be
  implemented like Patching-CI approach, by publishing jobs' logs only

* Change Fuel-CI fuel-library build package workflow since for now it
  hardly depends on fuel-main repo (LP-Bug: 1456096 )

* Create custom package build job to make it possible to define a set
  of commits to build custom perestroika repository (like custom_iso)

* Update custom_iso job with ability to provide the path to
  custom_perestroika_repository

* Remove DEB packages build from fuel-main

* PROD-885

* PROD-416

* Remove RPM packages build from fuel-main


Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


------------
Testing, QA
------------

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly.

If there are firm reasons not to add any other tests, please indicate them.


Acceptance criteria
===================

* ISO build script must not build any packages mentioned in table_
  but instead it should download them from Perestroika repos

* Ensure custom_iso job use packages from custom_perestroika_repository
  while build custom ISO


----------
References
----------

.. _`Alexandra Fedorova`: https://launchpad.net/~afedorova
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`Sergey Kulanov`: https://launchpad.net/~skulanov
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Vladimir Kuklin`: https://launchpad.net/~vkuklin

.. [1] `Fuel stackforge repos <https://github.com/stackforge/>`_
.. [2] `Custom ISO yaml definition <https://github.com/fuel-infra/jenkins-jobs/blob/master/servers/product-ci/7.0/custom_iso.yaml>`_
.. [3] `Chroots for building packages <https://github.com/stackforge/fuel-main/blob/master/sandbox.mk>`_
