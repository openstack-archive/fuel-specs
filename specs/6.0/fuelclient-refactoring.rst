==========================
Refactoring for fuelclient
==========================

https://blueprints.launchpad.net/fuel/+spec/refactoring-for-fuelclient

We need to perform refactoring for fuelclient for improving reusability for
its code base and gain more control for both whole system and particular parts
of it.

Problem description
===================

Now there are several issues in architecture of the project which cause
difficulties in maintaining, implementing new logic and reusing existing
code. These parts are:

* APIclient code for maintaining http communication with nailgun server;
  now slightly obsolete python module urllib2 is using so code for request
  operations is pretty excessive

* Formatter for console output; own written invention so it is hard to dive
  into, also not flexible for future changes

* Objects hierarchy; is overwhelming with many interconnections
  between objects, may be simplified

* Tests coverage; now only limited set of tests that check simple use
  cases is present, so it must be extended and if possible whole testing
  system should be rewritten to meet OS best practices in cli testing.

Proposed change
===============

There are several proposes for every problem mentioned in previous section:

* substitute urllib2 with requests module, this will leads to more simplified
  code in APIclient

* include cliff framework for cli and formatter part of the system

* perform minor refactoring when it needed.

Alternatives
------------

All other basic tools such argparse or docopt doesn't suffice in case of
fuelclient because we need to implement our own object hierarchy instead of
using base classes of framework which leads to complicated structure as that
we have now. There also others framework for building cli application
(e.g. http://click.pocoo.org/) but chosen tools are wide using in OS community
and are best practices for building OS related application.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Refactoring requires some additional packages to be installed on master node
so they should be present after upgrade to version which includes change
upon the table.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

End users workflow may be affected as interface of system
will be changed so adequate documentation must be provided for them

Performance Impact
------------------

None

Other deployer impact
---------------------

One should add needed rpm's to fuelclient spec. Packages must be already
present in repos.

Developer impact
----------------

After refactoring particular parts of the system may be reused in other
projects when such functionality is needed as ostf, system tests etc.
Also using cliff simplifying addition of new cli actions trough
mechanism of entry points for package.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  aroma-x

Work Items
----------

Whole task may be divide into following separate changes:

* plugging requests

* plugging cliff


Dependencies
============

Refactoring relies on additional package - python-cliff

Testing
=======

As purpose of the refactoring is to bring well recommended itself in OS
community technologies and tools it is naturally that testing system must be
changed too in order to use best practices from corresponding OS development
area, i.e. testing of cli clients. Also current coverage of use cases must be
extended as it is not enough for such big project as nailgun.

Documentation Impact
====================

Interface of fuelclient may be changed after refactoring so it must be
mirrored into corresponding documentation

References
==========

Cliff documentation:
http://cliff.readthedocs.org/en/latest/

Requests documentation:
http://docs.python-requests.org/en/latest/
