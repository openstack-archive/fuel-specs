..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================
Calculating dependent configuration options
===========================================

Current specs describe current situation with our scale deployments, which
requires custom patches in puppet's files to increase values of some
configuration options.

--------------------
Problem description
--------------------

Currently we have some dirty, but necessary hooks in puppets, which need for
correct work cloud on scale, e.g. max_template_size for Heat or timeouts for
some other services. Default values of these options are not possible to use
on huge scale deployment (e.g. 200 nodes), where we want test Heat stacks for
which creation time is more then 1 hour.

Obviously the right solution is to increase these defaults, because if we want
process heavy objects like huge Heat stack we need more time for it.
Unfortunately it also has bad side:
 - small installation (20 nodes) will have unreal limits, which never
will be reached.

Also constant values do not solve issue in case, when we want to have
deployment with more resources, then we expected when set previous values.

----------------
Proposed changes
----------------

Another, more elastic solution may be introducing dependencies of
configuration values from parameters of deployment. For example, based
on count of nodes in environment. In the worst case dependent options
may be calculated with some coefficients, which can be identified by
using hardware parameters. And then we can calculate needed values.

We can use information about hardware and nodes in deployment, which will
be used for calculations, in Nailgun. Then, we calculate all needed values
with some formula and after that put those values to fixtures files (like
astute.yaml)

According description above we need to split this work on follow items:
- Create a list of options, which are affected by mentioned issue.
- Create formulas, which allow to calculate values based on parameters of
  hardware used for deployment.
- Add this formulas to Nailgun.
- Put calculated values into fixtures.
- Take this calculated values during create/update deployment by puppet.
- Clearly document formulas and process of calculation.

Open questions, which can be done too:
- Send message or warning to user (in UI and CLI), that some options were
  changed/calculated during update/create deployment.

Web UI
======

Potentially updated options may be showed via UI.

Nailgun
=======

Create formulas, based on parameters of hardware used for deployment. Then
generate data, which will be put in fixtures.

Data model
----------

None

REST API
--------

None

Orchestration
=============

Now we need calculate some configuration options before create/update
deployment.

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

No actual changes, just need to use all calculated values, which was pass to
fixtures from Nailgun.

------------
Alternatives
------------

Update all these options manually or set inflated default values for some
configurations options, like we do it for scale lab now

--------------
Upgrade impact
--------------

During upgrading re-calculation should be called too for using new/updated
options. Also it allows to calculate new configuration options, which may be
dependent too.

---------------
Security impact
---------------

Nothing special, but we need make sure, that re-calculation will not touch any
security related configuration options.

--------------------
Notifications impact
--------------------

Current change has optional suggestion about implementation corresponding
notifications for user/operator about re-calculated values.

---------------
End user impact
---------------

After implementation mentioned changes user will get ability to deploy MOS with
different configuration options, which will depend on existing hardware/virtual
resources. If it's small base deployment, default values will be used.
Otherwise values for some options will be calculated according deployment
characteristics.

New values will allows to use more heavy objects in deployment, e.g.
create Heat stacks with more resources, which previously was blocked by limit
of Heat template size.

------------------
Performance impact
------------------

By design re-calculation should happen on create and on update deployment
paramaters, i.e. when new nodes are added.

-----------------
Deployment impact
-----------------

Nothing special, after each upgrade/update we just need to update current
fixtures on all nodes in environment.

----------------
Developer impact
----------------

None

--------------------------------
Infrastructure/operations impact
--------------------------------

There is only one case, which may affects Infrastructure:
 - additional Jenkins job with non trivial deployment, which requires
   re-calculation values of config options.

--------------------
Documentation impact
--------------------

Need to describe calculation process for dependent configuration options:
 - add list of affected configuration options with corresponding formulas for
   calculations
 - add notes, when this approch is used, e.g. for scale deployments.
 - which actions it affects - create and update whole deployment, e.g. adding
   new 20 hardware nodes.

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
 TBD

Other contributors:
 TBD

Mandatory design review:
 TBD


Work Items
==========

- Define list of config options for each service, which should be calculated
  depending on the deployment's characteristics.
- Implement calculation mechanism for choosen options in Nailgun.
- Add ability to pass calculated options to fixtures files on nodes.

Dependencies
============

None

------------
Testing, QA
------------

Introduced changes need to separate tests cases, which validates values
of configurations options parameters. Potentially it may be couple tests:
 - first for small deployment, when we use old/default values of configuration
   options
 - second for heavy deployment, where need to increase values of configuration
   options and check, that these values were applied for services.

Acceptance criteria
===================

Please specify clearly defined acceptance criteria for proposed changes.

----------
References
----------

None
