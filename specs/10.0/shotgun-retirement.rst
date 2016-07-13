======================
Shotgun replacement
======================

https://blueprints.launchpad.net/fuel/+spec/shotgun-retirement

Problem Description
===================

* It is not possible to limit a diagnostic snapshot content to
  particular nodes, dates and services

* Snapshot gathering is slow and requires quite a lot of space because
  it is suboptimal - gathering process is sequential, data in transit
  is not compressed.

* It is not possible to create a diagnostic snapshot when WebUI,
  Nailgun or Astute is broken.

Proposed Change
===============

The solution is to use existing tool which has already solved almost
all of the above problems - Timmy.

Alternatives
------------

* We could continue with shotgun improving it if necessary. This would
  require rewriting it.
* We could use one of existing 3rd party tools. There is no tool which
  covers the whole use case. LMA solutions are not inteded to collect
  configuration information, arbitrary command outputs etc. Generic
  solutions such as Ansible requires a lot of additional effort to
  make it do what we want.

Implementation
==============

Assignee(s)
-----------


Primary assignee:
  gkibardin

Mandatory design review:
  vkozhukalov

Work Items
----------

* Ensure Timmy default configuration produces snapshot with enough
  information.

* Add Timmy package to the master node.

* Make "generate snapshot" button use Timmy.

Impact
======

Resources
---------

No.

Daily routines
--------------

No.

Security
--------

No.

Public interfaces
-----------------

CI must be changed to adopt Timmy in order to be able to gather
diagnostic snapshots.

Release process
---------------

Additional action items for HCF and other milestones. Changes in deliverables.

Development process
-------------------

No.

QA process
----------

No.

Documentation
-------------

Documentation must be supplemented with a chapter devoted to Timmy
installation and usage and alternative tools to perform the diagnostic
snapshot gathering.

Dependencies
============

No.
