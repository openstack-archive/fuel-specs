..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Release description in fuel library
===================================

https://blueprints.launchpad.net/fuel/+spec/release-description-in-fuel-library

Now release is defined both in fuel-web and fuel-library that are required
to be in sync. Also it is not possible to deliver new release specification
the other way than updating Fuel library and database fixture.


-------------------
Problem description
-------------------

We have a problem, related to the Fuel releases. Supported releases
specification (openstack.yaml) is coupled with nailgun codebase and
implementation. There is no clear workflow to provide new release to the
existing fuel distribution.


----------------
Proposed changes
----------------

Web UI
======

None


Nailgun
=======

* Release description (openstack.yaml) should be moved to Fuel library

* Release description should be converted to the DB-agnostic format and
  separated to the different files

* Library -> Fuel sync procedure should be updated to sync release before the
  library deployment graph for given release is synced.

* ``deployment_tasks.yaml`` should be removed from fixtures.

Admin network including IP address, network range and network group records
and should support templating with config variables.

Fuel graph execution business logic is heavily relying on default deployment
tasks for all so this configuration could be considered as highly coupled with
current Fuel version.

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

None


Plugins
=======

None


Fuel Library
============

New folder ``deployment/openstack_metadata`` should be created In Fuel Library
repository. In the root of this folder there is a common shared configuration
across the introduced releases.

Also it contain ``release folders`` that are detected by presence of properly
defined ``release.yaml`` inside. This definitions will be merged over the
root shared configuration.

Also it is possible to define ``schemas`` folder that containing custom json
schemas to validate data field
content for release as well as for according plugins and cluster data fields.

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

------------
Alternatives
------------

None


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

(TBD) Custom notification fixture could be defined for release.


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
