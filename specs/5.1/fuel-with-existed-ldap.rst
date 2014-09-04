..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================
Fuel with existed ldap
================================

https://blueprints.launchpad.net/fuel/+spec/fuel-with-existed-ldap


Problem description
===================

Currently the OpenStack environment deployed by Fuel only supports SQL for
the Keystone identity backend. In some cases we already have our own LDAP
authentication service and we prefer not to maintain two authentication
services in the our environment. Therefore, it would be beneficial to
support LDAP identity backend too. Given that the Keystone team considers
SQL as the preferred assignment backend, the idea of LDAP assignment backend
is against it and therefore we prefer using SQL as assignment backend with no
switch option.


Proposed change
===============

We could let Fuel to switch identity backend by adding setting options at
cluster wizard page as a trigger which allowing deployers to choose their own
identity backend with SQL, or pre-existing LDAP server. We also need an
aditional setting block inside cluster setting tab for fill up LDAP detail
connection information include LDAP server administrator information, identity
domain scope, connection info, etc. Inside the connection info, user can
provide the user accounts from LDAP to Fuel after they decided which account
inside LDAP should be administrator to which service in Openstack. An test
connection button or link shloud be added inside cluster setting tab too, to
validate the settings.


Alternatives
------------

We can do nothing, but a deployer will not be able to use their pre-existed
LDAP as a identity backend for Openstack.


Data model impact
-----------------

We have to store following data in settings:

* The LDAP connection URL and login information.

* Each service correspond administrative account and its password in LDAP
  server.


REST API impact
---------------

No REST API modifications needed.


Upgrade impact
--------------

I see no objections about upgrades. LDAP connection are based on LDAP
identity driver which is a part of official set of identity drivers. So any
upgrades should be done in a common way.


Security impact
---------------

LDAP traffic exchanged in clear-text could be bad for some customers. It
would be worth to add a section on LDAP over SSL.


Notifications impact
--------------------

Some modifications of the Cluster Creation Wizard needed. Add setting options
for switching identity backend purpose. Need an aditional setting block
inside cluster setting tab for fill up LDAP detail connection information
and a services administrator assigning forms for fill up administrator
assignment form LDAP account to Openstack environment.


Other end user impact
---------------------

Deployer will be able to switch to their own pre-existed LDAP with Cluster
Creation Wizard in Fuel deployment. As an operation requirement, if
pre-existed LDAP selected, Deployer must fill up more detail information in
cluster setting tab.


Performance Impact
------------------

None.


Other deployer impact
---------------------

None.


Developer impact
----------------

The Configuration pattern of Keystone with LDAP backend will be different
from original sql backend. We change identity backend and assign
administrator for each services and default project. This should be care
for while developing relatived patterns.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  cy-lee

Other contributors:
  rico-lin


Work Items
----------

* Modify Cluster Creation Wizard page. Add switching identity backend option
  and test it.

* Modify Cluster setting tab. Add ldap connection information forms and test
  it.

* Modify Cluster setting tab. Add services administrator assigning forms and
  test it.

* Modify Keystone configuration pattern with Ldap backend information and
  test it.

* Modify all services configuration pattern with assigning administrator
  account from LDAP and test it.

* Create a pull request to Gerrit.

* Describe a test environment and additional System tests and discuss it in
  ML.

* Set up a test environment and provide System tests.
* Set up additional Jenkins jobs for System tests.


Dependencies
============

None


Testing
=======

* Additional functional tests for UI.

* Additional functional tests for puppet script.

* Additional System tests against a stand alone test environment(with ldap).

wrapped up as a separate Jenkins thread job.


Documentation Impact
====================

The documentation should describe how to set up LDAP for a simple test
environment.


References
==========

http://docs.openstack.org/admin-guide-cloud/content/configuring-keystone-for-
ldap-backend.html

https://wiki.openstack.org/wiki/OpenLDAP


