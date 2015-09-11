..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
Build ISO in less than 10 minutes
=================================

https://blueprints.launchpad.net/fuel/+spec/fast-iso-building

--------------------
Problem description
--------------------

Currently we have monolithic ISO build script, but, in fact, ISO
consists of a few components which can be built and published by separately.
Ideally, all Fuel components should be packaged into RPM/DEB by Perestoika
and then we just need to download them and put them together on the Fuel ISO.
So, ISO building should not take more than 10 minutes.

----------------
Proposed changes
----------------

The idea behind this spec is to collect top level information about all other
efforts towards making the Fuel build system simple and modular. The whole idea
is to split Fuel build script into a set of independent scripts which
are to be run separately. Besides, as far as we are moving towards package
based delivery approach, we should get rid of all things that bind ISO
build process with any Fuel logic (deployment, upgrade, etc).

#. We need to get rid of upgrade tarball and make upgrade flow
   totally package based [#upgrade]_.
#. We need to move building CentOS target images to the Fuel master
   node [#centostarget]_.
#. We need to get rid of CentOS based bootstrap image in favor of
   Ubuntu based one which is currently 'experimental' and is built
   on the master node [#ubuntubootstrap]_.
#. We need to move building of docker images package to Perestroika
   [#dockerperestroika]_.
#. We need to get rid of building any packages together with ISO. All packages
   (including L2) should be built using Perestroika [#packagesperestroika]_.


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

None

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

None

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

Developers are going to get faster testing procedure and shorter feedback loop.

--------------------------------
Infrastructure/operations impact
--------------------------------

There will be a set of separate jobs for building Fuel components. Apart from
L1 packages we still have 3 L2 packages (that depend on other packages):

* CentOS target images package
* CentOS based bootstrap image package
* Docker images package

Usually Perestroika jobs are triggered by gerrit events but for L2 packages
build jobs should be triggered by L1 jobs. Every time when one of the L1
packages is re-built, all L2 packages that depend on this L1 package should
be also re-built. For example, building docker images L2 package
usually takes 10-15 minutes. So, the load on Perestroika workers is going
to increase significantly.

--------------------
Documentation impact
--------------------

The part of the Fuel documentation describing build system and build
flow should be changed.

--------------------
Expected OSCI impact
--------------------

Perestroika should build Level 2 packages.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vladimir Kozhukalov <vkozhukalov@mirnatis.com>

Mandatory design review:
  Sergey Kulanov <skulanov@mirnatis.com>


Work Items
==========

See other specs, mentioned in Dependencies section.

Dependencies
============

* [#upgrade]_
* [#packagesperestroika]_
* [#centostarget]_
* [#ubuntubootstrap]_
* [#dockerperestroika]_

------------
Testing, QA
------------

ISO built using this new approach should be tested the same way as current ISO.

Acceptance criteria
===================

ISO building should not be longer than 10 minutes.

----------
References
----------

.. [#upgrade] https://blueprints.launchpad.net/fuel/+spec/package-master-node-upgrade
.. [#packagesperestroika] https://blueprints.launchpad.net/fuel/+spec/build-fuel-packages-using-perestroika
.. [#centostarget] https://blueprints.launchpad.net/fuel/+spec/fuel-agent-build-centos-images
.. [#ubuntubootstrap] https://blueprints.launchpad.net/fuel/+spec/fuel-bootstrap-on-ubuntu
.. [#dockerperestroika] https://blueprints.launchpad.net/fuel/+spec/docker-images-perestroika
