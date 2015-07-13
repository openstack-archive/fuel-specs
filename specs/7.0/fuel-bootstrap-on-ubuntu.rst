..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================================
Fuel bootstrap on Ubuntu 14.04, generated dynamically on Fuel master
====================================================================

https://blueprints.launchpad.net/fuel/+spec/fuel-bootstrap-on-ubuntu

Use Ubuntu as an operating system of Fuel bootstrap nodes.


Problem description
===================

Using CentOS 6.x based bootstrap in MOS 7.0 would be extremely problematic:
 - Hardware support is already the pain in the neck
 - The kernel (kernel.org 3.10.y) EOL is August 2015
   (http://www.kroah.com/log/blog/2013/08/04/longterm-kernel-3-dot-10)
 - Some bootstrap code (in particular IBP) uses OpenStack python
   libraries (oslo.*) which don't support python 2.6 anymore.


Proposed change
===============

Dynamically assemble a bootable Ubuntu image (AKA live image) which contains
necessary nailgun components and is configured to act as a discovery node.

Advantages:
 - Linux 3.13 (with Canonical modifications) provides a better hardware support
 - The same kernel on bootstrap and OpenStack nodes => less maintenance.
 - The initramfs images is moderately sized (~ 20MB), the root filesystem image
   is downloaded via http => less load on the master node.
 - Bootstrap is a full fledged Ubuntu system, it's possible install and
   upgrade packages (custom drivers, debugging symbols, etc) without
   rebuilding the image (the changes don't persist across reboots, though).
 - Faster development workflow: rebuild the nailgun-* package, rebuild
   the bootstrap image (run a script on the master node), restart the slave
   nodes.

Alternatives
------------

Use Debian instead of Ubuntu and ship the default bootstrap image on Fuel ISO.

Data model impact
-----------------

None.

REST API impact
---------------

None.

Upgrade impact
--------------

None.


Security impact
---------------

Building bootstrap images requires root privileges.

Notifications impact
--------------------

None.

Other end user impact
---------------------

The bootstrap images are generated during the master node deployment. This
process is supposed to work without any user intervention if the master node
has an access to the default Ubuntu_ and MOS_ mirrors. Otherwise the user
is prompted to configure the APT repositories using the Fuel menu.
The deployment of the master node fails if the bootstrap image can not be
generated (the master node is next to useless without a bootstrap image).
The advanced users can generate a custom bootstrap images using
the corresponding script on the master node.

.. _Ubuntu: http://archive.ubuntu.com/ubuntu
.. _MOS: http://mirror.fuel-infra.org/mos/ubuntu

Performance Impact
------------------

The OpenStack nodes themselves are not affected in any way. The master node
deployment time is expected to be somewhat longer due to building the default
bootstrap image. Building process requires around 2GB additional disk space
on master node.


Plugin impact
-------------

None.

Other deployer impact
---------------------

The master node must have an access to Ubuntu and MOS APT repositories
(either via Internet or a local mirror) in order for Fuel to be able to
detect the nodes. An access to 3rd party repositories is also required
to make use of the custom packages (such as the additional hardware
drivers) in the bootstrap image.


Developer impact
----------------

The new bootstrap is a full fledged Ubuntu system, one can install or
upgrade packages (although these changes are not persistent across reboots).
In particular it's possible to reinstall nailgun-agent, fuel-agent, etc
without rebuilding the bootstrap image.

Infrastructure impact
---------------------

The lab must have an access to Ubuntu and MOS APT repositories.
Deployment tests are going to run a bit slower (5 -- 10 minutes).


Implementation
==============

Build the "live" Ubuntu image, i.e. the root filesystem image (squashfs),
initramfs, and the kernel bootable via network. Initramfs detects and
configures the network interface(s) and downloads the root filesystem
image from the master node via HTTP. Initramfs configures a writable
overlay filesystem (using tmpfs as a writable branch). Use the live-boot_
package for building such initramfs.

The root filesystem must contain the software necessary for acting as
a discovery/bootstrap node (mcollective, nailgun-agent, nailgun-mcagents,
nailgun-net-check, fuel-agent, etc).

.. _live-boot: http://live.debian.net/devel/live-boot

Assignee(s)
-----------

Primary assignee:
  asheplyakov

Other contributors:

Work Items
----------

1. Change the ISO build process to make Ubuntu based bootstrap images.
   This approach is not feasible for a release (the images should be
   generated dynamically), however it requires minimal changes and allows
   to start testing early enough (intended to start hardware support
   test as early as possible).

2. Move the code for building based bootstrap images to the master node.
   Generate the bootstrap image during the master node deployment using
   the default Ubuntu and MOS. Note: at this stage deployment fails if
   the default mirrors are not accessible.

3. Make Ubuntu and MOS mirrors configurable via the fuel menu. Verify that
   the user specified mirrors are accessible.

4. Check if the default Ubuntu and MOS APT mirros are accessible from
   the master node, if not pop up the Fuel menu and prompt the user to
   configure the APT repositories for the bootstrap image.

5. [Optional] Reduce fuel-agent run time dependencies to keep the root
   filesystem reasonably small.


Dependencies
============

None


Testing
=======

Usual deployment tests cover the bootstrap functionality.

Acceptance criteria
-------------------


Documentation Impact
====================

* Master node should have the access to the default Ubuntu and MOS APT
  repositories in order for deployment of the master node to be fully
  noninteractive
* If the default Ubuntu and MOS APT repositories are not accessible from
  the master node (i.e. master node has no access to the Internet) the user
  is supposed to configure the corresponding APT repos via the Fuel menu.


References
==========
