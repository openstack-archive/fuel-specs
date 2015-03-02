..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================
Provide programable API to work with Fuel roles
===============================================

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

Allow creation of new nodes only as a plugin entity. But such approach
imposes bad UX experience for anyone who want to solve certain business
problems right on environment.

Data model impact
-----------------

Current role data is splitted over several places.
DB model describes only:

::

  id - unique identifier
  release_id - id of the role related release
  name - label of the node (controller, compute)

Roles metadata on release model stores:

::
  name - name that is shown on UI
  description: description that is shown on UI
  conditions and limitations of the role
  several flags that alters role behaviour

Volumes metadata on release model stores volumes and allocation strategies
for role.

Described inconsistencies will not be solved in the scope of this spec.

REST API impact
---------------

Provide object that is desribed with next schema:

::

    $schema: http://json-schema.org/draft-04/schema#
    description: Serialized Role object
    required: [id, name, release_id, meta, volumes]
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
      release_id: {type: integer}
      volumes:
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

This object will be served on URIs

::

  PUT/GET/DELETE /roles/(?P<obj_id>\d+)/

  POST/GET /roles/

  should atleast support filtering on release_id


Upgrade impact
--------------

In case database will be migrated into new state - added roles should be
migrated as well.

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

  fuel role

  name          | id | release_id
  controller    | 1  | 1

Save full role information to file

::

  fuel role --role 1 --file some

Create role from file

::

  fuel role --create --file some

Update role description

::

  fuel role --update --file some

Delete role

::

  fuel role --delete --role 2

Performance Impact
------------------

No impact

Plugin impact
-------------

Maybe in future described schema will be reused for role entity in plugin.

Other deployer impact
---------------------

Dep

Developer impact
----------------

Discuss things that will affect other developers working on Fuel,
such as:

* If the blueprint proposes a change to the driver API, discussion of how
  drivers would implement the feature is required.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  dshulyak

Work Items
----------

1. Implement REST Api for plugins
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
