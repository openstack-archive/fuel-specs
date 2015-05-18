..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================================
Support of clean separation of dedicated storage networks in Fuel
=================================================================

https://blueprints.launchpad.net/fuel/+spec/fuel-storage-networks

As a deployment engineer, I want to create clean segregation of storage
networks so that network bandwidth can be maximally utilized.


Problem description
===================

Both Swift and Ceph now require two storage segments not one.

For Ceph you have a "public" network, this is the network by which RADOS
clients will reach OSD (monitors use this network as well) and replication
network which is used for OSDs to talk to each other. Latest Swift has
introduced this concept as well with the Storage network proxy to object
servers and a replication network used by all background anti-entropy
processes.

We are currently mapping one of these network segments in Ceph (ceph/public) to
management network, which is not necessarily the right thing to do as
storage/public Ceph networks are high bandwidth network segments. We need to
be able to cleanly segregate these various storage networks away from the
management network. Network named 'storage' now carries replication traffic
of both Ceph and Swift. It should be split up into two different network roles.

Also required to secure the traffic between the nodes - especially with Swift
where the rsync traffic is not secure.


Proposed change
===============

https://docs.google.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4/edit#


Alternatives
------------

TBD


Data model impact
-----------------

TBD


REST API impact
---------------

New network roles description will be provided via API. Format of the
description is already set in flexible networking. Only particular network
roles will be added/modified/deleted.


Upgrade impact
--------------

Migration of schema and data must be provided to support previously created
environments and creation of environments with older releases. It will be done
within flexible networking feature.


Security impact
---------------

N/A


Notifications impact
--------------------

None


Other end user impact
---------------------

N/A


Performance Impact
------------------

No Nailgun/UI performance impact is expected.
Library performance impact is to be estimated.


Other deployer impact
---------------------

N/A


Developer impact
----------------

N/A


Implementation
==============

Assignee(s)
-----------

Feature Lead:

Mandatory Design Reviewers: Andrew Woodward, Sergey Vasilenko

Developers: Aleksey Kasatkin, Sergey Vasilenko, Ivan Kliuk

QA: Igor Shishkin


Work Items
----------

* Library:
   a. Separation of network roles in manifests.
      (Estimate: ?)

* Nailgun:
   a. Provide description for new network roles in Release attributes.
      (Estimate: 2-3d + QA time)


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/granular-network-functions


Testing
=======

* Additional System tests against a test environment with altered
  storage network roles to networks mapping, networks to interfaces mapping.

* Some part of old tests will become irrelevant and has to be redesigned.

Acceptance Criteria
-------------------

* Separate network roles should be available for storage services:
  ceph/replication, ceph/public, swift/replication, swift/public.

* Should we have separate swift/rsync network role?

* Particular network roles are available when corresponding services
  (ceph, swift) are configured.

* ceph/replication network role should only be available for nodes with ceph
  node role.

* swift/replication network role should only be available for nodes with
  swift node role.

* Should we have separate cinder/management and cinder/iscsi network roles?


Documentation Impact
====================

The documentation should describe new network roles separation in Fuel,
changes in network roles configuration process in UI.


References
==========

https://blueprints.launchpad.net/fuel/+spec/fuel-storage-networks

https://docs.google.com/document/d/1QVoexrDF_MS92IZd4jnwPWQDxTAWMzUUrcMyu8VjGF4/edit#
