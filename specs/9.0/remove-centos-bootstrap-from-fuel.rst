..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Example Spec - The title of your blueprint
==========================================

https://blueprints.launchpad.net/fuel/+spec/remove-centos-bootstrap-from-fuel


--------------------
Problem description
--------------------

Since Fuel 8.0 we are switched to Ubuntu bootstrap image usage [1]_ and CentOS
one became deprecated, so in Fuel 9.0 we can freely remove it [2]_.

By removing fuel-bootstrap-image [2]_ we:

* simplify patching/update story, since we don't need to rebuild/deliver this
  package on changes in dependent packages [3]_.

* speed-up ISO build process, since building centos bootstrap image takes ~ 20%
  of build-iso time.


----------------
Proposed changes
----------------

Here is where you cover the change you propose to make in detail. How do you
propose to solve this problem?

If this is one part of a larger effort make it clear where this piece ends. In
other words, what's the scope of this effort?

Web UI
======

None


Nailgun
=======

General changes to the architecture, tasks and encapsulated business logic
should be described here.

Data model
----------

None


REST API
--------

None


Orchestration
=============


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

We no longer need to deliver/update fuel-bootstrap-image package [2], this will
simplify patching/update story, since we don't need to rebuild this package on
each changes in any dependent packages [3]_:

  * fuel-agent;
  * nailgun-agent;
  * nailgun-mcagents;
  * network-checker;
  * rubygem-ffi-yajl;
  * rubygem-ffi;
  * rubygem-mime-types;
  * rubygem-mixlib-shellout;
  * rubygem-wmi-lite.


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

* ISO build time decreased at least for ~20%

* The OpenStack nodes themselves are not affected in any way


-----------------
Deployment impact
-----------------

Discuss things that will affect how you deploy and configure Fuel
that have not already been mentioned, such as:

* What configuration options are being added? Should they be more generic than
  proposed? Are the default values ones which will work well in
  real deployments?

* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

* If this change is a new binary, how would it be deployed?

* Please state anything that those doing continuous deployment, or those
  upgrading from the previous release, need to be aware of. Also describe
  any plans to deprecate configuration values or features.  For example, if a
  directory with instances changes its name, how are instance directories
  created before the change handled?  Are they get moved them? Is there
  a special case in the code? Is it assumed that operators will
  recreate all the instances in their cloud?


----------------
Developer impact
----------------

Discuss things that will affect other developers working on Fuel,
such as:

* If the blueprint proposes a change to the driver API, discussion of how
  drivers would implement the feature is required.


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

Changes should be reflected in documentation.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Sergey Kulanov`_


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

This should include changes / enhancements to any of the integration
testing. Most often you need to indicate how you will test so that you can
prove that you did not adversely effect any of impacts sections above.

If there are firm reasons not to add any other tests, please indicate them.

After reading this section, it should be clear how you intend to confirm that
you change was implemented successfully and meets it's acceptance criteria
with minimal regressions.

Acceptance criteria
===================

Please specify clearly defined acceptance criteria for proposed changes.


----------
References
----------

.. _`Sergey Kulanov`: https://launchpad.net/~skulanov

.. [1] `Use Ubuntu as an operating system of Fuel bootstrap nodes <https://blueprints.launchpad.net/fuel/+spec/fuel-bootstrap-on-ubuntu>`_
.. [2] `fuel-bootstrap-image RPM package spec <https://github.com/openstack/fuel-main/blob/master/packages/rpm/specs/fuel-bootstrap-image.spec>`_
.. [3] `fuel-bootstrap-image dependencies <https://github.com/openstack/fuel-main/blob/master/bootstrap/module.mk#L12-L50>`_
