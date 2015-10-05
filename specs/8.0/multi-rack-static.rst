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

5. API must allow VIP to be manually set to ANY valid IP address. If the IP on
update API is a member of any network in this environment then the address
should be put in the assignments table so that it can not be used in any other
automatic assignment. (This allows the user to override if the automatic
allocation doesn't match their needs or in the case that they want to use
external LB).
See https://bugs.launchpad.net/fuel/+bug/1482399

6. Ability to set the floating IP range. Now, Nailgun doesn't allow to set
floating IP range from non-default node network group. So, network and
controller nodes can be deployed in default nodegroup only. It should be
allowed to set floating range within any of Public networks. So, it will be
possible to deploy controller nodes in any node group. IPs from the
floating range need to be added to the allocated addresses pool.
See https://bugs.launchpad.net/fuel/+bug/1502829

7. Default gateway for nodes is always taken from Public network (or Admin
network when Public is absent). It should be possible to select any network
from existing ones where default gateway will be taken from. Selection should
be environment-wide for the first stage.
See https://bugs.launchpad.net/fuel/+bug/1502939

8. (Nice to have) Assignment of VIP for network managed by dhcp. It is about
Admin network. When some network role that requires VIP is mapped to Admin
network, IP address should be excluded from Admin networks' IP ranges
(i.e. from DHCP ranges). This can be done manually.
This should enable all-services-in-one-network scheme.

Web UI
======

GUI tasks are to be in separate ticket/spec.

Nailgun
=======

Task 1.
a. The "update_dnsmasq" task will be added to serve auto setup of dnsmasq on
master node. This Nailgun task will "upload_file", "puppet" and "cobbler_sync"
orchestrator tasks to update dnsmasq configuration.
b. Nailgun will run that task when some of IP ranges of Admin networks are
changed via API.
c. Nailgun API validator will check new Admin IP ranges against IPs of nodes
currently visible to Fuel (bootstrap and deployed ones). Also, Nailgun will
check IPS of newly added nodes against Admin IP ranges and mark nodes with
errors if they are out of known Admin IP ranges.

Task 2.
a. New Nailgun task will be added to rerun networking configuration on deployed
nodes (or deployment tasks graph will be rebuilt).
b. Deployment data for deployed nodes will be regenerated when required.
c. Controller nodes maybe triggered for redeploy when required.

Task 3.
a. VIPs addresses assignment should be reworked to determine the node network
group where VIP address should be allocated (using node roles and network role
from VIP description). Now the node network group that contains controllers is
always taken for assgnment of VIPs.
b. Nailgun should check that each VIP address should belong to exactly one 
nodegroup.

Task 4.
a. Validation of network parameters (NetworkCheck class methods) should allow
intersection of CIDRs and gateways (simultaneously only) of several networks
with the same name from different (not the same) node network groups. In case
of such intersection those networks are considered as one shared network and no
routes should be generated between segments.
b. Validation of network parameters (NetworkCheck class methods) should allow
equal VLAN IDs within environment. Exception is that every single network
interface cannot handle coincident VLAN IDs.

Task 5.
a. Setting of VIP addresses will be allowed together with change of other
networking parameters via urls:
/clusters/<cluster_id>/network_configuration/neutron/,
/clusters/<cluster_id>/network_configuration/nova_network/.
VIPs are returned there now by GET request. It will be possible to set them via
PUT request. VIPs addresses should be changed in 'vips' dict to be accepted by
API.
b. User-defined VIP addresses may match some networks known by Fuel or do not
match any known networks. Anyway, VIP address provided is saved into DB as
occupied. So, it cannot be used for other purposes.
c. To cancel manual address setup for particular VIP, user should set it to
'null' in network configuration YAML file ('None' in JSON) and run the same API
PUT request.

Task 6.
a. Change the verification of floating ranges to allow floating range to match
any of Public networks in environment. Now it may only match Public network
from default node network group.
b. Change the serialization of floating network to find appropriate Public
network for floating ranges defined.

