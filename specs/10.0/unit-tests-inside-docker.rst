..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Unit tests inside Docker containers
===================================

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

Fuel unit tests will be run on Docker containers which in turn are run on
Jenkins CI slaves. This allows us to use pre-configured environments with set
of packages we need, which is done by setting requirements in Dockerfiles and
build scripts, instead of Puppet manifests or installing packages while tests
are run. Current unit tests can use PyPi caching proxies if using tox, same
approach works for Ruby and npm packages, which does not requre lot of changes
to unit tests configuration. Containers will be rebuilt in two cases: on
changes to Dockerfiles (i.e. environment) with additional scripts and on
timer. These containers are checked for passing unit test and then pushed to
Docker Registry, from where they are pulled to Jenkins CI slaves and run Fuel
repositories unit tests, just like on Fuel CI, triggered by Gerrit.
Jenkins jobs which run tests will have optional parameter to commit and push
failed containers to images on Docker Registry, so developers and engineers
can then pull them and investigate.

-------------
Naming policy
-------------

Docker images generally are named after job basename. So for fuel-web unit
tests there are gate-fuel-web and verify-fuel-web jobs which use fuel-web
Docker image, e.g.:
- verify-fuel-web-ui job -> fuel-web-ui image
- gate-fuel-web job      -> fuel-web image
- fuellib_noop_tests job -> fuellib_noop_tests image

--------------
Version policy
--------------

Docker images can have prefix if stable branches are used, for example tests
for 8.0 branch of python-fuelclient will run from 8.0.python-fuelclient Docker
image and if master branch is used, no prefix applies.

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

Developers can update Docker containers environments images by sending patches
for Dockerfiles and/or runner scripts.

---------------------
Infrastructure impact
---------------------

* Requires additional storage on Docker Registry for saved contaner's images.
* Requires additional disk space on slaves for pulled images.
* Increses network traffic between storage server and slaves for pushed
  images.

--------------------
Documentation impact
--------------------

* Writing Dockerfiles and runners
* Running unit tests using standalone Docker containers on local machines.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Anton Tcitlionok (atcitlionok): atcitlionok@mirantis.com

Mandatory design reviewers:
  Aleksandra Fedorova (afedorova): afedorova@mirantis.com
  Nastya Urlapova (aurlapova): aurlapova@mirantis.com
  Tatyana Leontovich (tatyana-leontovich) tleontovich@mirantis.com
  Dennis Dmitriev (ddmitriev) ddmitriev@mirantis.com

Work Items
==========

* Documentation for developers

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
