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
process. All these packages reside on openstack [2]_:

.. _table:

**Table 1.** The list of openstack repositories and relevant fuel packages

+------------------+-----------------------------+----------------------------+
|    Repo-name     |       RPM packages          |   DEB packages             |
+==================+=============================+============================+
| fuel-agent       | fuel-agent,                 | fuel-agent,                |
|                  | fuel-bootstrap-cli,         | ironic-fa-bootstrap-       |
|                  | ironic-fa-bootstrap-configs | configs, ironic-fa-deploy  |
+------------------+-----------------------------+----------------------------+
| fuel-astute      | rubygem-astute,             | nailgun-mcagents           |
|                  | nailgun-mcagents            |                            |
+------------------+-----------------------------+----------------------------+
| fuel-library     | fuel-dockerctl,             | fuel-ha-utils,             |
|                  | fuel-ha-utils,              | fuel-misc,                 |
|                  | fuel-library8.0,            | fuel-rabbit-fence,         |
|                  | fuel-migrate,               | fuel-umm                   |
|                  | fuel-misc,                  |                            |
|                  | fuel-notify,                |                            |
|                  | fuel-rabbit-fence,          |                            |
|                  | fuel-umm,                   |                            |
+------------------+-----------------------------+----------------------------+
| fuel-main        | fuel,                       |                            |
|                  | fuel-docker-images,         |                            |
|                  | fuel-bootstrap-image,       |                            |
+------------------+-----------------------------+----------------------------+
| fuel-menu        | fuelmenu                    |                            |
+------------------+-----------------------------+----------------------------+
| fuel-mirro       | fuel-mirror,                | fuel-mirror                |
|                  | python-packetary            | python-packetary           |
+------------------+-----------------------------+----------------------------+
| fuel-octane      | fuel-octane                 |                            |
+------------------+-----------------------------+----------------------------+
| fuel-nailgun-    | nailgun-agent               | nailgun-agent              |
| agent            |                             |                            |
+------------------+-----------------------------+----------------------------+
| fuel-ostf        | fuel-ostf                   |                            |
+------------------+-----------------------------+----------------------------+
| fuel-upgrade     | fuel-upgrade                |                            |
+------------------+-----------------------------+----------------------------+
| fuel-web         | fencing-agent,              | fencing-agent              |
|                  | fuel-nailgun,               |                            |
|                  | fuel-provisioning-scripts,  |                            |
|                  | fuel-openstack-metadata,    |                            |
+------------------+-----------------------------+----------------------------+
| network-checker  | network-checker             | network-checker            |
+------------------+-----------------------------+----------------------------+
| python-fuelclient| python-fuelclient           |                            |
+------------------+-----------------------------+----------------------------+
| shotgun          | shotgun                     |                            |
+------------------+-----------------------------+----------------------------+


Building packages together with ISO has the following pros/cons:

:Pros:

#. Developer (in custom ISO build job) can explicitly provide a number
   of patchsets to different fuel repos from which packages will be built

.. _cons:

:Cons:

#. There might be the situation, when fuel packages on release ISO and
   release mirror are different

#. Breaks packages/repos signing workflow on perestroika side

#. Needs to update/support local chroot build system (from fuel-main [3]_)
   each time when fuel packages changed: added/removed/changed in specs, etc

#. No lintian checks for RPM, DEB packages specs

#. Additional sudo requirements for jenkins user (LP-Bug: `1348599`_)

#. Additional time required for building packages locally, which is 50% of
   all build ISO process


----------------
Proposed changes
----------------

This specification changes current workflow for building ISO and completely
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

Continue build packages during ISO build, but this approach has
`cons`_, discussed previously


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

Build ISO time should become ~30% time faster, since we are downloading
packages directly from mirrors and not building them locally


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
               |                     custom_repo             |
               |                          +------------------+
               |                          |
       +-------v------+           +-------v------+
       |              |           |              |
       |   make iso   |           |   make iso   |
       |              |           |              |
       +--------------+           +--------------+
              (I)                           (II)

The above workflow (II) should not break current developer experience and
Jenkins jobs must have the same interface as we have for custom_iso


---------------------
Infrastructure impact
---------------------

* Build ISO job [4]_ must be updated in the following parts:

  * remove `version.yaml` from artifacts

* New jobs for building fuel packages from patchsets should be created

* Implement fuel package building and install test on each patchset-created end
  merge gerrit events [5]_


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

* Implement BUILD_PACKAGES=0 variable in fuel-main which skips DEB/RPM packages
  build on ISO build process



Dependencies
============

* `separate-mos-from-centos`_
* `get-rid-of-upgrade-tarball-spec <https://review.openstack.org/#/c/213227>`_
* `dynamically-build-bootstrap`_
* `public-access-to-packaging-ci`_

------------
Testing, QA
------------

Manual Acceptance Tests
=======================

* Use custom_packages job to build any fuel-package from `table`_;
* Build custom iso with custom_repo defined in EXTRA_RPM_PACKAGES;
* Start custom_bvt_test with custom_iso and defined EXTRA_DEB_PACKAGES;


Acceptance criteria
===================

* ISO build script must not build any packages mentioned in `table`_
  but instead it should download them from Perestroika repos

* ISO passes all BVT & Swarm system tests acceptance level

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

.. _separate-mos-from-centos: https://github.com/openstack/fuel-specs/blob/master/specs/8.0/separate-mos-from-centos.rst
.. _dynamically-build-bootstrap: https://github.com/openstack/fuel-specs/blob/master/specs/8.0/dynamically-build-bootstrap.rst
.. _public-access-to-packaging-ci: https://blueprints.launchpad.net/fuel/+spec/public-packaging-ci
.. _1456096: https://bugs.launchpad.net/fuel/+bug/1456096
.. _1348599: https://bugs.launchpad.net/fuel/+bug/1348599

.. [1] `Custom ISO yaml definition <https://github.com/fuel-infra/jenkins-jobs/blob/master/servers/jenkins-product-ci/8.0/custom_iso.yaml>`_
.. [2] `Fuel openstack repos <https://github.com/openstack/>`_
.. [3] `Chroots for building packages <https://github.com/openstack/fuel-main/blob/master/sandbox.mk>`_
.. [4] `Build ISO job definition <https://github.com/fuel-infra/jenkins-jobs/blob/master/servers/new-product-ci/8.0/all.yaml>`_
.. [5] `Build fuel rpm packages for CentOS7 <https://github.com/openstack/fuel-specs/blob/master/specs/8.0/build-fuel-rpm-packages-for-centos7.rst>`_