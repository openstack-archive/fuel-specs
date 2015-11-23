..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================
Get rid of Docker containers on the master node
===============================================

https://blueprints.launchpad.net/fuel/+spec/get-rid-docker-containers

--------------------
Problem description
--------------------

We introduced Docker containers on the master node a while ago when we
implemented first version of Fuel upgrade feature. The motivation behind
was to make it possible to rollback upgrade process if something goes wrong.

Now we are at the point where we can not use our tarball based upgrade
approach any more and those patches that deprecate upgrade tarball has been
already merged. Although it is a matter of a separate discussion,
it seems that upgrade process rather should be based on kind of backup
and restore procedure. We can backup Fuel data on an external media,
then we can install new version of Fuel from scratch and then it is
assumed backed up Fuel data can be applied over this new Fuel instance.
The procedure itself is under active development, but it is clear that
rollback in this case would be nothing more than just restoring from
the previously backed up data.

Although there are potential advantages of using Docker on the Fuel
master node, but our current implementation of the feature seems not mature
enough to make us benefit from the containerization.

At the same time there are some disadvantages like:

* It is tricky to get logs and other information (for example, rpm -qa)
  for a service like shotgun which is run inside one of containers.
* It is specific UX when you first need to run
  `dockerctl shell {container_name}` and then you are able to debug something.
* When building IBP image we mount directory from the host file system
  into mcollective container to make image build faster.
* There are config files and some other files which should be shared
  among containers which introduces unnecessary
  complexity to the whole system.
* Our current delivery approach assumes we wrap into RPM/DEB packages
  every single piece of the Fuel system. Docker images are not an exception.
  As far as they depend on other rpm packages we forced to build docker-images
  RPM package using kind of specific build flow.
  Besides, this package is quite big (300M).
* It would be great to make it possible to install Fuel not from ISO
  but from RPM repository on any RPM based distribution. But it is double work
  to support both Docker based and package based approach.

----------------
Proposed changes
----------------

The proposal is to stop using Docker containers on the Fuel master node which
means at least the following:

* Remove all Docker related code from the build system (fuel-main). That is
  going to make build process a little bit faster.
* Modify the Fuel master node deployment script that will run
  :code:`puppet apply {service}.pp` tasks one by one.
  That is going to make the deployment process
  significantly simpler and around 5 minutes faster.

Also nailgun puppet module seems outdated and needs to be re-worked to reflect
our current deployment approach. For example, it contains python virtual
environment management code. Since we created this module with the intention
to use it with a single site.pp (contradicts to task based approach), it
contains a lot of anchors and :code:`require` statements that are simply
not needed when using separate tasks. If we remove these complications
the module will be much easier to maintain. So, the suggestion is to create
fuel puppet module based on nailgun module (i.e. fork nailgun module),
but free from all those complicated unnecessary things.

We won't remove Docker service itself from the master node, so
users/developers can still use it for running specific services. Third party
plugins will also be able to use Docker to isolate plugin related stuff.

Unfortunately, we don't have resources to follow OpenStack deprecation policy
in this field and support both Docker and Docker-free deployment schemes
at the same time during next couple releases.

Web UI
======

None

Nailgun
=======

None

Data model
----------

None

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

None

Fuel Library
============

Nailgun puppet module is going to be forked and Fuel puppet module will be
created.

------------
Alternatives
------------

Reimplement docker support as appropriate: like don't ship containers
as packages, don't build containers in run time but use custom and offline,
if required, docker repos on master node.


--------------
Upgrade impact
--------------

As said, we can not use our current upgrade approach any more, because
it assumes we can run upgrade script in place to bring the master node
to the up to date state. When switching from Centos 6 to Centos 7 it
is barely possible to be content with just a script. Instead, it is
much easier to backup all necessary data, then re-install
the node from scratch and then apply backed up data to
the newly installed node.

However, when upgrading from Fuel 8.0 to Fuel 9.0 we essentially have to
implement two restore procedures:

* w/o Docker support (for applying backed up data to the newly installed
  Fuel 9.0 master node w/o containers)
* with Docker support (for applying backed up data to the newly installed
  Fuel 8.0 master node with containers if something goes wrong)

