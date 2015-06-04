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
from here and below mentioning of 'nova-compute' we implicitly consider that
service is configured with VCDriver.  Right now it is not possible for user to
specify node on which these services will be running.  Some deployment
scenarios when vSphere is involved require more flexibility, but Fuel does not
provide a flexible way to distribute nova-compute services among available
nodes.


Problem description
===================

When vCenter is integrated OpenStack it is quite feasible to use vSphere VMs as
hosts for OpenStack.  VMware best practices recommend to deploy vCenter server
inside virtual machine that runs on ESXi host [0].

Also there is a problem with OpenStack cluster expansion with new vSphere
clusters, when OpenStack is deployed and running.  The only way to expand
OpenStack cluster and execute puppet run in Fuel is to add a new node to
cluster.  Since all web UI controls are disabled after cluster is successfully
deployed, cloud operator cannot specify more vSphere clusters on the VMware
tab and press 'Deploy Changes' button.  Right now there is no way to add more
vSphere clusters after OpenStack was deployed.Right now it is not possible to
add vSphere clusters to deployed and running OpenStack cloud. This
specification describes a way how to solve this problem.


Proposed change
===============

This specification proposes to introduce new role **compute-vmware** that will
deploy nova-compute service on arbitrary node.

After implementing this specification end user will be able to assign a node
role **compute-vmware** and specify which vSphere cluster will be managed by
this node/vSphere VM.  After cluster is deployed, it will be possible to add
vSphere clusters on the VMware tab.

If we move nova-compute from Controller nodes to standalone host we lose HA
support for this service, because now it is running under pacemaker
supervision.  If this host on which nova-compute will be running is a vSphere
VM then we can rely on VMware HA[1], otherwise we can rely on supervisor
service, e.g. Monit [2].


Alternatives
------------

We can still run nova-compute services on Controller nodes, but we need to
implement mechanism to run puppet on nodes without adding new node to deployed
OpenStack cluster, but this alternative will not solve flexible service
distribution problem.  Also we must enable controls on the VMware tab in the
Fuel web UI.


Data model impact
-----------------

None.

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
services. Actually he had to decide which nodes will manage what clusters.

User experience can be implemented different ways.  It can be done this way:
user assigns role to nodes on the Nodes tab, then he switches to VMware tab and
assigns nova-compute instances to nodes that were assigned **compute-vmware**
role.  Another way of user experience can be following: user enters vSphere
clusters data on the VMware tab, then switches to the Nodes tab and during
assignment of role **compute-vmware** to node he selects which cluster will be
managed by this node.


Performance Impact
------------------

None.

Plugin impact
-------------

None.

Other deployer impact
---------------------

Ceilometer compute agent must deployed on node with **compute-vmware** role in
order to retrieve metrics.


Developer impact
----------------

Ceilometer support for vCenter requires rework.  Ceilometer compute agent must
be installed on host with **compute-vmware** role when Ceilometer support was
enabled.


Infrastructure impact
---------------------

None.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Igor Zinovik <izinovik@mirantis.com>

Developers:
  Andriy Popovich <apopovych@mirantis.com>
  Anton Zemlyanov <azemlyanov@mirantis.com>
  Igor Zinovik <izinovik@mirantis.com>

QA engineers:
  Okesandr Kosse <okosse@miratnis.com>
  Olesia Tsvigun <otsvigun@mirantis.com>

Work Items
----------

* Add new role to Nailgun database
* Define which roles can be combined with **compute-vmware**
* Implement an opportunity to map nova-compute service to node with role
  **compute-vmware**
* Implement deployment task that will deploy nova-compute
* Extend Fuel deployment graph with new task
* Implement Ceilometer compute agent deployment actions


Dependencies
============

None.


Testing
=======

Following test cases must be implemented:

* Add vSphere cluster via Fuel web UI.  Assign **compute-vmware** to
  unallocated node.  Deploy the cluster. 'nova hypervisor-list' must list
  cluster assigned to the node.

* Create OpenStack environment with vCenter and Ceilometer support.  Assign
  **compute-vmware** role to unallocated node.  Deploy the cluster.  Verify
  that Ceilometer compute agent runs on node.

Documentation Impact
====================

Documentation must describe new role, what problems it solves, what limitations
are related to new role.


References
==========

[0] http://www.vmware.com/files/pdf/vcenter/VMware-vCenter-Server-5.5-Technical-Whitepaper.pdf

[1] http://www.vmware.com/files/pdf/VMwareHA_twp.pdf

[2] https://blueprints.launchpad.net/fuel/+spec/services-under-supervisor
