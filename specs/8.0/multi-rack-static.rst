..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Support for multi-rack deployment with static routes
====================================================

https://blueprints.launchpad.net/fuel/+spec/l3-multiple-racks

Fuel should allow user to deploy OpenStack to multiple racks with a scalable
underlay network design so that the user can meet his or her expanding business
needs without having to re-deploy/migrate workloads.


--------------------
Problem description
--------------------

Current implementation of multi-rack support lacks a number of features in
demand (all services via one network, networks shared between node network
groups, VIPs can be allocated in different node network groups, arbitrary VIP
addresses), and has a number of usability issues (manual setup of dnsmasq on
master node, lack of validation, nodes do not have connection with node network
groups until they are added into environment but in fact they have IPs from
different node network groups, new routes are not applied when node network
group is added to the deployed environment).

Current proposal deals with the issues listed above.


----------------
Proposed changes
----------------

1. Make additional setup of dnsmasq on master node when node network groups are
configured. User should do that by hands now. It should be done automatically
when parameters of any of Admin networks are changed or Admin network is
deleted. This will save a user from manual error-prone operations of setting
this up via a command line.
See https://bugs.launchpad.net/fuel/+bug/1495593

2. When a new node network group is added to the deployed environment new
routes should be applied to network configuration of all nodes. This will
resolve an issue with adding node network groups to the deployed environment.
Reconfiguration should also be done when any of netmasks for networks of
deployed environment is changed.
See https://bugs.launchpad.net/fuel/+bug/1502842

3. VIP auto-allocation is restricted to controller node group now in Nailgun.
It should be allowed to allocate VIP in any node group to allow proper
separation of HA services into different nodes. But other restriction remains
the same: VIP can be allocated only if all nodes which conform to its
node_roles section are in the same node group.
See https://bugs.launchpad.net/fuel/+bug/1487021

4. Provide an ability to share network (L2/L3 parameters)
between several node network groups. As for now, each particular node network
group have its own L2/L3 parameters for every network. It is 1:1 mapping.
It will be possible to share arbitrary networks (use the same L2/L3 parameters)
between several node network groups. It will be possible to use completely
arbitrary mapping.
To have some network shared between two node network groups user will have to
setup equal L3 parameters for those (CIDR an Gateway should be equal, IP ranges
do not matter). Routes between networks having same L3 will not be generated.
Only networks with the same name can be shared this way.
VLAN IDs of networks can be equal or different. VLAN IDs for the same network
interface should be different.
E.g. this ability is required to use a dedicated storage.
See https://bugs.launchpad.net/fuel/+bug/1473047

5. Ability to set the floating IP range. Now, Nailgun doesn't allow to set
floating IP range from non-default node network group. So, network and
controller nodes can be deployed in default nodegroup only. It should be
allowed to set floating range within any of Public networks. So, it will be
possible to deploy controller nodes in any node group. IPs from the
floating range need to be added to the allocated addresses pool.
See https://bugs.launchpad.net/fuel/+bug/1502829

Web UI
======

GUI tasks are to be in separate ticket/spec.

Nailgun
=======

Change 1.
a. The "update_dnsmasq" task will be added to serve auto setup of dnsmasq on
master node. This Nailgun task will "upload_file", "puppet" and "cobbler_sync"
orchestrator tasks to update dnsmasq configuration.
b. Nailgun will run that task when some of IP ranges of Admin networks are
changed via API.
c. Nailgun API validator will check new Admin IP ranges against IPs of nodes
currently visible to Fuel (bootstrap and deployed ones). Also, Nailgun will
check IPS of newly added nodes against Admin IP ranges and mark nodes with
errors if they are out of known Admin IP ranges.

Change 2.
a. New Nailgun task will be added to rerun networking configuration on deployed
nodes (or deployment tasks graph will be rebuilt).
b. Deployment data for deployed nodes will be regenerated when required.
c. Controller nodes maybe triggered for redeploy when required.

Change 3.
a. VIPs addresses assignment should be reworked to determine the node network
group where VIP address should be allocated (using node roles and network role
from VIP description). Now the node network group that contains controllers is
always taken for assgnment of VIPs.
b. Nailgun should check that each VIP address should belong to exactly one
nodegroup.

Change 4.
a. Validation of network parameters (NetworkCheck class methods) should allow
intersection of CIDRs and gateways (simultaneously only) of several networks
with the same name from different (not the same) node network groups. In case
of such intersection those networks are considered as one shared network and no
routes should be generated between segments.
b. Validation of network parameters (NetworkCheck class methods) should allow
equal VLAN IDs within environment. Exception is that every single network
interface cannot handle coincident VLAN IDs.

Change 5.
a. Change the verification of floating ranges to allow floating range to match
any of Public networks in environment. Now it may only match Public network
from default node network group.
b. Change the serialization of floating network to find appropriate Public
network for floating ranges defined.

Data model
----------

Change 1.
New task name and new node error type will be added.

Change 2.
New parameter for modular tasks is added: 'reexecute_on'. This parameter is a
list of Nailgun events on which this task should be re-executed. For example:

