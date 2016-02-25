..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================================================
Re-factor osnailyfacer Fuel Library Module to Be Compatible With Puppet Master
==============================================================================

https://blueprints.launchpad.net/fuel/+spec/fuel-refactor-osnailyfacter-for-puppet-master-compatibility

The Fuel Library module `deployment/puppet/osnailyfacter` is Fuel Library's
composition layer module.  In order to be able to use an LCM plugin to Fuel
& use a 3rd party service, such as Puppet Master, I need the modular manifests
contained in this module to be accessible by a 3rd party service.

--------------------
Problem description
--------------------

The modular manifests contained inside of 'osnailyfacter/modular' are
inaccessible to a 3rd party service, such as Puppet Master, as they are
located inside of 'osnailyfacter/modular'.  Under the Modular Fundamentals
guidelines outlined by Puppetlabs, Puppet's autoinclude looks in 'manifests'
for Puppet manifests.  It does not know anything about any directory named
'modular'.  This means that the top-scope modular manifests located inside
of 'osnailyfacter/modular' are not consumable by a 3rd party plugin
integration.

----------------
Proposed changes
----------------

I would like to leave the contents of these modular manifests
alone but I would like to reorganize them into profile classes inside of
the 'osnailyfacter/manifests' directory.

We will re-factor and move the configuration logic from the the manifests in
'osnailyfacter/modular' into consumable profile classes by copying their
contents to a file of the same name, but located in the
'osnailyfacter/manifests' directory.  We will also wrap them in a class
declaration, making them essentially profile classes.  The manifest inside of
'osnailyfacter/modular/<manifest name>.pp will be updated to simply include the
new profile class.  For example:

  osnailyfacter/modular/ceph/ceph_pools.pp would have its contents copied to
  'osnailyfacter/manifests/ceph/ceph_pools.pp' and be wrapped inside of a
  class declaration for the class 'ceph::ceph_pools'.

  osnailyfacter/modular/ceph/ceph_pools.pp would contain just the following:

  'include ::ceph::ceph_pools'

  This would include the class and apply the same configuration logic that it
  did before, but by being wrapped inside of a consumable class inside the
  'osnailyfacter/manifests' directory, integration of a 3rd party plugin to
  consume the class is now possible.

The tasks.yaml file can still reference the same 'modular/<name>.pp' manifest.
By applying the include statement shown above, the manifest will still apply
the same configuration logic as it did before.  The location of the code has
just been reorganized into the 'manifests' directory.  No new feature is added
outside of making top-scope modular manifests consumable by 3rd party plugin
integrations.

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
will have its contents copied into a corresponding file of the same name
in 'deployment/puppet/osnailyfacter/manifests' and will be wrapped inside of
a class declaration.  The manifest in the modular directory will have its
contents replaced with an include statement to include the new profile class.
For example:

  osnailyfacter/modular/ceph/ceph_pools.pp would contain:

  'include ::osnailyfacter::ceph::ceph_pools'

Nothing changes as far as what code is applied or in what order it is applied
via the standard granular deployment task doing a puppet apply on the manifest.

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

After this lands, developers would need to develop modular manifest code inside
of 'deployment/puppet/osnailyfacter/manifests' rather than under the current
directory 'deployment/puppet/osnailyfacter/modular'.

---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

Documentation should be updated to reference putting modular manifest code in
the manifests directory rather than modular.

--------------
Implementation
--------------

The re-factoring work has already been done.  We should wait for a quiet period
after FF when this work can be rebased and landed.

Assignee(s)
===========

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  Scott Brimhall (grimlock86)

Other contributors:
  Andrew Woodward (xarses)

Mandatory design review:
  Andrew Woodward (xarses)


Work Items
==========

* Identify changes dependent on https://review.openstack.org/#/c/281557/
  & https://blueprints.launchpad.net/fuel/+spec/fuel-remove-conflict-openstack

* Re-base commits of each directory and merge during an identified quiet period
  after all other FFE work concerning Fuel Library has been completed


Dependencies
============

None

------------
Testing, QA
------------

Existing CI and BVT tests will catch regression as the same code will be
applied for each granular deployment task using a modular manifest.

Acceptance criteria
===================

* All top-scope modular manifests located inside of 'osnailyfacter/modular/'
  have had their contents copied under a wrapper class inside of the
  'osnailyfacter/manifests' directory.

* CI, BVT, & nightly swarm tests are all successful.

* Fuel deployment is successful while using the same granular deployment
  tasks as before the change.

----------
References
----------

None
