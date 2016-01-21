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
which sometimes leads to dependency conflicts.
Another problem is the execution of test code, which is done in non-isolated
environment and may cause security concerns.

----------------
Proposed changes
----------------

- Docker containers will be used to provide environment isolation.
- Tests will run using pre-configured environments (like virtualenv,
  databases) out-of-the-box.
- Environments will be recreated on regular basis and on changes to
  test-requirements.
- Containers state will be saved (commited) to an image to investigate
  possible environment errors and failed tests.
- Store these saved images in Docker Registry so they could be grabbed at any
  time.

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
higher level of isolation and thus - higher security.
We think with containers' ease of use and deploy they have more pros than
cons.

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

Current version of Docker is said to be secure, but there are some
recommendations which should be followed in order to lessen security risks
(like running processes inside containers as non-root users, mostly because
there is no user ID isolation without user namespaces and root user can
interact with host's kernel with root privileges). More information can be
obtained with official Docker documentation:
https://docs.docker.com/engine/articles/security/

Note: user namespaces are to be included in Docker 1.10.

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

* Decreases time required for running tests due to deployed images with
  preconfigured tests environments.

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

* Requires additional storage on Docker Registry for saved contaner's images,
  this should be covered by devops.
* Requires additional disk space on slaves for pulled images.
* Increses network traffic between storage server and slaves for commited
  images.

--------------------
Documentation impact
--------------------

Requires to create documentation on preparing Dockerfiles for tests,
containers deployment, running tests, saving and storing images.
Documentation should also include instructions on creation of dockerized jobs
for stable and master branches.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Anton Tcitlionok (atcitlionok): atcitlionok@mirantis.com

Work Items
==========
* Create containers for unit tests for master branches (dockerfiles with
  prepared environment).
* Create Jenkins jobs with Docker runner, single YAML should be used.
* Make documentation on containers creation for unit tests for stable
  branches.

Dependencies
============

None

------------
Testing, QA
------------

None

Acceptance criteria
===================

* All unit tests are run in Docker containers with all dependencies
  installed using jenkins jobs.
* Tests environments results can be saved and downloaded over the network.
* There is no access to hardware from container.
* Images creation, configuration and CI infrastructure for containers are
  documented.

----------
References
----------

None
