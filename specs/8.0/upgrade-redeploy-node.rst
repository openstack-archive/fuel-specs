..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Upgrade and Redeploy Node with Data Preservation
================================================

https://blueprints.launchpad.net/fuel/+spec/upgrade-redeploy-node

Upgrade of OpenStack cluster includes installation of new versions of
software components, update of their configuration in certain cases and
restating services on some or all nodes in the cluster.

All these tasks are a part of deployment procedure performed by Fuel
installer. We use Fuel to repeat deployment procedure with certain
modifications to upgrade nodes in the cluster.

Stateless services keep their data on local disks of nodes. How this
data is organized and managed depends on a role(s) of the node in the
cluster.

For in-place upgrade, we must to ensure that the stateful data remains
intact on the node during the upgrade procedure (i.e. redeployment of
the node)

--------------------
Problem description
--------------------

Partition Preservation feature (PP) allows to reinstall node with existing
partition scheme. In its current implementation, it is low-level feature
that requires upfront configuration of node's disks before provisioning.

While it is flexible enough to preserve all kinds of data, PP has the
following problems:

* ``fuel-agent`` ignores actual partitions layout on the node, which could
  cause inconsistent results of provisioning in case if something changed
  in partitions schema.

* For different roles, different file systems and/or parititions must be
  preserved through the upgrade procedure. Additionally, if combination of
  roles is installed on a node, all preservation requirements must be
  satisfied.

* Roles can be modified/added by plugins. Plugins must provide information
  about which data have to be preserved.

----------------
Proposed changes
----------------

* Add driver to ``fuel-agent`` which will recognize the existing partition
  schema on devices and make changes to it according to the input metadata,
  taking PP flags into account to calculate sizes of partitions in the new
  layout.

* Use the driver above by adding certain parameter to call to ``fuel-agent``
  in Astute if PP flag is set.

* Set PP flag automatically for certain filesystems/volumes, depending on the
  role(s) of the node, when node is being reinstalled in the environment being
  upgraded. For example, for ``controller`` role, volumes ``mysql`` and
  ``logs`` shall be marked to keep data.

Web UI
======

None.

Nailgun
=======

General changes to the architecture, tasks and encapsulated business logic
should be described here.

Data model
----------

Roles definition must include a field to define volumes subjected for PP.
Proposed name for the field is ``data_volumes``. This fiels shall contain
names of volumes where the role stores user-bound data.


REST API
--------

None.

Orchestration
=============

RPC Protocol
------------

To initiate appropriate driver in ``fuel-agent``, additional parameter shall
be passed in calls to the agent via MCollective. This parameter must be added
depending on a context of RPC call that initiates re-deployment for upgrade.

Fuel Client
===========

None.

Plugins
=======

As plugins can define roles since 7.0 release, they should also specify
``data_volumes`` field for any role they create in role's metadata.

Fuel Library
============

For all the standard roles, some changes would be done in fuel-library to
protect data from destructive actions by Puppet manifests. For instance, in
Ceph module, we add checks to ensure that ``ceph-deploy prepare`` is not
executed for devices identified as OSD devices in ``prepared`` status.

The following modifications shall be made in modules:

* ``mysql`` module:

* ``mongodb`` module:



------------
Alternatives
------------

External logic can achieve the same results:

* match node and roles assigned to it

* configure PP on volumes based on matched roles via Fuel API

However, this logic will have to follow all the changes made to roles in Fuel,
i.e. added roles, changed roles, etc.

External logic will have difficulties handling plugin-defined roles: plugins
will need to expose their ``data_volumes`` somehow (via some API).

--------------
Upgrade impact
--------------

This change will allow for in-place upgrade without changing or moving data
of the existing data set.

Database migration scripts shall be added to Nailgun ``alembic`` repository
to add ``data_volumes`` field to role schema. Default value for the field
is empty list.

Per-role data transformation in the script will set value of the
``data_volumes`` field for existing roles.

---------------
Security impact
---------------

PP feature might pose additional security threat as it disables mechanisms
that clean up data. Potentially, user data could be accidentally exposed due
to that feature.

Setting PP automatically for certain API calls and hiding it from API used
might be beneficial to the level security overall.

--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

None.

------------------
Performance impact
------------------

Preservation of existing data set might be beneficial for performance of
deployment engine due to the fact that data won't be moved around in the
cluster.

From fuel-library standpoint, certain actions required to adopt the existing
data set, especially possible consistency checks, etc, could reduce visible
performance of the deployment engine.

Overall effect of this change on performance of the deployment is TBD.

-----------------
Deployment impact
-----------------

Role-based PP for upgrade/reinstallation is transparent for deployment
engineer. No additional actions required to preserve user-bound data upon
upgrade/redeployment.

----------------
Developer impact
----------------

None.

--------------------------------
Infrastructure/operations impact
--------------------------------

System tests for upgrade feature shall be extended to include verification of
how PP works depending on a role of the node being upgraded.

--------------------
Documentation impact
--------------------

Documentation of upgrade procedure must include a list of volumes that are
automatically preserved.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
    fuel-octane-team

Other contributors:
    fuel-octane-team

Mandatory design review:
    fuel-core-team


Work Items
==========

Following work items were identified:

* Automatically set PP flag (``keep_data``) when volumes table is generated,
  based on the node's role(s).

* Update ``ceph`` module in fuel-library.

* TBD

Dependencies
============

* Depends on Partition Preservation feature (PP), which was implemented in
  Release 7.0: https://blueprints.launchpad.net/fuel/+spec/partition-preservation

* Depends on ``fuel-agent`` driver capabilities:
  https://blueprints.launchpad.net/fuel/+spec/volume-manager-refactoring


------------
Testing, QA
------------

Testing of the feature must include verification that pre- and post-deployment
data set have no changes.

Acceptance criteria
===================

TBD

----------
References
----------