There is BP on development of proper backup/restore procedure to support
Centos 6/7 upgrade [#backup]_.

As for patching, it is also going to become simpler as we won't need to
re-build containers and restart them.

---------------
Security impact
---------------

Services won't be isolated from each other and from the master node.

--------------------
Notifications impact
--------------------

All those notifications that are related or just mention docker should
be either modified or removed to reflect the new container-free
deployment scheme.

---------------
End user impact
---------------

A user won't need to run `dockerctl shell {containername}` to get access to
the environment where a given service is running. So, it is going to
make UX simpler, which is rather positive.

As a part of proper deprecation process we should substitue dockerctl
script with a script that will print warning message and exit. Then
in the next Fuel release we will remove this warning script.

We should also inspect all other possible places where Docker containers
are mentioned one way or another. All such UX messages should either
be removed or substituted with approptiate warning messages.

------------------
Performance impact
------------------

Docker containers provide so thin abstraction layer that performance
is likely not to change. If there will be some notable changes, they
certainly must be positive. We should make sure that performance
impact of the feature is either positive or neutral.
Anyway, we should schedule testing hours for the feature
on Fuel scale lab.

The master node deployment is to become faster as we won't spend time
for unpackaing Docker images and rebuilding Docker containers.

-----------------
Deployment impact
-----------------

Deployment script is going to become simpler as we won't have this Docker
layer. All Fuel related services are to be deployed on the host. Besides,
this going to make the deployment process faster as we won't spend time
building containers from images.

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

Currently we wrap every single Fuel component into RPM/DEB packages and
Docker images are not an exception. As far as Docker images depend on other
packages, we are forced to build this docker-images package using kind of
specific flow, which makes the build process more complicated and longer.

Getting rid of Docker containers is going to make the Fuel build
infrastructure simpler and thus easier to maintain.

We should also make sure that all those places where the master node Docker
service is used (testing, building, etc.) will be properly modified.

--------------------
Documentation impact
--------------------

This change needs to be thoroughly reflected in the Fuel documentation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>

Mandatory design review:
  Anastasia Urlapova <aurlapova@mirantis.com>
  Igor Kalnitsky <ikalnitsky@mirantis.com>
  Oleg Gelbukh <ogelbukh@mirnatis.com>
  Sergii Golovatiuk <sgolovatiuk@mirantis.com>
  Matthew Mosesohn <mmosesohn@mirantis.com>

Work Items
==========

* Fuel Library
  Create fuel puppet module and a set of {task}.pp files that are going
  to be run one by one using `puppet apply`.
* Fuel Main
  Remove all Docker related code (packages, auxiliary scripts, etc.).
* Shotgun
  Modify report config file so it does not contain commands that are
  supposed to be run inside containers.
* Fuel Astute
  Modify log paths that are currently contain :code:`docker-logs` part.
* Fuel QA
  Modify all those tests which are based on Docker container so they
  use plane OS tools.

Dependencies
============

None

------------
Testing, QA
------------

Unit tests are not going to be affected by this change. System tests should
be modified so they stop using Docker capabilities related to the master node.
In turn those tests that use Docker as a runtime environment could continue
using it as we are not going to remove Docker service from the master node.

Cluster deployment process is not to be affected at all, so deployment tests
should not be touched except those which use Docker capabilities
(those should be modified).

Test plan should include at least the following:

* Build
  Build process should not be broken (custom and production).
* UX
  All master node Docker related commands, notifications, etc. should
  either be removed or properly warn a user.
* Performance
  We should make sure that performance impact of the feature is either
  positive or neutral.
* Components
  All Fuel components can properly interact with each other.
* Depoloyment
  It must be possible to deploy Openstack clusters with the same
  configuration as in case of using Docker approach on the master node.

Acceptance criteria
===================

* Fuel master node components should be deployed w/o Docker containers.
* It should be possible to run other docker containers on the master node.
* It should be doable to implement a Backup/Restore procedure for migrating
  from containerized scheme to container-free scheme.

----------
References
----------

.. [#backup] https://blueprints.launchpad.net/fuel/+spec/upgrade-master-node-centos7
