..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
Ceilometer support for vCenter
==============================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/ceilometer-vcenter

Introduction paragraph -- why is it necessary to do anything?
A single paragraph of prose that reviewers can understand.

Some notes about using this template:

* Your spec should be in ReSTructured text, like this template.

* Please wrap text at 79 columns.

* The spec should be gender neutral and written in the third person aspect

* The filename in the git repository should match the launchpad URL, for
  example a URL of: https://blueprints.launchpad.net/fuel/+spec/awesome-thing
  should be named awesome-thing.rst

* Please do not delete any of the sections in this template.  If you have
  nothing to say for a whole section, just write: None

* For help with syntax, see http://sphinx-doc.org/rest.html

* To test out your formatting, build the docs using tox, or see:
  http://rst.ninjs.org

* If you would like to provide a diagram with your spec, ASCII diagrams are
  required.  http://asciiflow.com/ is a very nice tool to assist with making
  ASCII diagrams.  The reason for this is that the tool used to review specs is
  based purely on plain text.  Plain text will allow review to proceed without
  having to look at additional files which can not be viewed in Gerrit.  It
  will also allow in-line feedback on the diagram itself.


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


---------------------
Infrastructure impact
---------------------

Explain what changes in project infrastructure will be required to support the
proposed change. Consider the following:

* Will it increase the load on CI infrastructure by making build or test jobs
  consume more CPU, network, or storage capacity? Will it increase the number
  of scheduled jobs?

* Will it require new workflows or changes in existing workflows implemented in
  CI, packaging, source code management, code review, or software artifact
  publishing tools?

  * Will it require new or upgraded tools or services to be deployed on project
    infrastructure?

  * Will it require new types of Jenkins jobs?

  * Will it affect git branch management strategies?

  * Will it introduce new release artifacts?

  * Will it require changes to package dependencies: new packages, updated
    package versions?

  * Will it require changes to the structure of any package repositories?

* Will it require changes in build environments of any existing CI jobs? Would
  such changes be backwards compatible with previous Fuel releases currently
  supported by project infrastructure?


--------------------
Documentation impact
--------------------

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.


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

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
