..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Release description in fuel library
===================================

https://blueprints.launchpad.net/fuel/+spec/release-description-in-fuel-library


-------------------
Problem description
-------------------

Now release specific data is defined both in fuel-web and fuel-library that
are required to be in sync. Also it is not possible to deliver new release
specification the other way than updating Fuel library and database fixture.

Also existing releases specification (openstack.yaml) is coupled with nailgun
codebase and implementation.

Also there is no clear workflow to provide new release to the existing fuel
distribution.


----------------
Proposed changes
----------------

Web UI
======

None


Nailgun
=======

* Release description ``openstack.yaml`` should be separated to multiple files
  and moved to Fuel library (see Fuel Library impact).

* Library -> Fuel sync procedure should be updated to sync release before the
  library deployment graph for given release is synced.

* ``deployment_tasks.yaml`` should be removed from fixtures and included as
  base tasks configuration in Fuel Library.


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

Following command should be added to the Fuel CLI:

``fuel rel --sync-metadata --dir METADATA_DIR``
``fuel2 release sync-metadata  --dir METADATA_DIR``

They will perform release information discovery and update.

During the update process there two cases - defined directory contain
``release.yaml`` and considered as the single release description.

If ``release.yaml`` is not defined in the root of the specified folder then
it will be considered as the multi-release definition and discovery/inheritance
mechanism will perform following steps:

1. Read all .yaml files in this folder and preserve them as the base metadata
   records. Empty files should be considered as not-existing.

2. Look for the sub-folders of the first level containing ``release.yaml``
   inside. Every folder of this kind is considered as the release definition.

3. For every release definition all .yaml (and .json?) files should be read.
   Empty files should be considered as not-existing.
   If there file with the same name is defined as base metadata merge
   should be performed following this set of rules:

3.1. If base file with metadata contain dict root all release-specific metadata
     will be merged to this root overriding existing properties.

3.2. If the file have list structure as root, all release specific records will
     be appended to this records.
     (TBD what is the expected behaviour is for the deployment engineers?)

3.3. If the base metadata file contain dict root and the release-specific
     metadata contains the list root (as vice versa) error should be raised.

3.4. If base metadata file is exists but the release-specific is not, or vise
     versa, only existing file should be taken as is, skipping merge process.

4. All resulting data should be combined to the single JSON structure with
   the content of ``release.yaml`` as root extended with
   ``filename: merged content``, for each metadata file.

5. Resulting data should be sent as POST request to the ``/api/v1/releases/``
   handler of Nailgun API.

Plugins
=======

Plugins could re-use code of ``sync-metadata`` CLI command and library file
schema to define release as the plugin.


Fuel Library
============

New folder ``deployment/openstack_metadata`` should be created In Fuel Library
repository. In the root of this folder there is a common shared configuration
across the introduced releases.

Also it contain ``release folders`` that are detected by presence of properly
defined ``release.yaml`` inside. This definitions will be merged over the
root shared configuration.

(TBD) Also it is possible to define ``schemas`` folder that containing custom
JSON schemas to validate data field content for release as well as for
according plugins and cluster data fields.

If schema file is not defined default validation is used. If do, then schema
validation is applying according in schema in file but all other validation
related to this field in Nailgun is applied.

deployment/
├── openstack_metadata/
    ├── deployment_tasks.yaml (common configuration)
    ├── components.yaml (common configuration)
    ├── ...
    ├── newton-10.0-ubuntu-16.0.4
        ├── release.yaml (release header, required)
        ├── attributes.yaml
        ├── components.yaml
        ├── network_roles.yaml
        ├── roles.yaml
        ├── volumes.yaml
        ├── node_attributes.yaml
        ├── nic_attributes.yaml
        ├── bond_attributes.yaml
        ├── vmware_attributes.yaml
        ├── deployment_tasks.yaml
        ├── schemas/
            ├── attributes.yaml
            ├── components.yaml
            ├── network_roles.yaml
            ├── roles.yaml
            ├── volumes.yaml
            ├── node_attributes.yaml
            ├── nic_attributes.yaml
            ├── bond_attributes.yaml
            ├── vmware_attributes.yaml
            ├── deployment_tasks.yaml
      ├── newton-10.0-...
          ├── release.yaml (release header, required)
          ├── ...

``fuel rel --sync-metadata --dir "$openstack_metadata"`` command (see the CLI
impact)should be added to the ``%post`` section of fuel-library spec before
``fuel rel --sync-deployment-tasks --dir "$taskdir"`` command, otherwise there
will be no point to attach deployment graph from Fuel Library.

------------
Alternatives
------------

Leave openstack.yaml in Fuel code.


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


Fuel Plugin Builder
===================

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

This feature is highly affects Fuel web, Fuel UI and Fuel library developers.
And Fuel-library repository management. By fact, all kind of developers who
are working on custom release implementation should be able to update
fuel-library.


---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Documentation for fuel-library should be updated.

Notes about recommended basic tasks structure with sync points should be added
as best practices recommendation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  ikutukov@mirantis.com

Other contributors:


Mandatory design review:
  bgaifulin@mirantis.com
  ikalnitsky@mirantis.com
  vkozhukalov@mirantis.com
  vkuklin@mirantis.com


Work Items
==========


Dependencies
============

None

-----------
Testing, QA
-----------

* Manual testing

* Custom release with all configuration field defined in library as well as
release with single or no config fields defined (except release.yaml) should
work.

* Validation should work.

* Multiple releases distinct by name and/or version should work.

Acceptance criteria
===================

* It should be possible provide arbitrary set of releases from library/

----------
References
----------

None
