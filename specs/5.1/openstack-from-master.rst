..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Install openstack from upstream source repositories
==========================================

https://blueprints.launchpad.net/fuel/+spec/openstack-from-master

Be able to deploy the very latest distribution of OpenStack from upstream
master. This is to provide community developers a way to deploy their own
additional changes through an easy to use deployment technology (i.e. Fuel).

Problem description
===================

* The idea behind that feature is to allow customers to compile OpenStack
  packages during a Fuel ISO build on the fly, both RPM and DEB versions.

* Customers may use spec files either from our public Gerrit, or from their
  own local/remote git repos.

Proposed change
===============

Changes will include:

* New configuration entries to fuel-main/config.mk
* New subroutines for our make system that will build RPM and DEB packages
  by using configuration entries from fuel-main/config.mk

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

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

* Additional options to the "make iso" command allow user to customize
  external sources to build OpenStack components from.

Performance Impact
------------------

By using this feature to build multiple custom OpenStack components, the total
ISO build time could be significantly higher than "vanilla" Fuel ISO one.

Other deployer impact
---------------------

The fuel-main/config.mk will contain the following new parameters:

* BUILD_OPENSTACK_PACKAGES - contains comma-separated list of OpenStack
  components to build, or "0" otherwise

Per each of OpenStack components, the following list of parameters is defined
(using Neutron as an example):

* NEUTRON_REPO
* NEUTRON_COMMIT
* NEUTRON_SPEC_REPO
* NEUTRON_SPEC_COMMIT
* NEUTRON_GERRIT_URL
* NEUTRON_SPEC_GERRIT_URL

These values will take effect only if BUILD_OPENSTACK_PACKAGES parameter
contains a name of respective OpenStack component, i.e.:

BUILD_OPENSTACK_PACKAGES:=neutron

It is possible to build specific OpenStack components only, by using make
command with the target component parameter, i.e.:

make neutron

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
    Vitaly Parakhin

Work Items
----------

Initial phase:

* Implement building RPM packages from master
* Produce the specs for building RPM from master

Second phase:

* Implement building DEB packages from master
* Produce the specs for building DEB from master

Dependencies
============

* https://blueprints.launchpad.net/fuel/+spec/build-packages-for-openstack-master-rpm
* https://blueprints.launchpad.net/fuel/+spec/osci-to-dmz

Testing
=======

The following tests should be performed:

* Building all OpenStack components from master using our specs
* Deployment tests for an ISO with customized OpenStack components

The existing deployment tests are adequate for testing customized ISO.

Acceptance criteria:
* Each of OpenStack components could be built from master using our specs
* Deployment of simple multinode OpenStack succeeds
* Diagnostic snapshot works
* Health Check works

Documentation Impact
====================

A note should be added to Fuel User Guide to describe the possibility to build
custom OpenStack components from upstream source repositories during ISO build.

References
==========

None