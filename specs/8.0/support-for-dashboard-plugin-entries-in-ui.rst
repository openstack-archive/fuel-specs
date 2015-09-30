..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================================
Support for external dashboard plugin entries in Fuel UI
========================================================

https://blueprints.launchpad.net/fuel/+spec/support-for-dashboard-plugin-entries-in-ui

Extend existing OpenStack environment Dashboard tab with entry points for
plugins giving them an ability to provide urls for post-deployment OpenStack
environment manipulation.


--------------------
Problem description
--------------------

Plugins have no way to add their urls to the Dashboard tab.


----------------
Proposed changes
----------------

Web UI
======

Urls, provided by plugins (services like Murano, Sahara, Ceilometer are
treated as plugins also) via API described in corresponding chapter
`REST API impact`_. Plugin entries will be displayed in the order of date
creation.


Nailgun
=======

Provide API with links to all possible necessary resources after OpenStack
environment deployment.

* link to Zabbix
* link to Murano (description and what to do with it)
* link to Sahara (description and what to do with it)
* link to Ceilometer (description and what to do with it)
* any other links provided by plugins

We'll have special /cluster/:id/dashboard_entries url by GETting which it will
be possible to get the list of dashboard entries in the format like this:

.. code-block:: json

        [
            {
                title: 'plugin',
                description: '',
                url: '',
                id: Number
            }
        ]

with optional 'description' field.

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

cluster_id field means one cluster may have many dashboard entries for plugin,
but it will belong to one cluster (one-to-many relationship)


REST API
--------

API POST, PUT and DELETE method should be available for plugins in their post-
deployment hooks.

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



Orchestration
=============

None.

RPC Protocol
------------

None.


Fuel Client
===========

None.


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

A migration should be created for DashboardEntries model, also
migrations are needed to generate dashboard entries for old OpenStack
environments - for Horizon, Sahara and Murano entries.


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
 tbd

Mandatory design review:
  Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com)



Work Items
==========

#. Finish backend implementation.
#. Implement UI logics.


Dependencies
============

None.


------------
Testing, QA
------------

Tests to be created for new REST API items.
UI side of Dashboard implementation should also be covered with
functional and unit tests - React components, new UX, new js model.


Acceptance criteria
===================

User can acccess plugin urls after OpenStack Environment deployment.


----------
References
----------

* #fuel-ui on freenode
