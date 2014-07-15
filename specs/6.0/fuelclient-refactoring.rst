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

Proposed change
===============

There are several proposes for every problem mentioned in previous section:

* substitute urllib2 with requests module, this will leads to more simplified
  code in APIclient

* rewrite objects hierarchy using cliff framework, also substitute existing
  formatter with default for cliff.

* perform minor refactoring when it needed.

Alternatives
------------

There is no other frameworks for building cli applications except cliff.
All other tools such argparse or docopt doesn't suffice in case of fuelclient
because we need to implement our own object hierarchy instead of using
base classes of framework which leads to complicated structure as that we have
now. Also chosen tools are wide using in OS community and are best practices
for building OS related application.

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

Change should be tested manually in order to verify that provided before
change functions of fuelclient are available after refactoring.

Documentation Impact
====================

None

References
==========

None
