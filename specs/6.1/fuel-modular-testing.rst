..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
Fuel Modular Testing Framework
==============================

https://blueprints.launchpad.net/fuel/+spec/fuel-library-modular-testing

Implement modular testing framework to perform functional and integration
testing of puppet modules.

Problem description
===================

In order to increase engineering velocity and testing coverage we need
to add intermediate level of testing that will allow us to test particular 
puppet modules or integration of particular modules.

Proposed change
===============

With this framework we introduce the opportunity to run particular
puppet manifests on the nodes in the environment after particular
dependencies are completed. E.g. in order to test neutron deployment
manifests changes we get an environment which already has all the 
prerequisites executed (base OS, networking, mysql, rabbit, keystone)
which is presumable going to be saved into VM snapshot, then we revert
the corresponding snapshot, sync system time, upload new manifests to
the master node and then deploy corresponding role. After deployment is
complete, we execute a bunch of tests which verify that corresponding
module deployed what we want and in a way that we want.

Alternatives
------------

There are no such frameworks at the moment

Data model impact
-----------------

None

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

Dmitry Ilyin aka ~idv1985
TBD: Someone from  QA team
Aleksandr Didenko aka ~adidenko

Work Items
----------

To be filled


Dependencies
============

Strong Dependency: https://blueprints.launchpad.net/fuel/+spec/granular-deployment-based-on-tasks
Weak Dependency: https://blueprints.launchpad.net/fuel/+spec/fuel-library-modularization

Testing
=======

TBD

Documentation Impact
====================

Corresponding testing documentation should be introduced

References
==========

https://blueprints.launchpad.net/fuel/+spec/fuel-library-modularization
https://blueprints.launchpad.net/fuel/+spec/granular-deployment-based-on-tasks
https://docs.google.com/a/mirantis.com/document/d/1GJHr4AHw2qA2wYgngoeN2C-6Dhb7wd1Nm1Q9lkhGCag/edit

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
