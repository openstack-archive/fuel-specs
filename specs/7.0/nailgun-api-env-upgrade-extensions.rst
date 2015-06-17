..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================
API Extensions For Environment Upgrade
======================================

https://blueprints.launchpad.net/fuel/+spec/nailgun-api-env-upgrade-extensions

Certain aspects of side-by-side upgrade procedure outlined in `this blueprint
<https://blueprints.launchpad.net/fuel/+spec/upgrade-major-openstack-environment>`_
have to be performed on Fuel side, especially those operations that require
database modifications. We propose extensions to Nailgun API that facilitate
creation of special type of environment to serve as a replacement for original
environment targeted for upgrade.


Problem description
===================

During the upgrade procedure, we create an special environment that must
satisfy the following requirements:

* It must be created with a release you want to upgrade your original
  environment to.

* It must have the same settings as the original environment in terms of
  selected components and architecture options.

* Settings changed in the new release must be properly upgraded and semantics
  of the settings must be preserved.

* Assignment of IP addresses of Controllers and Virtual IP addresses must
  duplicate the assignment in the original environment.


Proposed change
===============

We propose to extend definition of environment with Upgrade Seed environment
type. Such environment must refer to the original environment and have settings
copied from the original environment instead of generated in a usual way.

Separate API call will be added to create Upgrade Seed environment. Handler to
that call must copy and upgrade settings of the original environment and
create a new environment with those settings, both editable and generated.

We must add Controller nodes to Upgrade Seed environment. Network and disk
settings for those nodes must be replicated from a Controller node in the
original environment during the assignment. IP addresses in Public and
Management networks allocated to those nodes must duplicate addresses
allocated to Controllers of original environment.

Alternatives
------------

Alternative implementation of Upgrade Seed environment logic is external
script that performs the following actions:

* Copy editable env settings via Nailgun API

* Copy generated settings from original to upgrade seed environment in Nailgun
  DB via ``psql`` client

* Modify IP address assignments in Nailgun DB via ``psql`` client

* Change deployment information for nodes in the Upgrade Seed environment to
  ensure changes in Fuel installer behavior during deployment of the Seed.

This methodology, while working and producing acceptable results, is difficult
to maintain outside of Fuel mainstream. Direct communications with database
pose data consistency threats. It will be hard to integrate with the Fuel Web
UI in future.

Data model impact
-----------------

Proposed modifications to base class ``Cluster`` include additional
attributes, changed attributes and methods:

* Add ``Cluster.original_cluster_id`` attribute. This is an ID of environment
  that was picked for upgrade and for which the given environment will serve 
  as an Upgrade Seed.

* ``Cluster.update_attributes()`` method will be modified to derive
  editable and generated attributes from the Cluster instance idenified by;
  ``Cluster.original_cluster_id`` if this attribute has value (i.e. not
  ``None``).

REST API impact
---------------

We propose to add the following extensions to the Nailgun API.

Upgrade an environment
++++++++++++++++++++++

Endpoint for all methods related to upgrade. In future, when single-click
upgrade is supported, this will be a single call to upgrade the environment.
It will not be directly callable in Fuel 7.0.

* Specification for the method

  * Upgrades a given cluster by installing new controllers and upgrading state
    and configurations of the original OpenStack cloud. 

  * Method type: POST

  * Normal http response code(s): N/A

  * Expected http response code(s):

    * 501 Not Implemented
      In Fuel 7.0, this endpoint is not callable directly.

  * URL for the resource: ``/cluster/<cluster_id>/upgrade``

  * Parameters which can be passed via the url:

    * ``cluster_id``: ID of the cluster to upgrade

  * JSON schema definition for the body data if allowed: N/A

  * JSON schema definition for the response data if any: N/A

Clone upgraded environment
++++++++++++++++++++++++++

This is the first step in process of upgrade of MOS environment. Creates
Upgrade Seed cluster with configuration that matches configuration of the
original cluster, but has a new release version.

* Specification for the method

  * Create a new cluster with settings and attributes copied from the
    specified cluster, including generated attributes (i.e. service passwords
    and other credentials).

  * Method type: POST

  * Normal http response code(s): 200 OK

  * Expected error http response code(s)

    * 404 Not Found
      A cluster or release with given ID was not found in database.

  * URL for the resource: ``/cluster/<cluster_id>/upgrade/clone``

  * Parameters which can be passed via the url:
  
    * ``cluster_id``: ID of the cluster to copy parameters from it

  * JSON schema definition for the body data:

