..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================
Refactor cinder-vmware role
===========================

https://blueprints.launchpad.net/fuel/+spec/refactor-cinder-vmware-role

Introduction paragraph -- why is it necessary to do anything?


--------------------
Problem description
--------------------

A detailed description of the problem:

* For a new feature this might be use cases. Ensure you are clear about the
  actors in each use case: End User vs Deploy engineer

* For a major reworking of something existing it would describe the
  problems in that feature that are being addressed.


----------------
Proposed changes
----------------

Here is where you cover the change you propose to make in detail. How do you
propose to solve this problem?

If this is one part of a larger effort make it clear where this piece ends. In
other words, what's the scope of this effort?

Web UI
======

None.


Nailgun
=======

None.

Data model
----------

None.


REST API
--------

None.


Orchestration
=============

None.


RPC Protocol
------------

None.


Fuel Client
===========

None.


Plugins
=======

None.


Fuel Library
============

Are some changes required to Fuel Library? Please describe in details:

* Changes to Puppet manifests

* Supporting scripts

* Components packaging


------------
Alternatives
------------

What are other ways of achieving the same results? Why aren't they followed?
This doesn't have to be a full literature review, but it should demonstrate
that thought has been put into why the proposed solution is an appropriate one.


--------------
Upgrade impact
--------------

None.


---------------
Security impact
---------------

None.


--------------------
Notifications impact
--------------------

None.


---------------
End user impact
---------------

Aside from the API, are there other ways a user will interact with this
feature?

* Does this change have an impact on python-fuelclient? What does the user
  interface there look like?


------------------
Performance impact
------------------

None.


-----------------
Deployment impact
-----------------

None.


----------------
Developer impact
----------------

None.


--------------------------------
Infrastructure/operations impact
--------------------------------

None.


--------------------
Documentation impact
--------------------

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.


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

None.


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
