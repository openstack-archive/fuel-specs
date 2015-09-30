..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Support for plugin links in Environment and Equipment dashboards
================================================================

https://blueprints.launchpad.net/fuel/+spec/external-dashboard-links-in-fuel-dashboard

Extend Dashboard tab of operational OpenStack environment with links to
dashboards of plugins installed to the environment.


--------------------
Problem description
--------------------

For now dashboard links of plugins installed to environment are not available
for user from Fuel UI, that is not good UX. Fuel UI should cober the feature.


----------------
Proposed changes
----------------

Web UI
======

Dashboard tab of operational environment should display a set of installed
plugin dashboard links sorted by `id` attribute, if any.

Each entry should display the following data:

* plugin title
* plugin description
* link to plugin dashboard

.. image:: ../../images/8.0/support-for-dashboard-plugin-entries-in-ui/
   plugin_blocks.png
   :scale: 75 %

The entries come from Nailgun in
`GET /api/clusters/:cluster_id/dashboard_entries` response.


Nailgun
=======

New API `/cluster/:id/dashboard_entries` endpoint should be created to
support plugin dashboard links management.

The plugins should have a possibility to create/update/delete their entries
which will be shown in operational environment dashboard.


Data model
----------

The new table for dashboard entries should be created in Nailgun DB,
containing the following fields:

+----+--------+-------------+--------+------------+
| id | title  | description | url    | cluster_id |
+====+========+=============+========+============+
| id | String | String      | String | id         |
+----+--------+-------------+--------+------------+

All the attributes are mandatory for the table entry and should not have null
or empty string value.


REST API
--------

API should be extended with the following methods:

+--------+-----------------------------+---------------------+-------------+
| method | URL                         | action              | auth exempt |
+========+=============================+=====================+=============+
|  POST  | /api/clusters/:cluster_id/  | create a new entry  | true        |
|        | dashboard_entries           |                     |             |
+--------+-----------------------------+---------------------+-------------+
|  GET   | /api/clusters/:cluster_id/  | get list of entries | false       |
+--------+-----------------------------+---------------------+-------------+
|  PUT   | /api/clusters/:cluster_id/  | update a dashboard  | false       |
|        | dashboard_entries/:entry_id | entry               |             |
+--------+-----------------------------+---------------------+-------------+
| DELETE | /api/clusters/:cluster_id/  | delete a dashboard  | false       |
|        | dashboard_entries/:entry_id | entry               |             |
+--------+-----------------------------+---------------------+-------------+

The methods should return the following statuses in case of errors:

* 400 Bad Request - in case of invalid data (missing field, wrong format)
* 404 Not found - in case of missing entry
* 405 Not Allowed - for `PUT /api/clusters/:cluster_id/dashboard_entries`

GET method returns JSON of the following format:

.. code-block:: json

   [
     {
       title: 'Zabbix',
       description: 'Zabbix is software that monitors ...',
       url: 'http://www.zabbix.com/',
       id: Number(identificator)
     },
     {
       title: 'Murano',
       url: 'https://wiki.openstack.org/wiki/Murano',
       id: Number(identificator)
     },
     {
       title: 'My plugin',
       description: 'My awesome plugin',
       url: '/my_plugin',
       id: Number(identificator)
     }
   ]

POST method accepts data of the following format:

.. code-block:: json

   {
     title: 'My plugin',
     description: 'My awesome plugin',
     url: '/my_plugin'
   }

and return data of the same format as GET.

PUT method accepts data of the following format:

.. code-block:: json

   {
     id: Number(identificator),
     title: 'New plugin title'
   }

and returns:

.. code-block:: json

   {
     title: 'New plugin title',
     description: 'My awesome plugin',
     url: '/my_plugin',
     id: Number(identificator)
   }

DELETE method accepts data of the following format:

.. code-block:: json

   {
     id: Number(identificator)
   }


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

Plugin framework should be extended to provide an ability for the plugin to
create/update/delete its entry.

[TODO] the logic of composing plugin entry url should be described


Fuel Library
============

None


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

According to existing data model impact, an appropriate migration should be
created. Environments of old releases should support the feature too.


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

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

None


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

Both plugin documentation and user guides should be updated accordingly to
the change.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  vkramskikh (vkramskikh@mirantis.com)

Other contributors:
  jkirnosova (jkirnosova@mirantis.com)
  vsharshov (vsharshov@mirantis.com)
  astepanchuk (astepanchuk@mirantis.com)
  bdudko (bdudko@mirantis.com)

QA engineer:
  apalkina (apalkina@mirantis.com)

Mandatory design review:
  vkramskikh (vkramskikh@mirantis.com)
  akislitsky (akislitsky@mirantis.com)


Work Items
==========

#. Nailgun DB and API changes to support plugin dashboatrd links management
#. Plugin framework changes to support dashboard link management
#. Fuel UI changes to display plugin dashboard links in operational
   environment dashboard


Dependencies
============

None


-----------
Testing, QA
-----------

* Nailgun tests for the new API, DB table and migration
* Tests for plugins to check they provide an entry properly
* Manual testing
* Functional UI auto-tests should cover the feature


Acceptance criteria
===================

* User can access installed plugin dasboards from operational environment
  dashboard in Fuel UI


----------
References
----------

* #fuel-dev on freenode
