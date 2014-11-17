..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Create default templates for Sahara
===================================

https://blueprints.launchpad.net/fuel/+spec/sahara-create-default-templates

Automatically creating plugins templates for Sahara

Problem description
===================

A detailed description of the problem:

* Currently after succesfull deploying OpenStack with Sahara we should
  create templates for Sahara plugins manually. But for the proper setup
  of cluster must know Sahara plugins. That's why we need to give possibility
  automatic creation of Sahara plugins templates.

Proposed change
===============

Automatic creation of Sahara plugins templates can be implemented by
adding Sahara post-install script, which will add templates for the
next Sahara plugins:

* Vanilla;
* HortonWorks Data Platform (HDP);
* Cloudera distribution Hadoop (CDH);

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

This is needed in changes in puppet scripts. We should add script, which
will be run after installing Sahara, network provider (Neutron or Nova-Network).

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Users will interact with this feature after OpenStack deployment.

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

Primary assignee:
  degorenko

Work Items
----------

* Add example templates for Sahara plugins (degorenko)
* Add script, which will create templates for Sahara
  from example templates (degorenko)
* Edit puppet scripts to use this script (degorenko)

Dependencies
============

None

Testing
=======

Testing approach:

* Deploy OpenStack with Sahara
* Open Sahara Dashboard (Data Processing), 
  open tab Cluster/Node Group Templates
* Check that templates were created

Documentation Impact
====================

To Sahara docs will be added note about auto creating templates.

References
==========

None
