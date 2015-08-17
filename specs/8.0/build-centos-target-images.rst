..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================
Build Centos images on the master node
======================================

https://blueprints.launchpad.net/fuel/+spec/fuel-agent-build-centos-images

Problem description
===================

At the moment we build Centos target OS image together with ISO and then
package it into rpm. Since it depends on other rpm packages this approach
does not match to rpm usual flow. Those build jobs that depend on other
packages should be triggered other way than usual rpm build jobs. Besides,
building OS image takes usually 10-15 minutes which is much longer than
building of ordinary rpm package. So, we'd better avoid having so called
level-2 packages wherever it is possible.

At the same time we build Ubuntu target OS images on the master node using
Fuel Agent. Although Fuel Agent does not support building Centos images
we can implement such functionality comparatively easily.

Proposed change
===============

Currently we build Ubuntu target OS images on the master node using
Fuel Agent. Although Fuel Agent does not support building Centos images
we can implement such functionality comparatively easily.

We need to implement build image utilities for Centos and modify Fuel Agent
build image manager method and probably input data driver so as to make it
possible to use Fuel Agent to build Centos images.

Besides, we need to append corresponding pre-provisioning task into Nailgun
provisioning serializer. It is going to be exactly the same as for Ubuntu
including input data format.

Alternatives
------------

We can run that script which is currently used for building Centos images
together with ISO directly on the master node, but it does not sound rational
since we already have working data driven image building approach
in the context of Fuel Agent. We just need to use the same approach to
implement building Centos images.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

If one needs to upgrade Centos target images he will need to run image build
script instead of just installing new package.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

Building Centos target image is going to take 10-15 minutes. So, provisioning
is going to be significantly longer.

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Infrastructure impact
---------------------

Building ISO is going to take less time since we won't spend time for building
Centos images.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>


Work Items
----------

- Implement Centos image build capabilities in the context of Fuel Agent
- Modify Nailgun provisioning serializer so it runs fa_build_image
  right before starting actual provisioning

Dependencies
============

None

Testing
=======

Testing approach is going to stay the same. There is no need to change
anything about this.

Acceptance criteria
-------------------

Centos target image should be built on the master node.


Documentation Impact
====================

It should be described in the documentation than Centos target images
are to be built right before starting actual provisioning.


References
==========

