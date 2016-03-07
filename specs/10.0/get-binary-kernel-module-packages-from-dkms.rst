..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================================================================
Dynamically build binary kernel module packages from DKMS packages for Ubuntu-bootstrap
=======================================================================================

https://blueprints.launchpad.net/fuel/+spec/dynamicly-build-binary-modules-from-dkms


This document describes functionality for building binary kernel module
packages from corresponding DKMS packages (shipped in the DKMS format).
Using pre-built binary kernel module packages in the bootstrap image could
significantly reduce the size of the image. Rebuilding the package also
reveals potential build issues.

-------------------
Problem description
-------------------

The key strength of `Dynamic Kernel Module Support (DKMS)`_
is the ability to rebuild the required kernel module for a different version
of kernels. But there is a drawback of installing DKMS kernel modules into
bootstrap. DKMS requires additional packages like ``linux-headers`` and a
tool-chain building to be installed, which unnecessarily oversizes
the bootstrap.

DKMS allows to build a particular driver for various versions of the Linux
kernel. However, kernel ABI (binary API) may change, what makes the
given driver source code incompatible with the kernel. The driver could
invoke non-existed functions or data structures etc.
Rebuilding binary module packages from DKMS would have helped to reveal
potential issues which may be encountered installing a particular DKMS package.

In conclusion, implementing the functionality for rebuilding binary kernel
module packages from DKMS packages will allow reducing size of bootstrap images
(to compare with including DKMS modules case) and catch the potential faults
in building/installing DKMS modules on bootstrap.


Use cases
=========

.. note:: When DKMS kernel module packages are not to be installed
 on the bootstrap, the step of building binary kernel .deb packages
 from DKMS is absolutely unnecessarily.

The following use case describes how to avoid to install DKMS packages on
a bootstrap:

.. note:: The step creating dedicated repository should be done manually,
 only once, and at the beginning of the procedure.

* Create dedicated repository for keeping the binary kernel modules
  (in form of .deb packages). The repository could be placed on the
  Fuel master node next to the other repositories.
  (The `Packetary`_ is a sutable tool to do that.)

* Re-build required DKMS kernel module packages and save the produced
  binary kernel module packages in the created repository mentioned above.

* Update the content of the repository for the binary kernel modules (mentioned
  above) and rebuild the bootstrap with required binary kernel module packages.
  The capabilities of `Packetary`_ utility could be used to update repository
  metadata.

Rebuilding kernel module binaries shall be done prior building the bootstrap.
Each time, when the new version of the kernel is updated on a bootstrap,
the binary kernel modules shall be rebuilt against the new kernel as well.

The details about creating repository and building new bootstrap could be
found in the `document`_.


----------------
Proposed changes
----------------

#. The DKMS packages shall be excluded from the list of packages
   installed on the bootstrap by default. (Current implementation
   installs DKMS packages in the bootstrap image, which is not recomended.)
   A user shall explicitly include required (additional) kernel modules
   to the list of packages installing on the bootstrap.
   (Installing DKMS modules into target IBP images is still preferable
   due to ability of DKMS modules to be rebuilt against the new kernel
   version in case of kernel upgrade.)
#. The step of creating the additional repository, building binary kernel
   module packages from DKMS packages and updating the repositories
   metadata shall be done by a user and should not to be expected to be
   done by default during building a bootstrap.
#. The case of building a few bootstraps with different kernel version is
   possible. The repository will contain the packages for different kernel
   version, e.g.

    * i40e_1.3.47-3.13.0-77-generic_x86_64.deb
    * i40e_1.3.47-3.13.0-75-generic_x86_64.deb
    * i40e_1.3.47-3.13.0-83-generic_x86_64.deb

   A user shall specify exact version of the required kernel module package
   (e.g. i40e_1.3.47-3.13.0-77-generic) for building bootstrap with the
   corresponding kernel version (3.13.0-77-generic).
#. The name of binary kernel module package shall consist of (at least)
   the name of the kernel module, kernel version against which it has been
   built and the architecture.
#. The `Packetary`_ shall be extended with the additional functionality
   enabling a user to build binary kernel module packages from corresponding
   DKMS module packages. There is a `blueprint about re-building DKMS modules
   by Packetary`_.
#. The error messages shall be provided in case of fault when building
   a binary kernel module package from corresponding DKMS package failed.

The following steps are required to be implemented for building binary
kernel module packages from DKMS packages from high level view:

#. Create a chroot (isolated environment in which application processes
   could be executed) like it has been implemented in the script
   for building bootstrap images on fuel master node.
#. Install extra packages (required for building DKMS kernel modules):

    * linux-headers (the same version as it uses for building the bootstrap);
    * build-essential package;
    * dkms package;
    * deb-helper package;
#. Install all DKMS packages given in the list of packages required to rebuild.
#. Build (either build according the prepared set of debian/* files or
   run 'dkms mkdebtarball' command for each DKMS kernel module to create the
   disk-driver archive with corresponding binary kernel module built against
   the current kernel).
#. Destroy the chroot environment (implies killing of all processes which
   are running inside this chroot, unmounting of all necessary mount points
   and then finally, removing the chroot directory).
   The chroot environment could not be destroyed for debugging purposes,
   if it explicitly requested by an operator.


Web UI
======

None


