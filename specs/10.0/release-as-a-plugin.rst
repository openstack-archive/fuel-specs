..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================
Release as a plugin
===================

Blueprint: https://blueprints.launchpad.net/fuel/+spec/release-as-a-plugin

As a deployment Engineer I want to express a Fuel Release as a Fuel Plugin so
that I could define, maintain and deploy various flavors of customized
OpenStack deployments in a clean isolated way, externalized from common
Fuel provisioning layer.

-------------------
Problem description
-------------------

The nailgun repo still holds onto one of the remaining parts of the data model
the release fixture. This fixture is used to describe everything about the
deployment from the ground up and is where every change can possibly be
expressed.

----------------
Proposed changes
----------------

By moving the release fixtures ``openstack.yaml`` completely into the plugin
framework we're opening road to following changes:

* To make ``fuel-library`` repo a plugin.
* It is possible to ship multiple Openstack version release packages as
  each in its own plugin.
* Next steps allow Fuel to have different releases bundled or no pre-bundled
  releases at all (lightweight version) are possible as well.


Web UI
======

Support of the case when there are ``no release`` is required.

Basic releases will be shipped as pre-installed plugins. It become possible to
uninstall them completely leaving Fuel without releases at all.

UI should support case when no releases installed, not allowing to pass in
cluster creation wizard further that a release selection or not allow to start
this wizard at all.

Message about what to do if no releases are installed should be displayed to
user.


Nailgun
=======


Data model
----------

Data model of Nailgun will be left intact except the changes in incoming
release configuration.

Release name version is determined in metadata with following fields:

.. code-block:: yaml

  releases:
   -name: 'ExampleRelease'                      #required
    description: 'Example Release Description'  #required
    operating_system: 'ubuntu'                  #required, or its alias "os"
    version: '0.0.1'                            #required

Plugin name and version should be identical to the release name and version (TBD, better ideas?)

Now it is possible to uninstall release package, but not possible to detach
release model from cluster model. This case should be handled properly (TBD).

REST API
--------

It should be possible to run command, installing releases from a given path.

Orchestration
=============


RPC Protocol
------------

None


Fuel Client
===========

Plugins installation is not changed.


Plugins
=======

Plugin adapters
---------------

Fuel plugin adapter should now be able to understand new format of ``release:``
records declared in plugin ``metadata.yaml``.

New release loader should be integrated with plugin adapters.

Release package
---------------

If there are no relations to the existing releases are defined it is supposed
that plugin contains release data defined in ``releases:`` section with
``name`` attribute is a hallmark of release definition.

``is_hotpluggable`` flag is not available for the release plugins and will
be ignored.

Release could contain any data matching FPB and Fuel validation schema, without
any restriction related to the OS version or bundling something other than OS
into the release plugin.

To make updates/upgrades simpler, it's supposed that plugin could contain
releases or releases extensions, but not both of them. FPB validator should
provide warning if more than one release is defined or plugin name is different
from the release name.

Example of ``metadata.yaml``:

.. code-block:: yaml

  ...

  name: 'ExampleRelease'
  version: '10.0.0'
  package_version: '5.0.0'       # plugin package version

  releases:
    - name: 'ExampleRelease'                      #required
      description: 'Example Release Description'  #required
      operating_system: 'ubuntu'                  #required, or its alias "os"
      version: '10.0.0'                           #required

      # base_release_path allows to define template from which all data tree
      # will be inherited by overriding keys

      base_release_path: ubuntu-10.0.0/_base.yaml

      networks_path: ubuntu-10.0.0/metadata/networks.yaml
      volumes_path: ubuntu-10.0.0/metadata/volumes.yaml
      roles_path: ubuntu-10.0.0/metadata/roles.yaml
      network_roles_path: ubuntu-10.0.0/metadata/network_roles.yaml
      components_path: ubuntu-10.0.0/metadata/components.yaml

      attributes_path: ubuntu-10.0.0/attributes/attributes.yaml
      vmware_attributes_path: ubuntu-10.0.0/attributes/vmware.yaml
      node_attributes_path: ubuntu-10.0.0/attributes/node.yaml
      nic_attributes_path: ubuntu-10.0.0/attributes/nic.yaml
      bond_attributes_path: ubuntu-10.0.0/attributes/bond.yaml

      graphs:
        - type: deployment
          tasks_path: ubuntu-10.0.0/graphs/deployment_graph.yaml

        - type: provisioning
          tasks_path: ubuntu-10.0.0/graphs/provisioning_graph.yaml

        - type: deletion
          tasks_path: ubuntu-10.0.0/graphs/deletion_graph.yaml

        - type: network_verification
          tasks_path: ubuntu-10.0.0/graphs/network_verification_graph.yaml

      deployment_scripts_path: deployment_scripts/
      repository_path: repositories/ubuntu-10.0.0/


Fuel Plugin Builder
-------------------

Should be able to check new release schema and files are linked as files and
folders paths.

Also it should provide appropriate warnings in case of deprecated syntax signs.

Plugins Package v5.0.0 will be supported starting from Fuel v9.1.0.
Appropriate validation should be defined.

Under the hood FPB will perform three operations:

* Data files discovery and loading making data tree from plugin files and
  rendered configuration templates.

  During processing of metadata file all attributes with *_path suffix will be
  considered as special one and processed using following conditions:

  * if ``some_key_path`` key is pointing to file or file-like object and it is
    possible to load data from it (YAML/JSON) key will be replaced to version
    without suffix ``some_key`` and data will be placed under this key in data
    tree.

  * if *_path key is pointing to folder like ``./release/fuel-10.0/``, it will
    be left intact.

  * if *_path key is a glob expression like release/graphs/*.yaml file search
    will be run.

    All found files matching glob will be merged into one list
    if they all have list root or their properties will be merged into dict
    if their root is dict. In the case of mixed root loader will fail.

    After data is merged as well as data from single file it will be placed
    under the key without ``_path`` suffix and original key will be removed
    from data tree.

* Data tree validation.

* Plugin building and packaging (identical to the current functionality)


Deprecation
-----------

``modes`` release parameter is deprecated and will be removed in further versions.

``tasks.yaml`` no further supported.

``fuel_version`` field currently is not processed by any business logic in
nailgun and should be deprecated.


Fuel Library
============

In perspective current Fuel Library should become a plugin.


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

It will be possible to ship release upgrades as a plugin.


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

Fuel Plugin Builder
===================

Fuel Plugin Builder validator should be able to validate new releases parameter
structure.


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

This feature is highly affects Fuel plugins and library developers.


---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Add documentation about fuel plugins format.


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


Work Items
==========

* Bump plugins version (TBD version number).

* Add to ongiong Fuel release support of new manifest version.

Dependencies
============

None

-----------
Testing, QA
-----------

* Manual testing

* Automated testing with fuel library as the release.

Acceptance criteria
===================

* It is possible to deploy configuration with specific set of plugins and
  packages.
* It is possible to perform only discovering/provision and manage
  HostOS + underlay storage and networking.
* Vanilla Fuel 9.1 installation is possible without any release plugins, but
  cluster creation is blocked with the UI notice, explaining situation.


----------
References
----------

None
