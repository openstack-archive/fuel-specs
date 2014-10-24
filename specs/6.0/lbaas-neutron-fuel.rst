..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Neutron LBaaS support for Fuel
==========================================

https://blueprints.launchpad.net/fuel/+spec/lbaas-neutron-fuel


Problem description
===================

Neutron/LBaaS getting more stabilized after Icehouse and Juno releases.
Despite more advanced feature still under developing, the basic LBaaS is
already stable and seems have no critical issues on it. Therefore it should
be supported in Fuel.

Proposed change
===============

* Puppet modules

  * Add LBaaS agent module in Neutron
  * Add ocf file for LBaaS
  * Add LBaaS service plugin in sanitize_neutron_config
  * Modify horizon setting.py to enable LBaaS
  * Add LBaaS config with default Neutron LBaaS setting
  * Add LBaaS agent procedure entry in neutron_router module
  * Add LBaaS required service provider in neutron config. This currently
    lead to HAProxy as service provider

* Feul Web

  * Add list pool in sanity test
  * Add create pool in functional test

Alternatives
------------

There is manual way to adding Neutron/LBaaS in Fuel(https://docs.google.com/do
cument/d/1OZy8cA3dpsDFDygcAZz2ZPrUyHEjBjNFnfG1eJoQh-g/edit), but we should not
add any services after Fuel depolyment procedure been considered done.

Data model impact
-----------------

* Add setting for LBaaS config
* Modify enable_lbaas setting default value to True
* Add LBaaS service provider and service plugin setting in Neutron config

REST API impact
---------------

None

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

Fuel user can check and run relative tests insdie Health Check on Fuel web.

Performance Impact
------------------

* LBaaS installation procedure increase Fuel total developing time.

Other deployer impact
---------------------

None

Developer impact
----------------

* Current LBaaS package doesn't supported with in Redhat's OS.

Implementation
==============

Assignee(s)
-----------

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  rico-lin

Other contributors:
  None

Work Items
----------

* Puppet modules

  * Add LBaaS agent module in Neutron
  * Add ocf file for LBaaS
  * Add LBaaS service plugin in sanitize_neutron_config
  * Modify horizon setting.py to enable LBaaS
  * Add LBaaS config with default Neutron LBaaS setting
  * Add LBaaS agent procedure entry in neutron_router module
  * Add LBaaS required service provider in neutron config. This currently
    lead to HAProxy as service provider

* Feul Web

  * Add list pool in sanity test
  * Add create pool in functional test

* LBaaS deploy test 3d

Dependencies
============

None

Testing
=======

Test should added at Health check in Fuel web. This include list pool in
sanity test and create pool in functional test

Documentation Impact
====================

* Fuel Archtecture Guide have to notify that LBaaS is installed
* Modify configuration guide with LBaaS relative configurations
* LBaaS test must be add to any document that listing test objects
* LBaaS must be mentioned at all Neutron section in Fuel Document

References
==========

http://docs.openstack.org/admin-guide-cloud/content/install_neutron-lbaas-agent.html
https://docs.google.com/document/d/1OZy8cA3dpsDFDygcAZz2ZPrUyHEjBjNFnfG1eJoQh-g/edit
