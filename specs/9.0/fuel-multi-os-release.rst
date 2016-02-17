..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Supporting Multiple Openstack releases
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

----------------
Proposed changes
----------------

We will maintain at least one prior versions of OpenStack releases

This will primarily consist of:
* Keeping a 'release' fixture for the prior release(s) in openstack.yaml
* Adding code to compile multiple versions of fuel-library package using the
HEAD of fuel-library, but switching out the Puppetfile for dependencies on
puppet-openstack modules
* Coding cases into the fuel-library composition layer do deal changes
between the versions of puppet-openstack modules

Web UI
======

None

Nailgun
=======

General changes to the architecture, tasks and encapsulated business logic
should be described here.

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

Will add scripts to build Puppetfile so that portions can be changed between
OpenStack releases, this will allow for multiple fuel-library packages to be
created to support these versions

Composition calls into the puppet-openstack modules will need to be cased
where the interface changed between the two releases.

for example we would see something like:

``` puppet
  $openstack_version = hiera('openstack_version')

  if $::openstack_version != "mitaka-9.0" {
    # Remove nova::objectstore in Mitaka
    $simple_classes = [
      'nova::scheduler',
      'nova::objectstore',
      'nova::cert',
      ]
  } else {
    $simple_classes = [
      'nova::scheduler',
      'nova::cert',
      ]
  }
  class { $simple_classes:
    enabled => $enabled,
    ensure_package => $ensure_package
  }
```

------------
Alternatives
------------

While its possible to consume the previous releases serializers, this also
means that the entire composition layer must come from that version as well.
In this regard a newer version of fuel could deploy an older version of
openstack, but it will lack support for any of the newer features in fuel
and won't meet the acceptance criteria.

--------------
Upgrade impact
--------------

No negative impact is expected, it may actually reduce burden of upgrading
between the two 'native' releases as they would have been formed with the
same fixtures so data migration of the fixture may not be necessary as it is
with prior releases.

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

User will be able to select a release according to the existing methods
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

Fuel-library developers will need to be concious of changes to the
composition calls to the other puppet-openstack modules and propse case style
logic to account for the version details

---------------------
Infrastructure impact
---------------------

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

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.

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

Able to install fuel and select an older version of OpenStack while taking
advantage of the latest features of fuel

----------
References
----------

http://lists.openstack.org/pipermail/openstack-dev/2016-February/086309.html