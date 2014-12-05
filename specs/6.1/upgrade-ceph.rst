..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Upgrade ceph to the latest stable release
==========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/upgrade-ceph [1]_

Problem description
===================

Now we deploy the ceph version 0.80.7 but a new stable version 0.87 is released now. [2]_

There are a lot of improvements available that are connected with performance
and recovering and I think it would be great to have it in our new release.

Proposed change
===============

Upgrade ceph packages in our repository.

Alternatives
------------

Leave it as-is. But we wil leave our customers without this improvements.

Data model impact
-----------------

It is not supposed to change data models.

REST API impact
---------------

It is not supposed to change REST API.

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

None

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

smakar

Work Items
----------

#. Prepare the repository mirror with packages for Ubuntu and CentOS.

Dependencies
============

None

Testing
=======

#. We need to build new fuel ISO and test if deployment work as expected.

Documentation Impact
====================

#. Add to docs that we are using the latest stable ceph version (0.87).

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/upgrade-ceph
.. [2] http://ceph.com/docs/master/release-notes/#v0-87-giant
