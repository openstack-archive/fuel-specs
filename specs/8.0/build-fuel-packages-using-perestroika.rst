..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================
Building Fuel packages using Perestroika
========================================

https://blueprints.launchpad.net/fuel/+spec/build-fuel-packages-using-perestroika

--------------------
Problem description
--------------------

We have a number of DEB and RPM fuel packages that one builds during ISO build
process. All these packages reside on stackforge [1]_:

.. _table:

+--------------------+-----------------------------+---------------------+
|    Repo-name       |       RPM packages          |   DEB packages      |
+====================+=============================+=====================+
| fuel-agent         | - fuel-agent                | - fuel-agent        |
+--------------------+-----------------------------+---------------------+
| fuel-astute        | - ruby21-rubygem-astute     | - nailgun-mcagents  |
|                    | - ruby21-nailgun-mcagents   |                     |
|                    | - nailgun-mcagents          |                     |
+--------------------+-----------------------------+---------------------+
| fuel-library       | - fuel-dockerctl            | - fuel-ha-utils     |
|                    | - fuel-ha-utils             | - fuel-misc         |
|                    | - fuel-library8.0           | - fuel-rabbit-fence |
|                    | - fuel-migrate              |                     |
|                    | - fuel-misc                 |                     |
|                    | - fuel-notify               |                     |
|                    | - fuel-rabbit-fence         |                     |
+--------------------+-----------------------------+---------------------+
| fuel-main          | - fuel                      |                     |
+--------------------+-----------------------------+---------------------+
| fuel-nailgun-agent | - nailgun-agent             | - nailgun-agent     |
+--------------------+-----------------------------+---------------------+
| fuel-ostf          | - fuel-ostf                 |                     |
+--------------------+-----------------------------+---------------------+
| fuel-web           | - fencing-agent             | - fencing-agent     |
|                    | - fuel-package-updates      | - nailgun-net-check |
|                    | - fuel-provisioning-scripts |                     |
|                    | - fuelmenu                  |                     |
|                    | - nailgun                   |                     |
|                    | - nailgun-net-check         |                     |
|                    | - shotgun                   |                     |
+--------------------+-----------------------------+---------------------+
| python-fuelclient  | - python-fuelclient         |                     |
+--------------------+-----------------------------+---------------------+


Such workflow has the following pros/cons:

Pros:

#. Developer (in custom ISO build job [2]_) can explicitly provide a number
   of patchsets to different fuel packages' repos.

Cons:

#. There might be the situation, when fuel packages on release ISO and
   release mirror will be different

#. Breaks packages signing work-flow (link to public PROD-1029)

#. Needs to update/support local chroot build system (from fuel-main [3]_)
   each time when fuel packages changed: added/removed/changed in specs, etc

#. No checks for RPM, DEB packages specs

#. Additional sudo requirements for jenkins user (link to public PROD-420,
   LP-Bug: 1348599)

#. Additional time required for building packages locally, which is 50% of
   all build ISO process


----------------
Proposed changes
----------------

Here is where you cover the change you propose to make in detail. How do you
propose to solve this problem?

If this is one part of a larger effort make it clear where this piece ends. In
other words, what's the scope of this effort?

Web UI
======

If the proposed changes require changing the web UI please describe in details:

* How existing controls or representation is going to be changed

* What changes are required for underlying engines


Nailgun
=======

General changes to the architecture, tasks and encapsulated business logic
should be described here.

Data model
----------

Changes which require modifications to the data model often have a wider impact
on the system.  The community often has strong opinions on how the data model
should be evolved, from both a functional and performance perspective. It is
therefore important to capture and gain agreement as early as possible on any
proposed changes to the data model.

Questions which need to be addressed by this section include:

* What new data objects and/or database schema changes is this going to
  require?

* What database migrations will accompany this change.

* How will the initial set of new data objects be generated, for example if you
  need to take into account existing instances, or modify other existing data
  describe how that will work.


REST API
--------

Each API method which is either added or changed should have the following

* Specification for the method

  * A description of what the method does suitable for use in
    user documentation

  * Method type (POST/PUT/GET/DELETE)

  * Normal HTTP response code(s)

  * Expected error HTTP response code(s)

    * A description for each possible error code should be included
      describing semantic errors which can cause it such as
      inconsistent parameters supplied to the method, or when an
      instance is not in an appropriate state for the request to
      succeed. Errors caused by syntactic problems covered by the JSON
      schema definition do not need to be included.

  * URL for the resource

  * Parameters which can be passed via the URL

  * JSON schema definition for the body data if allowed

  * JSON schema definition for the response data if any

* Example use case including typical API samples for both data supplied
  by the caller and the response

* Discuss any policy changes, and discuss what things a deploy engineer needs
  to think about when defining their policy.


Orchestration
=============

General changes to the logic of orchestration should be described in details
in this section.


RPC Protocol
------------

RPC protocol is another crucial part of inter-component communication in Fuel.
Thus it's very important to describe in details at least the following:

