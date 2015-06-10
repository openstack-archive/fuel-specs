..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============
Hammer support
==============

https://blueprints.launchpad.net/fuel/+spec/ceph-module [1]_

Hammer is a new LTS version of ceph with lots of improvements. The main
ones performance improvement in OSD on SSD configurations.

Problem description
===================

Proposed change
===============

Ceph updated to 0.9X version

Alternatives
------------

Data model impact
-----------------

REST API impact
---------------

Upgrade impact
--------------

Security impact
---------------

Notifications impact
--------------------

Other end user impact
---------------------

Performance Impact
------------------

In SSD only systems perfromance should be greatly improved

Plugin impact
-------------

Other deployer impact
---------------------

Developer impact
----------------

Infrastructure impact
---------------------

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  kdanylov

Other contributors:
  diurchenko, akiselyova, yportnova, gstepanov,rzarzynski

Work Items
----------

Prepare deb and rpm packages for FUEL
Run tests

Dependencies
============

Testing
=======

Install openstack with ceph as a storage.
Login into controller node and run ceph -v
Ceph should show 0.93+ (this mean some version,
greater that 0.93) version.

Documentation Impact
====================

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/ceph-module
