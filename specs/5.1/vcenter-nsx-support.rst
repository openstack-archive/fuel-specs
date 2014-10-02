..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Integration of NSX with vCenter
===============================

https://blueprints.launchpad.net/fuel/+spec/vcenter-nsx-support

Fuel will be able to deploy OpenStack which will use VMWare vCenter as
a hypervisor and VMWare NSX as a network virtualisation backend.


Problem description
===================

Fuel 5.0 has a limited support of vCenter as a hypervisor and no NSX support
at all, but OpenStack can be integrated with both these components. There are
two other blueprints already about vCenter support improvements [0] and
introducing a basic NSX support [1]. But both features cannot be used
simultaneously without some additional work now. If a user has already paired
vCenter Cluster and the NSX platform (or multiple pairs vCenter + NSX) he
should be able to manage them by OpenStack.

[0] https://blueprints.launchpad.net/fuel/+spec/vcenter-hv-full-scale-support

[1] https://blueprints.launchpad.net/fuel/+spec/neutron-nsx-plugin-integration


Proposed change
===============

After the blueprints [0] and [1] mentioned above would be implemented, there
will be a possibility to enable both features deployed simultaneously. It's
mostly an administrative work needed because all the manifests will be ready,
and we need just to allow a simultaneous use of the features somewhere in
Release description.

Alternatives
------------

We can do nothing, but a user will not be able to use his already paired
vCenter + NSX environment as a hypervisor for OpenStack.

Data model impact
-----------------

No data models modifications needed.

REST API impact
---------------

No REST API modifications needed.

Upgrade impact
--------------

I see no objections about upgrades. NSX Neutron plugin is a part of official
set of plugins. Compute VMWareVCDriver is also official driver. So any
upgrades should be done in a common way.

Security impact
---------------

No additional security modifications needed.

Notifications impact
--------------------

Little modifications of the Cluster Creation Wizard needed.

Other end user impact
---------------------

None.

Performance Impact
------------------

None.

Other deployer impact
---------------------

There should be no significant changes in Puppet modules. Most of the work
should be done on the Nailgun/UI side.

Release upgrades should be covered by blueprints [0], [1] mentioned above.

Developer impact
----------------

No extra developer impact needed.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Andrey Danin (gcon-monolake)

Other contributors:
  Igor Zinovik (izinovik)

Work Items
----------

* Set up the dev environment with one vCenter and one NSX clusters.
* Modify openstack.yaml and test it.
* Create a pull request to Gerrit.
* Describe a test environment and additional System tests and discuss it in ML.
* Set up a test environment and provide System tests.
* Set up additional Jenkins jobs for System tests.


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/vcenter-hv-full-scale-support

https://blueprints.launchpad.net/fuel/+spec/neutron-nsx-plugin-integration

https://blueprints.launchpad.net/fuel/+spec/devops-bare-metal-driver


Testing
=======

* Manual testing using checklists according to acceptance criteria below.

Acceptance Criteria:

- User should be able to deploy environment with CentOS or Ubuntu OS
  in simple or HA mode, and with different roles on machine that
  will support vCenter as hypervisor and NSX plugin in simultaneous
  interrelation with required settings through Fuel UI;
- NSX+vCenter must be stable for destructive tests.
- All ostf tests according them must be passed and network connectivity
  must be verified successfully.

* Will be realized autotests for this features.

Documentation Impact
====================

The documentation should describe how to set up vCenter and NSX for a simple
test environment.

A reference architecture of the feature should be described also.


References
==========

http://docs.openstack.org/trunk/config-reference/content/vmware.html

https://www.edge-cloud.net/2013/12/openstack-vsphere-nsx/
