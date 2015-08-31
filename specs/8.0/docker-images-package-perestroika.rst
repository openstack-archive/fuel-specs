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
     -> MOS Infra (Verified +1)
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

None

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

Expected and known impact to OSCI should be described here. Please mention
whether:

* There are new packages that should be added to the mirror

* Version for some packages should be changed

* Some changes to the mirror itself are required


--------------
Implementation
--------------

Assignee(s)
===========

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

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


------------
Testing, QA
------------

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly.

If there are firm reasons not to add any other tests, please indicate them.


Acceptance criteria
===================

Please specify clearly defined acceptance criteria for proposed changes.


----------
References
----------

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
