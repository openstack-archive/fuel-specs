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
components are quite stable and in most cases they should not be rebuilt .
That means we spend extra time for re-building everything from
scratch every time when build workspace is cleaned.

Packaging everything into RPM/DEB packages does not sound like a good idea
because there are things like chroots and docker containers which require
other RPM/DEB packages to be built before them. Besides there is docker
registry which is native technology for distributing docker containers.

Another important point is that it is difficult to implement new features in
terms of GNU Make. Even for simple cases we forced to use non-trivial syntax
constructions.


Proposed change
===============

Approach
--------

The proposal is to switch to artifact based approach. We can split build
process into several pieces and publish the results of every build stage to
an artifact repository with some metadata (version, size, check sum,
git commit, etc). The format of artifact repository can depend on the nature
of a particular artifact. For example, it is going to be Docker registry for
Docker containers or it can be plain http for tarballs, or yum repository for
RPM packages, etc. This artifact based approach has some obvious advantages:

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
  versions of other artifacts. On the other side, when one needs to build
  testing environment (a.k.a. testing lab) from some components
  like tftp and http servers, etc., this environment can be easily be built
  if all necessary components are packaged into artifacts. For example, if one
  needs http server for testing some component the build flow would be
  step-by-spep installing http server package and downloading and extracting
  tarball with necessary content for this http server. These two dependencies:
  package and tarball are nothing more than artifacts.
  It is absolutely unnecesary to deploy the Fuel master node and use it as an
  testing lab every time when one just needs to test provisioning agent,
  or puppet module.

- *Easy hacking*
  It is much easier for a developer to build only those artifacts which
  depend on changes developer does. All other artifacts could be downloaded
  and quick test could be run to make sure changes work
  and are compatible with other components.


Implementation
--------------

Artifact based approach is a successful concept used widely in Java world.
There are some quite good tools like Maven and Gradle which flexible and
stable enough to be used in production. Unfortunatly, neither Maven nor Gradle
can be used for Fuel as is. We need to customize them which requires having
deep knowledge in Java or Groovy.

Fuel community is Python oriented, so it is would be great to find existent
Python tool implementing artifact based approach. Possible candidates are
Waf and Nix (requires additional research). However, if these tools are not
what we need, it does not look like a difficult task to implement such a tool
from scratch totally on our own.

The tool is not going to substitute GNU make or Ruby Rake.
Instead it is going to be a framework able to resolve
artifact dependencies taking into account md5, versions, other metadata.
Every single component could be built using GNU make, Ruby Rake, Shell script
or even Python script/object. The result of the build process of any
particualar component should be an artifact.
The same concept is using Ivy + Ant. Ant in
this pair plays the same role as GNU make does,
while Ivy is a tool to resolve artifact dependencies.

Such components as package mirrors, packages, chroot environments are
much easier to maintain when implemented as Python objects
(not GNU Make scripts). Moreover, splitting Fuel into projectbinary
artifacts allows us to stop forcing teams (mirror team, package team, web team)
to use GNU Make or any other particular tool.
A team could use that tool which fits better their working process.
We just need all these artifacts to be published and available for the whole
Fuel community.

Moving gradually
----------------

The thing is that we can not switch immediately to the artifact based approach.
We need to have a kind of strategy how to do this gradually. Let's outline
here main steps:

#. Refactoring of make system

  ##. Tidy up make system throwing away unnecessary code and simplifying it
  wherever it is possible. It includes at least the following:

    - getting rid of upgrade tarball
    - getting rid of old fashioned artifacts (a.k.a if
      an artifact not in DEPS_DIR, build it)

  ##. Move building all packages that depend only on source code (level-1)
  into "perestroika". "Perestroika" currently builds OpenStack, Linux and Fuel
  related packages on every patch set. So, to build, for example, custom ISO
  we need to modify ISO build process so it downloads necessary packages from
  "perestroika" instead of building them.

  ##. Simplify building packages that depend on other packages (level-2).
  Building such packages usually takes much longer (15 min) comparing
  to building "level-1" packages. Besides, such packages usaully
  depend on several "level-1" packages and thus are going to be triggered
  frequently. It is not quite clear how to do this so far, but there are
  some possible scenarios that could help:

    - create a separate level-2 repository and modify "perestroika" so it
      builds level-2 packages asynchronously in a queue. If there is a trigger
      in the queue to build a particular level-2 package, then the next event
      triggering the same package is not going to be appended to the queue.
    - split "docker-images" package into several packages
    - split ISO build into several independent pieces

#. Introduce artifact framework and start tracking artifact dependencies
taking into account their versions and other metadata.


Alternatives
------------

There are many build systems available and some of them are even written in
Python (like Scons and Bake). However, all those systems assume one uses task
based approach. That means we have to use a kind of DSL for describing building
process. That is convenient when one needs to do a number of simple and similar
actions. When there are quite a few various actions it is much easier
to use plain OOP approach.

Couple of build tools are available which have advanced highly customizable
pluggable architecture, allow to write object oriented plugings and have
artifacts and inter-project dependencies. Those tools are Maven [2]_ and
Gradle [3]_. However both those tools are quite complicated to learn and
require using Java and Groovy languages. As far as most of Fuel developers
have Python knowledge at some level, it seems to be a good approach
using pure Python and implement everything we need.

There are also couple Python based build systems like Waf and Nix
which need some research and probably can be used as
an artifact tracking framework.


Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Upgrade tarball is going to be modified into upgrade rpm package. We used to
put Ubuntu/Centos mirrors and Docker containers into upgrade tarball but
we don't need to do this any more because Ubuntu/Centos repos are supposed to
be available either online or locally cloned and Docker containers are
currently packages into RPM packages. So, upgrade RPM package is going to
provide only python script used to upgrade the Fuel master node.

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

Re-building ISO image is going to take less time as far as it is
supposed to avoid re-building everything from scratch every time we build ISO.

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

It is supposed one will be able to build exactly that Fuel component
where the changes take place and test if it works and if it is compatible with
other Fuel components. Testing feedback loop is going to shorten significantly.

Infrastructure impact
---------------------

Build process is going to be changed so as to make modular and fast.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <vkozhukalov@mirantis.com>


Work Items
----------

- Tidy up fuel-main
- Unify package building
- Introduce artifact tracking framework
- Develop modular functional tests

Dependencies
============

None

Testing
=======

None


Documentation Impact
====================

It is necessary to re-write those parts of Fuel documentation
which mention fuel-main.


References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/artifact-based-build-process
.. [2] http://maven.apache.org/
.. [3] http://www.gradle.org/