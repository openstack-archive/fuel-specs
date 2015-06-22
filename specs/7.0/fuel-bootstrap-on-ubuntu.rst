 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================================
Fuel bootstrap on Ubuntu 14.04, generated dynamically on Fuel master
====================================================================

Blueprint: https://blueprints.launchpad.net/fuel/+spec/fuel-bootstrap-on-ubuntu


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
 - Building the image dynamically on the master node allows local tweaking
   (such as adding custom drivers).
 - Bootstrap is a full fledged Ubuntu system, it's possible install and
   upgrade packages (custom drivers, debugging symbols, etc) without
   rebuilding the image (the changes don't persist across reboots, though).
 - Faster development workflow: rebuild the nailgun-* package, tell the master
   node to rebuild the bootstrap image, restart the nodes


Alternatives
------------

Use Debian instead of Ubuntu and ship the default bootstrap image on
Fuel ISO.

Data model impact
-----------------

New configuration options are necessary: Ubuntu, MOS, and additional APT
repositories (along with the corresponding pinning rules) for building
the bootstrap image.


REST API impact
---------------

Fuel API should be extended with calls for

 - rebuilding the bootstrap image,
 - configuring Ubuntu, MOS, and extra APT repositories (with pinning
   rules) for building the bootstrap image,
 - adding extra packages into the bootstrap image.

These calls should be added to Fuel CLI tools too.

Upgrade impact
--------------

N/A


Security impact
---------------

Building bootstrap images requires root privileges.

Notifications impact
--------------------


Other end user impact
---------------------

Ubuntu based bootstrap is supposed to work out of the box provided that
the master node has an access to the default Ubuntu and MOS repositories.
The advanced users can rebuild the bootstrap images using the fuel CLI
tools (or REST API).


Performance Impact
------------------

The OpenStack nodes themselves are not affected in any way. The master node
deployment time is expected to be somewhat longer due to building the default
bootstrap image. Building process requires around 2GB additional disk space
on master node.


Plugin impact
-------------

None (unless some wants to write a plugin for tweaking the bootstrap image).

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

Build "live" Ubuntu image, i.e. the root filesystem image (squashfs),
initramfs, and the kernel bootable via network. Initramfs detects and
configures the network interface(s) and downloads the root filesystem
image from the master node via HTTP. Initramfs configures a writable
overlay filesystem (using tmpfs as a writable branch). Use the live-boot
package for building such initramfs.

The root filesystem must contain the software necessary for acting as
a discovery/bootstrap node (mcollective, nailgun-agent, nailgun-mcagents,
nailgun-net-check, fuel-agent, etc).

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

3. Add an API for building/configuring those images (which APT repositories
   to use, pinning rules, additional packages).

4. Generate bootstrap image during the master node deployment using
   the default Ubuntu and MOS APT repositories.

5. [Optional] Reduce fuel-agent run time dependencies to keep the root
   filesystem reasonably small.


Dependencies
============

None

Testing
=======

Usual deployment tests cover the bootstrap functionality.


Documentation Impact
====================


References
==========
