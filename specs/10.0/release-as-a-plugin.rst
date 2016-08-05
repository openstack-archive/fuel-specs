..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================
Release as a plugin
===================

Blueprint: https://blueprints.launchpad.net/fuel/+spec/release-as-a-plugin

As a Mirantis Engineer I want to express a Fuel Release as a Fuel Plugin so
that I could define, maintain and deploy various flavors of customized
OpenStack deployments in a clean isolated way, externalized from common
Fuel provisioning layer.

-------------------
Problem description
-------------------

The nailgun repo sill holds onto one of the remaining parts of the data model
the release fixture. This fixture is used to describe everything about the
deployment from the ground up and is where every change can possibly be
expressed.

----------------
Proposed changes
----------------

By moving the release fixtures ``openstack.yaml`` completely into the plugin
framework we opening road to following changes:

* To make ``fuel-library`` repo a plugin.
* It is possible to ship multiple openstack version release packages as
  each is its own plugin.
* Next steps allowing Fuel to have different releases bundled or no pre-bundled
  releases at all (lightweight version) are possible as well.


Web UI
======

Support of the case when there are ``no release`` is required.


Nailgun
=======


Data model
----------

Data model of Nailgun will be left intact except the changes in incoming
release configuration.


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

None

Plugins installation is not changing.


Plugins
=======

Plugin adapters
---------------

Fuel plugin adapter should now be able to understand new format of ``release:`` records declared in plugin ``metadata.yaml``.

Release loader should be integrated with plugin adapters.

Release package
---------------

If there is no relations to the existing releases are defined it is supposed that
plugin contains release data defined in ``releases:`` section.

``name`` attribute is a hallmark of release definition.

``is_hotpluggable`` flag is not available for the release plugins and will
be ignored.

Installation of releases should be performed before releases extension (existing plugins functionality) operations.

Example of ``metadata.yaml``:

.. code-block:: yaml

  fuel_version: ['10.0']
  licenses: ['Apache License Version 2.0']
  authors: ['Mirantis']
  homepage: 'https://github.com/openstack/fuel-plugins'
  groups: []

  releases:
   -name: 'ExampleRelease'                      #required
    description: 'Example Release Description'  #required
    operating_system: 'ubuntu'                  #required, or its alias "os"
    version: '0.0.1'                            #required

    networks_path: ubuntu-10.0/metadata/networks.yaml
    volumes_path: ubuntu-10.0/metadata/volumes.yaml
    roles_path: ubuntu-10.0/metadata/roles.yaml
    network_roles_path: ubuntu-10.0/metadata/network_roles.yaml
    components_path: ubuntu-10.0/metadata/components.yaml

    attributes_path: ubuntu-10.0/attributes/attributes.yaml
    vmware_attributes_path: ubuntu-10.0/attributes/vmware.yaml
    node_attributes_path: ubuntu-10.0/attributes/node.yaml
    nic_attributes_path: ubuntu-10.0/attributes/nic.yaml
    bond_attributes_path: ubuntu-10.0/attributes/bond.yaml

    graphs_path:
      - ubuntu-10.0/graphs/deployment_graph.yaml
      - ubuntu-10.0/graphs/provisioning_graph.yaml
      - ubuntu-10.0/graphs/deletion_graph.yaml
      - ubuntu-10.0/graphs/network_verification_graph.yaml

    deployment_scripts_path: deployment_scripts/
    repository_path: repositories/ubuntu


Deprecation
-----------

``modes`` release parameter is deprecated and will be removed in further versions.

``tasks.yaml`` no further supported.


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
* Add to old Fuel releases ability to ignore releases records of the new version.

Dependencies
============

None

-----------
Testing, QA
-----------

* Manual testing



Acceptance criteria
===================

* It is possible to deploy configuration with specific set of plugins and
  packages.
* It is possible to perform only discover/provision and manage
  HostOS + underlay storage and networking.
* Vanilla Fuel 9.1 installation is possible without and release definition -
  only provisioning layer is in, expecting user to add releases.


----------
References
----------

None
