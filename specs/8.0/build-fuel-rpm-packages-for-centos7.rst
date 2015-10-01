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

We have to waste our resources each time we need to backport security or bug
fixes from upstream (especially Linux kernel). Building fuel packages
(see `table`_) for CentOS 7 is one of the steps towards using the latest stable
release of the operating system running on the master node
(currently, CentOS 7).

.. _table:

**Table 1.** The list of stackforge repositories and relevant fuel packages

+--------------------+-----------------------------+
|    Repo-name       |       RPM packages          |
+====================+=============================+
| fuel-agent         | - fuel-agent                |
+--------------------+-----------------------------+
| fuel-astute        | - ruby21-rubygem-astute     |
|                    | - ruby21-nailgun-mcagents   |
|                    | - nailgun-mcagents          |
+--------------------+-----------------------------+
| fuel-library       | - fuel-dockerctl            |
|                    | - fuel-ha-utils             |
|                    | - fuel-library8.0           |
|                    | - fuel-migrate              |
|                    | - fuel-misc                 |
|                    | - fuel-notify               |
|                    | - fuel-rabbit-fence         |
+--------------------+-----------------------------+
| fuel-main          | - fuel                      |
+--------------------+-----------------------------+
| fuel-nailgun-agent | - nailgun-agent             |
+--------------------+-----------------------------+
| fuel-octane        | - fuel-octane               |
+--------------------+-----------------------------+
| fuel-ostf          | - fuel-ostf                 |
+--------------------+-----------------------------+
| fuel-web           | - fencing-agent             |
|                    | - fuel-package-updates      |
|                    | - fuel-provisioning-scripts |
|                    | - fuelmenu                  |
|                    | - fuel-nailgun              |
|                    | - nailgun-net-check         |
|                    | - shotgun                   |
+--------------------+-----------------------------+
| python-fuelclient  | - python-fuelclient         |
+--------------------+-----------------------------+



----------------
Proposed changes
----------------

#. Create additional workflow (on packaging-ci) for building fuel [1]_ rpm
   packages for CentOS 7

#. Update fuel packages SPECs (if needed) to support both (CentOS 6 and 7)

#. Put packages on mirrors in all location with `base path`
   defined below:

  +----------+---------------------------------------+
  | OS Dist. |          URI path on mirrors          |
  +==========+=======================================+
  | CentOS 6 | mos-repos/centos/mos8.0-centos6-fuel  |
  +----------+---------------------------------------+
  | CentOS 7 | mos-repos/centos/mos8.0-centos7-fuel  |
  +----------+---------------------------------------+


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

Fuel packages naming schema must correspond to those that is described in
specification `separate-mos-from-centos`_


------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

Fuel packages naming schema must correspond to those that is described in
specification `separate-mos-from-centos`_


----------------
Developer impact
----------------

There is no impact on developing process, since packages for both CentOS 6
and CentOS 7 will be built and appeared in mirrors on the same gerrit events


--------------------------------
Infrastructure/operations impact
--------------------------------

* Expected jobs workload (building/publishing) will be double increased,
  because of triggering two sets of jobs (for CentOS 6 and 7) in parallel

* No additional branches required, all packages will be built from the master
  branch

* No additional HW resources required, since build process of fuel packages
  lasts no longer then max 2 minutes and the size of a package < ~10Mb

* Additional CI jobs should be created to build fuel packages for CentOS 7

* Since we have limitation `one Zuul one Gerrit`, we need additional Zuul
  instance, which will `listen` to openstack gerrit (see pic. 1)

* Since we have limitation `one Zuul one Jenkins`, we need to share `Gearman`
  instance between two `Zuuls` (see pic. 1)

::


  +---------------------+                 +---------------------+
  |                     |                 |                     |
  |       +-------------+-------+         |       +-------------+-------+
  |       |   build OpenStack   |         |       |                     |
  +-------+   packages + deps   |         +-------+  build fuel packages|
          |         jobs        |                 |        jobs         |
          +---------^-----------+                 +----------^----------+
                    |                                        |
                    +-------------------+--------------------+
                                        |
                                 +------+-------+
                                 |              |
                                 |   jenkins    |
                                 | packaging-ci |
                                 |              |
                                 +------^-------+
                                        |
                        +---------------+
                        |
          +---------------------------+      +---------------------------+
          |Zuul01 +-----v-----+       |      |Zuul02                     |
          |       |           |       |      |                           |
          |       |  Gearman  <-----------+  |                           |
          |       |           |       |   |  |                           |
          |       +-----------+       |   |  |                           |
          |       +-----------+       |   |  |       +-----------+       |
          |       |           |       |   |  |       |           |       |
          |       |  Gerrit   |       |   +----------+  Gerrit   |       |
          |       |    +      |       |      |       |     +     |       |
          |       +-----------+       |      |       +-----------+       |
          +---------------------------+      +---------------------------+
                       |                                   |
                       |                                   |
                       |                                   |
                       v                                   v
              review.fuel-infra.org              review.openstack.org

                            Picture 1 - Zuul schema


--------------------
Documentation impact
--------------------

All infrastructure changes should be documented


--------------------
Expected OSCI impact
--------------------

Related mirrors should be created/rsynced to all location with the `base`
path defined below:

+----------+---------------------------------------+
| OS Dist. |          URI path on mirrors          |
+==========+=======================================+
| CentOS 6 | mos-repos/centos/mos8.0-centos6-fuel  |
+----------+---------------------------------------+
| CentOS 7 | mos-repos/centos/mos8.0-centos7-fuel  |
+----------+---------------------------------------+

Fuel packages naming schema must correspond to those that is described in spec
`separate-mos-from-centos`_


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Sergey Kulanov`_

CI-team:
  `Alexander Evseev`_


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

* CI builds Fuel packages for CentOS 7, based on the existing packages specs

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
.. _Stackforge namespace retirement: https://wiki.openstack.org/wiki/Stackforge_Namespace_Retirement_

.. [1] `Fuel stackforge repos <https://github.com/stackforge/>`_
.. [2] `Zuul-layouts <https://review.fuel-infra.org/#/admin/projects/fuel-infra/zuul-layouts>`_
.. [3] `Jenkins job builder <https://github.com/fuel-infra/jenkins-jobs>`_
