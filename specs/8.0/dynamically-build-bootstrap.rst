=======================================================
Dynamically build Ubuntu-based bootstrap on master node
=======================================================

https://blueprints.launchpad.net/fuel/+spec/dynamically-build-bootstrap

This document describes bootstrap images configuration,
rebuilding, and switching between several bootstrap images
using Fuel UI and CLI.

We should support Ubuntu bootstrap images to have one common Operating System
for bootstrapping and deploying nodes. Only ubuntu kernel image customization
should be possible. Other kernels will not be supported.

-------------------
Problem description
-------------------

Now we use Centos as bootstrap image. This leads to old
version of kernel/drivers/packages. We need to move from Centos to Ubuntu
which will delivers fresh components.
Moreover we use Ubuntu as post-provisioning system,
this will give us more consistent environment.

At the moment bootstrap image customization is a complicated process.
Currently the builder script requires editing config files and running scripts
on the master node. Functionality of the builder script is not available
to be called through CLI or Web UI.
In addition operator needs a way to add custom packages inside bootstrap.

The second issue is that only one bootstrap image can exist.
In case of mixed environments with custom drivers requirements
it can cause a problem to boot these mixed environments at once.

Therefore a proper Fuel CLI and web UI for configuring, rebuilding
and switching between bootstrap images is required.

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

#. Apply customized bootstrap image to MOS nodes
   Goal: Customize bootstrap image to particular deployment requirements

    #. Use Case 1 is finished (Fuel master node is deployed).
    #. User applies documented procedure + tooling to rebuild bootstrap image
       on Fuel master node (including options such as kernel version pinning,
       driver enabling, package installation).
    #. By the end of rebuild process the bootstrap image is applied
       as "active" for particular Fuel master instance.
    #. Previous versions of bootstrap image are stored and used
       in scenarios when node has to be restored to "bootstrap" stage
       (removal from Environment, reset of Environment).
    #. User has the way to switch "active" bootstrap image.

User Experience
===============

* Fuel Menu allows user to specify repo location for bootstrap building
  and proxy setting
* Fuel WebUI and CLI show indication of bootstrap building failure
  if such happened during master node installation

    * Actionable hint is included on how to use tooling to rebuild bootstrap
      on Fuel master node when it's already installed

* Fuel CLI provides utilities to rebuild Ubuntu-based bootstrap
  with customizations
* Fuel Web UI exposes "completely wipe" option that allows individual
  node to be completely removed from Fuel management
  (incl. association with a bootstrap image)

    * This is required in order to allow re-bootstrapping of a node in case
      when a just-customized bootstrap image failed on some reason

----------------
Proposed changes
----------------

Extend nailgun to manage the bootstrap images and the related settings.

Fuel master should track list of previously built bootstrap images.
Using CLI or Web UI user can switch between bootstrap images. Only one single
bootstrap image can be active at the same time.

Active bootstrap image is used for each NEW node that is not
tracked by Fuel yet. Fuel tracks bootstrap image that was used
for node boot up.
This allows to use the same bootstrap image when node is rebooted
or environment reset operation is performed.

In case when node is already running with invalid bootstrap image
user should remove node from the Fuel master and restart it with
valid active bootstrap image.

To achieve desired behavior we need make next changes:

#. Provide script for building image that allows the following actions:
    * Customize list of packages installed in the image.
    * Inject custom files inside the bootstrap image.
    * Configure PXE parameters (e.g. kernel cmdline).
    * Configure repositories for bootstrap image.
#. Update nailgun.
    * Nailgun should manage bootstrap images.
    * Nodes should have references to appropriate bootstrap images.
#. Update Web UI to allow generic user select active bootstrap image.
#. Provide documentation with examples of bootstrap image customization:
     * Generic way to build bootstrap image from custom repositories.
     * Kernel version selection.
     * Adding custom drivers.
     * PXE parameters configuration (e.g. kernel cmdline).
#. [optional] Add possibility to skip default bootstrap building process
   to speedup Fuel master deployment.


Web UI
======

It's assumed that Web UI should have only functions that can be used by
any user and don't require advanced administrator guidance.
The following UI changes should be done:

* If bootstrap image building was failed during master node installation
  and/or there is no default bootstrap image to use, then UI should provide
  an error panel on the default `Environments` page with an appropriate
  message about boostrapping failure and some instructions what user can do
  next. User should not be able to close the panel, because the message
  is important and should not be missed.
  [TODO] what DB data should be used to check if UI need to display the error
  message?

* [TBD] UI should provide a control to change active bootstrap image globally.
  New root-level Fuel Settings page can be created to display a list of
  installed bootstrap images with radio button or combo-box.
  [TODO] what API should be used to update bootstrap image Fuel setting?

* [TBD] When a just-customized bootstrap image failed on some reason UI should
  provide a button to completely remove already discovered node from Nailgun.
  In this case after node next boot up, it will be discovered again.
  [TODO] If the button should appear in Fuel UI, then the following questions
  should be discussed:

    * will existing 'Remove' button, that is presented for offline nodes, suit
      the case? The button send DELETE /api/nodes/<node_id> request and remove
      a node from Nailgun DB
    * should UI support a bulk node removal?


Nailgun
=======

Nailgun should be able to manage registered bootstrap images.
Next operation are required:

    * Register new bootstrap image
    * Activate bootstrap image(set it as default)
    * Delete bootstrap image
    * Delete all bootstrap images,
      that are not used by any node or not activated.
    * Set new bootstrap image for the existing node.
    * nailgun upload - means uploading archive with data,
      and put bootstrap in structure:

      ::

            /var/www/nailgun/bootstrap/<ID>/root_fs.file
                                           /linux_kernel.file
                                           /metadata.yaml

    * [optional] Reboot node after bootstrap is changed.


