..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================================================
Re-factor osnailyfacer Fuel Library Module to Be Compatible With Puppet Master
==============================================================================

https://blueprints.launchpad.net/fuel/+spec/fuel-refactor-osnailyfacter-for-puppet-master-compatibility

The Fuel Library module `deployment/puppet/osnailyfacter` is Fuel Library's
composition layer module and has been incompatible with Puppet Master for
a long time, as it does not conform to Puppetlabs' module fundamentals.

In order to be able to use an LCM plugin to Fuel & use Puppet Master,
I need this module to be a valid Puppet module.

--------------------
Problem description
--------------------

Specifically, the module has many manifests located inside of
'osnailyfacter/modular' rather than 'osnailyfacter/manifests'.  This poses
a problem and is incompatible with Puppet Master as autolookup will fail,
since Puppet Master expects manifests to be located within a directory named
'manifests'.  If the classes inside of these manifests are attempted to be
included in a catalog via 'include' or a 'class' instantiation, the compilation
will fail as Puppet Master will not be able to find them.  They need to be
inside of 'osnailyfacter/manifests' for the module to be compatible with
Puppet Master.

In this way we would change:

  osnailyfacter/modular/\*.pp

  osnailyfacter/modular/\*/\*.pp

  ...

It would become:

  osnailyfacter/manifests/\*.pp

  osnailyfacter/manifests/\*/\*.pp

  ...

These classes will also need to be renamed as necessary to allow autoinclude
to work properly.

----------------
Proposed changes
----------------

As described in Problem description, we will re-factor and move the configuration
logic from the existing manifests located inside 'osnailyfacter/modular' to classes
located in'osnailyfacter/manifests'.  We will create class definitions inside of the
manifests to fit into a proper Puppet module format.  The existing tasks.yaml can be
left where they are and the existing task puppet files should be updated to leverage
the newly created osnailyfacter classes.

For example:

  osnailyfacter/modular/ceph/ceph_pools.pp does not contain a class definition.

  We will create class osnailyfacter::ceph::ceph_pools inside of
  'osnailyfacter/manifests/ceph/ceph_pools.pp' and the class could then be
  included on a Puppet Master via 'include ::osnailyfacter::ceph::ceph_pools'.
  The existing 'osnailyfacter/modular/ceph/ceph_pools.pp' should be updated to
  reference the new osnailyfacter::ceph::ceph_pools class as to continue to
  support the task based deployment methodology.

For masterless Puppet/puppet apply tasks, each task would also need to be
updated to include the new 'osnailyfacter/manifests' location for the
manifest being applied.


Web UI
======

None

Nailgun
=======

None

Data model
----------

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

Each manifest contained inside of 'deployment/puppet/osnailyfacter/modular'
will need to be moved inside of 'deployment/puppet/osnailyfacter/manifests'
and each corresponding task.yaml needs to be updated to reflect the directory
change.  This will make osnailyfacter compatible with either master or
masterless Puppet approach.

osnailyfacter module should also be moved into its own git repository.
Fuel Library's Puppetfile should be updated to include the new repo and ref for
osnailyfacter.

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

This enables an end user to be able to enable LCM features via a Puppet Master
Fuel plugin.  Users can then have the ability to manage the day 2 operations
and configuration needs of their deployments.

No end user impact if not using a Puppet Master/LCM plugin as this enables
compatibility of the osnailyfacter composition layer for both master and
masterless puppet approaches.

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

Changes to osnailyfacter would need to be done in a new repo for the module.
Any tasks should include the updated directory structure from modular
to manifests.  Any changes to osnailyfacter should be compatible with the
module fundamentals outlined by Puppetlabs for a valid Puppet module structure.

---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

Documentation for Fuel Library should be updated where any references to
'osnailyfacter/modular' exist and updated to 'osnailyfacter/manifests'.

--------------
Implementation
--------------

The re-factoring work has already been completed by AT&T and is intended
to be upstreamed/merged with Fuel Library.  Any gaps between when the work was
completed and any changes that have occurred to osnailyfacter between that time
and the time of implementation will be addresssed by AT&T at the time of
implementation to ensure that all code is accounted for.

Assignee(s)
===========

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  Scott Brimhall (sbrimhall)

Other contributors:
  Andrew Woodward (xarses)

Mandatory design review:
  Andrew Woodward (xarses)


Work Items
==========

* identify any changes in osnailyfacter manifests that have occurred since
  re-factoring was done and the time of merging of code.

* ensure all code is accounted for and merge code to move manifests in
  osnailyfacter/modular to osnailyfacter/manifests.


Dependencies
============

None

------------
Testing, QA
------------

Existing testing coverage should be sufficient to ensure that there are no
regressions introduced by these changes. In some cases, it may be necessary
to extend the NOOP coverage to cover changes.

Acceptance criteria
===================

* All classes inside of osnailyfacter/manifests can be included via 'include'
  puppet function while only specifying either the location of 'osnailyfacter'
  or 'modules' directory as the module path.

* All tasks using osnailyfacter/modular are updated to osnailyfacter/manifests

* Fuel deployment is successful while using tasks with the updated directory
  structure


----------
References
----------

None
