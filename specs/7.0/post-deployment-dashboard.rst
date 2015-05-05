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

After deployment is done typical Fuel user doesn't know what to do next.
So, with this new tab he will get the basic
instructions on what to do next. It should become visible and default only
after cluster deployment.
This would be a simple dashboard on tab with plugin
information after deployment -
with links to Horizon, any plugins.
Should be extensible for future plugins.


Proposed change
===============

For nailgun
-----------

Provide API with links to all possible necessary resources
after cluster deployment
(list of them to be discussed).
Should be pluggable.

For UI developers - Implement design and layout with
the data provided
from nailgun and short useful descriptions.

Alternatives
------------

As one of the alternatives can be considered
`global` dashboard, not only with
after-deployment tasks, but this approach appears
to be not as agile and versatile
as post-deployment dashboard. Also, it rises a lot of unanswered
questions about contents of this tab and its neccessity
in terms of not repeating your self with already existing
tabs functionality.

Data model impact
-----------------

None.

REST API impact
---------------

Might require some changes, but to be discussed.
All optimization have to be backward compatible.
Should support GET - request providing
the list of entry point for further usage.
e.g. GET /post_deployment_tasks

POST/PUT/DELETE are unlikely to be supported.

Ok code 200, server error code starting from 500.

No parameters expected.

JSON format, something like:

http://paste.openstack.org/show/214983/

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

After my OpenStack deployment has successfully completed,
the default tab displayed shows links out to all
relevant dashboards (Horizon, Murano, plugin UIs).
If plugins were included, links should include
plugin-relevant UIs. Changing plugin
settings and/or removing plugins is not a part of this page.


Documentation Impact
====================

Part about post-deployment should be updated.

References
==========

1. https://blueprints.launchpad.net/fuel/+spec/post-deployment-dashboard