Nailgun
=======


Fuel-bootstrap
--------------

None

Data model
----------

The binary kernel module packages rebuilt from the DKMS is expected to be saved
into the dedicated repository (folder) next to the deployed on Fuel master
node. So no changes to the Data model are required.


REST API
--------

None


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Library
============

None


Fuel Client
===========

None


User Experience
===============

* Packetary shall provides command-line utilities to build binary kernel module packages
  from given DKMS packages with customizations. There is a `blueprint about re-building
  DKMS modules by Packetary`_.

The implementation and syntax of the CLI commands are the corresponding team
responsibility.

Example of user steps, required to build

.. code-block:: bash

  $ Packetary dkms2bin --dkms i40e-dkms-1.3.47~ --out-dir /var/www/nailgun/repo/dkms2bin-repo

  ... creating chroot
  ... installing DKMS packages, building
  ... exporting kernel binary module packages into the --out-dir

The documentation shall be extended with the new command description.


Bootstrap generator
===================

The bootstrap generator has had the option for including extra packages
in a bootstrap image. Since additional kernel modules are to be add as
regular .deb packages, nothing shall be done for the bootstrap generator.


Bootstrap container format:
---------------------------

None


Bootstrap management
====================

None

Fuel-agent
==========

None


Plugins
=======

None

------------
Alternatives
------------

Installing DKMS packages in a bootstrap image is not a good idea due to
oversizing bootstrap images and increasing time of building them. But
this is the current implementation.
There is alternative to build a binary kernel modules for each kernel
version on CI side and keep it in own repo. The pros are keeping all
built packages in one place. The cons are:

#. Testing built modules required access to corresponding hardware, but
   customer could built and check the built module with his hardware.

#. New kernel updates shall be tracked and the DKMS modules should be
   rebuilt against the new kernel, but we don't know exactly do someone
   need it or not.

So there is no advantages to build DKMS modules on our side.

The other way is extend the Fuel-bootstrap CLI command with new commands
for rebuilding DKMS packages to binary kernel module packages. In
such case Fuel-agent should be modified with additional 'do_action'. But
it will add unneccesarely code and doesn't have sense because the Packetary
was invented for (re)building deb and rpm packages. So using the Packetary
looks a better solution.

There is a document describing the steps to `rebuild DKMS manually`_, but
it would better to have a tool to simplify work.

--------------
Upgrade impact
--------------

Removing DKMS packages from list of packages installing in a bootstrap image
by default will request a couple of additional steps during building bootstrap
for non-supported equipment (creating additional repo, rebuilding DKMS packages
to binary kernel packages, adding the built kernel modules on the bootstrap).

All these efforts are required only in case when equipment is not supported
with the drivers shipped in Ubuntu by default.

The step of building new bootstrap with additional kernel modules could not
be done by default (during installation), because it's a user burden to add
drivers for non-standard equipment based on what equipment he/she actually
uses.


---------------
Security impact
---------------

None

--------------------
Notifications impact
--------------------

None

------------------
Performance impact
------------------

None

---------------
End user impact
---------------

None

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

The documentation describing this design change shall be made up. There
should be a clearly documented procedure how to add new repository, build
a custom bootstrap image with binary kernel module packages and update the
content of the custom repository.

--------------------
Expected OSCI impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
    * Albert Syriy <asyriy@mirantis.com>

Mandatory design review:
    * Vladimir Kazhukalov <vkazhukalov@mirantis.com>
    * Bulat Gaifullin <bgaifullin@mirantis.com>
    * Aleksey Kasatkin <akasatkin@mirantis.com>
    * Alexey Zvyagintsev <azvyagintsev@mirantis.com>

QA engineers:
    * Dmitry Kalashnik <dkalashnik@mirantis.com>


Work Items
==========

* Modify `Packetary`_ to provide required changes for rebuilding DKMS
  packages to binary kernel module packages.
* Exclude DKMS packages from list of packages installed in a bootstrap
  image by default.
* Create documentation regarding implemented changes.

Dependencies
============

-----------
Testing, QA
-----------

* Manual testing should be run according to the CLI use cases steps.
* System tests should be created for the implementation of rebuilding
  DKMS modules into binary kernel module packages.


Acceptance criteria
===================

* The implementation shall allow to build binary kernel module packages
  from corresponding DKMS packages and save the outcome to created prior
  repository/folder etc.
* The implementation shall provide error message(s) when the build failed.
* The documentation covering use cases for rebuilding DKMS packages into
  binary kernel module packages and adding the packages on the bootstrap
  shall be provided for users/operators/administrators.


----------
References
----------

.. _`Dynamic Kernel Module Support (DKMS)`: https://help.ubuntu.com//community/DKMS
.. _`document`: https://docs.mirantis.com/openstack/fuel/fuel-8.0/fuel-install-guide.html#bootstrap-inject-driver
.. _`Packetary`: https://wiki.openstack.org/wiki/Packetary
.. _`blueprint about re-building DKMS modules by Packetary`: https://blueprints.launchpad.net/fuel/+spec/packetary-rebuild-dkms
.. _`rebuild DKMS manually`: http://docs.openstack.org/developer/fuel-docs/devdocs/develop/custom-bootstrap-node.html#adding-dkms-kernel-modules-into-bootstrap-ubuntu
