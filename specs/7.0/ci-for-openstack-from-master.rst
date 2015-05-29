..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
CI for Openstack from master
==========================================

https://blueprints.launchpad.net/fuel/+spec/ci-for-openstack-from-master

This specification describes CI for Openstack from master - from building
packages to releasing tested community ISO that will deploy latest
Openstack. Creating such process will benefit Openstack developers as well as
Fuel developers.


Problem description
===================

Every Openstack developer needs some tool to deploy latest code plus his
own work to perform functional testing. Fuel is the most sophisticated
Openstack deployment tool and a great candidate for such work. But it is always
one step back regarding Openstack releases it supports.


Proposed change
===============

Create CI analogous to our current CI for regular releases but targeted at
master branch of Openstack.


Alternatives
------------

None.


Data model impact
-----------------

None.


REST API impact
---------------

None.


Upgrade impact
--------------

None.


Security impact
---------------

None.


Notifications impact
--------------------

None.


Other end user impact
---------------------

None.


Performance Impact
------------------

None.


Plugin impact
-------------

None.


Other deployer impact
---------------------

Community users get Fuel ISOs with master Openstack.


Developer impact
----------------

Fuel developers need to monitor test results and continuously update
fuel-library to support master Openstack. For every OpenStack master
compatibility change in the Fuel code, a reasonable effort should be
dedicated to making that change backwards compatible with the
currently supported stable OpenStack version.

A new branch called "future" will be created in Fuel repositories. It
is acceptable to put an OpenStack master compatibility change in this
branch, iff the only way to ensure backwards compatibility is to
introduce a conditional statement with a check for specific OpenStack
release. Every time a change is merged to a "future" branch, the core
reviewer approving the change is responsible for rebasing the whole
"future" branch onto the current head of master branch of the
corresponding Fuel git repository.


Infrastructure impact
---------------------

Creating CI for master Openstack puts additional load on Jenkins masters and
slaves (`OSCI Jenkins`_, `Fuel Jenkins`_). The amount of load is comparable to
existing CI branches for releases.

New jobs will be created, similar to jobs for numbered releases. Existing jobs
will be not affected. Also it's necessary to create one additional type of
Jenkins jobs. Usually package is built when developer uploads and then submits
a change request. In case with master branch Openstack code is synchronized
with upstream daily via git (without CRs). Thus we need to perform daily builds
of Openstack packages. Jobs that perform this task are called autobuild-master
jobs.

A new kind of release appears: community ISO with master Openstack.


Implementation
==============

Assignee(s)
-----------

* Primary assignee, package build: `Alexander Tsamutali`_
* ISO build: `Alexandra Fedorova`_
* ISO testing with `fuel-qa`_: `Timur Nurlygayanov`_
* ISO testing with Tempest and Rally: `Artur Kaszuba`_


Work Items
----------

* Create branch "future" in Fuel repos.
* Create `OSCI Jenkins`_ jobs to build master branch of system packages,
  dependencies and Openstack.

  + master.mos.build-deb-request, master.mos.build-rpm-request
      Build Openstack packages after new PS was uploaded.
  + master.mos.build-deb-deps-request, master.mos.build-rpm-deps-request
      Build Openstack dependencies and system packages after new PS was
      uploaded.
  + master.mos.build-deb, master.mos.build-rpm
      Build Openstack packages after merge.
  + master.mos.build-deb-deps, master.mos.build-rpm-deps
      Build Openstack dependencies and system packages after merge.
  + master.mos.autobuild, master.mos.autobuild-deb, master.mos.autobuild-rpm
      Build Openstack packages every day.

* Create `OSCI Jenkins`_ jobs to copy packages to mirrors.

  + master.mos.publisher
      Publish built package in repository.

* Create `OSCI Jenkins`_ jobs to test packages.

  + master.mos.install-deb, master.mos.install-rpm
      Simple install test for packages built from PS.

* Create `Fuel Jenkins`_ jobs to build ISOs.
* Create `Fuel Jenkins`_ jobs to test ISOs.
* Release tested ISOs via fuel-infra.org_.


Dependencies
============

Related to task of supporting master Openstack in Fuel.


Testing
=======

Packages built with these jobs will be tested for installation
only. ISOs will be tested with most generic fuel-qa_ tests, Tempest
and Rally. Only ISOs that pass this test will be released on
fuel-infra.org_.


Documentation Impact
====================

None.


References
==========

None.


.. _`OSCI Jenkins`: http://osci-jenkins.srt.mirantis.net
.. _`Fuel Jenkins`: http://ci.fuel-infra.org
.. _`Alexander Tsamutali`: https://launchpad.net/~astsmtl
.. _`Alexandra Fedorova`: https://launchpad.net/~afedorova
.. _`Timur Nurlygayanov`: https://launchpad.net/~tnurlygayanov
.. _`Artur Kaszuba`: https://launchpad.net/~akaszuba
.. _fuel-infra.org: http://fuel-infra.org
.. _fuel-qa: http://git.openstack.org/cgit/stackforge/fuel-qa
