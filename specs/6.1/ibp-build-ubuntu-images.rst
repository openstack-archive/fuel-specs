..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================
Building target images with Ubuntu on master node
=================================================

https://blueprints.launchpad.net/fuel/+spec/ibp-build-ubuntu-images

Target images with Ubuntu for image based provisioning should be built on
master node.

Problem description
===================

Currently we build target OS images during ISO building and then put those OS
images into Fuel ISO. This approach is not suitable for the following reasons:

* it does not allow us to customize OS image according to user's wishes

* it make Fuel ISO larger (to be particular 350M per every supported OS)

Proposed change
===============

A script from build system should be adopted to fit to master node's run-time
capabilities.

* It should be less error prone and less invasive as it's known of having some
  kind of magic around dealing with loop devices.

* It should contain the nearest to possible minimum amount of sudo calls.

* It should build images relatively fast.

The script builds target images for image based provisioning. Those images will
be deployed to a node during image based provisioning stage.

The script will be run in MCollective container and will be triggered by Astute
via asynchronous task executing.
More details about that in consume-external-ubuntu bp [1]_

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

During upgrade all required packages to perform image building should be
installed.

Security impact
---------------

Build script requires the use of sudo.

Resource exhaustion isn't possible as it's the once per master node deployment
action and will never repeat.

Notifications impact
--------------------

None

Other end user impact
---------------------

The release flavor choice will be disabled until the images build is completed.

Performance Impact
------------------

Building images takes additional time. Roughly about 10-15 min. Will be called
only once per masternode setup.

`eatmydata` package could be used to speed up the build.

Other deployer impact
---------------------

The script should be packaged to regular RPM package to install on master node.
Package name is TBD.

Developer impact
----------------

In regard to IBP, most changes to images building system will be concentrated
in that script.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <agordeev@mirantis.com>

Work Items
----------

*rework the image building script to fit new requirement*

Dependencies
============

Depends on consume-external-ubuntu blueprint [1]_

List of package dependencies:
* debootstrap

Testing
=======

It can be tested with the following scheme:
* deploy a master node
* execute the building of images
* deploy a cluster with that images to verify that all is ok

Documentation Impact
====================

New way of dealing with building target images should be documented

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/consume-external-ubuntu
