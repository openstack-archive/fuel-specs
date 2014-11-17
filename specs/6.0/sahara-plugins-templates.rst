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

* Currently after succesful deployment of OpenStack with Sahara, templates
  for Sahara should be created manually. However, in order to determine if an 
  environment is properly configured, Sahara plugins are necessary.
  That is why this spec adds the possibility to create Sahara plugin templates.

Proposed change
===============

Automatic creation of Sahara plugins templates can be implemented by
adding a Sahara post-install script, which will add templates for the
following Sahara plugins:

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

It is necessary to ensure that obsolete templates are managed properly. For
now, templates have static names to ensure idempotency.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Users will be able to interact with this feature after OpenStack deployment.

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
* Add script which will create templates for Sahara
  from example templates (degorenko)
* Modify Sahara puppet module to make use this script (degorenko)

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

Upstream Sahara docs include notes about automatically creating templates.

References
==========

None
