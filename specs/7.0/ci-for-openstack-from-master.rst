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
fuel-library to support master Openstack. Exact procedure is out of scope of
this document.


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

Primary assignee: `Alexander Tsamutali`_


Work Items
----------

* Create `OSCI Jenkins`_ jobs to build master branch of system packages,
  dependencies and Openstack.
* Create `OSCI Jenkins`_ jobs to copy packages to mirrors.
* Create `Fuel Jenkins`_ jobs to build ISOs.
* Create `Fuel Jenkins`_ jobs to test ISOs.
* Release tested ISOs via fuel-infra.org_.
  

Dependencies
============

Related to: FIXME: specification about support for master Openstack in Fuel


Testing
=======

Packages built with these jobs will be tested for installation only. ISOs will
be tested with most generic fuel-qa_ tests. Only ISOs that pass this test
will be released on fuel-infra.org_.


Documentation Impact
====================

None.


References
==========

None.


.. _`OSCI Jenkins`: http://osci-jenkins.srt.mirantis.net
.. _`Fuel Jenkins`: http://ci.fuel-infra.org
.. _`Alexander Tsamutali`: https://launchpad.net/~astsmtl
.. _fuel-infra.org: http://fuel-infra.org
.. _fuel-qa: http://git.openstack.org/cgit/stackforge/fuel-qa