Task 7.
a. Add a environment-wide (for the first stage) selector of network from
existing ones where default gateway will be taken from. Add it into attributes
of environment (Settings tab).
b. Serialize default gaeways on nodes according to that selection.

Task 8.
a. IP ranges of Admin networks should automatically be modified so that they do
not include VIP addresses which were set by user. Such request for VIP address
changing will be rejected if desired VIP address matches any known node's
address.

Data model
----------

Task 1.
New task name and new node error type will be added.

Task 5.
Some new properties can be added into IPAddress (to distinguish
user-defined VIP address).

Task 7.
New editable attributes (to Release) will be added to be shown on Settings tab.

REST API
--------

Data formats remain the same. Flow for network configuration is changed for
Task 5.

Orchestration
=============

TBD

RPC Protocol
------------

TBD

Fuel Client
===========

TBD

Plugins
=======

None

Fuel Library
============

TBD

------------
Alternatives
------------

This feature can be treated as a composition of several smaller changes. Seems,
all of them can be implemented separately. But some tasks have dependences:
8 depends on 1 and 5, 


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

TBD

---------------
End user impact
---------------

TBD

------------------
Performance impact
------------------

N/A

-----------------
Deployment impact
-----------------

Discuss things that will affect how you deploy and configure Fuel
that have not already been mentioned, such as:

* What configuration options are being added? Should they be more generic than
  proposed? Are the default values ones which will work well in
  real deployments?

* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

* If this change is a new binary, how would it be deployed?

* Please state anything that those doing continuous deployment, or those
  upgrading from the previous release, need to be aware of. Also describe
  any plans to deprecate configuration values or features.  For example, if a
  directory with instances changes its name, how are instance directories
  created before the change handled?  Are they get moved them? Is there
  a special case in the code? Is it assumed that operators will
  recreate all the instances in their cloud?


----------------
Developer impact
----------------

None

--------------------------------
Infrastructure/operations impact
--------------------------------

Explain what changes in project infrastructure will be required to support the
proposed change. Consider the following:

* Will it increase the load on CI infrastructure by making build or test jobs
  consume more CPU, network, or storage capacity? Will it increase the number
  of scheduled jobs?

* Will it require new work-flows or changes in existing work-flows implemented
  in CI, packaging, source code management, code review, or software artifact
  publishing tools?

  * Will it require new or upgraded tools or services to be deployed on project
    infrastructure?

  * Will it require new types of Jenkins jobs?

  * Will it affect git branch management strategies?

  * Will it introduce new release artifacts?

* Will it require changes in build environments of any existing CI jobs? Would
  such changes be backwards compatible with previous Fuel releases currently
  supported by project infrastructure?


--------------------
Documentation impact
--------------------

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.


--------------------
Expected OSCI impact
--------------------

Expected and known impact to OSCI should be described here. Please mention
whether:

* There are new packages that should be added to the mirror

* Version for some packages should be changed

* Some changes to the mirror itself are required


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
- It should be allowed to set user-defined IP for any VIP. This IP can even be
  out of any environment's networks.
- Make it possible to set floating IP range from non-default node network
  group.
- It should be possible to select any network from existing ones where default
  gateway will be taken from.
- There is a special case when network managed by dhcp (PXE network) needs VIPs
  to be assigned. IP addresses should be excluded from Admin networks' IP
  ranges (i.e. from DHCP ranges). (Nice to have).


Dependencies
============

N/A

------------
Testing, QA
------------

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly.

If there are firm reasons not to add any other tests, please indicate them.


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
- It should be allowed to set user-defined IP for any VIP. This IP can even be
  out of any environment's networks.
- Make it possible to set floating IP range from non-default node network
  group. So, it will be possible to deploy controller nodes in any node group.
- It should be possible to select any network from existing ones where default
  gateway will be taken from.
- There is a special case when network managed by dhcp (PXE network) needs VIPs
  to be assigned. IP addresses should be excluded from Admin networks' IP
  ranges (i.e. from DHCP ranges). (Nice to have).

----------
References
----------

https://blueprints.launchpad.net/fuel/+spec/l3-multiple-racks
