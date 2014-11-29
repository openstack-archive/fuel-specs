..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================
 Code testing policy 
======================

https://blueprints.launchpad.net/fuel/+spec/code-testing-improvements

Current unit/integration tests should follow a single code testing policy.

Introduction paragraph -- why are we doing anything? A single paragraph of
prose that operators can understand.

Problem description
===================

Right now ``fuel-web`` project doesn't have:

 * a strict rules of how the code is tested

 * which testing approach is used for particular component 

 * tests composition rules 

 * test grouping

 * unit and functional tests are located in a mess and don't correspond
   their purpose


Proposed change
===============


Each push request must have a test which makes sure the code is working. Push
request is not merged in master until the functionality hasn't been covered
with the tests. The component module/class/function can be tested in different
ways and can have a set of unit/functional/integration tests.

Every component has be covered with unit tests.

The components to be covered with integration tests:

* REST API handlers

* Database interaction

Unit tests are located in ``tests/unit/`` directory. The structure of unit
tests mimics the project one.
Integration tests are located in ``tests/integration`` and grouped by
components name.

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



Describe any potential performance impact on the system, for example
how often will new code be called, and is there a major change to the calling
pattern of existing code.

Examples of things to consider here include:

* A periodic task might look like a small addition but if it calls conductor or
  another service the load is multiplied by the number of nodes in the system.

* Scheduler filters get called once per host for every instance being created,
  so any latency they introduce is linear with the size of the system.

* A small change in a utility function or a commonly used decorator can have a
  large impacts on performance.

* Calls which result in a database queries (whether direct or via conductor)
  can have a profound impact on performance when called in critical sections of
  the code.

* Will the change include any locking, and if so what considerations are there
  on holding the lock?

Other deployer impact
---------------------

None

Developer impact
----------------

Developers have to follow the code testing policy

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ivankliuk

Other contributors:
  fuel-python

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


Testing
=======

This document describes testing itself.

Documentation Impact
====================

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.


References
==========

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
