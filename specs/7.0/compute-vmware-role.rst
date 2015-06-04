..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================================
Deploy nova-compute (VCDriver) service on separate node
=======================================================

https://blueprints.launchpad.net/fuel/+spec/compute-vmware-role

Starting from Fuel 5.0 nova-compute services that manage virtual machines in
vSphere clusters via vCenter server are deployed on Controller nodes, starting
from here and below mentioning of 'nova-compute' term we implicitly consider
that service is configured with VCDriver.  Right now it is not possible for
user to specify node on which these services will be running.  Some deployment
scenarios where vSphere is involved require more flexibility, but Fuel does not
provide a flexible way to distribute nova-compute services among available
nodes.


Problem description
===================

When vCenter is integrated with OpenStack it is quite feasible to use vSphere
VMs as hosts for OpenStack.  VMware best practices recommend to deploy vCenter
server onto virtual machine that runs on ESXi host [0]_.

Also there is a problem with OpenStack cluster expansion with new vSphere
clusters, when OpenStack is deployed and running.  The only way to expand
OpenStack cluster and execute puppet run in Fuel is to add a new node to
cluster.  Since all web UI controls are disabled after cluster is successfully
deployed, cloud operator cannot specify more vSphere clusters on the VMware tab
and press *Deploy Changes* button.  Right now there is no way to add more
vSphere clusters after OpenStack was deployed with Fuel.  Right now it is not
possible to add vSphere clusters to deployed and running OpenStack cloud. This
specification describes a way how to solve this problem.


Proposed change
===============

This specification proposes to introduce new role **compute-vmware** that will
allow deploy nova-compute service on standalone node.

After implementing this specification end user will be able to assign a node
role compute-vmware and specify which vSphere cluster will be managed by
this node/vSphere VM.  After cluster is deployed, it will be possible to add
vSphere clusters on the VMware tab and assign compute-vmware role to free
nodes.

This specification do not proposes to change current situation with
nova-compute deployment on controller nodes.

Special attribute will be provided on the VMware tab in 'Nova computes'
section.  This attribute will be implemented as dropdown UI control that will
hold names of nodes that were assigned compute-vmware role and special value
*controllers* that let user deploy nova-compute usual way (on controller
nodes).  If user decides that particular service is going to be running on such
node he selects a node in this dropdown list.

It will be not possible to combine compute-vmware role any other available
roles.

Cloud operator workflow will look like this:

#. Create cluster with a bunch of controllers, compute and storage nodes

#. vSphere infrastructure runs 4 clusters

#. Operator decides that 3 clusters will be controlled by compute-vmware
   nodes and last one will be managed by nova-compute on controller node

#. He creates a small cluster in vCenter that will hold compute-vmware
   nodes, creates 3 virtual machines, configures their networking such way that
   they can boot over PXE from Fuel master node

#. In Fuel web UI operator assigns compute-vmware role to 3 new nodes

#. On the VMware tab operator assigns vSphere clusters to nodes using dropdown
   list in 'Nova computes' settings group

#. Operator starts cloud deployment.  UI controls appear enabled on the VMware
   tab after successful cloud deployment

If we move nova-compute from controller nodes to standalone host we lose HA
support for this service, because now it is runs under pacemaker supervision.
If this host on which nova-compute will be running is a vSphere VM then we can
rely on VMware HA [1]_.


Alternatives
------------

We can still run nova-compute services on Controller nodes, but we need to
implement mechanism to run puppet on nodes without adding new node to deployed
OpenStack cluster, but this alternative will not solve flexible service
distribution problem.


Data model impact
-----------------

VMware tab on Fuel web UI requires additional UI control - dropdown list, which
will hold names of nodes that were assigned compute-vmware role and special
value *controllers* which means that service will be deployed on controller
nodes.  While there are no nodes with compute-vmware role, value *controllers*
is the only option for dropdown list, it is considered as a sane default value.
*openstack.yaml* will be extended with new metadata for *target_node* attribute
in *vmware_attributes* section.

.. code-block:: yaml

    openstack.yaml
    ...
    # target_node metadata definition
    vmware_attributes_metadata:
      editable:
        metadata:
        ...
          name: "target_node"
          type: "dropdown"
          label: "Target node"
          description: "Target node for nova-compute service"


    # target_node definition
        ...
        value:
          availabitliy_zones:
            -
              az_name: "vcenter"
              vcenter_host: ""
              ...
              value: "controllers"
              values:
                -
                  data: "controllers"
                  value: "controllers"

Nailgun should be able to serialize new attribute *target_node* and pass it
into astute.yaml file:

