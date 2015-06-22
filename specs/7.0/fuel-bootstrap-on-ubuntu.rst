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
 - Faster development workflow: rebuild the nailgun-* package, tell the master
   node to rebuild the bootstrap image, restart the nodes


Alternatives
------------


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

N/A


Performance Impact
------------------

Increased deployment time because of downloading and building bootstrap image.
Building process requires around 2GB additional disk space on master node.


Plugin impact
-------------

N/A

Other deployer impact
---------------------

The master node must have an access to Ubuntu and MOS APT repositories
(either via Internet or a local mirror) in order for Fuel to be able to
detect the nodes.


Developer impact
----------------

Development cycle for nailgun-* packages (nailgun-agent, nailgun-mcagents,
nailgun-net-check, fuel-agent) is going to change:

 - make a patch
 - rebuild the deb package
 - add repository with newly build packages
 - tell the master node to rebuild the bootstrap image
 - test/debug the changes

In many cases rebuilding the bootstrap image is not necessary as the modified
packages can be installed directly on the bootstrap nodes.


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

1. Fix nailgun and astute packaging.

   - nailgun-agent
   - nailgun-mcagents
   - nailgun-net-check
   - fuel-agent

   and other Fuel components should use the common packaging workflow
   It's time to retire those homebrew scripts which are used to build
   those packages at the moment.

2. Change the ISO build process to make Ubuntu based bootstrap images.
   This approach is not feasible for a release (the images should be
   generated dynamically), however it requires minimal changes and allows
   to start testing early enough.

3. Move the code for building based bootstrap images to the master node.

4. Add an API for building/configuring those images (which APT repositories
   to use, pinning rules, additional packages).

5. [Optional] Reduce fuel-agent run time dependencies to keep the root
   filesystem reasonably small.


Dependencies
============


Testing
=======

Usual deployment tests cover the bootstrap functionality.


Documentation Impact
====================


References
==========
