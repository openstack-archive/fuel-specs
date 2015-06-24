This work is licensed under a Creative Commons Attribution 3.0 Unported
License.

http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
split fuel-web repository
==========================================

https://blueprints.launchpad.net/fuel/+spec/split-fuel-web-repo

The fuel-web repository currently contains lots of projects which should be
maintained independently: fuel_agent, nailgun, network_checker, shotgun,
tasklib, fuelmenu, and more. This blueprint is about splitting this unique
repository into several.

Problem description
===================
As a result of the current situation (many components into a single git
repository), it's hard to package fuel-web in a proper way, and there's no
proper versionning of each element. Separating them will make it possible to
build each individual component individually. Also, in the current form, it's
very hard to package the fuel-web repository for distributions.

Proposed change
===============
Create and maintain individual components in a separated Git repository. Here
is a list:
- fuel_agent
- nailgun
- keystone javascript client
- fuel UI
- network_checker
- shotgun
- tasklib
- fuelmenu

Alternatives
------------

None.

Data model impact
-----------------

None.


REST API impact
---------------

None.


Upgrade impact
--------------

None.


Security impact
---------------

None.


Notifications impact
--------------------

None.


Other end user impact
---------------------

None.


Performance Impact
------------------

None.


Plugin impact
-------------

None.


Other deployer impact
---------------------

Community users get Fuel ISOs with master Openstack.


Developer impact
----------------

Fuel developers will need to write paches on each individual projects instead
of the general fuel-web.


Infrastructure impact
---------------------

Creating CI tests for each individual projects, and building independent
packages.


Implementation
==============

Assignee(s)
-----------

Primary assignee: TBD


Work Items
----------

* Create individual repository, as fork of the fuel-web repository.
* Build individual packages out of the new repositories.
* Create `Fuel Jenkins`_ jobs to build ISOs out of that.
  

Dependencies
============

None.

Testing
=======

Packages built with these jobs will be tested for installation only,
and then tested with other components of the former fuel-web.


Documentation Impact
====================

None.


References
==========

None.


.. _`Fuel Jenkins`: http://ci.fuel-infra.org
