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
Using the built binary kernel module packages on bootstrap could signicantly
reduce the size of the bootstrap.

.. note:: Since the Ubuntu is currently used for deploying, building of
 .deb packages only shall be implemented.

-------------------
Problem description
-------------------

The key strength of `Dynamic Kernel Module Support (DKMS) <https://help.ubuntu.com//community/DKMS>`_
is the ability to rebuild the required kernel module for a different version
of kernels. But there is a drawback of installing DKMS kernel modules into
bootstrap. DKMS builds a module during installation, that queries the
installation of additional packages like ``linux-headers`` and a tool-chain
building. Adding such packages unnecessarily oversizes the bootstrap.


DKMS builds the given drivers sources against different kernels versions,
but not all the kernel module sources can be compiled by DKMS.
The ABI (kernel functions) may be changed among different kernels, and
the compilation of a module can potentially fail when calling
non-existing of expired functions of the kernel. Building binary kernel
module packages from DKMS let us know about issues with the sources
(if any) prior building new bootstrap.

In order to reduce the size of dynamically built bootstrap image and catch
the potential faults of building binary modules against the current kernel
used on the bootstrap the functionality for building binary kernel module
packages from the corresponding DKMS packages shall be implemented. 

Use cases
=========

.. note:: When DKMS kernel module packages are not to be installed
 on the bootstrap, the step of building binary kernel .deb packages
 from DKMS is absolutely unnecessarily.

The following use case describes how to avoid to install DKMS packages on
a bootstrap:

.. note:: The step creating dedicated repository should be done manually,
 only once, and at the beginning of the procedure.

* Create dedicated repository (folder) for keeping the binary kernel modules
  (in form of .deb packages) exported from the corresponding DKMS packages.
  The repository could be placed on the Fuel master node next to existed
  one.

* Re-build required DKMS kernel module packages and save the produced
  binary kernel module packages in the created repository mentioned above.
  (This functionality is expected to be implemented in the scope of this spec.)

* Update the content of the repository (created on the very first step)
  and rebuild the bootstrap with required binary kernel module packages keeping
  in the repository.

Rebuilding kernel module binaries shall be done prior building the bootstrap.
Each time, when the new version of the kernel is updated on a bootstrap,
the binary kernel modules shall be rebuilt against the new kernel as well.

The details about creating repository and building new bootstrap could be
found in the `document`_.
.. _`document`: https://docs.mirantis.com/openstack/fuel/fuel-8.0/fuel-install-guide.html#bootstrap-inject-driver

User Experience
===============

* Fuel provides command-line utilities to build binary kernel module packages
  from given DKMS packages with customizations.

Example of user steps, required to build 

.. code-block:: bash

  $ fuel-bootstrap dkms2bin --dkms i40e-dkms-1.3.47~ --out-dir /var/www/nailgun/repo/dkms2bin-repo
  
  ... creating chroot
  ... installing DKMS packages, building
  ... exporting kernel binary module packages into the --out-dir


----------------
Proposed changes
----------------

#. The DKMS packages shall be excluded from the list of packages
   installing on the bootstrap by default. (In the current
   implementation DKMS packages are installed on bootstrap, what
   is not a good idea.) A customer shall explicitely include required
   additional kernel modules to the list. (Installing binary module packages
   on the bootstrap is more preferable than DKMS moules.)
#. The step of creating additional repository, building binary kernel
   module packages from DKMS packages and updating the repositories
   methodata shall be done by a customer and should not to be expected
   done by default.
#. The script for building a boostrap image shall be extended with the
   additional command and keys enabling a customer to build binary
   kernel module packages (in .deb format) from corresponding DKMS
   module packages.
#. The additional command (let call it "fuel-bootstrap dkms2bin") shall
   contain the keys which specify: 

     * list of DKMS packages required to rebuild;
     * output directory where rebuilt binary kernel module packages
       should be placed; 
     * version of linux kernel using for building kernel modules
#. The command shall provide warning message when building a binary
   kernel module package from corresponding DKMS package failed.
#. New tests covering the implementation of the new functionality
   (build binary kernel module packages from corresponding DKMS) 
   shall be designed in scope of the work.
#. The documentation shall be extended with the new command description.
#. The same functions have been designed for building bootstrap shall be
   used for rebuilding DKMS to binary kernel module packages.

The following steps are required to be implemented for building binary
kernel module packages from DKMS packages from high level view:

#. Create a chroot folder like it has been implemented in the script 
   for building bootstrap images on fuel master node.
#. Install extra packages (required for building DKMS kernel modules):
   
    * linux-headers (the same version as it uses for building the boostrap);
    * build-essential package;
    * dkms package;
    * deb-helper package;
