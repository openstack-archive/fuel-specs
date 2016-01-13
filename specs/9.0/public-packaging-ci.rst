::

  Copyright 2016 Mirantis Inc.

  This work is licensed under a Creative Commons Attribution 3.0
  Unported License.
  http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Setup initial infrastructure for public packaging CI
====================================================

Create public packaging CI to provide tested Linux packages (DEB/RPM).

Problem Description
===================

Most Linux distributions using package managers to install software, but
at the moment there is no any upstream packaging workflow.

We need create public infrastructure for building, testing, and
publishing packages for upstream OpenStack projects.

Proposed Change
===============

Setup set of servers for packaging CI:

* One server for Zuul (VM)
* One server for Jenkins master (VM)
* One Jenkins slave for publishing packages (VM)
* One or more Jenkins slave for package building (HW)
* One or more Jenkins slave for install testing (HW)
* One or more Jenkins slave for system tests (HW)

Zuul, Jenkins master and publishing host must be public available, other
nodes (jenkins slaves) not need to be world-wide accessible.

Public available servers should have DNS-names in public zone.

Access restrictions should permit:

* Access to all hosts by SSH for management purposes, and also for connectivity
  Jenkins master to slaves. (Authentication/autorization source?)
* Access from Jenkins master to Zuul by TCP port 4730 (Gearman)
* Access all three public available hosts by HTTP/HTTPS (Web-interfaces and
  package repositories). (Authentication/autorization source for Web-interfaces?)

Services must be deployed by using existing Puppet manifests.

Alternatives
------------

To completely isolate public packaging CI from Mirantis services, it's
possible to use hardware nodes for all servers, and not use private
virtualization infrastructure for public hosts.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
 `Aleksander Evseev <https://launchpad.net/~aevseev-h>`_

Work Items
----------

* order required servers from IT services
* deploy services using Puppet manifests with corresponding roles
* check connectivity to hosts and between hosts
* prepare and deploy Jenkins jobs
* configure Zuul pipelines

Impact
======

Resources
---------

Virtual machines:

* Zuul: 2 CPU, 4 GB RAM, 100 GB HDD
* Jenkins master 2 CPU, 4 GB RAM, 100 GB HDD
* publishing host: 2 CPU, 2 GB RAM, 500+ GB HDD
* logging host: 1 CPU, 512 MB - 1 GB RAM, 100+ GB HDD (???)

Hardware (physical) servers:

* for package building: 8 Cores, 32 GB RAM, 50+ GB HDD
* for install testing: 8 Cores, 32 GB RAM, 20+ GB HDD
* for system tests: 8 Cores, 32 GB RAM, 1500+ GB HDD

Three "white" IP addresses with DNS names assigned to:

* Zuul (DNS name?)
* Jenkins master (DNS name?)
* Publishing host (DNS name?)
* Logging host (DNS name?) (???)

Daily routines
--------------

* Monitoring (?)
* Backup (?)

Public interfaces
-----------------

There will be three new Web-interfaces:

* Jenkins' web interface
* Zuul's status page
* Package repositories
* Logs and artifacts from build and test jobs (???)

Zuul posts to Gerrit links:

* to itself when jobs are queued but not started (i.e. not having build number)
* to logging host when there is any result (???)
* to builds of Jenkins jobs when there is any result (or ???)

Release process
---------------

None

Development process
-------------------

Package maintainers should take into account tests results.

QA process
----------

None

Documentation
-------------

None

Dependencies
============

None
