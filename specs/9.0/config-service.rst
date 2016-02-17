..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================
Configuration Service
=====================

https://blueprints.launchpad.net/fuel/+spec/configuration-service

This document is a description of architecture of Configuration Service.
You can find earlier discussion in original mailing list thread [#dec_sers]_,
brainstorm summary document [#ext_sers_bs]_, discussion on Solar channel
[#solar_sess]_ and Solar workshop minutes [#sol_ws]_.

--------------------
Problem description
--------------------

Configuration Service aims at providing a consistent way of storing,
versioning, retrieving and updating all configuration values for one big entity
(in Fuel context it is an environment).

User stories
============

Pluggable data sources
----------------------

Cloud operator wants to fetch settings from different data source. Currently
Fuel supports only itself (Nailgun database) as a data source. There is a
demand for using external Puppet Master or LDAP as a source for all (some)
configurable values.

Isolated configuration description for deployment modules
---------------------------------------------------------

Deployment module author wants to describe data required for one's module in a
clear way separately from other modules as opposed to changing Nailgun code.
Different deployment modules should be allowed to consume the same data
consistently.

Upgradable cluster configuration
--------------------------------

Cloud operator wants to deploy new version of cluster (set of deployment
modules, e.g. OpenStack) with minimal required (or none at all) changes to
source data.

Overridable configuration values
--------------------------------

Cloud (maintenance) operator wants to override certain values directly on any
level. For example, to check if one rack can use a different gateway address or
if one node should use a different block storage driver.

Configuration values overridable by plugins
-------------------------------------------

Plugin author wants to override (recalculate) certain config values for a
cluster. For example, one might want to provide OVS plugin that would change
network provider to OVS and keep all other settings in place.

Hierarchical data
-----------------

Component author wants to define certain values on different levels of
deployment hierarchy (cluster, datacenter, rack/group, node, etc). To avoid
locking in on one deployment architecture levels should be
configurable.

Current state of affairs
========================

Currently Nailgun has hardcoded set of serializers that are called in some
predefined order. The result is some hash that is then modified by every
plugin. This option doesn’t cover any of listed user stories:

* Nailgun is the only source of information, there is no way to add another
  source;
* every deployment module is disconnected from its data: module itself lives in
  library while serializer has to be written in Nailgun;
* after deployment cluster configuration is stored only as a YAML blob in
  database, so any changes that are required during upgrade have to be done on
  the whole blob at once which is not maintainable;
* overrides are implemented in unmanageable way using a separate YAML file that
  is dynamically put directly to the node;
* plugins override values in config as a black boxes, no way of knowing which
  values will be overrided and where did certain value came from without
  examining them;
* while there are several levels of hierarchy (cluster and node at least) you
  cannot set values for parameters on different levels and change their
  hierarchy.

----------------
Proposed changes
----------------

We propose to create a new API on top of Solar database layer that will provide
necessary abstractions to read and write configuration information for
clusters. Configuration Service will allow components (see definition below) to
register themselves or be registered as a part of installation process of the
component, provide strictly defined versioned schema for both provided and
consumed values. For each environment these schemas will be filled with
concrete values from different sources and each consumer (deployment task now,
but in future it could be any other component that needs to exchange metadata,
e.g. UI or API service) will get requested values in consistent manner.

Web UI
======

This blueprint doesn't cover any changes in Web UI although it enables us to
provide user with advanced settings configuration.

Nailgun
=======

Data model
----------

No changes in data model in Nailgun.

REST API
--------

No changes of Nailgun API.

Orchestration
=============

Instead of receieving deployment information via Astute, Puppet on nodes will
directly query Config Service for it.

RPC Protocol
------------

Instead of pushing deployment information to Astute Nailgun will push it to
Config Service.

.. note::
    TODO: add concrete changes to RPC protocol

Fuel Client
===========

No changes.

Plugins
=======

Plugins are not affected by this change. This change enables them to provide
changes to Config Service instead of plugging into Serializers infrastructure.

Fuel Library
============

Hiera backend will be changed to fetch data directly from Config Service. No
other changes in Fuel Library are covered by this blueprint.

------------
Alternatives
------------

Solar
=====

Solar stores configuration in versioned storage, provides functionality to
store hierarchical data and is planned to have ways to fetch data from external
sources, but it doesn’t provide necessary abstractions to user. For example,
you can have resources linked with each other in hierarchical fashion, but you
cannot just ask "Give me a version of this resource for this node" since user
has to know what’s “node” level and how is resource name constructed for it.
Configuration Service and Solar compliment each other in a way that the former
creates Data Resources in Solar with metadata values collected from Data
Sources. Configuration Service will handle hierarchy, keep the catalog of Data
Sources and poll them on behalf of Solar. Essentially, Configuration Service
will provide API for creating Data Resources in Solar.

--------------
Upgrade impact
--------------

.. note::
    TODO

---------------
Security impact
---------------

This change provides new API service that will expose environment data to
deployment modules.

.. note::
    TODO: Keystone integration?

--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

User will be able to change values either manually or programmatically using
Config Service API.

------------------
Performance impact
------------------

This change introduces new link in the chain of getting data to environment
nodes which might have impact on performance of deployment of OpenStack.

-----------------
Deployment impact
-----------------

New service will need to be deployed on Master node as a separate package. It
will require Postgres database set up and a directory for data resource
definitions repository.

----------------
Developer impact
----------------

.. note::
    TODO

---------------------
Infrastructure impact
---------------------

This change will produce new package that will need to be created on CI.

--------------------
Documentation impact
--------------------

Since Configuration Service will be accessible by user, interaction with it
should be covered in docs.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  yorik-sar

Work Items
==========

.. note::
    TODO

Dependencies
============

* This feature uses Solar database layer, so it needs Solar to be packaged and
  accessible.

------------
Testing, QA
------------

.. note::
    TODO

Acceptance criteria
===================

Fuel deploys OpenStack as before, but data flow from Nailgun to Puppet goes
through Config Service.

----------
References
----------

.. [#dec_sers] [openstack-dev] [Fuel][Fuel-Modularization] Proposal on
    Decoupling Serializers from Nailgun -
    http://lists.openstack.org/pipermail/openstack-dev/2015-October/077286.html

.. [#ext_sers_bs] Externalized Serializers in Fuel Brainstorm Summary -
    `<https://docs.google.com/a/mirantis.com/document/d/1bUS90ZQVVMw5okHzLFks0svLYjMGKxdGUbz87-0_>`_

.. [#solar_sess] https://etherpad.openstack.org/p/solar-sessions

.. [#sol_ws] https://etherpad.openstack.org/p/fuel-solar-workshop-poznan-jan-16