#. Install all DKMS packages given in the list of packages required to rebuild.
#. Run 'dkms mkdebtarball' command for each DKMS kernel module to create the
   archive with corresponding binary kernel module built against the current
   kernel.
#. Extract and save the produced binary kernel module packages from the tarballs
   into output directory.
#. Remove the chroot folder. 


Web UI
======

No changes is required in UI. 
All has been implemented in scope of the dynamically building bootstrap.


Nailgun
=======

The CLI tool shall be extended to allow rebuilding the DKMS packages into binary
kernel module packages.


Nailgun-agent
-------------

Fuel-agent boostrap CLI command shall be extended with new command enabling user
rebuild DKMS packages to binary kernel module packages.

Data model
----------

The binary kernel module packages rebuilt from the DKMS is expected to be saved
into the dedicated repository (forlder) next to the deployed on Fuel master
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

Bootstrap generator
===================

None

The bootstrap generator has had the option for including extra packages
on bootstrap. Since additional kernel modules are going to be add as
ordinal .deb packages, nothing shall be done for the boostrap generator.


Bootstrap container format:
---------------------------

None


Bootstrap management
====================

The python-wrapper script for managing bootstrap images is called
fuel-bootstrap and has the following commands: 

::

    fuel-bootstrap < COMMAND > [ arguments ] [ flags ]


Commands:

.. code-block:: bash


  list              lists all available bootstrap images

  import            allows to import already created bootstrap image to the
                    system
                    (archive file in format tar.gz)

  activate          sets selected image as an active - i.e. the image that will
                    be used to bootstrap all the nodes deployed from this
                    Fuel Master

  delete            deletes specified image from the system


The current fuel-bootstrap implementation shall be extended with the additional
command:

.. code-block:: bash

  dkms2bin          rebuild DKMS modules into binary kernel module packages
                    against the current kernel version

The command dkms2bin shall have the following obligatory keys:

.. code-block:: bash

 --dkms    < DKMS package >    
 --out-dir < output dir > 

The --dkms key could be repeatable to let emumirate a few DKMS packages for
rebuilding.
The --out-dir option sets the output directory where the binary kernel module
packages should be saved.


The optional kernel version key shall allow changing the kernel version against
which the DKMS kernel module should be built:

.. code-block:: bash

 --kver  < kernel version > 

The additional option ``do not remove`` the temporary build image for
debugging perposes shall be implemented as well:

.. code-block:: bash

 --do-not-remove


Example:

.. code-block:: bash

  $ fuel-bootstrap dkms2bin --dkms i40e-dkms hpsa-dkms --out-dir /var/www/nailgun/ubuntu/dkms/pool

    ... creating chroot environment
    ... installing i40e-dkms package, building .. OK
    ... installing hpsa-dkms package, building .. OK
    ... exporting kernel binary module packages into /var/www/nailgun/ubuntu/dkms/pool/


.. note:: The CLI command arguments and output could be changed during implementation. The final version shall be described in the documentation.


Plugins
=======

None

------------
Alternatives
------------

Installing DKMS packages on boostrap is not a good idea due to oversizing
boostrap images and increasing time of building them. But this is how it
has been implemented now. 


--------------
Upgrade impact
--------------

Removing DKMS packages from list of packages installin on boostrap by default
now will request a couple of additional steps during building boostrap for 
non-supported equipment (creating additional repo, rebuilding DKMS packages
to binary kernel packages, adding the built kernel modules on the boostrap).

All these efforts are required only in case when equipment is not supported
with the drivers shipped in Ubuntu by default.

The step of building new boostrap with additional kernel modules could not
be done by default (during installation), because it's a user burden to add
drivers for non-standard equipment based on what equipment he actually uses.


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

A fuel master operator will be available to build customized bootstrap images
without DKMS kernel modules (but with binary kernel modules), which reduce
size of bootstrap images and time for deploying huge infrostructure.

Since the DKMS kernel modules are not to be included to the boostrap
by default any more, the rebuilding required binary kernel modules from
DKMS packages and adding the additional kernel modules on the boostrap
is a fuel master operator burden.

--------------------
Documentation impact
--------------------

The documentation describing this design change shall be make up. There
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
    * Aleksey Kasatkin <akasatkin@mirantis.com>
    * Alexey Zvyagintsev <azvyagintsev@mirantis.com>

QA engineers:
    * Dmitry Kalashnik <dkalashnik@mirantis.com>


Work Items
==========

* Modify builder script to provide required changes for rebuilding DKMS
  packages to binary kernel module packages.
* Exclude DKMS packages from list of packages installed on bootstrap
  by default.
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
* The implementation shall provide warning message(s) when the build failed.
* The documentation covering use cases for rebuilding DKMS packages into
  binary kernel module packages and adding the packages on the bootstrap
  shall be provided for users.


----------
References
----------