::

  - id: netconfig
    type: puppet
    groups:
      [primary-controller, controller, cinder, cinder-vmware, compute,
      ceph-osd, primary-mongo, mongo, virt, ironic]
    required_for: [deploy_end]
    requires: [tools]
    reexecute_on: [deploy_changes]
    parameters:
      puppet_manifest:
        /etc/puppet/modules/osnailyfacter/modular/netconfig/netconfig.pp
      puppet_modules: /etc/puppet/modules
      timeout: 3600

It means that 'netconfig' task will be re-executed on 'deploy_changes' event.

REST API
--------

Data formats remain the same. Flow for network configuration is changed for
change 5.

Orchestration
=============

We introduce new Nailgun hook in Astute - "cobbler_sync". It runs cobbler sync
to reload dnsmasq configuration. It does not affect other aspects of deployment
orchestration.

RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

None

Fuel Library
============

New "nailgun::dnsmasq::dhcp_range" class added. It creates separate dnsmasq
configuration file in `/etc/dnsmasq.d/` directory for every dhcp-range. We also
configure dnsmasq to use `/etc/dnsmasq.d/` as conf-dir. `/etc/dnsmasq.d`
directory is stored on the host system to prevent data loss due to container
restart/rebuild.

------------
Alternatives
------------

This feature can be treated as a composition of several smaller changes. Seems,
all of them can be implemented separately. But some tasks have dependencies:
8 depends on 1 and 5.


--------------
Upgrade impact
--------------

N/A

---------------
Security impact
---------------

N/A

--------------------
Notifications impact
--------------------

When a node group or a cluster is deleted there can be some nodes in bootstrap
which have IPs corresponding to those deleted node groups. They cannot be
provisioned as dnsmasq configuration does not contain information about those
admin networks anymore. Nailgun marks such nodes as 'error' and sends
appropriate notification.

---------------
End user impact
---------------

User no longer needs to update dnsmasq.template file manually and append
EXTRA_ADMIN_NETWORKS. All the DHCP related changes are being applied by Fuel
automatically.

------------------
Performance impact
------------------

N/A

-----------------
Deployment impact
-----------------

It's possible to change admin network even for default node group (node group
where Fuel node is). DHCP/PXE related settings provided via fuel-menu during
Fuel node bootstrap are used only for initial DHCP configuration. After that
Nailgun controls all the network related settings even for DHCP/PXE network.
Please note that if you change DHCP/PXE CIDR for the default node group and
it requires to change Fuel node IP address, you should change it on admin
interface of Fuel node manually and check/update docker containers.

----------------
Developer impact
----------------

None

--------------------------------
Infrastructure impact
--------------------------------

TBD

--------------------
Documentation impact
--------------------

We should remove documentation about manual update of dnsmasq.template file
here:
https://docs.mirantis.com/openstack/fuel/fuel-7.0/operations.html#configuring-multiple-cluster-networks

--------------------
Expected OSCI impact
--------------------

N/A

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee: Alex Didenko

Other contributors: Aleksey Kasatkin, Sergey Vasilenko

Mandatory design review: Andrew Woodward, Sergey Vasilenko


Work Items
==========

- Make additional setup of dnsmasq on master node when admin network parameters
  are changed in any node network group.
- Re-apply the network configuration on all nodes when new node group is added
  into deployed env and when network masks are changed for the deployed env.
- It should be allowed to auto-allocate VIP in any node group to allow proper
  separation of HA services into different nodes.
- CLI/API only: There is an ability to share network between several node
  network groups or to use separate L2/L3 parameters for each node network
  group.
- Make it possible to set floating IP range from non-default node network
  group.

Dependencies
============

N/A

------------
Testing, QA
------------

In order to verify the quality of new features, automatic system tests will be
expanded by the cases listed below:

1. Environment is deployed using slaves from non-default nodegroup as
controller nodes. See https://blueprints.launchpad.net/fuel/+spec/test-custom-nodegroup-controllers

2. New nodegroup is added to operational environment.
See https://blueprints.launchpad.net/fuel/+spec/test-nodegroup-add

3. Environment is deployed using default gateway from non-public network.
See https://blueprints.launchpad.net/fuel/+spec/test-custom-default-gw

4. Deploy environment with few nodegroups and shared network parameters between
them. See https://blueprints.launchpad.net/fuel/+spec/test-nodegroups-share-networks

5. Default IP range is changed for admin/pxe network.
See https://bugs.launchpad.net/fuel/+bug/1513154

6. Slave nodes are bootstrapped and successfully deployed using non-eth0
interface for admin/pxe network. See https://bugs.launchpad.net/fuel/+bug/1513159

Also there is a need to align existing tests for multiple cluster networks with
new features. See https://blueprints.launchpad.net/fuel/+spec/align-nodegroups-tests

Acceptance criteria
===================

- Make additional setup of dnsmasq on master node when admin network parameters
  are changed in any node network group. User should do that by hands now.
- Re-apply the network configuration on all nodes when new node group is added
  into deployed env and when network masks are changed for the deployed env.
- It should be allowed to auto-allocate VIP in any node group to allow proper
  separation of HA services into different nodes.
- CLI/API only: There is an ability to share network between several node
  network groups or to use separate L2/L3 parameters for each node network
  group.
- Make it possible to set floating IP range from non-default node network
  group. So, it will be possible to deploy controller nodes in any node group.

----------
References
----------

https://blueprints.launchpad.net/fuel/+spec/l3-multiple-racks
