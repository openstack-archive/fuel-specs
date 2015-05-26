..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================
Fuel integrate ironic
================================

https://blueprints.launchpad.net/fuel/+spec/fuel-integrate-ironic


Problem description
===================

Ironic is an OpenStack project which provisions bare metal (as opposed to
virtual) machines by leveraging common technologies such as PXE boot and
IPMI to cover a wide range of hardware, while supporting pluggable drivers
to allow vendor-specific functionality to be added.
A common use case is to start user instances on baremetal hosts (skipping the
virtualization layer) with the help of Ironic driver in Nova, leveraging
better performance of such instances (e.g. member of a Hadoop cluster or
Docker host with multiple containers running).

Proposed change
===============

We could let Fuel to setup additional 'ironic' role. Which can be assigned to
controllers or non-controller nodes. Having analyzed the Ironic use-cases, we
plan to support only the shared Flat Network in MOS 7.0. This does not require all
the environment to be in a single VLAN, only baremetal nodes. At the cluster
creation wizard page add additional 'ironic' role. We also need to add
additional block at cluster settings tab to configure baremetal subnet
and interface/vlan to which baremetal baremetal subnet is be mapped.


Alternatives
------------



Data model impact
-----------------

We have to store following data in settings:

* The baremetal subnet.

* Interface/vlan to which baremetal subnet is mapped.


  REST API impact
---------------

No REST API modifications needed.


Upgrade impact
--------------

I see no objections about upgrades. Ironic is upstream OpenStack
project, so any upgrades should be done in a common way.


Security impact
---------------

Since only shared Flat Network network is supported there is no way to
filter traffic between baremetal nodes among tenanets.
Also additional filtering is needed to strict access from 'Baremetal'
network to other openstack networks such as 'admin', 'management' etc.


Notifications impact
--------------------

Some modifications of the Cluster Creation Wizard needed. Add new 'ironic'
role. Need an aditional setting block inside cluster setting tab for fill
up 'baremetal' network and its interface/vlan.


Other end user impact
---------------------

Deployer will be able to assign 'ironic' role to controller or non-controller
nodes. If 'ironic' role is assigned, Deployer must fill up more detail
information in cluster setting tab or left default settings.


Performance Impact
------------------

None.


Other deployer impact
---------------------

None.


Developer impact
----------------

Ironic is comunitty supported official project, so there is  no additional
impact for Developers.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ashestakov

Other contributors:
  vsaienko


Work Items
----------

* Modify Cluster Creation Wizard page. Add 'ironic' role and test it.

* Modify Cluster setting tab. Add 'Baremetal'settings information forms and test
  it.

* Integrage new role to puppet manifests.

* Update core puppet manifests from upstream projects.

* Create a pull request to Gerrit.

* Describe a test environment and additional System tests.

* Set up a test environment and provide System tests.

* Set up additional Jenkins jobs for System tests.


Dependencies
============

None


Testing
=======

* Additional functional tests for UI.

* Additional functional tests for puppet script.

wrapped up as a separate Jenkins thread job.


Documentation Impact
====================

* The documentation should describe how to set up Ironic via Fuel. Add
  baremetal nodes to ironic database, prepare images and do provisioning.

* The documentation should warn about possible security issues with shared
  Flat network setup.


References
==========

http://docs.openstack.org/developer/ironic/deploy/user-guide.html

https://wiki.openstack.org/wiki/Ironic

