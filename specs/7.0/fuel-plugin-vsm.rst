..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================================
Manage Fuel-deployed Ceph using Virtual Storage Manager
=======================================================

https://blueprints.launchpad.net/fuel/+spec/manage-fuel-deployed-ceph-using-vsm

Provide a Fuel-plugin that deploys VSM as it provides a unified view of
a Ceph storage system. Its web interface provides an operator with the ability
to monitor overall cluster status, inspect detailed operation status of Ceph
subsystems and manage Ceph interoperation with OpenStack Cinder.

Problem description
===================

Fuel-deployed Ceph does not have any GUI-tool to monitor the cluster.

Proposed change
===============

Virtual Storage Manager is by far the most perspective graphical management
tool for Ceph. A Fuel-plugin that deploys VSM is proposed.

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
  rzarzynski

Other contributors:
  kdanilov, akiselyova, diurchenko, mgolub

Work Items
----------


Dependencies
============


Testing
=======


Documentation Impact
====================


References
==========
