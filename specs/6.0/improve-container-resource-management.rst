..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Improve Docker Container Resource Management
============================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/improve-container-resource-management

LXC tuning is necessary to ensure Fuel API and its database backend can operate
more smoothly. 

Problem description
===================

There is no management of compute resources on Fuel Master with Docker,
leaving a risk of denial of service from one Docker container.

Proposed change
===============

Disk, CPU, and Memory allocation can be implemented to balance resource
consumption.

Alternatives
------------

We could opt to not implement this, but approach the problem per-app
with greater tuning, not unlike existing tuning already in place for
MySQL.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

This change should improve overall Fuel Master performance, leading
to fewer issues where deployment fails because of slow response time.

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  raytrac3r

Work Items
----------

Phase one of this change involves identifying all tunable properties of
cgroups that affect performance and adding them to dockerctl.
Phase two involves testing high load deployments with tuned parameters
for acceptance testing.


Dependencies
============

Docker 1.0 or newer.


Testing
=======

This change must be able to deploy 20 nodes in parallel, but also 
noticeably improve performance towards deploy 50 or even 100 nodes.

Documentation Impact
====================

None

References
==========

None
