..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Openstack environment Dashboard
==========================================

https://blueprints.launchpad.net/fuel/+spec/post-deployment-dashboard

Create a single entry point for user to have access to all the necessary
information before, in progress and after deployment.

Problem description
===================

It might be quite hard for a newbie user to understand what he should do after
Openstack environment creation. To help user setup the Openstack environment
we'll introduce dashboard.
Users typically don't know what to do next after Openstack environment deploy.
To accumulate information about the Openstack environment and give the user an
idea of what to do next and what in general can be done with Openstack
environment. The most useful info here will be link to Horizon and links to
Mirantis documentation. Also plugin links may be introduced here. Should be
extensible for future plugins.

Proposed change
===============

Create a separate tab in UI combining all the necessary information and useful
links for the user. This tab will also replace current Actions tab, combining
data from there.

The main information will be displayed in the first block - with instructions
what to do next and what currently is wrong.

For the new just-created Openstack environment there will be:

* link to *Add nodes screen* with warning *No nodes added to Openstack*
  *environment*
* for Openstack environments with nodes, but no network verification -
  corresponding warning and link to Networks tab.

To be short - all warnings and errors, shown in Deploy changes dialog should be
shown here.

For deployed Openstack environment there will be OSTF tests status with link to
Healthcheck tab.

For error Openstack environment here will be error message, dublicating the one
under Openstack environment page breadcrumbs.

Also the list of items to be shown can be different. The suggestion is to show
all the necessary information after deployment.

The additional content here may be

* node statistics - number of online nodes not in deployed and in Openstack
  environments, number of error nodes etc - to be discussed. (In case of error
  offline node I suggest to calculate this node as an error one, because even
  if it becomes online it will be error-containing, but if the error will be
  fixed this node will go to online category)
* link to plugins (where to get and how, what are the available plugins)
* storage backend info (might be needed to know in order to not search
  through the whole settings tab)
* other Openstack environment information (Openstack Release, Network etc)
* nodes configuration (HDD, CPU, RAM)

The suggestion is to have a unified source of truth for either deployed
Openstack environment and a new one, this tab would be the first one and Nodes
tab will go after it.

The proposed mockup of dashboard for new Openstack environment:

 .. image:: images/dashboard/New_env_mock.png

The proposed mockup of dashboard for Openstack environment being deployed:

 .. image:: images/dashboard/in_progress_Deployment_Dashboard_mock.png

 The proposed mockup of dashboard for Openstack environment deployed:

 .. image:: images/dashboard/Post-Deployment_Dashboard_mock.png

And more true-to-life mocks:

 .. image:: images/dashboard/Pre-Deployed_Dashboard.jpg

 .. image:: images/dashboard/Deployed_Dashboard.jpg


For nailgun
-----------

Provide API with links to all possible necessary resources after Openstack
environment deployment.

* link to Horizon
* link to Zabbix
* link to Murano (description and what to do with it)
* link to Sahara (description and what to do with it)
* link to Ceilometer (description and what to do with it)
* any other links provided by plugins

Should be pluggable.

We'll have special /cluster/:id/dashboard_entries url by GETting which it will
be possible to get the list of dashboard entries in the format like this:

.. code-block:: javascript

            plugin: {
                title: '',
                description: '',
                url: '',
                id: Number
            }

To solve authentication issues we'll use OAuth exception.

(TBD) - provide more python part details here.

For UI
-----------

For UI developers - Implement design and layout with the data provided from
nailgun and short useful descriptions.

Alternatives
------------

None

Data model impact
-----------------

Unlikely

REST API impact
---------------

Might require some changes, but to be discussed. All optimization have to be
backward compatible. Should support GET - request providing the list of entry
points for further usagelike described in changes For Nailgun section.

GET /cluster/:id/dashboard_entries

POST/PUT/DELETE are unlikely to be supported.

Ok code 200, server error code starting from 500.

No parameters expected.

JSON format, something like:

.. code-block:: javascript

    response: {
        environment_operations: {
            zabbix: {
                title: '',  // might be optional
                description: '', // might be optional
                url: ''
            },
            horizon: {
                title: '',  // might be optional
                description: '', // might be optional
                url: ''
            },
            sahara: {
                title: '',  // might be optional
                description: '', // might be optional
                url: ''
            },
            murano: {
                title: '',  // might be optional
                description: '', // might be optional
                url: ''
            },
            ceilometer: {
                title: '',  // might be optional
                description: '', // might be optional
                url: ''
            }
        }
    }


Upgrade impact
--------------

Only if database is changed, but unlikely.

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

Will provide an entry point for plugins to access post-deployment dashboard.

Other deployer impact
---------------------

Better UX.

Developer impact
----------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  astepanchuk@mirantis.com
Other contributors (design):
  * Bogdan Dudko  <bdudko@mirantis.com>
  * Steve Doll <sdoll@mirantis.com>
Approver:
  * Nathan Trueblood <ntrueblood@mirantis.com>
  * Sheena Gregson <sgregson@mirantis.com>
Reviewer:
  * Vitaly Kramskikh <vkramskikh@mirantis.com>

Work Items
----------

Blueprint will be implemented in several stages:

* Initial design and logic approval
* Markup implementation with logic

Dependencies
============

None

Testing
=======

Probably test should be created for new API items.
UI side should also be covered with functional and unit tests.

Aceptance criteria
------------------

After my OpenStack deployment has successfully completed, the default tab
displayed shows links out to all relevant dashboards (Horizon, Murano, plugin
UIs). If plugins were included, links should include plugin-relevant UIs.
Changing plugin settings and/or removing plugins is not a part of this page.


Documentation Impact
====================

Part about post-deployment should be updated.

References
==========

1. https://blueprints.launchpad.net/fuel/+spec/post-deployment-dashboard
