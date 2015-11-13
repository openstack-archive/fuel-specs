..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Task Based Deployment With Astute
==========================================


https://blueprints.launchpad.net/fuel/+spec/task-based-deployment-astute

* Intro

  This blueprint is a suggestion to improve our deployment orchestration
  to make it possible to improve deployment time and decrease our technical
  and architectural debt by an order of magnitude.


--------------------
Problem description
--------------------
  So far we have had a really neat but half-completed orchestration engine since 6.1
  This engine allowed us to split gigantic puppet catalogue into pieces and run tasks
  one by one allowing users to introduce tasks within plugins thus making Fuel much 
  more flexible. Unfortunately, due to lack of resources we had to postpone complete
  implementation of an orchestrator that can orchestrate tasks instead of roles. This
  leads to performance issues of the deployment significantly affecting deployment time.
  While in fact it could be almost O(1), it is almost O(n*m) where *n* is number of roles
  and *m* is number of nodes. This became especially harmful when we introduced role-as-a-plugin
  feature [0] as role dependencies make deployment take up to 4-6 hours, simply waiting for roles
  to be completed without actual dependencies between them.

  This makes our deployment go 80 minutes for a basic BVT use case, while it could have taken
  30 minutes with parallelized deployment. This blueprint suggests a change that should once
  and forever remove such roadblocks from Fuel. 

  This would allow us to drastically improve things:

  * Shrink CI time to 30 minutes

  * Make our infra gating swift for packages

  * Provide developers with very quick feedback

  * Allow us to unlock settings tabs to do simple redeployment after settings change (partial lifecycle management)

  * Make Fuel look even more awesome


----------------
Proposed changes
----------------

We propose to enable this feature by applying the following changes:

* Make roles just a Nailgun entity, not known to Astute

* Make Nailgun generate a graph of tasks for execution based not on roles, but on tasks

* Make Astute traverse the graph according to dependencies 

* Introduce new version of tasks.yaml format allowing depl. engineer to set cross-node dependencies

* Introduce 'anchor' type of task which does not require any type of execution

* Refactor Fuel Library to introduce cross-node dependencies and anchors

* Adjust FUEL CLI correspondingly

* Allow a user to disable task-based deployment in case he does not want this feature or faces any
  issues with it

Web UI
======

Allow a user to disable parallel deployment flag in case he faces a race condition
by setting corresponding cluster attribute.

Nailgun
=======

Nailgun

Data model
----------

Add 'task-based-deployment-enabled' flag to cluster configuration.

Default: true for >= 8.0 clusters, false for all other clusters.

Tasks YAML format Change
--------

Orchestration
=============

Astute should be extended with a set of methods that respect the following:

* Dependencie between the tasks provided by Nailgun

* Concurrency policies for tasks (e.g. no more than 6 replication slaves for
  Galera at a time)

* One task per node at a time.

There will be a set of new tasks states introduced:

Astute will form a view of tasks for execution for each particular node and synchronously monitor
a set of tasks that are being executed with periodic check. Whenever a node is free for execution,
Astute starts iterating through tasks

There 

RPC Protocol
------------

RPC Protocol change is the following:

Nailgun sends a message for execution in new format with deployment graph embedded into it.
Astute identifies that it should use new deployment/orchestration engine and passes this graph
for further execution to this engine.

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

This change does not affect plugins except for enabling pluggable roles/tasks
to be executed in more optimal way. This optimal way will be enabled only when
all tasks associated with the cluster are set into new version format and when
'parallel deployment' flag for cluster is not set to 'true'.

Fuel Library
============

Adjust Fuel Library tasks

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

[0] https://blueprints.launchpad.net/fuel/+spec/role-as-a-plugin

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