* How messaging between Nailgun and Astute will be changed in order to
  implement this specification.

* What input data is required and what format of results should be expected

* If changes assume performing operations of nodes, a description of messaging
  protocol, input and output data should be also described.


Fuel Client
===========

Fuel Client is a tiny but important part of the ecosystem. The most important
is that it is used by other people as a CLI tool and as a library.

This section should describe whether there are any changes to:

* HTTP client and library

* CLI parser, commands and renderer

* Environment

It's important to describe the above-mentioned in details so it can be fit
into both user's and developer's manuals.


Plugins
=======

Plugins are ofter made by third-party teams. Please describe how these changes
will affect the plugin framework. Every new feature should determine how it
interacts with the plugin framework and if it should be exposed to plugins and
how that will work:

* Should plugins be able to interact with the feature?

* How will plugins be able to interact with this feature?

* There is something that should be changed in existing plugins to be
  compatible with the proposed changes

* The proposed changes enable or disable something for new plugins

This section should be also described in details and then be put into the
developer's manual.


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

If this change set concerns any kind of upgrade process, describe how it is
supposed to deal with that stuff. For example, Fuel currently supports
upgrading of master node, so it is necessary to describe whether this patch
set contradicts upgrade process itself or any supported working feature that.


---------------
Security impact
---------------

Describe any potential security impact on the system.  Some of the items to
consider include:

* Does this change touch sensitive data such as tokens, keys, or user data?

* Does this change alter the API in a way that may impact security, such as
  a new way to access sensitive information or a new way to login?

* Does this change involve cryptography or hashing?

* Does this change require the use of sudo or any elevated privileges?

* Does this change involve using or parsing user-provided data? This could
  be directly at the API level or indirectly such as changes to a cache layer.

* Can this change enable a resource exhaustion attack, such as allowing a
  single API interaction to consume significant server resources? Some examples
  of this include launching subprocesses for each connection, or entity
  expansion attacks in XML.

For more detailed guidance, please see the OpenStack Security Guidelines as
a reference (https://wiki.openstack.org/wiki/Security/Guidelines).  These
guidelines are a work in progress and are designed to help you identify
security best practices.  For further information, feel free to reach out
to the OpenStack Security Group at openstack-security@lists.openstack.org.


--------------------
Notifications impact
--------------------

Please specify any changes to notifications. Be that an extra notification,
changes to an existing notification, or removing a notification.


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


--------------------------------
Infrastructure/operations impact
--------------------------------

Explain what changes in project infrastructure will be required to support the
proposed change. Consider the following:

* Will it increase the load on CI infrastructure by making build or test jobs
  consume more CPU, network, or storage capacity? Will it increase the number
  of scheduled jobs?

* Will it require new work-flows or changes in existing work-flows implemented
  in CI, packaging, source code management, code review, or software artifact
  publishing tools?

  * Will it require new or upgraded tools or services to be deployed on project
    infrastructure?

  * Will it require new types of Jenkins jobs?

  * Will it affect git branch management strategies?

  * Will it introduce new release artifacts?

* Will it require changes in build environments of any existing CI jobs? Would
  such changes be backwards compatible with previous Fuel releases currently
  supported by project infrastructure?


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

Primary assignee:
  Sergey Kulanov <skulanov@mirantis.com>

CI-team:
  Alexandra Fedorova <afedorova@mirantis.com>

QA:
  Artem Panchenko <apanchenko@mirantis.com>
  Denis Dmitriev <ddmitriev@mirantis.com>

Mandatory Design Reviewers:
  Vladimir Kuklin <vkuklin@mirantis.com>
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>
  Roman Vyalov <rvyalov@mirantis.com>


Work Items
==========

* Move all packages build process to Perestroika

* Set build packages jobs in voting mode (blocker PROD-81), but can be
  implemented like Patching-CI approach, by publishing jobs' logs only

* Change Fuel-CI fuel-library build package workflow since for now it
  hardly depends on fuel-main repo (LP-Bug: 1456096 )

* Create custom package build job to make it possible to define a set
  of commits to build custom perestroika repository (like custom_iso)

* Update custom_iso job with ability to provide the path to
  custom_perestroika_repository

* Remove DEB packages build from fuel-main

* PROD-885

* PROD-416

* Remove RPM packages build from fuel-main


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

* ISO build script must not build any packages mentioned in table_
  but instead it should download them from Perestroika repos

* Ensure custom_iso job use packages from custom_perestroika_repository
  while build custom ISO


----------
References
----------

.. [1] `Fuel stackforge repos <https://github.com/stackforge/>`_
.. [2] `Custom ISO yaml definition <https://github.com/fuel-infra/jenkins-jobs/blob/master/servers/product-ci/7.0/custom_iso.yaml>`_
.. [3] `Chroots for building packages <https://github.com/stackforge/fuel-main/blob/master/sandbox.mk>`_
