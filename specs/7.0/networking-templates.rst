..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================
Networking templates support in Fuel
====================================

https://blueprints.launchpad.net/fuel/+spec/templates-for-networking

Fuel will be able to provide more flexible networking configurations via
templates.
Services will not be tied to networks 1:1. User will be able to create
any number of networks and map them to services (i.e. network roles).
User will be able to use different sets of network roles for different nodes
depending on node roles' sets for those nodes.

It is required to support both "new" and "old" networking strategies
in RPC. We need to support "old" one for environments based on earlier
releases and for environments configured via API.

Nova-Network is not supported for new environments, it is supported for old
ones only. Multi-rack is supported with templates only.


Problem description
===================

Fuel 6.1 has a very straightforward networking configuration procedure.
It's required for environment to use 4-5 networks depending on environment
configuration. Every service uses its own (predefined) network. Furthermore,
most networks are configured on all environment nodes no matter are they
required or not (with the exception of Public network for Fuel 5.1 and later).
Topology configuration is not flexible enough (e.g. subinterface bonding cannot
be used via API).


Proposed change
===============

Template solution is proposed to provide the following capabilities:
* Ability to have variable number of networks.
* Have a specific set of network roles.
* Ability to create network only in case relevant node role is present on the
  node.
* Ability to provide custom networking topologies (e.g. subinterface bonding).

Template solution details:
* REST API handler is added to load/cancel template for given environment
  (/clusters/x/network_configuration/template/).
* Template is applied during serialization if it was set for the env. So,
  template can be loaded/reloaded any time before deployment is started.
  Deployment serializer for networking will be selected with regard to the fact
  whether template was loaded or not.
* Template has priority over networking data in DB. If it is applied then
  DB data is ignored by networking serializer. If it is not applied then
  DB data is taken into account by networking serializer. Serizlization of
  other data is not affected.
* Astute.yaml for particular node has priority over template. If yaml was
  uploaded for particular nodes serialized data will be taken from there.
* Template allows to override networks (their quantity and parameters) and
  topology (to support complex cases which cannot be configured via API, like
  subinterface bonding). Network roles' set can be not equal to core set, it is
  up to user. No verification of network roles' set is provided at this stage.
  Network roles to networks mapping can be set for each node role
  independently.
* Template allows to use distinct network schemes for different node roles and
  for different node network groups. It also allows to use different NICs' sets
  for particular node network groups and particular nodes.

User should be able to use specific networks for swift & cinder traffic:
* Puppet manifests should support separated network roles for these services.
* Template solution will allow to use this separation for API side.

All the networking metadata which is now defined within networks should be
moved to network roles description:
* Every task description has section [network_roles] where the list of names of
  network roles required is declared.
* Descriptions of network roles are propagated to nailgun and include metadata
  which is required for serialization to orchestrator.


Alternatives
------------

N/A


Data model impact
-----------------

Coming soon.


REST API impact
---------------

Add "/clusters/x/network_configuration/template/" url to load/cancel template
for given environment.


Upgrade impact
--------------

Migration of schema and data must be provided to support previously created
environments and creation of environments with older releases. It should
include migration of existing releases and clusters.


Security impact
---------------

No additional security modifications needed.


Notifications impact
--------------------

N/A.


Other end user impact
---------------------

N/A

Performance Impact
------------------

No Nailgun/Library performance impact is expected.


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

Feature Lead: Aleksey Kasatkin

Mandatory Design Reviewers: Andrew Woodward, Sergey Vasilenko

Developers: Ivan Kliuk, Ryan Moe, Sergey Vasilenko, Stas Makar

QA: Alexander Kostrikov, Artem Panchenko


Work Items
----------

* Nailgun:
   a. Add network roles descriptions for core network roles
      (Estimate: 2d)
   b. VIPs allocation using network roles info
      (Estimate: 2-3d)
   c. Add API handler for loading/cancellation of template and serialization
      double-logic
      (Estimate: 2-4d)
   d. Add template serialization
      (Estimate: 5-8d)
   e. Add 'roles' section into 'network_metadata' (to get rid of
      internal_address, etc. in library)
      (Estimate: 2-3d)
   f. Add section [network_roles] into task descriptions
      (Estimate: 1-2d + library to provide info)
   g. Provide data for network verification tool in case of template
      (to be estimated)

* Network verification tool:
   a. Update verification for template solution.
      Under consideration. Update of nailgun part maybe enough.

* Library:
   a. Decoupling of networks and roles in manifests.
      (Estimate: ?)

* CLI:
   a. Add templates functionality
      (Estimate: 2-3d in total)


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/multiple-cluster-networks


Testing
=======

* Additional unit/integration tests for Nailgun.
* Additional System tests against a test environment with networking
  configuration set using a template.

* Some part of old tests of all types will become irrelevant and
  are to be redesigned.

Acceptance Criteria
-------------------

* Descriptions of network roles are propagated to nailgun and include metadata
  which is required for serialization to orchestrator.
* Every task description has section [network_roles] where the list of names of
  network roles required is declared.
* API handler is added to apply/cancel template for given environment.
* Template is applied during serialization if it was set for the env.
* Template has priority over networking data in DB. If it is applied DB data is
  ignored by networking serializer. If it is cancelled DB data is taken into
  account by networking serializer.
* Astute.yaml for particular node has priority over template. If yaml was
  uploaded for particular nodes serialized data will be taken from there.
* Template allows to override networks (their quantity and parameters),
  topology (to support complex cases which cannot be configured via API, like
  subinterface bonding). Network roles' set can be not equal to core set, it is
  up to user. No verification of network roles' set is provided at this stage.
* Template allows to use distinct network schemes for different node roles and
  for different node network groups. It also allows to use different NICs order
  for particular node network groups and particular nodes.


Documentation Impact
====================

The documentation should describe new networking architecture of Fuel,
networking templates workflow.


References
==========

https://blueprints.launchpad.net/fuel/+spec/templates-for-networking
