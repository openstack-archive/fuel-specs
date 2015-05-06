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
Users typically don't know what to do next after OpenStack environment deploy.
To accumulate information about the OpenStack environment and give the user an
idea of what to do next and what in general can be done with OpenStack
environment. The most useful info here will be link to Horizon and links to
Mirantis documentation. Also plugin links may be introduced here. Should be
extensible for future plugins.

Proposed change
===============

Create a separate tab in UI combining all the necessary information and useful
links for the user. This tab will also replace current Actions tab, combining
data from there.

The main information will be displayed in the separate block - with
instructions what to do next and what currently is wrong.

For the new just-created OpenStack environment there will be:

* link to *Add nodes screen* with warning *No nodes added to OpenStack*
  *environment*
* for OpenStack environments with nodes, but no network verification -
  corresponding warning and link to Networks tab.

To be short - all warnings and errors, shown in Deploy changes dialog should be
shown here.

For deployed OpenStack environment there will be OSTF tests status with link to
Healthcheck tab. For new cluster this block will be shown but disabled.

For error OpenStack environment here will be error message, replacing
(or duplicating) the one under OpenStack environment page breadcrumbs.

Also the list of items to be shown can be different. The suggestion is to show
all the necessary information after deployment.

The additional content here will be

* nodes statistics - number of online nodes in OpenStack environments, in graph
  view. Number of error nodes - just in red. (In case of error
  offline node I suggest to calculate this node as an error one, because even
  if it becomes online it will be error-containing, but if the error will be
  fixed this node will go to online category)
* link to plugins (where to get and how, what are the available plugins)
* storage backend info (is needed to know in order to not search this
  information
  through the whole settings tab)
* other OpenStack environment information (in one cumulated block)
* nodes configuration (HDD, CPU, RAM)

The suggestion is to have a unified source of truth for either deployed
OpenStack environment and a new one, this tab would be the first one and
Nodes tab will go after it.

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

Should be pluggable.

We'll have special /cluster/:id/dashboard_entries url by GETting which it
will be possible to get the list of dashboard entries in the format like this:

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

All optimizations have to be backward compatible. Should support
GET - request providing the list of entry points for further
usage, like described in changes 'for nailgun`_ section.

GET /cluster/:id/dashboard_entries

POST/PUT/DELETE are unlikely to be supported.

Ok code 200, server error code starting from 500.

No parameters expected.

JSON format - the stucture providing key and id in any way.
Other contents may vary - something like 'title',
'description' and 'url' will be the initial variant:

.. code-block:: json

    response: {
        environment_operations: {
            zabbix: {
                title: '',
                description: '',
                url: '',
                id: Number(identificator)
            },
            horizon: {
                title: '',
                url: '',
                id: Number(identificator)
            },
            sahara: {
                description: '',
                url: '',
                id: Number(identificator)
            },
            murano: {
                title: '',
                description: '',
                url: '',
                id: Number(identificator)
            },
            ceilometer: {
                title: '',
                description: '',
                url: '',
                id: Number(identificator)
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
* Markup implementation
* Javascript React components implementation

Dependencies
============

None

Testing
=======

Tests to be created for new REST API items.
UI side of Dashboard implementation should also be covered with
functional and unit tests - React components, new UX, new js model.

Aceptance criteria
------------------

After my OpenStack deployment has successfully completed, the default tab
displayed shows links out to all relevant dashboards (Horizon, Murano, plugin
UIs). If plugins were included, links should include plugin-relevant UIs.
Changing plugin settings and/or removing plugins is not a part of this page.


Documentation Impact
====================

Part about user flow, with new Dashboard tab should be updated.

References
==========

1. https://blueprints.launchpad.net/fuel/+spec/post-deployment-dashboard
