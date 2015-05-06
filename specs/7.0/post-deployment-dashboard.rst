..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Post Deployment Support
==========================================

https://blueprints.launchpad.net/fuel/+spec/post-deployment-dashboard

Create a single entry point for user to have access to all the necessary
information after deployment.

Problem description
===================

After deployment is done typical Fuel user doesn't know what to do next. So,
with this new tab he will get the basic instructions on what to do next. It
should become visible and default only after cluster deployment. This would be
a simple dashboard on tab with plugin information after deployment - with links
to Horizon, any plugins. Should be extensible for future plugins.

Proposed change
===============

For nailgun
-----------

Provide API with links to all possible necessary resources after cluster
deployment (list of them to be discussed). Should be pluggable.

For UI developers - Implement design and layout with the data provided from
nailgun and short useful descriptions.

Also the list of items to be shown can be different. The suggestion is to show
all the necessary information after deployment, as shown on mock-up

 .. image:: images/dashboard/dashboard-static-v1.jpg

:scale: 50 %

The additional content here may be

* node statistics - number of online nodes not in deployed and in clusters,
  number of error nodes etc - to be discussed
* deployed nodes configuration by deployed clusters (HDD, CPU, RAM)
* link to plugins (where to get and how, what are the available plugins)
* storage backend info (might be needed to know in order to not search
  through the whole settings tab)
* diagnostic snapshot - to remove from support tab, ehich is not really the
  right place for it and to have it on dashboard

Also it is still an open question whether it should be `global` dashboard, not
only with after-deployment tasks, but being an `entry point` for the Fuel,
replacing the place of the Nodes tab.


Alternatives
------------

None

Data model impact
-----------------

Andrew Woodward (awoodward@mirantis.com) suggested to leverage the instance of
keystone that fuel uses to register a catalog of these endpoints for each env.
We could likely store each env as a region. This would allow:

* dynamically add and remove endpoints
* end user can create arbitrary endpotins that they want
* allow plugins an easy way to access endpoints
* gives the end-user access to a familiar interface if they want to consume

the data in another system

REST API impact
---------------

Might require some changes, but to be discussed. All optimization have to be
backward compatible. Should support GET - request providing the list of entry
point for further usage. e.g.
GET /post_deployment_tasks
POST/PUT/DELETE are unlikely to be supported.

Ok code 200, server error code starting from 500.

No parameters expected.

JSON format, something like:

.. code-block:: javascript

    response: {
        environment_operations: {
            zabbix: {
                description: '',
                url: ''
            },
            log_analylics: {
                description: '',
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

Will improve user experience for after deployment scenarios.
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

Probably test should be created for new APi items.
UI side should also be covered with tests.

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
