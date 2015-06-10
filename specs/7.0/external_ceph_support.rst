..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================
Extended ceph support
=====================

The goal is to allow FUEL to connect to external ceph cluster.

Problem description
===================

Connectiong FUEL to external ceph cluster is a hightly requested customer feature.
Currently this can be done only ad-hoc by manually editing openstack config files
after deployment is done via FUEL.

Proposed change
===============

Update UI to allow user to provide external cluster credentials:

Add "external cluster" checkbocks. Selecting this checkbox would leads
to disabling ceph-osd role and enabling fields:

* "ceph client key", where user would put ceph client key content
* "mon ip(s)" for list of mon ip(s)
* "Using external radosgw" - checkbocks to use external radosgw

If "Using external radosgw" checkbocks is selected - additional
field "swift root url" was enabled.
All mentioned fields must be filled to save settings.

When external cluster selected next action would take a place:

 * Deployment of ceph-mon and ceph-osd is skipped
 * cinder-volume is deployed on controller, as now
 * User-provided ceph credentials is used for OS services
 * Radosgw might not be installed, depending on user settings

This would be done by updating puppet manifests.

Alternatives
------------

Data model impact
-----------------

External clusters info would need to be stored in DB. New fields
would be added to 'storage' part of astute.yaml 

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

UI changes would be required to allow user to provide
ceph cluster connection info and select ceph management tool.
Changes can be made by modifing openstack.yaml and would requires no
JS/HTML code to be changed.

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
  kdanylov

Other contributors:
  diurchenko, akiselyova, yportnova, gstepanov,rzarzynski

Work Items
----------

Dependencies
============

Testing
=======

UI should allows to enter external ceph cluster creds and FUEL should connect
OS to provided OS cluster

Documentation Impact
====================

Setting up external cluster connectin need to be documents.

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/ceph-module
.. [2] https://mirantis.jira.com/wiki/display/MOL/Ceph+API+for+FUEL
.. [3] https://github.com/01org/virtual-storage-manager