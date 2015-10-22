..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Cinder Block Device driver
==========================================

https://blueprints.launchpad.net/fuel/+spec/TBD

Problem description
===================

In production for better performance for Hadoop should use direct
attached HDD to VM. For attaching disks directly need to use
BlockDeviceDriver in Cinder. Right now user should use Fuel plugin
for using this feature.

Proposed changes
================

For implementing this feature we need to add a new node role. It should
be available to do through Web UI. After we will add node with such role
(e.g. Cinder-Block-Device Storage), we need to choose disks, wich should
used for this role. Those disks should be used only for this role. So it
assumes that for choosed node available at least two disks. Also,
another roles (like, Cinder LVM and Ceph OSD) should be unavailable for
our node. Also we need one more restriction - our role should conflict
with controller.

When all configuration is done, all information about our new role and
choosed disk should be serialized by Nailgun and passed to nodes in Astute
yaml config. So, that assumes that Nailgun should be able to serialize a new
data - disks for our role and passed it to Astute.

Example of yaml file:

.. code-block:: yaml

   - cinder-block-devices:
      node-2: /dev/sdb, /dev/sdc
      node-3: /dev/sdb, /dev/sdg
      node-4: /dev/sdy

Also should be updated Puppet side by adding a new task for new role,
wich will be runned only on Cinder-Block-Device Storage nodes. Puppet
manifests will configure all needed files, services and install all
needed packages.

We don't need to build any new packages, because this driver already
implemented in Cinder and we should just enable it and configure
properly.

According description above we have next steps:
- Add a new node role on Web UI;
- Allocate only full disks for our role and check that role has at
least two disks;
- Add a new feature to Nailgun API, which will serialize our data and
then pass it to astute;
- Add a new Puppet task and manifests for deploy.


Web UI
======

Add a new node role and check disks.


Nailgun
=======

Add ability to serialize a new data: which disks are allocated for
our role. Then pass it to Astute.


Data model
----------

None


REST API
--------

None


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

None


Fuel Library
============

Add a new Puppet task, which will runned only on appropriate nodes.
Add new puppet manifests for deploying this feature.


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

None


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None


------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

None


----------------
Developer impact
----------------

None


--------------------------------
Infrastructure/operations impact
--------------------------------

Need add one more job and tests, which will cover a new
deployment scheme. No any additional actions.


--------------------
Documentation impact
--------------------

All infrastructure changes should be documented


--------------------
Expected OSCI impact
--------------------

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Denis Egorenko`_


Mandatory Design Reviewers:
  - `Sergey Reschetnyak`_
  - `Nikita Konovalov`_


Work Items
==========

* Implement related changes to Fuel Web UI and Nailgun

* Implement related changes to Fuel Library

* Implement related changes to Fuel OSTF and CI tests;


Dependencies
============

None


------------
Testing, QA
------------

Introduced changes should be covered by system tests.

QA engineers:
  `Evgeny Sikachev`_


Acceptance criteria
===================

* Disks attached to VM without LVM

* If VM and disk on the same host then necessary check that libvirt
uses virtio driver instead iSCSI for attached disk.


----------
References
----------

.. _`Denis Egorenko`: https://launchpad.net/~degorenko
.. _`Sergey Reschetnyak`_:
.. _`Nikita Konovalov`:
.. _`Evgeny Sikachev`:
