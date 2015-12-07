..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================================
Separate deployment of Fuel node from base OS provisioning
==========================================================

https://blueprints.launchpad.net/fuel/+spec/separate-fuel-node-provisioning

Split the Fuel node deployment process into base OS provisioning and Fuel
deployment parts.

--------------------
Problem description
--------------------

Currently, the setup of Fuel node is provided by monolithic combination
of Anaconda kickstart with custom preinstall/postinstall scripts, and the
mixed set of upstream and MOS packages. There is no possibility to install
Fuel on a pre-provisioned system containing only base OS packages.

----------------
Proposed changes
----------------

Web UI
======

No changes required.

Nailgun
=======

No changes required.

Data model
----------

No changes required.

REST API
--------

No changes required.

Orchestration
=============

No changes required.

RPC Protocol
------------

No changes required.

Fuel Client
===========

No changes required.

Plugins
=======

No changes required.

Fuel Library
============

Some parts of Fuel node provisioning steps need to be shifted to Puppet
manifests.

A script for Fuel deployment should be packaged as well as other Fuel
components.

------------
Alternatives
------------

A next step (rather than alternative way) here would be to move Fuel towards
the fully networked installation, where an ISO contains nothing but the
netinstall files, with external public MOS repositories configured along
with the upstream OS ones. Implementing this feature, and all upcoming
specifications allows us to diversify the ways Fuel could be installed.

--------------
Upgrade impact
--------------

No changes required.

---------------
Security impact
---------------

No changes required.

--------------------
Notifications impact
--------------------

No changes required.

---------------
End user impact
---------------

Implementing this feature greatly affects the end user, by providing the
ability to install Fuel using pre-provisioned node.
There will be no automated Fuel installation after base OS is provisioned.
User will be given an instruction on how to install Fuel manually.

------------------
Performance impact
------------------

No changes required.

-----------------
Deployment impact
-----------------

Changes described in ths document only affect Fuel node installation.

----------------
Developer impact
----------------

No changes required.

---------------------
Infrastructure impact
---------------------

Implementing this feature could greatly affect the CI systems by minimizing
the efforts needed to install Fuel on top of an existing base OS environment.

--------------------
Documentation impact
--------------------

The new workflow of Fuel provisioning should be reflected in user documentation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  vparakhin

Mandatory design review:
  rvyalov
  vkozhukalov

Work Items
==========

* Modify kickstart to separate base OS provisioning from Fuel deployment
* Prepare package for automatical configuration of the MOS repositories in yum
* Package the Fuel installation script

Dependencies
============

None

------------
Testing, QA
------------

Integration Tests
-----------------

As long as the feature introduces the ability to install Fuel separately from
product ISO, there should be a test that implements that feature.

Acceptance criteria
===================

* Installation of Fuel node is clearly separated between base OS provisioning
  (upstream packages) and Fuel deployment (MOS packages)
* Fuel can be installed on an pre-provisioned CentOS 7 server using either
  online repositories (Internet access is required), or a MOS ISO (Internet
  access is optional)

----------
References
----------

None