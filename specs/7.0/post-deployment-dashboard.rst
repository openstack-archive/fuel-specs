..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
OpenStack environment Dashboard
==========================================

https://blueprints.launchpad.net/fuel/+spec/post-deployment-dashboard

Create a single entry point for user to have access to all the necessary
information before, in progress and after deployment.

Problem description
===================

It might be quite hard for a newbie user to understand what he should do after
OpenStack environment creation. To help user setup the OpenStack environment
we'll introduce dashboard.
Also users typically don't know what to do next after OpenStack environment
deploy.
Dashboard will accumulate information about the OpenStack environment
It also will give the user an idea of what to do next and what in general can
be done with OpenStack environment. The most useful info here will be link
to Horizon and links to  documentation. Also plugin links should be introduced
here. Should be extensible for future plugins, providing API for them.

Proposed change
===============

Create a separate tab in UI combining all the necessary information and useful
links for the user. This tab will also replace current Actions tab, combining
data from there.

The main information should be displayed in the separate block - with
instructions what to do next and what currently is wrong.

For the new just-created OpenStack environment there should be:

* link to *Add nodes screen* with warning *No nodes added to OpenStack*
  *environment*
* for OpenStack environments with nodes, but no network verification -
  corresponding warning and link to Networks tab

To be short - all warnings and errors, shown in Deploy changes dialog should be
shown here.

For deployed OpenStack environment there will be OSTF tests status with link to
Healthcheck tab. For new OpenStack environment this block will be shown but
disabled.

For error OpenStack environment here will be error message, replacing
the one under OpenStack environment page breadcrumbs.

The additional content here will be:

* nodes statistics - number of online nodes in OpenStack environments, in graph
  view, donut chart. Number of error nodes - just in red (in case of error
  offline node this node will be counted as an error one)
* link to plugins documentation
* link to Openstack documentation
* storage backend info - what volume and image type is selected (Cinder or
  Ceph) (is needed to know in order to not search this information
  through the whole settings tab)
* other OpenStack environment information (in one cumulated block) - OpenStack
  environment name, operating system, OpenStack release, selected compute
  hypervisors (KVM, QEMU or vCenter), network option (Neutron or Nova)
* nodes configuration (HDD, CPU, RAM)

The suggestion is to have a unified source of truth for either deployed
OpenStack environment and a new one, this tab would be the first one and Nodes
tab will go after it.

The proposed mockups of dashboard: for new OpenStack environment:

 .. image:: images/dashboard/new_cluster.png

For new OpenStack environment being deployed:

 .. image:: images/dashboard/deployment_in_progress.png

 For OpenStack environment already deployed:

 .. image:: images/dashboard/deployment_done.png


For nailgun
-----------

Provide API with links to all possible necessary resources after OpenStack
environment deployment.

* link to Horizon
* link to Zabbix
* link to Murano (description and what to do with it)
* link to Sahara (description and what to do with it)
* link to Ceilometer (description and what to do with it)
* any other links provided by plugins

We'll have special /cluster/:id/dashboard_entries url by GETting which it will
be possible to get the list of dashboard entries in the format like this:

.. code-block:: javascript

            plugin: {
                title: '',
                description: '',
                url: '',
                id: Number
            }

with optional 'description' field.

To solve authentication issues we'll use auth exemption.


For UI
-----------

For UI developers - implement design and layout with the data provided from
nailgun and short useful descriptions.

Alternatives
------------

None

Data model impact
-----------------

The new table for dashboard entries should be created, containing the
following fields:

+----+--------+-------------+--------+
| id | Title  | Description | url    |
+====+========+=============+========+
| id | String | String      | String |
+-------------+-------------+--------+

REST API impact
---------------

API POST, PUT and DELETE method should be available for plugins in their post-
deployment hooks.

There will be a new REST API url added:

+--------+--------------------------------+--------------------------+-------+
| method | URL                            | action                   | auth  |
|        |                                |                          | exemp |
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

Upgrade impact
--------------

A migration should be created for DashboardEntries model.

Security impact
---------------

None

Notifications impact
--------------------

Unlikely.

Other end user impact
---------------------

Will improve user experience.
Unlikely to impact python-fuelclient.

Performance Impact
------------------

None.

Plugin impact
---------------------

Will provide an entry point for plugins to access post-deployment
dashboard.

Other deployer impact
---------------------

None.

Developer impact
----------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Aleksandra Morozova <astepanchuk@mirantis.com>
Other contributors:
  * Bogdan Dudko  <bdudko@mirantis.com> - designer
  * Steve Doll <sdoll@mirantis.com> - designer
  * Vitaly Kramskikh <vkramskikh@mirantis.com> - backend developer
Approver:
  * Nathan Trueblood <ntrueblood@mirantis.com>
  * Sheena Gregson <sgregson@mirantis.com>
Reviewer:
  * Vitaly Kramskikh <vkramskikh@mirantis.com>

Work Items
----------

Blueprint will be implemented in several stages:

* Initial design and logic approval
* Markup implementation
* Javascript React components implementation
* Backend implementation

Dependencies
============

None

Testing
=======

Tests to be created for new REST API items.
UI side of Dashboard implementation should also be covered with
functional and unit tests - React components, new UX, new js model.

Acceptance criteria
-------------------

User can access OpenStack documentation, list of changes, available actions,
cumulated information and what is missing for OpenStack environment, also
plugin urls will be shown on this separate Dashboard tab.
Cumulated environment information, actions that can be done with environment
and links to OpenStack documentation should always be visible for the user.
Before deployment user can see list of changes, a list of warnings/errors if
any in addition to information displayed always.
In the process of environment deployment, user can see current deployment
progress state, besides the information mentioned above.
After OpenStack deployment has successfully completed, the default displayed
tab shows links out to all relevant dashboards (Horizon, Murano, plugin
UIs). If plugins were included, links should include plugin-relevant UI blocks.
Changing plugin settings and/or removing plugins is not a part of this page.

Documentation Impact
====================

Part about user flow, with new Dashboard tab should be updated.

References
==========

1. https://blueprints.launchpad.net/fuel/+spec/post-deployment-dashboard
