..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
Separate MOS from Linux repos
=============================

https://blueprints.launchpad.net/fuel/+spec/separate-mos-from-linux

Problem description
===================

As a Cloud Operator I should be able to run OS updates as well as MOS updates
during Product Life cycle.
As a Cloud Operator I would like to know the packages from MOS and OS provider.
As a Cloud Operator I would like to have OS support contract as well as MOS
support.
As a Cloud Operator I would like to get security updates as fast as possible
independantly from OS Provider as well as from MOS.
As a Cloud Operator I should be able to see sources of OS and MOS packages.
As a Cloud Operator I should be able to see debug symbols of OS and MOS
packages.

To provide highest quality MOS should separate lifecycle OS and Cloud
lifecycle management. Meanwhile OS Updates shouldn't break MOS functionality
and vice versa. 

Proposed change
===============

Separate MOS mirrors and OS mirrors. This change will allow to
- differentiate packages installed by OS provider and MOS
- have different lifecycle management for OS packages and MOS packages

Nailgun should consume OS mirror as well as MOS mirror and have functionality
to create IBP file as well as cobbler profiler using OS and MOS mirror. [1]_

This separation creates additional challenges:
* MOS should introduce mirror for MOS packages with updates and security
repositories
* MOS should provide own SRU channel [2]_ that will be run on CI before
putting packages to updates
* MOS CI should run tests against OS SRU https://wiki.ubuntu.com/StableReleaseUpdates#Examples
* CI Infrastructure should mirror official OS mirrors to speed up CI operations
* CI should provide the list of vanilla packages consumed from OS Provider

This document proposes to modify the following parts of the Fuel build
system:

Local mirrors creation module
-----------------------------

Ubuntu part of local mirror creation module will be dropped.

Handling of one or several extra repositories added via EXTRA_DEB_REPOS
variable will be shifted from the local mirror building context to
Nailgun logic. [1]_

Packages building module
------------------------

Fuel DEB packages build routine will be dropped. Fuel DEB packages will be
consumed from the MOS mirror directly on master node. [1]_
Control files for Fuel DEB packages will be moved to the public MOS Gerrit
instance.

Explicit list of Fuel DEB packages is below:

* fencing-agent
* nailgun-mcagents
* nailgun-net-check
* nailgun-agent
* python-tasklib

Image-based provisioning (IBP) module
-------------------------------------

Ubuntu part of the IBP module will be dropped, all manipulations with
Ubuntu-based images will be shifted to the master node. [1]_

ISO assembly module
-------------------

ISO assembly module will be adjusted to exclude all parts mentioned above.


Alternatives
------------

There is no alternative to the repositories separation approach due to
considerations related to distribution policies of major OS vendors.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Other deployer impact
---------------------

Changes described in this document allow to increase product flexibility,
by making possible to choose an operating system and install it independent
of MOS.

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Vitaly Parakhin <vparakhin@mirantis.com>

Mandatory Design Reviewers:
  Roman Vyalov <rvyalov@mirantis.com>
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>

QA:
  Artem Panchenko <apanchenko@mirantis.com>
  Denis Dmitriev <ddmitriev@mirantis.com>

Work Items
----------

* Create local Ubuntu mirrors for CI purposes (OSCI)
* Change Fuel make system to exclude Ubuntu packages from ISO (OSCI)
* Change process for building of Fuel DEB packages (OSCI)
* Create DEB repositories for MOS updates and security packages (OSCI)
* Create CI jobs for testing against Ubuntu SRU (DevOps)

Dependencies
============

None

Testing
=======

As this document introduces structural changes to the ISO composition and
structure of Fuel mirror, testing procedure must reflect the updated
workflow for deploying Ubuntu environments described in this blueprint. [1]_

<TBD> with QA

Documentation Impact
====================

None

References
==========

.. [1]  `Fetch Ubuntu Packages as external source <https://blueprints.launchpad.net/fuel/+spec/downloadable-ubuntu-release>`_
.. [2]  `Ubuntu SRU procedure <https://wiki.ubuntu.com/StableReleaseUpdates#Examples>`_