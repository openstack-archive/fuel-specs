..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================================================
Compliance openstack global requirements for MOS OpenStack and Fuel
===================================================================

https://mirantis.jira.com/browse/PROD-529

We must restrict ourselves to use only packages from both Fuel
Requirements and Global Requirements for the version of OpenStack.

Problem description
===================

A detailed description of the problem:

* For a new feature this might be use cases. Ensure you are clear about the
  actors in each use case: End User vs Deployer

* For a major reworking of something existing it would describe the
  problems in that feature that are being addressed.


Proposed change
===============

We strict ourselves to use only packages from both Fuel Requirements and
Global Requirements for the version of OpenStack, Fuel is installing
in the following manner:

* If a requirement is in Global Requirements, the version spec in all Fuel’s
  components should be exactly like that.

* If a requirement is not in the Global Requirements list, then
  Fuel Requirements list should be used to check whether all
  Fuel’s components require the same version of a library/package.

* OSCI mirror should contain the maximum version of a requirement that
  matches its version specification.

* Set up CI jobs in both OpenStack CI and FuelCI to check all patches
  against both Global Requirements and Fuel Requirements and block,
  if either of checks doesn’t pass.

* Set up CI jobs to notify OSCI team if either Global Requirements or Fuel
  Requirements are changed.

* Set up requirements proposal jobs that will automatically propose
  changes to all fuel projects once either of requirements lists was
  changed, just like it’s done for OpenStack projects.

* When the base Linux distro has a package that satisfies the global
  requirements, the distro package should be used even if a more
  recent version is available from upstream.

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
* Implement an automatic notification to the developers about the new
  changes in Openstack global requirements

* Implement an automatic notification to the developers of the
  compatibility versions between Openstack and fuel

Other end user impact
---------------------

None

Performance Impact
------------------

None

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

* Transfer library versions fuel required in line Openstack global
  requirements.

Infrastructure impact
---------------------

Proposed change requires a new Jenkins job called Fuel Requirements,
all changes to it should go through a standard review procedure.

Implementation
==============

Assignee(s)
-----------

Dmitry Kaigarodеsev  <dkaiharodsev@mirantis.com>

Work Items
----------

The Implementation is splitted on a few steps:

* Implement job on http://osci-jenkins.srt.mirantis.net:8080/

* Write a JJB YAML configuration file for implementing on
  http://jenkins-product.srt.mirantis.net:8080/

Dependencies
============

None

Testing
=======

Testing approach:

* In case of non-compliance to Global Requirements with
  MOS OpenStack and Fuel we must be able to get notification.

Documentation Impact
====================

None

References
==========

* https://mirantis.jira.com/browse/PROD-529

* https://blueprints.launchpad.net/fuel/+spec/automate-the-verification-of-compliance-openstack-global-requirement
