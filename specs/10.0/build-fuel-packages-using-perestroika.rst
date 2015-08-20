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

:MOS repo: original repo with all MOS packages, eg:

  .. code-block:: python

      * http://mirror.fuel-infra.org/mos-repos/centos/mos10.0-centos7/
      * http://mirror.fuel-infra.org/mos-repos/ubuntu/10.0/

:Custom_repo: temporary repository, which perestroika creates on gerrit events
  (patchset created/updated), in format:

  .. code-block:: python

      http://packages.fuel-infra.org/review/FUEL-<patchset-num>/repositories/<os>/

  Eg:

  .. code-block:: python

      * http://packages.fuel-infra.org/review/FUEL-302965/repositories/centos/
      * http://packages.fuel-infra.org/review/FUEL-302965/repositories/ubuntu/

  Custom_repo should be removed on MERGE gerrit-event

:Custom_iso: jenkins job which allows developer to provide list of patchsets to
  different fuel projects and build ISO with changes introduced by this
  patchsets [1]_


--------------------
Problem description
--------------------

We have a number of DEB and RPM fuel packages that one builds during ISO build
process. All these packages reside on openstack (see zuul config [2]_):

.. _table:

**Table 1.** The list of OpenStack repositories and relevant Core Fuel packages

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
|                  | fuel-library10.0,           | fuel-rabbit-fence,         |
|                  | fuel-migrate,               | fuel-umm                   |
|                  | fuel-misc,                  |                            |
|                  | fuel-notify,                |                            |
|                  | fuel-rabbit-fence,          |                            |
|                  | fuel-umm,                   |                            |
+------------------+-----------------------------+----------------------------+
| fuel-main        | fuel                        |                            |
|                  | fuel-release,               |                            |
|                  | fuel-setup,                 |                            |
+------------------+-----------------------------+----------------------------+
| fuel-menu        | fuelmenu                    |                            |
+------------------+-----------------------------+----------------------------+
| fuel-mirror      | fuel-mirror,                | fuel-mirror                |
|                  | python-packetary            | python-packetary           |
+------------------+-----------------------------+----------------------------+
| fuel-octane      | fuel-octane                 |                            |
+------------------+-----------------------------+----------------------------+
| fuel-nailgun-    | nailgun-agent               | nailgun-agent              |
| agent            |                             |                            |
+------------------+-----------------------------+----------------------------+
| fuel-ostf        | fuel-ostf                   |                            |
+------------------+-----------------------------+----------------------------+
| fuel-ui          | fuel-ui                     |                            |
+------------------+-----------------------------+----------------------------+
| fuel-upgrade     | fuel-upgrade                |                            |
+------------------+-----------------------------+----------------------------+
| fuel-web         | fencing-agent,              | fencing-agent              |
|                  | fuel-nailgun,               |                            |
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

New workflow should be applied (II): packages MUST be build in
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


---------------------
Infrastructure impact
---------------------

* Build ISO job [4]_ should consume packages from mirrors instead of building
  them

* Implement fuel package building and install test on each patchset-created end
  merge gerrit events [5]_


--------------------
Documentation impact
--------------------

Related changes should be reflected in documentation.


--------------------
Expected OSCI impact
--------------------

Perestroika must support building `customized repo` either on gerrit patchsets'
events or `rebuild` comment message to the patchset


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
  - `Vitaly Parakhin`_


Work Items
==========

* Move all packages build process to Perestroika

* Set build packages jobs in voting mode (`public-access-to-packaging-ci`_)

* Create custom package build job with possibility to define a set
  of patchsets to build `custom repository` in Perestroika (like custom_iso)

* Update custom_iso job with ability to provide the path to
  custom_perestroika_repository


Dependencies
============

* `separate-mos-from-centos`_
* `get-rid-of-upgrade-tarball-spec <https://review.openstack.org/#/c/213227>`_
* `public-access-to-packaging-ci`_

------------
Testing, QA
------------

Manual Acceptance Tests
=======================

* All fuel packages should be build by perestroika
* On each patchset to fuel project [5]_, related custom repo should be created
* Build custom iso with custom_repo defined in EXTRA_RPM_PACKAGES;
* Start custom_bvt_test with custom_iso and defined EXTRA_DEB_PACKAGES;


Acceptance criteria
===================

* ISO build script must not build any packages but instead it should download
  them from mirrors

* ISO passes all BVT & Swarm system tests acceptance level


----------
References
----------

.. _`Alexandra Fedorova`: https://launchpad.net/~afedorova
.. _`Dmitry Burmistrov`: https://launchpad.net/~dburmistrov
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`Sergey Kulanov`: https://launchpad.net/~skulanov
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Vitaly Parakhin`: https://bugs.launchpad.net/~vparakhin

.. _separate-mos-from-centos: https://github.com/openstack/fuel-specs/blob/master/specs/8.0/separate-mos-from-centos.rst
.. _public-access-to-packaging-ci: https://blueprints.launchpad.net/fuel/+spec/public-packaging-ci
.. _1348599: https://bugs.launchpad.net/fuel/+bug/1348599

.. [1] `Custom ISO yaml definition <https://github.com/fuel-infra/jenkins-jobs/blob/master/servers/custom-ci/10.0/custom.iso.yaml>`_
.. [2] `Zuul config for Fuel packages <https://review.fuel-infra.org/gitweb?p=fuel-infra/zuul-layouts.git;a=blob;f=servers/gate01-scc.fuel-infra.org/layout.yaml>`_
.. [3] `Chroots for building packages <https://github.com/openstack/fuel-main/blob/master/sandbox.mk>`_
.. [4] `Build ISO job definition <https://github.com/fuel-infra/jenkins-jobs/blob/master/servers/new-product-ci/8.0/all.yaml>`_
.. [5] `Build fuel rpm packages for CentOS7 <https://github.com/openstack/fuel-specs/blob/master/specs/8.0/build-fuel-rpm-packages-for-centos7.rst>`_
