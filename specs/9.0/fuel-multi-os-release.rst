..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Decouple Fuel and OpenStack dependcies
==========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-multi-os-release


Given the current development patterns in OpenStack we hard tie fuel to the
version of OpenStack that it was developed for. However given our own
patterns, and the availability or even stability of the next OpenStack
release we only switch to and propose possibly breaking changes with the
prior version very late in the development cycle. This support can often
be maintained with minimal effort into the next release.

Operators often find reason to use the latest versions of fuel for
enhancements in fuel being able to support features that where already
available in previous versions of fuel (DVR, SR-IOV, hugepages, granular
ssl, etc...) However they may need to continue to use one of these older
releases. Instead of back-porting features from a more recent release,
operators could leverage the newer features of fuel with the previously
supported OpenStack release.

--------------------
Problem description
--------------------

As a deployment engineer, I want to be able to take advantage of the latest
features in fuel and the previous release of OpenStack (given the fuel
features are supported)

As a fuel developer, I want to be able to test my changes on fuel against a
stable version of OpenStack in order to minimize churn to implement my changes

As a fuel developer, I want to be able to test my changes against the next
version of OpenStack to get a sense of support for the changes

Currently, we have tight coupling between the tasks that configure and
install a specific version of OpenStack and the remaining tasks in fuel,
this creates a hard relationship between the version of OpenStac and fuel.
Untangling this in the current state is remarkably difficult and leads to a
full fork, and quickly results in the loss of feature parity.

----------------
Proposed changes
----------------

We will construct an interface that would allow for an interested party to
easily use or create tasks that are compatible with a specific version of
OpenStack while retaining as little divergence from fuels non-version
specific tasks as possible.

`osnailyfacter/tasks/*` currently contains a mix of version specific and
generic tasks. By splitting these apart, we easily version one while keeping
another.  Since deployment tasks are found by effectively
`find /etc/puppet/<release> -name tasks.yaml` they can be present anywhere
in the puppet modules directory.

Initially, we will prepare these by moving them into a directory structure
out side of osnailyfacter. At the same time we should start cutting any
remaining tasks apart that contain both version and version-less changes
in them.

Once we have a good handle on the separation of the tasks, they would be
moved to their own repository as a puppet module. We can pull this back into
the fuel-library package by adding the desired version to Puppetfile.

Puppetfile will need to be broken into parts so that it is also easy to
separate modules that are tightly coupled between OpenStack versions and
those that are shared across many versions. A script should be added to
compile these parts back to a single file so that it can be consumed as
normal.

Maintaining the interface:

In order to ensure that interface is working as expected (and that we are not
inappropriately deprecating) we will add simple coverage to test a previous
version of OpenStack Most often, this will be the prior release. Testing
should only cover the most basic deployment and passing OSTF

To support this, a experimental release should be maintained, along with
the corresponding fuel-library package version that supports this release.

In the future, we could consider making the release API exposed so that
this release schematic is carried with the fuel-library package instead
of nailgun.

Web UI
======

None

Nailgun
=======

No changes are required, we can use existing release model as-is

Data model
----------

Releases will be added to the openstack.yaml fixture. This will enable us to
control the release version key, as well as package locations.


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

Plugins will continue to function as intended, they can already specify fuel
and release version support separately.

Fuel Library
============

We will start separating the tasks that directly interact with the
puppet-openstack, and other openstack version specific calls.

normally tasks are most often found in:

  osailyfacter\modular\*tasks.yaml

We can start moving them to a separate module location <TBD>. This location
should attempt to follow puppet module syntax and while changing tasks as
little as possible (another spec is proposed to make them actual valid
modules)

(placeholder for name feedback)::
  <TDB>
    manifests\
    manifests\neutron\{tasks.yaml, *.pp, etc...}
    manifests\keystone\{tasks.yaml, *.pp, etc...}
    etc...

We will want to generate the Puppetfile from parts, this can be done by
creating a folder structure for common and versions so that the Puppetfile
can be compiled back to a single file and usable by tools that expect it like
puppet-librarian-simple.


------------
Alternatives
------------

While its possible to consume the previous releases serializers, this also
means that the entire composition layer must come from that version as well.
In this regard a newer version of fuel could deploy an older version of
openstack, but it will lack support for any of the newer features in fuel
and won't meet the acceptance criteria.

Its also possible to case in all of the conditions directly in the
composition layer, however this is highly undesired due to the high
maintenance burden.

--------------
Upgrade impact
--------------

No negative impact is expected.

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

End user will be able to select a release according to the existing methods
already present in the fuel-web and python-fuelclient interfaces.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

None beyond what has been expressed.

----------------
Developer impact
----------------

Fuel-library developers will need to be conscious of the proper task location
and maintain separation of function between the sets of tasks.

A developer-user whom intends to use this entry point will need to be aware
that in order to ensure the highest level of features from the recent fuel
version, they would need to fork the version repo, and back port changes from
the newer versions of the tasks

---------------------
Infrastructure impact
---------------------

[note: not updated yet along new direction, needs to be re-hashed]

keywords used for this spec for demonstration

Liberty - the last stable OpenStack release
Mitaka - the current development OpenStack release
Neuton - the next development OpenStack release

CI Work flow for fuel-library

Early dev cycle:
* voting / gating CI will target the last OpenStack stable release (Liberty)
  from packages.
* Daily BVT jobs will target OpenStack stable release (Liberty) from packages
* (if available) non-voting CI will target the current development release
  (Mitaka) from trunk

Mid dev cycle: (once packages are ready for current dev)
* voting / gating CI will target the last OpenStack stable release (Liberty)
  from packages.
* non-voting CI will target the current development release (Mitaka) from
  packages
* Daily BVT jobs will target OpenStack stable release (Liberty) from packages
* Daily BVT jobs will target next OpenStack development release (Mitaka)
  from packages
* (if available) non-voting CI will target the current development release
  (Mitaka) from trunk

Late dev cycle: (once current dev is stable)
* non-voting CI will target the last OpenStack stable release (Liberty) from
  packages.
* voting / gating CI will target the current development release (Mitaka)
  from packages
* Daily BVT jobs will target OpenStack stable release (Liberty) from packages
* Daily BVT jobs will target next OpenStack development release (Mitaka)
  from packages
* (if available) non-voting CI will target the current development release
  (Mitaka) from trunk

Early in the cycle we will have voting jobs for the stable openstack
(Liberty), as we progress and are ready, we start adding non-voting CI for
the current dev release (Mitaka). Later, once dev has stabilized, we can
invert the voting and non-voting jobs. Then after the close of the release
(ie. cut stable) We drop the prior openstack release (Liberty), keep the new
stable (Mitaka) and develop towards the next release (Neuton).

Jobs:
An additional fuel-library CI job will be needed for most of the cycle
An additional BVT job will be needed for most of the the cycle
An additional package job will be needed to build the two versions of
fuel-library
The ISO job will need a parameter to more effectively control which OpenStack
version is included on the ISO / Default.

--------------------
Documentation impact
--------------------

How-to will need to be written

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Andrew Woodward<xarses>

Other contributors:
  <launchpad-id or None>

Mandatory design review:
  <launchpad-id or None>

Work Items
==========



Dependencies
============

None

------------
Testing, QA
------------

Explained above in infra

Acceptance criteria
===================

Able to install fuel with a custom fuel-library and release bundle, and
select an older version of OpenStack while taking advantage of the latest
features of fuel

----------
References
----------

http://lists.openstack.org/pipermail/openstack-dev/2016-February/086309.html