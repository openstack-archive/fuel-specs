..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Enable Heat docker resource by default
==========================================

https://blueprints.launchpad.net/mos/+spec/murano-docker-based-applications

Docker resource is disabled by default for Heat, current Blueprint
needs to enable this resource for using it by Murano without additional
deployment workarounds.

Problem description
===================

MOX 2.3 already contains a bunch of Murano Docker-based applications.
These apps are being forward-ported to MOX 3.0. At this moment these
applications are not available in MOS. To avoid further differences
between MOS and MOX, we're going to add Docker-based apps to MOS 6.1.


Proposed change
===============

Currently docker resource is palced in Heat contrib directory and can not be
used without installation and restarting Heat services.
These changes adds ability to install docker resource on deployment step, so
it makes docker resource available for Heat on first launch.

Alternatives
------------

None

Data model impact
-----------------

It does not require any changes in Data Base.

REST API impact
---------------

No API changes.

Upgrade impact
--------------

Several new packages should be installed (heat_docker and docker requirements)

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

User should see available docker resource in output of command:

heat resource-list

Performance Impact
------------------

None

Other deployer impact
---------------------

Requires installation of addtional packages and small changes in manifests,
which need to configure the right path to docker files.

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  skraynev@mirantis.com
Other contributors:
  iyozhikov@mirantis.com

Work Items
----------

 - Build packages for docker requirements.
 - Build package for Heat docker resource.
 - Update fuel manifests to allow install packages above.


Dependencies
============

None

Testing
=======

Enough manual testing, that current resource is available.

Documentation Impact
====================

Changes about new added resource.

References
==========

1. https://blueprints.launchpad.net/mos/+spec/murano-docker-based-applications
