..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================
External MongoDB Support
========================

https://blueprints.launchpad.net/fuel/+spec/external-mongodb-support

Be ably to use external specific MongoDB as ceilometer backend.

Problem description
===================

A detailed description of the problem:

* Currently we're providing MongoDB from the box, although,
  it might be a situation when some specific MongoDB installation is needed.
  That's why we need to give possibility of external MongoDB providing
  not to implement all possible DB settings inside Fuel itself.

Proposed change
===============

External MongoDB support can be implemented by adding checkbox and
textboxes to Fuel UI for specifying such parameters as:

* db_username
* db_user_password
* db_name
* mongodb_hosts

Also we shouldn't allow to deploy cluster with mongo role and even choose
mongo role on node if external mongo is enabled.

Alternatives
------------

Add posibility to specify connection to database but it's difficult to
validate connection string instead of validating separated parameters.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

This is needed in changes in puppet scripts and fuel UI. In Fuel Web UI
we need to add one checkbox to choose external MongoDB to use
and four textboxes for separated MongoDB parameters such as:
db_username, db_user_password, db_name, db_hosts_ips.
Pick Mongo role on node should be forbidden if external mongo is chosen.
In puppet scripts we should use this parameters to set connection
string to MongoDB for ceilometer in ceilometer.conf.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Users will interact with this feauture through Fuel Web UI.

Performance Impact
------------------

None

Other deployer impact
---------------------

* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

  This should be enabled by using Fuel Web UI.

Developer impact
----------------

Discuss things that will affect other developers working on Fuel,
such as:

* There will be an impact on ceilometer that have to be enabled and it's
  checkbox should present (and should be checked) on Fuel Web UI.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  iberezovskiy

Other contributors:
  dbelova

Work Items
----------

* Edit Fuel Web UI by adding checkbox and textboxes for MongoDB
  auth parameters (iberezovskiy)
* Validate user input (iberezovskiy)
* Forbid to choose mongo role (iberezovskiy)
* Edit puppet scripts to use these parameters  (iberezovskiy)
* Write a documentation (dbelova)

Dependencies
============

None

Testing
=======

Testing approach:

* Nailgun tests should be passed
* Environment with ceilometer and external mongo should be
  successfully deployed

Documentation Impact
====================

A note should be added to Fuel User Guide to describe the possibility to
specify external MongoDB to use.

References
==========

None

