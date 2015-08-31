..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================================================
Build fuel-docker-images package using Perestroika
==================================================

https://blueprints.launchpad.net/fuel/+spec/docker-images-perestroika

--------------------
Problem description
--------------------

Currently we build fuel-docker-images RPM package together with ISO.
Our intention for the future is to get rid of building any packages during
ISO building. Fuel-docker-images package is so called Level 2 package (it
depends on other RPM packages) and it usually takes 10-15 minutes to
build this package which makes it impossible to build this package
the same way as other packages using conventional Perestroika flow.
We need to implement a separate job(s) to build this package and
run this job periodically unlike other jobs which are gerrit driven.


----------------
Proposed changes
----------------

#. Split docker images build code from everything else in fuel-main project,
   so as to make it possible to build docker containers from remote
   repositories passed as parameters.

#. Create Level 2 Perestroika instance. It is going to be a set of jobs
   defined in files:
   - mos.build.fuel.rpm.level2.yaml
   - mos.build.fuel.rpm.level2.request.yaml

#. Include Level 2 Perestroika instance in the Packaging CI. The triggering
   flow is going to be like this

::

   Code Review (CR)
   (A developer sends review request)
     -> Fuel CI (Verified +1)
        (Unit tests)
        -> Packaging CI (Packaging +1)
           (Perestroika builds Level 1 package[s])
           -> Packaging CI (Level 2 Packaging +1)
              (Perestroika builds Level 2 packages)
              -> Packaging CI (Verified +2)
                 (System tests)
                 -> Workflow +1

The same is for merge gates.

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

None

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

None

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

None

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

As far as fuel-docker-images package is the only L2 package which is going to
be a part of Fuel release 8.0 and it will be built by Perestroika, ISO build
time can be significantly reduced which is going to make test feedback loop
much shorter.

--------------------------------
Infrastructure/operations impact
--------------------------------

fuel-docker-images package (level 2 package) depends on other packages and is
going to be build for almost every review request. Building this package
usually takes 10-15 minutes and we should have enough workers to deal with
such quite high load. It is approximately one third of resources necessary for
packaging system tests.

--------------------
Documentation impact
--------------------

It should be described in the documentation that level 2 packages are built
using Perestroika scripts and hardware capacity but level 2 jobs are to
be triggered continuously (not by gerrit). Once build is finished,
next build is to be started with last available snapshot repository.


--------------------
Expected OSCI impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>

Work Items
==========

#. Split docker part of fuel-main from other parts so it is possible to build
   docker images independently.
#. Create jobs in Packaging CI to build fuel-docker-images package

Dependencies
============

None

------------
Testing, QA
------------

Same as before.

Acceptance criteria
===================

fuel-docker-images package should be available for downloading from Perestroika
mirrors like all other packages. So, it is supposed that during ISO building
this package will be downloaded as is and put into ISO.

----------
References
----------

None
