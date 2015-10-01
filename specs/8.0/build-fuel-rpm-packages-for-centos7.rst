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
fixes from upstream (especially Linux kernel). Building fuel packages for
CentOS 7 is one of the steps towards using the latest stable release of the
operating system running on the master node (currently, CentOS 7).


----------------
Proposed changes
----------------

Use the same packaging workflow as we have for OpenStack projects:

#. Mirror the below fuel repos [1]_ to review.fuel-infra.org [2]_:

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

#. Periodically pull (~ 15 min) updates from upstream fuel repos [1]_
#. Separate packages specs from source code using schema::

        Project          Branch        Description
    -----------------  -----------   ------------------
    openstack/*          master       fuel source code
    openstack-build/*    master       fuel code specs

    for example:

        Project                        Branch        Description
    -------------------------------  -----------   ----------------------
    openstack/fuel-ostf                master       fuel-ostf source code
    openstack-build/fuel-ostf-build    master       fuel-ostf code specs

#. Build fuel packages from the code in [2]_


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

TBD: Since we are planning to completly switch to CentOS 7 and as the result
have the only CentOS 7 specs we need to discuss transition procedure:

* specs for CentOS 6 and CentOS 7 should be separated, for example on branch
  base or folder base.

* specs for CentOS 6 and CentOS 7 should be in the same file with `ifelse`
  approach, after complete switching we can remove it.


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
                                   +----+----+
                                   |         |
                                   | jenkins |
                                   |         |
                                   +----^----+
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

Related mirrors should be created in all location with the `base` path defined
below:

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

* Implement related changes to zuul-layouts configuration [3]_

* Implement related changes to jenkins-job-builder [4]_


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
.. [2] `review.fuel-infra.org <https://review.fuel-infra.org>`_
.. [3] `Zuul-layouts <https://review.fuel-infra.org/#/admin/projects/fuel-infra/zuul-layouts>`_
.. [4] `Jenkins job builder <https://github.com/fuel-infra/jenkins-jobs>`_
