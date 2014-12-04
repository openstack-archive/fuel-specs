..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================
Artifact based build system
===========================

https://blueprints.launchpad.net/fuel/+spec/artifact-based-build-process [1]_


Problem description
===================

Currently we use GNU Make as our build tool and we build targets with
all their prerequisites at once. Tracking lots of small files makes build
process difficult to maintain and to make sure build workspace is consistent
we run 'make deep_clean' every time before building ISO. Moreover, some ISO
components are quite stable. That means we spend
extra time for re-building everything from scratch every time when build
workspace is cleaned.

We also have poor versioning scheme for RPM and DEB repositories which does
not allow us to exactly reproduce ISO image from source code only (depends on
the state of RPM and DEB mirrors).

Another important point is that it is difficult to implement new features in
terms of GNU Make. Good example here is building upgrade tarball.


Proposed change
===============

The proposal is to switch to artifact based approach. We can split build
process into several pieces and publish the results of every build stage to
an artifact repository with some metadata (version, size, check sum,
git commit, etc). This artifact based approach has some obvious advantages:

- *Build time*
  It is possible to download binary artifacts whenever
  they are needed avoiding re-building them from scratch every time.

- *Stability*
  When we have several binary artifacts under version control it is easy to
  make build process stable and consistent. It is easy to exactly reproduce the
  results of a particular build job.

- *Flexibility*
  It is possible to combine components to get ISO image which contains definite
  set of features or implementations of a given feature.

- *Maintainability*
  It is easy to track several independent binary artifacts (their versions,
  md5). We don't need to build all artifacts from a particular commit even
  if they are located in one git repository. Most of components are quite
  independent so are their versions.

- *Ability to test components independently*
  Having binary components under version control allows us to organize
  granular functional testing. In a sense granular testing can be considered
  as a build process of a special kind. To build some artifact one needs some
  versions of other artifacts and to test some artifact again one needs some
  versions of other artifacts. For example, to test Fuel Agent (provisioning
  agent) we don't need to deploy Fuel master node, we just need to have
  pre-built OS images and bootstrap image (with Fuel Agent installed). One we
  have them we can run VM and run functional tests which can tell us whether
  Fuel Agent works and whether a particular version of Fuel Agent is compatible
  with a particular version of OS image.

- *Easy hacking*
  It is much easier for developer to build only those artifacts which depend on
  changes developer does. All other artifacts could be downloaded and quick
  test could be run to make sure changes work and are compatible with other
  components.

Let's implement artifact based build/test system in object oriented manner
using Python. Such components as package mirrors, packages, chroot environments
much easier to maintain when implemented as abstract objects (apart from
GNU Make scripts). Moreover, splitting Fuel into binary artifacts allows us
to stop enforcing teams (mirror team, package team, web team) using GNU Make
or any other particular tool. A team could use that tool which is fits their
working process better. They just need to publish their artifacts with some
metadata to an artifact repository.


Alternatives
------------

There are many build systems available and some of them are even written in
Python (like Scons and Bake). However, all those systems assume one uses task
based approach. That means we have to use a kind of DSL for describing building
process. That is convenient when one needs to do a number of simple and similar
actions. When one has to do various actions it is much easier to use plain
OOP approach.

Couple of build tools are available which have advanced highly customizable
pluggable architecture, allow to write object oriented plugings and have
artifacts and inter-project dependencies. Those tools are Apache Maven [2]_ and
Gradle [3]_. However both those tools are quite complicated to learn and
require using java and groovy languages. However, most of Fuel developers
have Python knowledge at some level. So, it seems to be a good approach
using pure Python and implement everything we need.


Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

Re-building ISO image gonna take less time as far as it is supposed to avoid
re-building everything from scratch every time we build ISO.

Other deployer impact
---------------------

None

Developer impact
----------------

It is supposed one will be able to quickly build exactly that Fuel component
where their do changes and test if it works and if it is compatible with
other Fuel components.

Implementation
==============

It is supposed to implement this change step-by-step.

0) Split Make based build system into several independent components and
organize several Jenkins jobs to build those components independently.
The result (artifact + metadata) of a job is supposed to be published
to a plain HTTP server via SCP.

If a job requires artifacts, it must be able to download those
artifacts via HTTP. If downloading fails (any reason), job must fail as well.

Those independent components are:

- deb and rpm mirrors
- puppet modules
- os images
- bootstrap image
- docker containers
- iso image
- upgrade tarball

Packages are not supposed to be treated as separate artifacts in this stage.

1) Implement artifact based build/test framework in Python so as to make it
possible to implement particular components just inheriting corresponding
Python classes. Artifacts are supposed to be implemented as highly
parametrized objects configurable using YAML files.

It is also supposed to implement universal runner class which is to run script
(GNU Make or Bash). So, YAML for runner is supposed to contain env variables
and command line string.

It is also supposed to implement serializer to make it possible to create
Jenkins jobs automatically (maybe some other serializers).

2) Implement all necessary components and their YAML descriptions (production
stage).

3) Implement helper classes (checking artifact repository consistency,
build and dependency statistics, notifiers, etc.)

Jenkins jobs are supposed to follow git and artifact repository changes and
to re-build artifacts periodically or change event driven. Every new
combination of artifacts must be tested for their compatibility. Testing is
not going to take much time as far as it is not supposed to deploy master node
and go through the total deployment flow.


Assignee(s)
-----------

Primary assignee:
  <vkozhukalov@mirantis.com>
  <nmarkov@mirantis.com>


Work Items
----------

- POC scheme
- implement build/test framework
- implement Fuel build/test system using build framework

Dependencies
============

TODO

Testing
=======

TODO


Documentation Impact
====================

It will be necessary to re-write those parts of Fuel documentation
which mention cobbler and provisioning.


References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/artifact-based-build-process
.. [2] http://maven.apache.org/
.. [3] http://www.gradle.org/