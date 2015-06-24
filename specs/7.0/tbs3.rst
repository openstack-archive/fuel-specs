..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================
Migration to Twitter Bootstrap 3
================================

https://blueprints.launchpad.net/fuel/+spec/tbs3

Migrate from Twitter Bootstrap 2 (TB2) to Twitter Bootstrap 3 (TB3).


Problem description
===================

Currently Fuel UI is based on TB2, which is not supported for more than a
year. The current version of Twitter Bootstrap is 3.3.4. Also, our styles file
(for TB2) is poorly structured as we haven't refactored it since the very
beginning.


Proposed change
===============

We should migrate to TB3 and reimplement Fuel UI markup according to Twitter
Bootstrap changelog. Migrating to a newer version of Twitter Bootstrap is a
great chance to reduce technical debt: we'll also have to reimplement all the
styles.

Migration can be done in a few steps:

* Base layout markup (navbar, footer, page wrapper)
* Simple pages (support page, login page, releases page, etc.)
* Cluster page markup
* Cluster page tabs
* Nodes tab screens (disks, interfaces)
* Dialogs

Alternatives
------------

Migrate to some other HTML framework, though it doesn't makes much sense.

Data model impact
-----------------

None.

REST API impact
---------------

None.

Upgrade impact
--------------

None.

Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

As we're changing markup, we also can alter look of some features to match
the new style.

Performance Impact
------------------

There could be slight impact to performance of Fuel UI in browser as we
overhaul the styles and markup, not sure if it get worse or better.

Plugin impact
-------------

None.

Other deployer impact
---------------------

None.

Developer impact
----------------

Fuel UI contributors should be aware of the changelog of TB3 to efficiently
write new code.

Infrastructure impact
---------------------

None.


Implementation
==============

Assignees
---------

Primary assignee:
* Vitaly Kramskikh <vkramskikh@mirantis.com>

Other contributors:
* Alexandra Morozova <astepanchuk@mirantis.com>
* Bogdan Dudko <bdudko@mirantis.com>
* Julia Aranovich <jkirnosova@mirantis.com>
* Kate Pimenova <kpimenova@mirantis.com>
* Nikolay Bogdanov <nbogdanov@mirantis.com>

Mandatory design review:
* Vitaly Kramskikh <vkramskikh@mirantis.com>

QA engineer:
* Anastasia Palkina <apalkina@mirantis.com>

Work Items
----------

As described in ``Proposed change`` section, though some changes could be more
granular.


Dependencies
============

None.


Testing
=======

Existing functional test suite should be modified to support new markup.

Acceptance criteria
-------------------

TBD


Documentation Impact
====================

Screenshots of Fuel UI in the existing documentation should be updated.


References
==========

* #fuel-ui on freenode
