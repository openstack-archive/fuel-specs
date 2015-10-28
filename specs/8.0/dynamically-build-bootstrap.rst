..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================================
Dynamically build Ubuntu-based bootstrap on master node
=======================================================

https://blueprints.launchpad.net/fuel/+spec/dynamically-build-bootstrap


This document describes bootstrap images configuration,
building, and switching between several bootstrap images
using CLI.

We should support Ubuntu bootstrap images to have one common Operating System
for bootstrapping and deploying nodes. Only ubuntu kernel image customization
should be possible. Other kernels will not be supported.

-------------------
Problem description
-------------------

Now we use CentOS as bootstrap image. This leads to old
version of kernel/drivers/packages. We need to move from CentOS to Ubuntu
which will delivers fresh components.
Moreover we use Ubuntu as post-provisioning system,
this will give us more consistent environment.
Last but not least, having Ubuntu on bootstrap stage will help us support
the discovery and configuration of components on new servers users might have
(of those not supported by CentOS 6.x)

At the moment bootstrap image customization is a complicated process.
Currently the builder script requires editing config files and running scripts
on the master node.
In addition operator needs a way to add custom packages inside bootstrap.

Therefore a proper CLI-tool for configuring, building
and switching to new bootstrap images is required.

Use cases
=========

#. Dynamically build Ubuntu-based bootstrap image during
   Fuel Master node installation [DONE]
   Goal: Build initial bootstrap image during Fuel master node installation,
   prepare for node discovery via PXE boot

    #. User launches Fuel master node from Fuel ISO
    #. Fuel Menu presents user with (new and always shown) options to:
        * adjust repo location for bootstrap image
          (default should be provided) [DONE]
        * specify proxy server to access the repos [DONE]
    #. User configures the options from previous steps and commits changes
    #. Fuel Menu checks the accessibility of repos for bootstrap
       via networking configuration.

        #. If repo is not accessible - indicate informative + actionable
           error message: "The repo specified for Fuel Bootstrap
           is not accessible via network. Please check network settings
           and repo location, adjust them and try again". [DONE]
        #. If repo is STILL not accessible - user can prompt Fuel Menu to
           proceed with Fuel master bootstrap
           (with the intent to sort out repo later)
        #. If repo is accessible - proceed with normal process of
           Fuel master installation and bootstrap building.

#. Manually create a custom bootstrap image

   Goal: Customize bootstrap image to particular deployment requirements
    #. User applies documented procedure + tooling to build bootstrap image
       on Fuel master node (including options such as kernel version pinning,
       driver enabling, package installation).
    #. By the end of build process the bootstrap image created in
       --output-dir, and can be applied as "active" for Fuel master.

#. Managing of existing bootstrap images

   Goal: Give user the possibility to work with already created bootstrap
         images and manage them on the system.

    #. User can import already created bootstrap image to the system. This
       applies both to images created in previous use case as well as images
       which are obtained from 3rd party sources
       (e.g. user can import image created in neighboring cloud)
    #. User has the way to switch "active" bootstrap image.
       User can have several bootstrap images built, but only one can
       be activated for all environments.
    #. User can re-discover any of existing (even already discovered or
       provisioned) nodes with new bootstrap by rebooting this node in PXE boot
       mode. No DB cleanup or any other actions in Fuel/Cobbler are required.
    #. User can manage existing bootstrap images: he can list and delete
       existing images.

User Experience
===============

* Fuel Menu allows user to specify repo location for bootstrap building
  and proxy setting

* Fuel provides command-line utilities to build Ubuntu-based bootstrap
  with customizations.

* Fuel provides command-line utility to import, list, apply and delete images

Example of user steps, required to build a new bootstrap image and set
  is as the default(active):

.. code-block:: bash

  $ mkbootstrap /root/latest-ubuntu-bootstrap.tar.gz
         ...Assembling bootstrap with default parameters...
                            ...
         ...Assembling done..
         ...Bootstrap saved to /root/latest-ubuntu-bootstrap.tar.gz...
         ...Bootstrap UUID: 765556d0-8b8e-4017-89e0-a5feb4d4518e ...
  $ bootstrap-manage import /root/latest-ubuntu-bootstrap.tar.gz
  $ bootstrap-manage activate 765556d0-8b8e-4017-89e0-a5feb4d4518e
  # or in one command:
  $ bootstrap-manage import /root/latest-ubuntu-bootstrap.tar.gz --activate

----------------
Proposed changes
----------------

#. Extend script for building image that allows the following actions:
    * Customize list of packages installed in the image.
    * Inject custom files inside the bootstrap image.
    * Configure repositories for bootstrap image creating.
    * Add warning message:
      Every time when you build a bootstrap image please make sure
      that you keep all the options required by all the servers
      managed by Fuel master in place. For example, if you're building
      bootstrap with new NIC or RAID driver added - make sure
      that previously added drivers remain enabled.
