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
A common use case is to deploy user images on baremetal hosts (skipping the
virtualization layer) with the help of Ironic driver in Nova, leveraging
better performance of such instances (e.g. member of a Hadoop cluster or
Docker host with multiple containers running).

Proposed change
===============

New 'Ironic' role will be added to Fuel which configure 'ironic-conductor',
tftp  services on node. It can be assigned to controllers or non-controller
nodes. Once 'ironic' role is checked, it should add 'ironic-api' on all
controller nodes behind HA proxy. Having analyzed the Ironic use-cases, we
plan to support only Neutron VLAN with additional shared Flat Network for
baremetal nodes in MOS 7.0. This does not require all the environment to be
in a single VLAN, only baremetal nodes. At the cluster creation wizard page
new role 'ironic' - assigned to separate nodes where 'ironic-conductor' and
nova-compute with baremetal driver are deployed. We also need to add
additional block at cluster settings tab to configure baremetal subnet and
interface/vlan to which baremetal baremetal subnet is be mapped.


Alternatives
------------

None

Data model impact
-----------------

We have to store following data in settings:

- 'ironic' node role
- 'baremetal' subnet with its interface/vlan.

REST API impact
---------------

No REST API modifications needed.

Upgrade impact
--------------

It is new components, upgrade from previous versions will be transparent.

Security impact
---------------

- Since only Neutron shared Flat Network network is supported there is
  no way to filter traffic between baremetal nodes among tenants.
- Additional filtering is needed to strict access from 'Baremetal'
  network to other openstack networks such as 'admin', 'management' etc.
- Baremetal servers should have access to neutron dhcp/metadata and tftp
  server (which listening on 'ironic' node on baremetal network) and
  swift URL.
- Nodes with "ironic" role (conductors) should have access to baremetal
  network.

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

Ironic is comunity supported official project, so there is  no additional
impact for Developers.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ashestakov

Other contributors:
  vsaienko

Design reviewers:
  pshchelokovskyy
  yzveryanskyy

Work Items
----------

* Modify Cluster Creation Wizard page. Add 'ironic' role and test it.

* Modify Cluster setting tab. Add 'Baremetal'settings information forms
  and test it.

* Integrage new role to puppet manifests.

* Update core puppet manifests from upstream projects.

* Create a pull request to Gerrit.

* Describe a test environment and additional System tests.

* Set up a test environment and provide System tests.

* Set up additional Jenkins jobs for System tests.


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/granular-network-functions

https://blueprints.launchpad.net/fuel/+spec/baremetal-deploy-ironic

Testing
=======

* Manual testing and acceptance criteria:

 - Fuel can assign 'ironic' roles to discovered nodes.
 - Admin plug servers to 'baremetal' network, make sure that IPMI
   interfaces are  accessible from controller.
 - Admin user of deployed OpenStack environment can register baremetal
   nodes via   ironic-client.
 - The ordinary user is able to deploy a nova instance to a baremetal
   node via the Ironic baremetal driver.
 - The user should be able to concurrently deploy several baremetal
   nodes.

* Automated testing, OSTF:

 - As the test run depends on what exactly are actual parameters of
   the baremetal nodes (HW MAC address and other host capabilities,
   IPMI credentials), it seems really hard to implement an automatic
   testing framework that will test the real Ironic drivers. The
   automated testing instead would use virtual Ironic environments
   to test the Ironic inner workings only.

* Testing at Scale:

 For load testing an environment with several/many available extra
 baremetal nodes is required to test concurrent provisioning workload
 to several baremetal nodes. In our Scale lab it might be possible to
 test Ironic automatically if a tool/script could be created to
 collect data on some nodes and register those with Ironic service of
 the deployed OpenStack environment. Then it would be possible to
 test Ironic scalability and performance at our Scale lab following
 next simplified scenario:

 - Create an environment with e.g. 100 nodes, 3 of them controllers,
   2 with “ironic” role.
 - Run the above mentioned tool to register 95 nodes in Ironic.
 - Upload an image suitable for baremetal deployment to Glance.
 - Boot 95 baremetal servers via Nova.

* A Rally scenario must also be created to automate such testing.

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

