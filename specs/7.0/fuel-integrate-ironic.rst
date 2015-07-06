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
interface/vlan to which baremetal subnet is be mapped.

Ironic deployment is optional and must be implemented using granular
deployment mechanisms available in Fuel to be a separate task
not interfering with other deployment tasks.
Ironic API deployment should use separate custom role to facilitate later
decoupling of API services from controllers
(blueprint detach-components-from-controllers).


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

- Since only Neutron shared Flat Network is supported there is no way to
  filter  Layer 2 traffic between baremetal nodes among tenants. It is
  possible to perform Layer 2 attacks like MAC spoofing, traffic interception
  etc among tenants. A user is still able to filter Layer 2 traffic on
  baremetal node itself.
- Neutron FWAAS plugin can be used for Layer 3 and upper filtering.
- Additional filtering is needed to strict access from 'Baremetal'
  network to other OpenStack networks such as 'admin', 'management' etc.
- Baremetal servers should have access to:

  - Neutron dhcp/metadata
  - Nova metadata service (for guest OS to be boot-time configurable)
  - TFTP server (which is listening on 'ironic' node on baremetal network)
  - TempURLs exposed by Swift (for downloading target user OS image)
  - Ironic API (for 'I am ready' callback).

- Nodes with "ironic" role (conductors) should have access to baremetal
  network.

HA impact
---------

Ironic API services must be put under HAProxy similar to other
OpenStack API services.

Ironic Conductor services implement their own HA setup based on DB timestamps.
Workloads assigned to a particular ironic-conductor service instance that
has failed are automatically re-assigned to other working ironic-conductor
service instances on the basis of consistent hash-ring algorithm.
Thus failover stability is dependent on overall HA implementation of DB layer.
Notifications on failed ironic-conductor service must be realized as part
of existing cluster monitoring solution (e.g. as Zabbix plugin).
Thus if deploying ironic role on separate nodes, overall at least 6 nodes
are needed for deployment in HA mode (3 controllers + 3 ironic nodes).

HW support impact
-----------------

Given blueprint fuel-bootstrap-on-ubuntu, its functionality
will be used to build a custom image to be used as bootstrap image for
baremetal deployment with Ironic during environment deployment with Fuel.
This image will basically be the same Fuel bootstrap image,
with the same kernel, sans packages/components that are not needed
for Fuel Agent (like nailgun agent etc).
It will be build as usual kernel/ramdisk image.
A more unified with new Fuel bootstrap approach with rootfs
downloadable over HTTP might be implemented in next MOS release.

Usage of such Fuel-bootstrap based image will ensure that the hardware
supported by Ironic baremetal deployment is the same as supported by
Fuel deployment.

Notifications impact
--------------------

Some modifications of the Cluster Creation Wizard needed. Add new 'ironic'
role. Need an additional setting block inside cluster setting tab for filling
up 'baremetal' network and its interface/vlan.

Other end user impact
---------------------

Deployer will be able to assign 'ironic' role to controller or non-controller
nodes. If 'ironic' role is assigned, Deployer must fill up more detail
information in cluster setting tab or keep default settings.

Performance Impact
------------------

None.

Other deployer impact
---------------------

None.

Developer impact
----------------

Ironic is community supported official project, so there is no additional
impact for Developers.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ashestakov

Other contributors:
  vsaienko

QA engineers:
  kromanenko

Design reviewers:
  pshchelokovskyy
  yzveryanskyy

Mandatory design review:
  tnapierala
  vkuklin

Work Items
----------

* Modify Cluster Creation Wizard page. Add 'ironic' role and test it.
* Modify Cluster setting tab. Add 'Baremetal' settings information forms
  and test it.
* Integrate new role to puppet manifests.
* Update core puppet manifests from upstream projects.
* Describe a test environment and additional System tests.
* Set up a test environment and provide System tests.
* Set up additional Jenkins jobs for System tests.

High-level list of changes to deployed components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* DB

  * add Ironic required tables

* controllers

  * Ironic

    * install python-ironicclient
    * install ironic-api

      * plug ironic-api in HAProxy


  * Nova

    * configure to use IronicHostManager
    * configure to use baremetal scheduler filters

*  Ironic role

   * Ironic

     * install ironic-conductor
     * install ironic-fuelagent-driver
     * install TFTP server

   * Nova

     * install python-ironicclient
     * install nova-compute

       * configure to use ironic-virt-driver
       * configure to use Ironic's ClusteredComputeManager


* Fuel master

  * build Ironic bootstrap image
  * upload Ironic bootstrap image to Glance

* Zabbix

  * add plugin for ironic-api
  * add plugin for ironic-conductors


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
    nodes via ironic-client.
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

  * For load testing an environment with several/many available extra
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

