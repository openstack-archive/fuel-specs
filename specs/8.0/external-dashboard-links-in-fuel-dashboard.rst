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


-------------------
Problem description
-------------------

For now dashboard links of plugins installed to environment are not available
for user from Fuel UI, that is not good UX. Fuel UI should cover the feature.


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

.. image:: ../../images/8.0/external-dashboard-links-in-fuel-dashboard/
   plugin_blocks.png
   :scale: 75 %

The environment-level entries come from Nailgun in
`GET /api/clusters/:cluster_id/plugin_links` response.

If url provided in plugin entry is relative, then Fuel UI code should process
it in the following way:

* check `public_ssl.services` environment setting (comes in
  `GET /api/clusters/:cluster_id/attributes response`) value:

  * if `public_ssl.services` is True, then a protocol for result url should be
    `https` and hostname is a `public_ssl.hostname` environment setting value
  * if `public_ssl.services` is False, then a protocol for result url should
    be `http` and hostname is environment virtual IP (stored in environment
    network configuration data)

No processing required for an absolute plugin url.

Nailgun
=======

New API `api/clusters/:id/plugin_links` endpoint should be created to
support environment plugin dashboard links management.

Appropriate API `api/plugins/:id/links` should be created to support management
of plugin-level dashboards links that refer to dashboards on master node.

The plugins should have a possibility to create/update/delete their entries
which will be shown in operational environment dashboard.


Data model
----------

The new table for dashboard entries should be created in Nailgun DB,
containing the following fields:

+----+----------+---------------+----------+------------+
| id | title    | description   | url      | cluster_id |
+====+==========+===============+==========+============+
| id | String   | String        | String   | id         |
| id | required | default: None | required | required   |
+----+----------+---------------+----------+------------+

All the attributes are mandatory for the table entry and should not have null
or empty string value.

Also quite similar table for Master node dashboards entries is required.

+----+----------+---------------+----------+------------+
| id | title    | description   | url      | plugin_id  |
+====+==========+===============+==========+============+
| id | String   | String        | String   | id         |
| id | required | default: None | required | required   |
+----+----------+---------------+----------+------------+


REST API
--------

Cluster Dashboards Links
^^^^^^^^^^^^^^^^^^^^^^^^

API should be extended with the following methods:

+--------+-----------------------------+---------------------+-------------+
| method | URL                         | action              | auth exempt |
+========+=============================+=====================+=============+
|  POST  | /api/clusters/:cluster_id/  | create a new plugin | true        |
|        | plugin_links                | link                |             |
+--------+-----------------------------+---------------------+-------------+
|  GET   | /api/clusters/:cluster_id/  | get list of plugin  | false       |
|        | plugin_links                | links               |             |
+--------+-----------------------------+---------------------+-------------+
|  PUT   | /api/clusters/:cluster_id/  | update a plugin     | false       |
|        | plugin_links/:entry_id      | link                |             |
+--------+-----------------------------+---------------------+-------------+
| DELETE | /api/clusters/:cluster_id/  | delete a plugin     | false       |
|        | plugin_links/:entry_id      | link                |             |
+--------+-----------------------------+---------------------+-------------+

The methods should return the following statuses in case of errors:

* 400 Bad Request - in case of invalid data (missing field, wrong format)
* 404 Not found - in case of missing entry
* 405 Not Allowed - for `PUT /api/clusters/:cluster_id/plugin_links`

GET method returns JSON of the following format:

.. code-block:: json

   [
     {
       title: 'Zabbix',
       description: 'Zabbix is software that monitors ...',
       url: 'https://172.5.6.24:80/zabbix_dashboard',
       id: Number(identificator)
     },
     {
       title: 'Murano',
       description: 'Murano dashboard link ...',
       url: '/openstack/murano_dashboard',
       id: Number(identificator)
     },
     ...
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


Plugin Dashboards Links
^^^^^^^^^^^^^^^^^^^^^^^

There will be a new REST API url added:

+--------+--------------------------------+--------------------------+-------+
| method | URL                            | action                   | auth  |
|        |                                |                          | exempt|
+========+================================+==========================+=======+
|  POST  | /api/v1/plugins/:plugin_id/    | create a new item        | true  |
|        | links                          | for dashboard links      |       |
+--------+--------------------------------+--------------------------+-------+
|  GET   | /api/v1/plugins/:plugin_id/    | get a list of            | false |
|        | links                          | dashboard links          |       |
+--------+--------------------------------+--------------------------+-------+
|  PUT   | /api/v1/plugins/:plugin_id/    | update a dashboard link  | false |
|        | links/:link_id                 | with specified id        |       |
+--------+--------------------------------+--------------------------+-------+
| DELETE | /api/v1/plugins/:plugin_id/    | delete a dashboard       | false |
|        | links/:link_id                 | link with specified id   |       |
+--------+--------------------------------+--------------------------+-------+

The methods should return the following statuses in case of errors:

* 400 Bad Request - in case of invalid data (missing field, wrong format)
* 404 Not found - in case of missing entry
* 405 Not Allowed - for `PUT /api/clusters/:cluster_id/plugin_links`

GET method returns JSON of the following format:

.. code-block:: json

    [
        {
            id: Entry Number (identificator)
            title: 'Zabbix',
            description: 'Zabbix is software that monitors numerous' +
            + 'parameters of a network and the health and integrity' +
            + ' of servers',
            url: '/'
        }
    ]

POST to `/api/v1/plugins/:plugin_id/links` will be formed in
the same format as GET request.

.. code-block:: json

    {
        title: 'My plugin',
        description: 'My awesome plugin',
        url: 'https://10.0.0.42:8080/my_dashboard'
    }

Title and port fields is required.

PUT request `/api/v1/plugins/:plugin_id/links/:link_id` will
provide an ability to change existing dashboard links entries.

.. code-block:: json

    {
        title: 'My plugin1',
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

Both plugin development documentation and user guides should be updated
accordingly to the change.


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
  ikutukov (ikutukov@mirantis.com)

QA engineer:
  apalkina (apalkina@mirantis.com)

Mandatory design review:
  vkramskikh (vkramskikh@mirantis.com)
  akislitsky (akislitsky@mirantis.com)


Work Items
==========

#. Nailgun DB and API changes to support plugin links management
#. Plugin framework changes to support plugin links management
#. Fuel UI changes to display plugin links in operational environment
   dashboard


Dependencies
============

None


-----------
Testing, QA
-----------

* Nailgun tests for the new API, DB changes and migration
* Tests for plugins to check they provide a plugin link data properly
* Manual testing
* Functional UI auto-tests should cover the feature


Acceptance criteria
===================

* User can access dashboards of installed environment plugins from Dashboard
  tab of the operational environment in Fuel UI


----------
References
----------

* #fuel-dev on freenode
