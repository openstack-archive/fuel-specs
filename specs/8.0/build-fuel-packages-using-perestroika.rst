..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================
Building Fuel packages using Perestroika
========================================

https://blueprints.launchpad.net/fuel/+spec/build-fuel-packages-using-perestroika

-----------
Definitions
-----------

:MOS repo: original repo with all MOS packages

:Custom_repo: contains the only fuel packages, for which gerrit
  commit(s) were provided

:Custom_iso: jenkins job which allows developer to provide list of patchsets to
  different fuel projects and build ISO with changes introduced by this
  patchsets [1]_


--------------------
Problem description
--------------------

We have a number of DEB and RPM fuel packages that one builds during ISO build
process. All these packages reside on stackforge [2]_:

.. _table:

**Table 1.** The list of stackforge repositories and relevant fuel packages

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

#. Developer (in custom ISO build job) can explicitly provide a number
   of patchsets to different fuel repos from which packages will be built

.. _cons:

Cons:

#. There might be the situation, when fuel packages on release ISO and
   release mirror are different

#. Breaks packages signing workflow (link to public PROD-1029)

#. Needs to update/support local chroot build system (from fuel-main [3]_)
   each time when fuel packages changed: added/removed/changed in specs, etc

#. No lintian checks for RPM, DEB packages specs

#. Additional sudo requirements for jenkins user (LP-Bug: `1348599`_)

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
job) - the ability to provide patch (or list of patchsets) for different
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
Jenkins jobs must have the same interface as we have for custom_iso


--------------------------------
Infrastructure/operations impact
--------------------------------

* Build ISO job [4]_ must be updated in the following parts:

  * remove `version.yaml` from artifacts

* Staging workflow MUST be changes, since `version.yaml` is going to be
  removed [5]_

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

* Set build packages jobs in voting mode (blocker
  `public-access-to-packaging-ci`_), but can be implemented like Patching-CI
  approach, by publishing jobs' logs only

* Change Fuel-CI fuel-library build package workflow since for now it
  hardly depends on fuel-main repo (LP-Bug: `1456096`_)

* Create custom package build job with possibility to define a set
  of patchsets to build `custom repository` in Perestroika (like custom_iso)

* Update custom_iso job with ability to provide the path to
  custom_perestroika_repository

* Remove DEB packages build from fuel-main

* Remove RPM packages build from fuel-main


Dependencies
============

* `separate-mos-from-centos`_
* `get-rid-of-upgrade-tarball-spec <https://review.openstack.org/#/c/213227>`_
* `build-centos-image-on-the-master-node`_
* `public-access-to-packaging-ci`_

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

* ISO passes all BVT & Swarm system tests

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

.. _separate-mos-from-centos: https://review.openstack.org/#/c/205109
.. _build-centos-image-on-the-master-node: https://review.openstack.org/#/c/213686/
.. _public-access-to-packaging-ci: https://blueprints.launchpad.net/fuel/+spec/public-packaging-ci
.. _1456096: https://bugs.launchpad.net/fuel/+bug/1456096
.. _1348599: https://bugs.launchpad.net/fuel/+bug/1348599

.. [1] `Custom ISO yaml definition <https://github.com/fuel-infra/jenkins-jobs/blob/master/servers/product-ci/7.0/custom_iso.yaml>`_
.. [2] `Fuel stackforge repos <https://github.com/stackforge/>`_
.. [3] `Chroots for building packages <https://github.com/stackforge/fuel-main/blob/master/sandbox.mk>`_
.. [4] `Build ISO job definition <https://github.com/fuel-infra/jenkins-jobs/blob/master/servers/product-ci/7.0/all.yaml>`_
.. [5] `Get rid of upgrade tarball spec <https://review.openstack.org/#/c/213227>`_
