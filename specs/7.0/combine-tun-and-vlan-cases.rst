..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Allow Fuel to have VLAN and TUN modes for Neutron simultaneously
================================================================

https://blueprints.launchpad.net/fuel/+spec/combine-tun-and-vlan-cases

For a customer, we need to provide more network data plane flexibility. It is
advisable configure Neutron for using VLAN and TUN modes simultaneously if
system administrator didn't disable some of this modes.
There a few reason for this:

* Neutron, by default, start to use networks with TUN segmentation if vlan
  segmentation IDs into existing cloud are finished.
* Currently, we should run two copy of system tests for each segmentation type.
  In the closest future we plan implement "provider networks" solutions and this
  copies will be three. But we can reduce load to test subsystem by implementing
  this feature and test all network subcases in parralel.
* customer will get more flexible configuration for use networks with different
  segmentation types inside one environment.


Problem description
===================

Fuel 7.0 and earlier has a separated network subcases for deploy Neutron in
TUN (VXLAN or deprecated GRE) and VLAN modes.

Proposed change
===============

* Deploy both TUN and VLAN network modes simultaneously. Use VXLAN as default
  solution for TUN segmentation type.
* Rename base networks, that will be creted for 'admin' tenant while deploy
  to more descriptive names.
* Allow network roles, related to corresponded Neutron deployment cases,
  to carry some deployment parameters as network role metadata (see
  corresponded blueprint)

Alternatives
------------

Leave networks names and deployment models as is.


Data model impact
-----------------

...in progress...

REST API impact
---------------

...in progress...

UI impact
--------------

Significant changes are expected in UI with regard to networking configuration
experience. User will be allowed to configure both pre-defined networks.


Upgrade impact
--------------

Migration of schema and data must be provided to support previously created
environments and creation of environments with older releases. It should
include migration of existing releases, clusters and their nodes data.


Security impact
---------------

No additional security modifications needed.


Notifications impact
--------------------

N/A.


Other end user impact
---------------------

N/A.


Performance Impact
------------------

No Nailgun/Library/UI performance impact is expected.


Other deployer impact
---------------------

N/A


Developer impact
----------------

N/A


Implementation
==============

Assignee(s)
-----------

Feature Lead: Sergey Vasilenko

Mandatory Design Reviewers: Andrew Woodward, Chris Clason, Vladimir Kuklin

Developers: Aleksey Kasatkin, Vitaly Kramskikh, Ivan Kliuk

QA: Anastasiia Urlapova


Work Items
----------

* Nailgun: Temporary hardcode network properties for TUN segmentation type.
  This unblock work on library-part of this task.
* Nailgun: provide new data structures in astute.yaml for network
   configuration.
* Library: prepare manifests for using new data structures
* Nailgun: provide changes in API.
* UI: support network roles metadata edit from UI (part of
  https://blueprints.launchpad.net/fuel/+spec/flexible-network-roles )
* Nailgun: remove tempopary-hardcoded values as soon as UI will be support
  network roles metadata.


Dependencies
============

Partially depends on 'flexible networking' feature.


Testing
=======

* Additional unit/integration tests for Nailgun.
* Additional functional tests for UI.
* Changes to System tests for subbort both network backend simultaneously.
* Some part of old tests of all types will become irrelevant and
  are to be redesigned.

Acceptance Criteria
-------------------

* There is no need to select networking backend when environment
  is being created (in wizard).
* Any or both of VLAN and TUN backends can be set up for the environment.


Documentation Impact
====================

The documentation should describe new networking architecture of Fuel,
changes and new features in networking configuration process in UI.


References
==========

https://blueprints.launchpad.net/fuel/+spec/combine-tun-and-vlan-cases
https://blueprints.launchpad.net/fuel/+spec/flexible-network-roles