::

    {
         "$schema": "http://json-schema.org/draft-04/schema#",
         "title": "Cluster Clone Parameters",
         "description": "Serialized parameters to clone clusters",
         "type": "object",
         "properties": {
             "name": {"type": "string"},
             "release_id": {"type": "number"},
         },
    }

  * JSON schema definition for the response data:

::

    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "Cluster",
        "description": "Serialized Cluster object",
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "mode": {
                "type": "string",
                "enum": list(consts.CLUSTER_MODES)
            },
            "status": {
                "type": "string",
                "enum": list(consts.CLUSTER_STATUSES)
            },
            "net_provider": {
                "type": "string",
                "enum": list(consts.CLUSTER_NET_PROVIDERS)
            },
            "grouping": {
                "type": "string",
                "enum": list(consts.CLUSTER_GROUPING)
            },
            "release_id": {"type": "number"},
            "pending_release_id": base_types.NULLABLE_ID,
            "replaced_deployment_info": {"type": "object"},
            "replaced_provisioning_info": {"type": "object"},
            "is_customized": {"type": "boolean"},
            "fuel_version": {"type": "string"},
            "original_cluster_id": {"type": "number"}
        }
    }

Assign a node to Upgrade Seed cluster
+++++++++++++++++++++++++++++++++++++

Modification of the standard handling of 'assignment' method of the cluster
triggered by setting ``original_cluster_id`` parameter in cluster attributes.
Shall only be used to add Controllers to the Upgrade Seed environment.

* Specification for the method

  * Assign a node with 'controller' role to the Upgrade Seed environment. Disk
    and network attributes for the node are replicated from 'controller' node
    in the original environment. Only 'controller' role is supported.

  * Method type: POST

  * Normal http response code(s): 200 OK

  * Expected error http response code(s)

    * 400 Bad Request
      Node assigned with role other than 'controller' to the environment that
      has non-empty ``original_cluster_id`` parameter.

    * 404 Not Found
      A cluster or a node with given ID was not found in database.

  * URL for the resource: ``/cluster/<cluster_id>/assignment``

  * Parameters which can be passed via the url:
  
    * ``cluster_id``: ID of the cluster to copy parameters from it

  * JSON schema definition for the body data:

::

    {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'assignment',
        'description': 'assignment map, node ids to arrays of roles',
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'id': {
                    'description': 'The unique identifier for id',
                    'type': 'integer'
                },
                'roles': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            },
            'required': ['id', 'roles'],
        }
    }

  * JSON schema definition for the response data: None

Upgrade impact
--------------

This patch set will extend the standard Nailgun API and will be a subject to
modification during the upgrade procedure as a part of Nailgun codebase.

Security impact
---------------

Clone environment call creates a copy of cluster's generated attributes, which
include sensitive data like passwords for system users. Sensitive data cannot
be accessed directly using this API call.

Notifications impact
--------------------

No impact.

Other end user impact
---------------------

This change will not have impact on python-fuelclient in 7.0 release cycle.
Functions implemented in this change shall be added to python-fuelclient in
future release cycles.

Performance Impact
------------------

No impact.

Plugin impact
-------------

No impact.

Other deployer impact
---------------------

No impact.

Developer impact
----------------

No impact.

Infrastructure impact
---------------------

This change will require additional system test to verify that a clone of the
cluster was created successfully.

This change must be also tested against upgrade tests in a sense that it
properly creates a clone of the cluster with new release version.

Implementation
==============

Assignee(s)
-----------

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  ikharin (Ilya Kharin)

Other contributors:
  yorik.sar (Yuriy Taraday)

Work Items
----------

* implement API handler for url ``/cluster/<id>/upgrade``.

* implement API handler for url ``/cluster/<id>/upgrade/clone``.

* modify API handler for url ``/cluster/<id>/assignment``.

Dependencies
============

None.

Testing
=======

This change will require additional system test to verify that a clone of the
cluster was created successfully.

This change must be also tested against upgrade tests in a sense that it
properly creates a clone of the cluster with new release version.

Documentation Impact
====================

The feature will be documented along with the other API handlers.

References
==========

