 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================================
Fuel bootstrap on Ubuntu 14.04, generated dynamically on Fuel master
=======================================================

Blueprint: https://blueprints.launchpad.net/fuel/+spec/fuel-bootstrap-on-ubuntu

(1) In MOS 7.0, it would be extremely problematic to keep CentOS 6.5 based bootstrap on the master node. The kernel is getting old and won't be supported soon. So we have to move away from the current bootstrap.
(2) Ubuntu 14.04 has a newer 3.16 kernel and a larger HCL. 
(3) Building the image dynamically on the master node will allow us to solve the issue of injecting custom h/w drivers into bootstrap. Something that we needed for a while.

Problem description
===================

Use live-build [1] to assemble a bootable Ubuntu image which contains
necessary nailgun components and is configured to act as a discovery node.

Proposed change
===============

Convince nailgun maintainers to fix nailgun packaging.
   
   - nailgun-agent
   - nailgun-mcagents
   - nailgun-net-check
   - fuel-agent

   and other nailgun/Fuel components do not follow common packaging workflow
   (low quality home brew scripts are used to build those packages).

Add Debian container for building bootstrap images (for live-build).

One of requirements for using bootstrap images is NFS. Configure master node for exporting images via NFS.

Alternatives
------------
To build images manually with debootstrap and pack them as initramfs.

Data model impact
-----------------
New configuration option might be necessary - path to the mirror for building bootstrap image.

REST API impact
---------------
N/A

Upgrade impact
--------------
N/A

Security impact
---------------
NFS a as potential attack vector.
Bootstrap building is running as root.

Notifications impact
--------------------


Other end user impact
---------------------
N/A

Performance Impact
------------------
Deploying time will be increased, because of downloading and building bootstrap image.
Building process requires 12GB additional space on disk on master node.

Plugin impact
-------------
N/A

Other deployer impact
---------------------
Internet is required on master node. If there is no access to the Internet, bootstrap image is not built and Fuel is unable to detect nodes.

Developer impact
----------------
Deployment workflow will be changed.

Infrastructure impact
---------------------
Internet in the lab is required for testing.
Time for deployment tests will be increased.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  asheplyakov

Other contributors:
  

Work Items
----------


Dependencies
============


Testing
=======


Documentation Impact
====================


References
==========
