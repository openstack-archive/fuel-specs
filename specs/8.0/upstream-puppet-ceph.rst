.. -*- coding: utf-8 -*-

..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================
Upstream Puppet-Ceph
====================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/fuel-upstream-ceph

Problem description
===================

As we have moved under Big Tent, we should stop using self-written ceph puppet
module and proceed with upstream openstack/puppet-ceph module instead.

Proposed change
===============

We would like to rewrite ceph related puppet modular task in order to use new
ceph module. 

Alternatives
------------

* pros:
  * we will be using community module that is being maintained by lots of ceph
SME.

* cons:
  * upstream module is not very flexible yet, but almost suits our needs. 


Data model impact
-----------------

TBD


REST API impact
---------------

None


Upgrade impact
--------------

No need to upgrade, because end state is supposed to be the same.


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

TBD


Implementation
==============


Assignee(s)
-----------

Primary assignee:

Work Items
----------

* Write fuel modular tasks for ceph infrastructure deployment
* Write noop tests to cover changes

Dependencies
============

* Upstream ceph* rpm/dpkg packages

Testing
=======

Acceptance criteria:

* should pass BVT, that contains ceph related tests

Documentation Impact
====================

None
