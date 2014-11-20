..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Re-thinking Fuel Client
==========================================

https://blueprints.launchpad.net/fuel/+spec/re-thinking-fuel-client

The major problem of Fuel Client is that it is not used in the most of real
life use cases due to the lack of features, pure quality and inappropriate
design as for a library. This specification describes the way of redisigning
it the right way for making it usable both as a CLI tool and as a client
library.

Problem Description
===================

Most common problems of Fuel Client include:

* Bad coverage of Fuel API.

* Not very clear command line interface

* Inappropriate design as for library

* It is not convenient enough to use it outside of Fuel-Web project

* It suffers from bad quality of the codebase in general


Proposed Changes
================

Proposed refactoring consists of several major steps:

* Get migration to Cliff done.

  Now a lot of code in Fuel Client re-invents the wheel and does it in the
  lease effective manner possible. Getting rid of it and re-using the same
  functionality from Cliff is the what everyone agreed to do.

* Re-use existing tools and libraries from OSLO for building clients.

  That would allow to implement less weels and be more compatible with
  some stuff from upstream there is a need to be compatible with, e.g,
  client configuration options and settings.

* Get rid of the old library code. Leave CLI code as a compatibility layer.

  Fuel Client is unusable as a library now. There's no sense in keeping that
  code so it can be removed and replaced with an appropriate implementation
  which can be used as a Python API wrapper.

  Keeping compatibility with the old command line interface for at least one
  release is a must. For that the original argument parser and result rendeder
  should be kept as a compatibility layer. It can be removed in any of the
  following releases.

  The implementation of the CLI should only parse command line arguments and
  render results. The rest of the work should be done by the above mentioned
  API wrapper.

* Move Fuel Client into a separate repository.

  Keeping it in it's current location inside the common fuel-web repo makes it
  harder to use it outside of Fuel project. Also it puts more repsonsibility to
  the fuel-core team. Since Fuel CLient is ment to be a simple API wrapper for
  Python and a CLI tool, it does not require as many fuel-core's attention as
  the rest of the stuff in the fuel-web repo and can be easily moved out.
  In addition to that having a separate repository will allow re-using several
  jobs from OpenStack-Infra in for making gate testing better.

  The proposal is to create a python-fuelclient repository at Stackforge and
  place source code of the client there. Since the client was stored in the
  common repository, there's no sane way of preserving the history of changes.

  Making another Launchpad repo should also make it easier for developers from
  outside of Fuel project to file and fix bugs in Fuel Client.

* Use own versioning for Fuel Client.

  Moving Fuel Client into a separate repository allows to introduce a separate
  versioning model for it. That will allow to release bug fixes without
  depending of Fuel's release cycle.

  Unbinding from the Fuel releases completely does not seem reasonable so the
  proposal is to introduce the following versioning model:

  All stable versions will have a A.B.C name where A and B are the same as the
  newest version of Fuel supported, i.e., the current stable version of Fuel
  and C is the release of Fuel Client within that stable version of Fuel.

  In order to let usage of the current development version of Fuel the alpha
  postfix is added to the version name, e.g., python-fuelclient_6.1.5-alpha.

* Publish releases of Fuel Client to PyPi.

  In order to make it possible to use Fuel Client outside of the Fuel's scope
  it's reasonable to publish it to PyPi. Since it's open-source and is released
  under the Apache license there's no obstacle for that.


Other End User Impact
---------------------

* This refactoring is excepted to bring cleaner CLI and make it possible to
  use the Fuel Client as a Python wrapper for Fuel API.

* Potentially proposed changes could lead to a sligthly different command line
  interface. However, keeping it backwards-compatible for a one or a few more
  releases should be sufficient for all end-users. Finally users will get
  a cleaner command line interface.

* It will be easier including fuelclient as a requirement to any project.
  Publishing to PyPi will also allow installing and updating it easier.


Performance Impact
------------------

There should be no performance impact.


Deployer Impact
---------------------

Proposed changes include moving Fuel Client into a separate repository so
all the stuff which now looks for it inside fuel-web repository won't be able
to find it there. If it's crucial to have Fuel Client inside fuel-web repo
it will be possible to greate a git submodule for it.

However, since Fuel Client will be released on PyPi it will be possible to just
add it to standard package requirements or install manually from a script with
pip. Those will be the recommended ways of installing Fuel Client.

Separate versioning will allow to update Fuel Client faster where it is
required.


Developer Impact
----------------

* As a result of moving to a separate repo the whole change log will be lost.

* Developers will have to migrate their ongoing patches to the new repo.

* Merging patches will be faster due to smaller load to the repo-core team.

* Triaging and searching bugs will be easier because of a separate Launchpad
  project.


Alternatives
------------

* Keep Fuel Client in the same common repository.

  It makes merging patches, triaging bugs, reviewing code and using
  the client outside of Fuel project harder.

* Bind client releases to Fuel releases.

  Does not allow to release hot fixes and aplphas.

* Not publishing to PyPi.

  Makes installation and upgrades harder. Has no technical reason.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>

Work Items
----------

* Create a separate repository in Stackforge and Gerrit and set up basic CI
  jobs.

* Move Fuel Client's sources to that repo and move all unmerged patches to the
  appropriate gerrit project.

* Make an alpha release of the client so I can be tested with the ongoing
  release of Fuel.

* Land basic Cliff integration patch which leaves the old CLI arguments parser
  as a compatibility layer.

* Start implementing other improvements.


Dependencies
============

* [1] Refactoring Fuel Client blueprint incorporates some of the ideas
      described here and therefore should be implemented.


Testing
=======

Unit testing
------------

Unit tests should be ran on different Python versions. It is possible to use
python-jobs from OpenStack CI for that. Unit tests should not do invocations
to Nailgun as they do now.

Integration Tests
-----------------

For integration testing a separate job should be set up. That job should run
real Nailgun and excercise Fuel Client against it.

Documentation Impact
====================

Since Fuel Client can be used as a library all it's functions have to be
implemented. Documentation should be put into a doc directory in the root
of the repository. It is possible to use documentation jobs from OpenStack CI
to automatically test build and publish documentation.

User Documentation
------------------

Fuel user manual will have to be updated.

Developer Documentation
-----------------------

Fuel developer documentation. Probably there is a need for having a place
where Fuel Client documentation gets published independently of Fuel's main
documentation.

References
==========

* [1] https://blueprints.launchpad.net/fuel/+spec/refactoring-for-fuelclient
