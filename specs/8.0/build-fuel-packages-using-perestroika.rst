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
   of patchsets to different fuel repos from which packages will be built

.. _cons:

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

This specification changes current workflow for building ISO and completly
removes building packages procedure (both RPM and DEB). Instead make system
must download all required packages from MOS mirrors and/or any other
`customized repos`.

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

We can, implement flag BUILD_PACKAGES, which will preserve
current functionality for building packages:

* BUILD_PACKAGES=0 - do not re-build fuel packages
* BUILD_PACKAGES=1 - do re-build fuel packages

But this approach has `cons`_, duscussed previously


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

We need to preserve original approach for developer (used in custom_iso
job [2]_) - the ability to provide patch (or list of patchsets) for different
repos. The new workflow should be applied (II): packages MUST be build in
Perestroika, which produces `customized repo` with newly build packages.
`Customized repo` should pass to make system as parameter
(see, example below)::

  +-------------------------+   +-------------------------+
  |  nailgun_gerrit_commit  |   |  nailgun_gerrit_commit  |
  |                         |   |                         |
  | refs/changes/10/55310/1 |   | refs/changes/10/55310/1 |
  | refs/changes/10/55310/2 |   | refs/changes/10/55310/2 |
  +------------+------------+   +------------+------------+
               |                             |
               |                             +---------------+
  +------------v------------+                                |  Perestroika
  | git clone ... git fetch |                +--------------------------------+
  +------------+------------+                |  +------------v------------+   |
               |                             |  | git clone ... git fetch |   |
               |                             |  +------------+------------+   |
   +-----------v----------+                  |               |                |
   |    build packages    |                  |       +-------v--------+       |
   +-----------+----------+                  |       | build packages |       |
               |                             |       +----------------+       |
               |                             +--------------------------------+
               |                  customize_repo             |
               |                          +------------------+
               |                          |
       +-------v------+           +-------v------+
       |              |           |              |
       |   make iso   |           |   make iso   |
       |              |           |              |
       +--------------+           +--------------+
              (I)                           (II)

The above workflow (II) should not break current developer expirience and
Jenkins jobs must have the same interface as we have for custom_iso [2]_


--------------------------------
Infrastructure/operations impact
--------------------------------

* Staging workflow MUST be changes, since `version.yaml` is going to be
  removed [4]_

* New jobs for building fuel packages from patchsets should be created


--------------------
Documentation impact
--------------------

None


--------------------
Expected OSCI impact
--------------------

Perestroika must support building `customized repo` from patchset(s), provided
by developer


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
  - `Dmitry Burmistrov`_
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

* ISO build script must not build any packages mentioned in `table`_
  but instead it should download them from Perestroika repos

* Ensure custom_iso job use packages from custom_perestroika_repository
  while build custom ISO


----------
References
----------

.. _`Alexandra Fedorova`: https://launchpad.net/~afedorova
.. _`Dmitry Burmistrov`: https://launchpad.net/~dburmistrov
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`Sergey Kulanov`: https://launchpad.net/~skulanov
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Vladimir Kuklin`: https://launchpad.net/~vkuklin

.. [1] `Fuel stackforge repos <https://github.com/stackforge/>`_
.. [2] `Custom ISO yaml definition <https://github.com/fuel-infra/jenkins-jobs/blob/master/servers/product-ci/7.0/custom_iso.yaml>`_
.. [3] `Chroots for building packages <https://github.com/stackforge/fuel-main/blob/master/sandbox.mk>`_
.. [4] `Get rid of upgrade tarball spec <https://review.openstack.org/#/c/213227>`_