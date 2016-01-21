..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Unit Tests Inside Docker Containers
==========================================

https://blueprints.launchpad.net/fuel/+spec/unit-tests-inside-docker

For the terms of security, isolation, reliability and tolerance of test
environments we need to run all unit tests in isolation from Hardware Node.
Introducing Docker containers to our CI will allow us to achieve this.

--------------------
Problem description
--------------------

Various unit tests require different python packages and environment setup,
which sometimes leads to dependencies intersection and therefore to conflicts.
Another problem is the execution of test code, which is done in non-isolated
environment and can cause security concerns.

----------------
Proposed changes
----------------

TODO: turn those terms to text paragraphs.
- Docker containers are going to be used to provide us with environment
isolation.
- How the containers are going to be prepared?
- How the tests are going to be technically run?
- Ability to save (commit) container state to an image to investigate possible
environment errors and failed tests.
- Store these saved images in Docker Registry so they could be grabbed at any
time.
- Make sure old and unused iamges are destroyed to control disk space.

Here is where you cover the change you propose to make in detail. How do you
propose to solve this problem?

If this is one part of a larger effort make it clear where this piece ends. In
other words, what's the scope of this effort?

Web UI
======

None

Nailgun
=======

None

Data model
----------

None

REST API
--------

None

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

Test isolation can also be achieved using virtualization technology like KVM,
though we are going to face higher resource overhead than while using
containers. There is also a way to preserve failed tests state in the form of
virtual machines snapshots, but they would require more disk space to store
and also more time to download and start.
The strongest part of KVM (and any other virtualization technology) is
lower level of isolation and thus - higher security. 
Stil, we think that easier to use and deploy containers are in fact have more
pros than cons.

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

Docker containers are said to be secure, but there are some recommendations
which should be followed in order to lessen security risks (like running
processes inside containers as non-root users, mostly because there is no user
ID isolation and root user can interact with host's kernel with root
privileges). More information can be obtain with official Docker
documentation: https://docs.docker.com/engine/articles/security/


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None

------------------
Performance impact
------------------

TODO

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

TODO

---------------------
Infrastructure impact
---------------------

TODO

--------------------
Documentation impact
--------------------

TODO

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  TODO

Work Items
==========

TODO

Dependencies
============

TODO

------------
Testing, QA
------------

TODO

Acceptance criteria
===================

TODO

----------
References
----------

TODO