.. code-block:: yaml

    /etc/astute.yaml
    ...
    vcenter:
     computes:
     - datastore_regex: "openstack-.*"
       service_name: cluster1
       availability_zone_name: vcenter
       vc_cluster: Cluster1
       vc_host: 172.16.0.254
       vc_password: Qwer!1234
       vc_user: administrator@vsphere.local
       target_node: controllers
     - datastore_regex: "openstack-.*"
       service_name: cluster2
       availability_zone_name: vcenter
       vc_cluster: Cluster2
       vc_host: 172.16.0.254
       vc_password: Qwer!1234
       vc_user: administrator@vsphere.local
       target_node: node-42


REST API impact
---------------

None.

Upgrade impact
--------------

None.

Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

User must be able to select on which nodes he wants to run nova-compute
services. Actually he had to decide which nodes will manage by what clusters.


Performance Impact
------------------

None.

Plugin impact
-------------

None.

Other deployer impact
---------------------

Ceilometer compute agent must be deployed on node with compute-vmware role in
order to retrieve telemetry data if Ceilometer support was enabled.


Developer impact
----------------

Fuel web UI impact
~~~~~~~~~~~~~~~~~~
Specification requires changes in Fuel web UI interface in order to provide
desired user experience.  Frontend code must also be able fetch list of nodes
with compute-vmware role in order to render their names in dropdown UI
control.

Controls on the VMware tab must not be locked after cluster is deployed to
allow user add more vSphere clusters.

Nailgun impact
~~~~~~~~~~~~~~

Deployment serializer must pass new attribute to orchestrator.

Ceilometer support impact
~~~~~~~~~~~~~~~~~~~~~~~~~

Fuel library 'vmware' module must deploy ceilometer compute agent on node with
compute-vmware role if ceilometer support was enabled for OpenStack
environment.


Infrastructure impact
---------------------

None.


Implementation
==============

Assignee(s)
-----------

Primary assignee:

  Igor Zinovik <izinovik@mirantis.com>

Mandatory design review:

  Andrey Danin <adanin@mirantis.com>

  Sergii Golovatiuk <sgolovatiuk@mirantis.com>

Developers:

  Nailgun

  Andriy Popovich <apopovych@mirantis.com>

  Fuel web UI

  Anton Zemlyanov <azemlyanov@mirantis.com>

  Fuel-library

  Igor Zinovik <izinovik@mirantis.com>

Quality assurance

  Okesandr Kosse <okosse@mirantis.com>

  Olesia Tsvigun <otsvigun@mirantis.com>

Work Items
----------

* [Nailgun] Add new role to Nailgun database
* [Nailgun] Restrict combining compute-vmware with other roles
* [Nailgun] Modify deployment serializer
* [UI] Implement function that will fetch names of nodes with compute-vmware
  role
* [UI] Implement dropdown UI control for nodes on the VMware tab
* [UI] Allow controls on the VMware tab stay enabled after successfull cluster
  deployment
* [Fuel-library] Implement deployment task that will deploy nova-compute
* [Fuel-library] Extend Fuel deployment graph with new task
* [Fuel-library] Implement ceilometer compute agent deployment actions


Dependencies
============

None.


Testing
=======

Following test cases must be implemented:

* Cluster with nova-compute only on controllers

  * Create a cluster with vCenter support
  * Skip adding vmware-compute hosts
  * Deploy the cluster

* Cluster with nova-compute on controllers and compute-vmware nodes

  * Create a cluster with vCenter support
  * Add one vmware-compute node
  * Assign vSphere cluster to vmware-compute node
  * Deploy the cluster

* Ceilometer enabled cluster with nova-compute on controllers and
  compute-vmware nodes

* Cluster with nova-compute only on compute-vmware nodes

  * Create a cluster with vCenter support
  * Add vmware-compute nodes; amount of nodes must be equal to number of
    vSphere clusters
  * Assign vSphere clusters to vmware-compute nodes
  * Deploy cluster

* Add vSphere cluster to OpenStack environment with nova-computes running only
  on controllers

* Add vSphere cluster to OpenStack environment with nova-computes running on
  controllers and compute-vmware nodes

* Add vSphere cluster to OpenStack environment with nova-computes running only
  on compute-vmware nodes

Acceptance criteria
-------------------

User is able to deploy nova-compute service on node with
compute-vmware role.


Documentation Impact
====================

Documentation must describe new role, what problems it solves, what limitations
are related to new role.


References
==========

.. [0] http://www.vmware.com/files/pdf/vcenter/VMware-vCenter-Server-5.5-Technical-Whitepaper.pdf

.. [1] http://www.vmware.com/files/pdf/VMwareHA_twp.pdf