#. Update Web UI "warning-message":
    * Message should be "non-closable" while default image not added.
#. Provide documentation with examples of bootstrap image customization:
    * Generic way to build bootstrap image from custom repositories.
    * Kernel version specification.
    * Adding custom drivers.
    * PXE parameters configuration (e.g. kernel cmdline).
#. Add possibility to skip default bootstrap building process
   to speedup Fuel master deployment(from fuel-menu).
#. Add possibility to configure custom repositories via fuel-menu
#. Add possibility to configure separated HTTP and HTTPS proxies for
   repository access
#. Provide CLI tool which is capable of managing bootstrap images and supports
   the following operations:

    * list the available bootstrap images
    * import already created image to the system
    * set the given image as active
    * delete the image from filesystem


Web UI
======

While default bootstrap not added, UI should provide an error panel on
`Environments` page with an appropriate message and some instructions what
user can do next.
User should not be able to close the panel, because the message is important
and should not be missed.

To display the error message UI should check the existence of
`bootstrap_error` attribute in master node settings. If this attribute exists,
it's value is exactly the text to be displayed on UI.


Nailgun
=======

[TBD] Should be described how to update master node settings with
`bootstrap_error` attribute if no defaut bootstrap was added.

No changes is required on nailgun side. Only CLI tools will be provided to
create and manage bootstrap images.


Nailgun-agent
-------------

We need to know, which exactly bootstrap image currently loaded to node.

* Optional field with "Bootstrap uuid" will be added.

Data model
----------

Existing bootstrap images will be put to local filesystem of the Fuel Master
node. They will not be kept in the Fuel DB. So no changes to the Data model
are required.

All files for each bootstrap will be stored under:

::

  /var/www/nailgun/bootstraps/${bs_uuid}/

Where examples:
    * bs_uuid = unique id for each bootstrap.

Each folder contains:
    * metadata.yaml - description yaml file
    * initramfs.img - initramfs
    * linux - kernel image
    * (optional) root - root filesystem

Active bootstrap will be determined like symlink on filesystem
Example: /var/www/nailgun/bootstraps/active_bootstrap => ${bs_uuid}/


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

* Extend fuel-library import-bootstrap system.
* Implement fuel-library skip-bootstrap option.

Fuel manifests will be changed to allow to skip bootsrap image creation
during fuel master deployment process. Additionally manifests could be used
to change active bootstrap image.


Fuel Client
===========
None

Bootstrap generator
===================

Bootstrap generator create bootstrap images for fuel-master.
It use default configurations and allow user to make customization.
There is 3 ways to make customization:

    * set additional packages for installation
    * copy custom files into root bootstrap
    * perform user script at bootstrap file system during image creation


Example:

::
    mkbootstrap <file-name>.tar.gz [ options ]

.. code-block:: bash

  --ubuntu-repo REPOSITORY      Use the specified Ubuntu repository.
                                **Warning:** ubuntu-repo is mandatory variable,
                                should be a mirror of archive.ubuntu.com

  --http-proxy URL              Pass http-proxy URL
  --https-proxy URL             Pass https-proxy URL

  --ubuntu-repo 'http://archive.ubuntu.com/ubuntu trysty main universe multiverse restricted'

  --mos-repository REPOSITORY   Add link to repository with fuel* packages.
                                That should be either http://mirror.fuel-infra.org/mos-repos
                                or its mirror.

  **Warning:** mos-repository is mandatory variable.

  --repository REPOSITORY       Add one more repository


**REPOSITORY variable  format:**
The '--repository' option can be specified multiple times, several repositories
will be added.

.. code-block:: bash

  --repository 'uri distribution [component],[priority]'
  --repository 'http://mirror.fuel-infra.org/mos-repos/ubuntu/8.0 mos8.0 main,priority=1101'
  --repository 'http://mirror.fuel-infra.org/mos-repos/ubuntu-test/9.0 mos9.0 main,priority=1120'

  Note: priorities higher than 1000 select a package from the repository in
  question  even if the newer versions of the same package are available from
  other repositories or a newer version of the package is already installed in
  the system. This can be used to force the installation of a previous
  version(s) of a package (say, linux-image-*) in a case of regressions.

You can find more information about apt-pinning `here <https://www.debian.org/doc/manuals/debian-reference/ch02.en.html#_tweaking_candidate_version>`_.


