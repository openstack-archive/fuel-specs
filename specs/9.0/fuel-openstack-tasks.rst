..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Decouple Fuel and OpenStack tasks
==========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-openstack-tasks


Given the current development patterns in OpenStack we hard tie fuel to the
version of OpenStack that it was developed for. However given our own
patterns, and the availability or even stability of the next OpenStack
release we only switch to and propose possibly breaking changes with the
prior version very late in the development cycle. This support can often
be maintained with minimal effort into the next release.

Operators often find reason to use the latest versions of fuel for
enhancements in fuel being able to support features that where already
available in previous versions of OpenStack (DVR, SR-IOV, hugepages, granular
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

There is already an existing method that is close to this which is a
byproduct of the upgrade process. The difference between the "upgrade"
strategy and decoupling the current fuel and open stack releases.

The present "upgrade" method relies on:

* previous version of serializer
* previous version of release meatdata
* previous version of openstack install (puppet-opnstack modules)
* previous version of fuel components (fuel-library components, cluster,
  pacemaker, haproxy, rabbit, db, High avalailibility, huge pages, etc...)
* previous version of fuel tasks for everything fuel and openstack
  (osnailyfacter)
* previous version of network manager, volume manager, etc...

The result is, that there are no features from the new version of fuel, there
is no functional difference between a cluster installed with fuel 8.0
release, and a cluster that was deployed loading the all of the components
of the prior release into the fuel 9.0.

The intent here is that by increasing the separation between 'fuel' and
'openstack' bits (we all ready have the puppet-modules separated) we can
enable others to be able to take advantage of new features and enhancements
in fuel, while consuming an older version of openstack


----------------
Proposed changes
----------------

We will seperate the tasks and their entry puppet/shell code between those
generic to fuel and those specific to openstack. This will allow for an
interested party to refactor the openstack tasks to work with their desired
version of fuel and openstack.

To help visualize the speration, we will end up with a scheme that would be
considered:

* osailyfacter/modular/ - fuel-9.0 - would contain generic tasks, and is
  intended to stay in the fuel-library repo
* openstack_tasks - mitaka-9.0 - would contain openstack specific tasks and
  will eventually move into its own repo.


`osnailyfacter/modular/*` currently contains a mix of version specific and
generic tasks. By splitting these apart, we easily version one while keeping
another.  Since deployment tasks are found by effectively
`find /etc/puppet/<release> -name tasks.yaml` they can be present anywhere
in the puppet modules directory.

Initially, we will prepare these by moving them into a directory structure
out side of osnailyfacter, to prepare it as its own module. At the same time
we should start cutting any remaining tasks apart that contain both version
and version-less changes in them.

Once we have a good handle on the separation of the tasks, they would be
moved to their own repository as a puppet module. We can pull this back into
the fuel-library package by adding the desired version to Puppetfile.

Puppetfile will need to be broken into parts so that it is also easy to
separate modules that are tightly coupled between OpenStack versions and
those that are shared across many versions. A script should be added to
compile these parts back to a single file so that it can be consumed as
normal.


Web UI
======

None

Nailgun
=======

No changes are required, we can use existing release model as-is

Data model
----------

No changes in tree. User will be able to register a release that will have
call custom version combination using existing interfaces


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

We can start moving them to a separate module location, openstack_tasks This
location should attempt to follow puppet module syntax and while changing
tasks as little as possible (another spec is proposed to make them actual
valid modules)

example structure for new tasks folder::

  openstack_tasks
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

After End user installs custom release, user will be able to select a release
according to the existing methods already present in the fuel-web and
python-fuelclient interfaces.

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

New parameters would need to be added to the spec for building the
fuel-library package so that it can build it as expected when the folder/repo
is overloaded.

--------------------
Documentation impact
--------------------

How-to will need to be written

An abstract of using this separation would look like:

* create a fork of the mitaka-9.0 tasks
* alter your Puppetfile to point to the desired puppet-opestack modules
* adapt these tasks to work with the versions of puppet-opestack modules
  you are using, effectively mixing the inputs from the newer tasks with
  the calls from an older version of them.
* build a new fuel-library package (or use source) for kilo-9.0
* create a new release (nailgun) that is a clone of the mitaka-9.0 release,
  altering the version string kilo-9.0, alter the repo locations to point
  to your desired packages
* sync tasks in nailgun
* create env
* deploy
* ???
* profit!

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

* Move tasks only containing openstack calls into a single folder
* Separate tasks that contain a mix of openstack, and other module calls
* Move this repo to a separate repo (most likely not in 9.0, but early
  against 10)
* Update the build process of the fuel-library package to be able to switch
  the openstack tasks repo

Dependencies
============

None

------------
Testing, QA
------------

Existing testing is sufficient to cover the scope of this change as this will
follow the same pattern as the puppet-openstack modules being managed by
Puppetfile.


Acceptance criteria
===================

Able to install fuel with a custom fuel-library and release bundle, and
select an older version of OpenStack while taking advantage of the latest
features of fuel

----------
References
----------

http://lists.openstack.org/pipermail/openstack-dev/2016-February/086309.html

Example fork of Kilo and 9.0
https://github.com/xarses/fuel-library/tree/9-Kilo