..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================
Move ceph code to external modue with clean API
===============================================

https://blueprints.launchpad.net/fuel/+spec/ceph-module [1]_

Currently ceph-related code is speaded across Nailgun code.
This makes it hard to update track and suport. Also customers
often requests external cluster support and allow to manage
ceph with 3rd party tools, like VSM [3]_.

Goals is to move ceph code into package inside Nailgun and prepare
if for making a plugin in next FUEL versions. Package should provide
clean API and allow to use external ceph clusters or deploy/manage ceph
with external tools.


Problem description
===================

* Ceph code embedded into many places in Nailgun, which makes it
  maintenance hard
* It's hard to provide external cluster support
* It's hard to deploy ceph with external tool
* Ceph partitioning logic is located in several places

Proposed change
===============

Move ceph code into package inside FUEL. Make package to provide 
clean API [2]_. New code would provides integration with 
VMS/Calamary/etc using plugin mechanism. All ceph partiotion management
logic would be moved into this module as well.


Alternatives
------------

Data model impact
-----------------

External clusters info would need to be stored in DB

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
Changes can be made by modifing upenstack.yaml and would requires no
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

Documentation Impact
====================


References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/ceph-module
.. [2] https://mirantis.jira.com/wiki/display/MOL/Ceph+API+for+FUEL
.. [3] https://github.com/01org/virtual-storage-manager