Data model
----------

Bootstrap images are introduced.
Table ``bootstrap_images``:

    * id - integer, the ID of the current bootstrap image
    * is_active - boolean, indicates that bootstrap image is
      currently activated
    * name - string, the Name of current bootstrap
    * description - string, the description of current bootstrap
    * metadata - json, dictionary that contains at least:
        - rootfs_uuid - uniq uuid from rootfs
        - kernel_v - uniq name of kernel, from uname -rv
        - custom user-defined kernel\pxe parameters.

Node record should have additional field that references
to the corresponding bootstrap image.
Add new field to ``nodes`` table.

    * bootstrap_id - foreign key, references to bootstrap.id field


REST API
--------

Add ``/bootstrap`` URL to register new bootstrap image (POST).

Add ``/bootstrap/<ID>`` URL to retrieve or delete bootstrap image (GET\DELETE).

Add ``/bootstrap/<ID>/activate?reboot={true|false}``
URL to set the specified bootstrap image as active (PUT).
Reboot parameter is optional and should be added as part of reboot node
feature implementation.


Orchestration
=============


RPC Protocol
------------


Fuel Library
============

Implement fuel-library import-bootstrap(template-based) system.
Implement fuel-library skip-bootstrap option.

Fuel Client
===========

::

    fuel bootstrap upload --name NAME --input-directory PATH [--id ID]
    [--description DESCRIPTION]

::

    fuel bootstrap download --id ID [--output-directory PATH]

::

    fuel bootstrap list [--outdated]

--outdated         Displays only outdated bootstrap images

::

    fuel bootstrap delete [--outdated] [--force] [ID|NAME]

--outdated        Deletes all bootstrap images that are not used by any node
                  and not active.
--force           Deletes specified bootstrap image even
                  if it's used by any node.

::

    fuel bootstrap activate <ID|name>

::

    fuel node --node-id ID --set-bootstrap ID --reboot``

::

    fuel bootstrap show [--active] ID|NAME``


Bootstrap generator
===================

Bootstrap generator create bootstrap images for fuel-master.
It use default configurations and allow user to make customization.
There is 3 ways to make customization:

    * set additional package for installation
    * unpack tarball or copy folder into  root bootstrap
    * perform user script at bootstrap file system during image creation

::

    mkbootstrap file-name [ options ]

--repository REPOSITORY         Add additional repository
--package PKGNAME               Install package from the repository.
--package-file FILE_PATH        Install package from DEB file.
--package-list-file FILE_PATH   Install list of packages. Package names listed
                                in the given file.
--inject-files-from DIR_OR_ARCHIVE   Directory or archive that will be injected
                                     to the image root filesystem.
--script FILE_PATH              Script to be executed during image creation
                                on the image root filesystem.
--kernel-params PARAMS          Custom kernel parameters

Plugins
=======

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

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

to be filled

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

We need to prepare documentation which will describe this design change.

--------------------
Expected OSCI impact
--------------------


--------------
Implementation
--------------


Assignee(s)
===========

Primary assignee:
    # TODO: Add primary assignee

Mandatory design review:
    * Aleksey Kasatkin <akasatkin@mirantis.com>

QA engineers:
    * Dmitry Kalashnik <dkalashnik@mirantis.com>


Work Items
==========

* Modify builder script to provide required bootstrap image customization.
* Implement REST API to manage bootstrap images.
* Implement per node link to bootstrap image in Nailgun.
* Extend Web UI to manage bootstrap images.
* Extend CLI to manage bootstrap images, customize image properties
  and trigger image build process.
* Implement fuel-library import-bootstrap system.
* Create example for changing linux kernel version.
* Create example for drivers customization.
* [optional] Bootstrap image verification.


Dependencies
============


-----------
Testing, QA
-----------

* Manual testing should be run according to the UI use cases steps
* UI auto-tests should cover the changes in Fuel UI
* Manual testing should be run according to the CLI use cases steps
* System tests should be created for the new bootstrap image building feature
* System tests should be created for the new bootstrap customization feature


Acceptance criteria
===================

* Use Cases 1 and 2 from Problem description pass
* Bug with interface naming by Ubuntu
  (https://bugs.launchpad.net/mos/+bug/1487044) is fixed.

    - The method of fixing (PredictableNetworkInterfaceNames or another one)
      is to be vetted by Services stakeholders (Roman Zhnichkov, Dmitry Ukov)

* Bug with accessing external repos via proxy
  (https://bugs.launchpad.net/fuel/+bug/1460169) is fixed
* User must have a documented way to adjust settings described above and
  rebuild bootstrap image later, when Fuel master node is installed.
* User must have a documented way to inject additional
  driver/configuration into bootstrap image

    - This has to be available for with tools at a later stage
      (after Fuel master is deployed)
    - The example of Mellanox Connect-X and some RAID storage
      driver should be taken

* User must have a documented way to pin kernel version
  to be used: mirantis default (relevant for the moment of GA release),
  ubuntu latest, user specified
* Fuel Menu network check must ensure that the specified bootstrap
  repositories can be accessed from the Fuel Master
* If an error occurs during bootstrap image build:

    - Fuel master must gracefully complete provisioning of itself
    - User must receive an indication about bootstrap image being not available
      on Web UI and CLI, with pointer to a log for troubleshooting.

* Bootstrap repos MUST NOT BE THE SAME as repos used for building
  Host OS nodes of MOS clouds.

----------
References
----------
