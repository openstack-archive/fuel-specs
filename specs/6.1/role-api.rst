..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Provide programable API to work with Fuel node roles
====================================================

Problem description
===================

Current state of nailgun only allows to create roles by inserting them
in nailgun/fixtures/openstack.yaml and create entities based on this
description.

Such approach can not be considered as extensible and imposes difficulties
when user wants to move certain services on to separate nodes
(the closest example is ceph-mon which is always installed on controller).

Proposed change
===============

Current spec proposes to allow user create/update/delete roles by nailgun
rest-api and fuel client.

Alternatives
------------

Allow creation of new roles only as a plugin entity. But such approach
imposes bad UX experience for anyone who want to solve certain business
problems right on environment.

Data model impact
-----------------

Current data model will be reused, as it is sufficient for needs of
this specification.

REST API impact
---------------

Object can be described by next schema, but not limited to this schema,
it will also contain limitations, conflicts and range of other parameters.

::

    $schema: http://json-schema.org/draft-04/schema#
    description: Serialized Role object
    required: [name, meta, volumes]
    title: Role
    type: object
    properties:
      id: {type: integer}
      meta:
        description: {description: Short description of role functionality,
                      type: string}
        properties:
          name: {description: Name that will be shown on UI, type: string}
        required: [name, description]
        type: object
      name: {type: string}
      volumes_roles_mapping:
        items:
          description: Volume allocations for role
          properties:
            allocate_size:
              id: {type: string}
              type:
                enum: [all, min, full-disk]
          required: [allocate_size, id]
          type: object
        minItems: 1
        type: array

volumes_roles_mapping will be used for partitioning of this roles,
the same way it is described in openstack.yaml

This object will be served on URIs

::

  PUT/GET/DELETE /releases/(?P<release_id>\d+)/roles/(?P<role_name>\w+)/

  POST/GET /releases/(?P<release_id>\d+)/roles/

It is common practice to create multiple endpoints for nested resources,
but in case of role - root URI (/roles/) doesnt make much sense because role
is isolated per release entity.

Upgrade impact
--------------

In case database will be migrated into new state - added roles should be
migrated as well. Given that all data will be covered by schema - the only
possible limitation is that we need to be smart with code in migration and
assume that conditional expression can be changed.

Security impact
---------------

No impact

Notifications impact
--------------------

No impact

Other end user impact
---------------------

CLI commands will be added to work with API:

Get list of all roles:

::

  fuel role --rel 1

  name          | id | release_id
  controller    | 1  | 1

Save full role information to file

::

  fuel role --rel 1 --role controller --file some

Create role from file. Role data is stored in file.

::

  fuel role --rel 1 --create --file some

Update role description. Role data is stored in file.

::

  fuel role --rel 1 --update --file some

Delete role

::

  fuel role --rel 1 --delete --role controller

Performance Impact
------------------

No impact

Plugin impact
-------------

Maybe in future described schema will be reused for role entity in plugin.

Other deployer impact
---------------------

Will allow to easily create new role and attach any tasks to it for deployment.

Developer impact
----------------

No impact

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  dshulyak

Work Items
----------

1. Implement REST Api for roles
2. Implement CLI commands
3. Write documentation on added REST Api and CLI command

Dependencies
============

No dependencies

Testing
=======

Unit tests coverage, and manual tests.

Optionally system test can be implemented that will deploy ceph-mon,
or neutron l3 agent as separate role, but it depends on library state of things

Documentation Impact
====================

Documentation will be improved to contain

References
==========

No references
