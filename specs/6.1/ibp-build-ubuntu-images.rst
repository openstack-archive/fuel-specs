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

* It should build images relatively fast.

* It should retry to fetch packages prior their installation.

The script builds target images for image based provisioning. Those images will
be deployed to a node during image based provisioning stage.

The script accepts the json encoded string as the first positional parameter. That
string should contain at least of the following fields:
::

 {
    "image_data": {
        "/boot": {
            "container": "gzip",
            "uri": "http://127.0.0.1:8080/targetimages/env_4_ubuntu_1204_amd64-boot.img.gz",
            "format": "ext2"
        },
        "/": {
            "container": "gzip",
            "uri": "http://127.0.0.1:8080/targetimages/env_4_ubuntu_1204_amd64.img.gz",
            "format": "ext4"
        }
    },
    "output": "/var/www/nailgun/targetimages",
    "repos": [
        {
            "name": "MOS",
            "section": "main",
            "uri": "http://127.0.0.1:8080/2014.2-6.1/ubuntu/x86_64",
            "priority": 1001,
            "suite": "precise",
            "type": "deb"
        }
    ],
    "codename": "precise"
 }

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

None
Since script is going to be executed in MCollective container, all requirements
have to be installed in this container. So.. there's no upgrade impact, since
during upgrade we're just uploading new containers and that's it.

Security impact
---------------

Build script is going to be executed under root credentials.

Resource exhaustion is possible as it's the once per cluster node deployment
action.

Notifications impact
--------------------

None

Other end user impact
---------------------

The release flavor choice will be disabled until the images build is completed.

Performance Impact
------------------

Building images takes additional time. Roughly about 10-15 min. Will be called
only once per cluster.

`eatmydata` package could be used to speed up the build.

Other deployer impact
---------------------

The script should be packaged to regular RPM package to install on master node.
Package name is fuel-image.

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