.. code-block:: bash

  --script FILE_PATH            The script is executed after installing
                                package (both mandatory and user specified
                                ones) and before creating the initramfs
                                Also, it is possible to land into chroot
                                system and made any customm changes  with
                                '--script=/bin/bash' command.

  --include-kernel-module       make sure the given modules are included into
                                initramfs image.(by adding module into
                                /etc/initramfs-tools/modules)

   **Note**
   If the module in question is not shipped with the kernel itself please add
   the package providing it (see the `--package' option).
   Keep in mind that initramfs image should be kept as small is possible.
   This option is intended to include uncommon network interface cards'
   drivers so the initramfs can fetch the root filesystem image via the
   network.


  --package PKGNAME             The option can be given multiple times, all
                                specified packages and their dependencies will
                                be installed.

  --package-list-file FILE_PATH Install list of packages. Package names listed
                                in the given file.

  --label LABEL                 Custom string, which will be presented in
                                bootstrap listing

  --blacklist-kernel-module    Make sure the given modules never get
                                loaded automatically

**Note** Direct injection of files into the image is not recommended, and a
         proper way to customize an image is adding (custom) packages.

.. code-block:: bash

  --inject-files-from PATH      Directory or archive that will be injected
                                     to the image root filesystem.

**Note** Files/packages will be injected after installing all packages,
  but before generating system initramfs - thus it's possible to adjust
  initramfs.

Example:

.. code-block:: bash

  # tree /tmp/cool_stuff_directory/
  /tmp/cool_stuff_directory/
  └── root
      └── dir1
          └── dir2
              └── dir3

  $ mkbootstrap [opt] --inject-files-from /tmp/cool_stuff_directory/
  $ # will be injected in bootstrap like:
  {image}/root/dir1/dir2/dir3

.. code-block:: bash

  --kernel-params PARAMS          Custom kernel parameters(opt)
  --kernel-flavor                 Defines kernel version
                                (default=-generic-lts-trusty)
  --ubuntu-release                Defines the Ubuntu release (default=trusty)
  --ssh-keys FILE                 Copy public ssh keys into image - makes it
                                possible to login as root into any bootstrap
                                node using the key in question.

Examples:

.. code-block:: bash

   $ mkbootstrap new_bootstrap.tar.gz --ubuntu-repo 'http://archive.ubuntu.com/ubuntu trysty main' --repository 'http://mirror.fuel-infra.org/mos-repos/ubuntu/8.0 mos8.0 main,priority=1101' --repository 'http://me.example.com/my-openstack kilo main,priority=1104' --package screen

Bootstrap container format:
---------------------------

To simplify bootstrap sharing and delivery, we propose to pack all needed for
bootstrap files in simply tar.gz archive, which also can be simply created
manually by user, w\o mkbootstrap script.

Bootstrap archive shoule contain at least(filenames are also mandatory!):
    * metadata.yaml - description yaml file
    * initramfs.img - initramfs
    * linux - kernel image

Any other files can be also added :
    * (optional) root - root filesystem

Mandatory data fields for metadata.yaml:

.. code-block:: yaml

 extend_kopts : 'panic=120 biosdevname=1'
   # ks\cmd opts will be extended with Fuel default opts.But, its also
   # possible to re-write default params - w\o any guarantee of work.

 distro : 'ubuntu'
   # Currently only one valid value : 'ubuntu'

 uuid : <string>
   # Uniq uuid for bootstrap.

In case manual-builded bootstrap, user can simply generate it with
command :

::

   python -c "import uuid; print str(uuid.uuid4())"

Example for typically builded ubuntu-bootstrap:

.. code-block:: bash

  $ tar -ztvf ubuntu-bs.tar.gz
  -rwxr-xr-x root/root   5820640 2015-09-21 22:31 linux
  -rwxr-xr-x root/root 220590080 2015-09-29 16:06 root.squashfs
  -rwxr-xr-x root/root  16005932 2015-09-29 16:03 initramfs.img
  -rwxr-xr-x root/root       932 2015-09-29 16:03 metadata.yaml
  # Where metadata.yaml contain :
  $ cat metadata.yaml
    extend_kopts : 'boot=live toram components fetch=http://${bs_root_on_server/root.squashfs biosdevname=0'
    uuid : 765556d0-8b8e-4017-89e0-a5feb4d4518e
    label : "ubuntu-with-driver-fix"

Note: "${bs_root_on_server}" mandatory variable, which will be automatically
  replaced with correct value.

Bootstrap manager
=================

Bootstrap manager operates with images for fuel-master.
It allows user to manage existing bootstrap images and upload a new ones.

::

    bootstrap-manage < COMMAND > [ arguments ] [ flags ]


Commands:

.. code-block:: bash


  list              lists all available bootstrap images

  import            allows to import already created bootstrap image to the
                    system
                    (archive file in format tar.gz)
  activate          sets selected image as an active - i.e. the image that will
                    be used to bootstrap all the nodes deployed from this
                    Fuel Master
  delete            deletes specified imagefrom the system


Examples:

.. code-block:: bash

   $ bootstrap-manage list
     uuid                                   | label                  | status
   -----------------------------------------+------------------------+--------
    d8a38f0c-ac69-4357-895f-59c981c13191    | ubuntu-default         | active

.. code-block:: bash

   $ bootstrap-manage import <bootstrap_archive_file>.tar.gz
    uuid                                   | label                  | status
   ----------------------------------------+------------------------+--------
    d8a38f0c-ac69-4357-895f-59c981c13191   | ubuntu-default         | active
    765556d0-8b8e-4017-89e0-a5feb4d4518e   | ubuntu-with-driver-fix |

**Note** All images in the system should have different names.

.. code-block:: bash

   $ bootstrap-manage activate 765556d0-8b8e-4017-89e0-a5feb4d4518e
     uuid                                  | label                  | status
   ----------------------------------------+------------------------+--------
    d8a38f0c-ac69-4357-895f-59c981c13191   | ubuntu-default         | active
    765556d0-8b8e-4017-89e0-a5feb4d4518e   | ubuntu-with-driver-fix |

.. code-block:: bash

   $ bootstrap-manage delete d8a38f0c-ac69-4357-895f-59c981c13191
     uuid                                   | label                  | status
   -----------------------------------------+------------------------+--------
    765556d0-8b8e-4017-89e0-a5feb4d4518e    | ubuntu-with-driver-fix | active

**Note** You cannot delete active image using regular deletion operation.

Plugins
=======

None

------------
Alternatives
------------
Support only the latest version of a bootstrap for fuel.
In that case if operator installs new version of the bootstrap for all nodes.
Otherwise he will loose a possibility to manage bootstrap-per-node function.

   Cons:
      - All nodes have the same version of the bootstrap.
        Operator doesn't have possibility to use different
        versions of bootstrap for node.
   Pros:
      - Some part of this spec can be abandoned.

--------------
Upgrade impact
--------------

User can manually reassemble bootstrap image once updated version of components
or drivers is available.

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

--------------------------------
Infrastructure/operations impact
--------------------------------

Fuel master operator will be available to build customized bootstrap images.

--------------------
Documentation impact
--------------------

We need to prepare documentation which will describe this design change. Also
there should be a clearly documented procedure for end-user how to build a
custom bootstrap image.

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
    * Alexey Zvyagintsev <azvyagintsev@mirantis.com>

Mandatory design review:
    * Aleksey Kasatkin <akasatkin@mirantis.com>

QA engineers:
    * Dmitry Kalashnik <dkalashnik@mirantis.com>


Work Items
==========

* Modify builder script to provide required bootstrap image customization.
* Extend Web UI to show blocker warning.
* Extend fuel-library import-bootstrap system.
* Modify bootstrap image settings tab in fuel-menu.
* Create example for changing linux kernel version.
* Create example for drivers customization.
* Create a CLI tool to manage existing bootstrap images.

Dependencies
============

-----------
Testing, QA
-----------

* Manual testing should be run according to the UI use cases steps
* Manual testing should be run according to the CLI use cases steps
* System tests should be created for the new bootstrap image building feature
* System tests should be created for the new bootstrap customization feature


Acceptance criteria
===================

* Use Cases 1, 2 and 3 from Problem description pass
* The workaround for bug with interface naming by Ubuntu
  (https://bugs.launchpad.net/mos/+bug/1487044) is applied for bootstrap
  context (hardcoded NIC names in bootstrap)
* User must have a documented way to adjust settings described above and
  build bootstrap image later, when Fuel master node is installed.
* User must have an ability to skip building bootstrap image from fuel-menu
* User must have a documented way to inject additional
  driver/configuration into bootstrap image

    - This has to be available at later stage
      (after Fuel master is deployed\some env already exist)
    - The example of Mellanox Connect-X and some RAID storage
      driver should be taken

* User must have a documented way to pin kernel version
  to be used: Mirantis default (relevant for the moment of GA release),
  ubuntu latest, user specified
* Fuel Menu network check must ensure that the specified bootstrap
  repositories can be accessed from the Fuel Master
* If an error occurs during bootstrap image build:

    - Fuel master must gracefully complete provisioning of itself
    - User must receive an indication about bootstrap image being not available
      on Web UI and CLI, with pointer to a log for troubleshooting.

* Ubuntu and MOS repositories should be configurable, in particular the user
  should be able to specify alternative URLs.
* Ubuntu, MOS, and custom repositories can be accessed via HTTP/HTTPS proxy
  as specified by --http-proxy/--https-proxy options or HTTP_PROXY/HTTPS_PROXY
  environment variables.
* User has an ability to list existing bootstrap images in the system
* User has an ability to import already created bootstrap image to the system
* User has an ability to set any existing image to be active
* User has an ability to delete any non-active image
* User has an ability to create new customized bootstrap

----------
References
----------

