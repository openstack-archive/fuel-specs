..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Support for multi-rack deployment with static routes
====================================================

https://blueprints.launchpad.net/fuel/+spec/l3-multiple-racks

Fuel should allow user to deploy Fuel to multiple racks with a scalable
underlay network design so that the user can meet his or her expanding business
needs without having to re-deploy/migrate workloads.


--------------------
Problem description
--------------------

Current implementation of multi-rack support lacks a number of features in
demand (all services via one network, networks shared between node network
groups, VIPs can be allocated in different node network groups, arbitrary VIP
addresses), and has a number of usability issues (manual setup of dnsmasq on
master node, lack of validation, nodes do not have connection with node network
groups until they are added into environment but in fact they have IPs from
different node network groups, new routes are not applied when node network
group is added to the deployed environment).

Current proposal deals with the issues listed above.


----------------
Proposed changes
----------------

1. Make additional setup of dnsmasq on master node when node network groups are
configured. User should do that by hands now. It should be done automatically
when parameters of any of Admin networks are changed or Admin network is
deleted. This will save a user from manual error-prone operations of setting
this up via a command line.

2. Validation of provided node network groups configuration is done on backend.
Validation is very simple now, it is done for a limited number of cases.

3. Assignment of VIP for network managed by dhcp. It is about 'admin' network
now. When some network role that requires VIP is mapped there, IP address
should be reserved via dnsmasq. This can be done as a separate task or as a
predeployment hook. This solves all-in-one network problem.

4. When a new node network group is added to the deployed environment new
routes should be applied to network configuration of all nodes. This will
resolve an issue with adding node network groups to the deployed environment.

5. VIP allocation is restricted to controller node group now in Nailgun.
It should be allowed to allocate VIP in any node group to allow proper
separation of HA services into different nodes. But other restriction remains
the same: VIP can be allocated only if all nodes which conform to its
node_roles section are in the same node group.

6. Node network groups are moved out from environment. Node network groups will
be managed independently from environments. This will provide more consistent
UX where user will have bootstrap nodes grouped by Admin networks before nodes
are added into any environment. Networks' parameters and nodes data can be
checked for consistency on early stages. Also, configuration of Admin networks
and corresponding dnsmasq setup can be made prior to creation of environments.
But DB relations become more complicated in this case if we allow using of the
same node network group in different environments.

7. Provide an ability to share network (L2/L3 parameters) between
several node network groups. As for now, each particular node network group
have its own L2/L3 parameters for every network. It is 1:1 mapping. It will be
possible to share arbitrary networks (use shared L2/L3 parameters) between
several node network groups. It will be possible to use completely arbitrary
mapping via API (may be CLI as well) and UI will support two options: share
particular network among all node network groups within environment or create
separate network (L2/L3 parameters) for every node network group.
E.g. this ability is required to use a dedicated storage.

8. It should be allowed to set user-defined IP for any VIP. This IP can even be
out of any environment's networks, to be managed by external means (e.g.
external LB).

Web UI
======

GUI tasks are to be in separate ticket/spec.

Nailgun
=======

A number of tasks will be added to serve auto setup of dnsmasq on master node,
IP reservation for VIP on DHCP network.
DB relations will be changed for tasks 6 and 7.
REST API will be changed for tasks 6, 7 and 8.

Data model
----------

TBD

REST API
--------

TBD

Orchestration
=============

TBD

RPC Protocol
------------

TBD

Fuel Client
===========

TBD

Plugins
=======

None

Fuel Library
============

TBD

------------
Alternatives
------------

This feature can be treated as a composition of several smaller changes. Seems,
all of them can be implemented separately. But implementation of tasks 6 and 7
is dependent one from another.


--------------
Upgrade impact
--------------

N/A

---------------
Security impact
---------------

N/A

--------------------
Notifications impact
--------------------

TBD

---------------
End user impact
---------------

TBD

------------------
Performance impact
------------------

N/A

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

None

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
