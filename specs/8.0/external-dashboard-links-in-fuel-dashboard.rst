..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Support for plugin links in Environment and Equipment dashboards
================================================================

https://blueprints.launchpad.net/fuel/+spec/external-dashboard-links-in-fuel-dashboard

Extend existing OpenStack environment Dashboard tab and Nodes page with entry
points for installed plugins giving them an ability to provide urls to plugin
dashboards for post-deployment OpenStack environment manipulation.


--------------------
Problem description
--------------------

Plugins have no way to add their dashboard urls to the Dashboard tab.


----------------
Proposed changes
----------------

Web UI
======

The plugins will have a possibility to create their own dashboard entries in
operational OpenStack Environment dashboard tab and on Nodes page by providing
plugin url, title and description via API described in corresponding chapter
`REST API impact`_. Plugin entries will be sorted by 'id' attribute.

.. image:: ../../images/8.0/support-for-dashboard-plugin-entries-in-ui/plugin_blocks.png


Nailgun
=======

Provide API with links to all possible necessary resources after OpenStack
environment deployment.

* link to Zabbix
* link to Murano (description and what to do with it)
* link to Sahara (description and what to do with it)
* link to Ceilometer (description and what to do with it)
* any other links provided by plugins

The special /cluster/:id/dashboard_entries url will be available, by GETting
which it will be possible to get the list of dashboard entries.

To solve authentication issues we'll use auth exemption.


Data model
----------

The new table for dashboard entries should be created, containing the
following fields:

+----+--------+-------------+--------+------------+
| id | Title  | Description | url    | cluster_id |
+====+========+=============+========+============+
| id | String | String      | String | id         |
+-------------+-------------+--------+------------+

cluster_id field means one OpenStack environment may have many dashboard
entries for plugin, but it will belong to one OpenStack environment
(one-to-many relationship).


REST API
--------

API GET, POST, PUT and DELETE method should be available for plugins in their
post-deployment hooks.

The following validation cases for the data will be supported:

  * 400 Bad Request -  in case of invalid data (missing field, wrong format)
  * 404 Not found (missing entry)

There will be a new REST API url added:

+--------+--------------------------------+--------------------------+-------+
| method | URL                            | action                   | auth  |
|        |                                |                          | exempt|
+========+================================+==========================+=======+
|  POST  | /api/v1/clusters/:cluster_id/  | create a new  item       | true  |
|        | dashboard_entries              | for dashboard entries    |       |
+--------+--------------------------------+--------------------------+-------+
|  GET   | /api/v1/clusters/:cluster_id/  |  get a list of           | false |
|        | dashboard_entries              |   dashboard entries      |       |
+--------+--------------------------------+--------------------------+-------+
|  PUT   | /api/v1/clusters/:cluster_id/  | update a dashboard entry | false |
|        | dashboard_entries/:entry_id    |  with specified id       |       |
+--------+--------------------------------+--------------------------+-------+
| DELETE | /api/v1/clusters/:cluster_id/  | delete a dashboard       | false |
|        | dashboard_entries/:entry_id    | entry with specified id  |       |
+--------+--------------------------------+--------------------------+-------+

GET returns JSON like this:

.. code-block:: json

    [
        {
            title: 'Zabbix',
            description: 'Zabbix is software that monitors numerous' +
            + 'parameters of a network and the health and integrity' +
            + ' of servers',
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

POST to `/api/v1/clusters/:cluster_id/dashboard_entries` will be formed in
the same format as GET request.

.. code-block:: json

    {
        title: 'My plugin',
        description: 'My awesome plugin',
        url: '/my_plugin'
    }

PUT request `/api/v1/clusters/:cluster_id/dashboard_entries/:entry_id` will
provide an ability to change existing dashboard entries.

.. code-block:: json

    {
        title: 'My plugin1',
    }



Orchestration
=============

None.

RPC Protocol
------------

None.


Fuel Client
===========

There needs to be implement support for managing dashboard entries from the
CLI.


Plugins
=======

Will provide an entry point for plugins to access post-deployment
dashboard.


Fuel Library
============

None.


------------
Alternatives
------------

None.


--------------
Upgrade impact
--------------

A migration should be created for DashboardEntries table, also
migrations are needed to generate dashboard entries for old OpenStack
environments - for Sahara and Murano entries.


---------------
Security impact
---------------

None.


--------------------
Notifications impact
--------------------

None.


---------------
End user impact
---------------

Ability to access plugins urls will be provided.


------------------
Performance impact
------------------

None.


-----------------
Deployment impact
-----------------

None.


----------------
Developer impact
----------------

None.


--------------------------------
Infrastructure/operations impact
--------------------------------

None.


--------------------
Documentation impact
--------------------

The change should be reflected in the documentation.


--------------------
Expected OSCI impact
--------------------

None.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com)

Other contributors:
  Julia Aranovich, jkirnosova (jkirnosova@mirantis.com)
  Vladimir Sharshov, vsharshov (vsharshov@mirantis.com)
  Alexandra Morozova, astepanchuk (astepanchuk@mirantis.com)
  Bogdan Dudko, bdudko (bdudko@mirantis.com)

QA engineer:
    Anastasia Palkina, apalkina (apalkina@mirantis.com)

Mandatory design review:
  Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com)
  Aleksandr Kislitskii, akislitsky (akislitsky@mirantis.com)



Work Items
==========

#. Backend support for OpenStack environemnt dashboard plugin entries.
#. Extend environment Dashboard tab UI with the plugin entries.


Dependencies
============

None.


------------
Testing, QA
------------

* Tests to be created for new REST API items.
* UI side of Dashboard implementation should also be covered with
  functional and unit tests - React components, new UX, new js model.
* DB migrations should be tested.
* JSON schema should be added.
* Manual testing


Acceptance criteria
===================

User can access plugin urls and descriptions after OpenStack Environment
deployment from the OpenStack environment dashboard in Fuel UI.

----------
References
----------

* #fuel-ui on freenode
