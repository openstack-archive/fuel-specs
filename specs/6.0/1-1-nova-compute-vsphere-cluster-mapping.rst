..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
1-1 mapping between nova-compute and vSphere cluster
====================================================

https://blueprints.launchpad.net/fuel/+spec/1-1-nova-compute-vsphere-cluster-mapping

Problem description
===================

Currently an only nova-compute service instance utilizes all vSphere clusters
(clusters that are formed by ESXi hosts) managed by a single vCenter server
which is specified by a user. This behaviour prevents a user to specify a
vSphere cluster he or she wants to run a VM instance at. Now that decision
happens automatically and is controlled by nova-scheduler logic and vCenter
DRS logic.

Also, Fuel cannot add vSphere clusters to an already deployed environment on
the fly, but there are customers, who want it.

A single nova-compute service instance also acts as a single point of failure,
even we defend it with Pacemaker. If the service fails for some reason a whole
cloud loses an access to compute resources.

Also, VMWare itself recommends to avoid 1-M mapping between a nova-compute
service and vSphere clusters.

Proposed change
===============

Launch multiple instances of nova-compute service and map each nova-compute to
a single vSphere cluster.  Nova-compute services will be running on OpenStack
controller nodes like it does now. We are not proposing creation of a separate
compute node for each nova-compute.

::

 +--------------------+
 |                    |
 | OSt controller     |
 |                    |
 |+------------------+|       +------------------+       +-------------------+
 ||                  ||       |                  |       |                   |
 ||  nova-compute-1  +--------+ - - - - - - - - -+-------+ vSphere cluster 1 |
 ||  (login1/pass1)  ||       |                  |       |                   |
 ||                  ||       |                  |       +-------------------+
 |+------------------+|       |                  |
 |                    |       |                  |
 |+------------------+|       |  vCenter server  |       +-------------------+
 ||                  ||       |                  |       |                   |
 ||  nova-compute-2  +--------+ - - - - - - - - -+-------+ vSphere cluster 2 |
 ||  (login2/pass2)  ||       |                  |       |                   |
 ||                  ||       |                  |       +-------------------+
 |+------------------+|       |                  |
 |                    |       |                  |
 |+------------------+|       |                  |       +-------------------+
 ||                  ||       |                  |       |                   |
 ||  nova-compute-N  +--------+ - - - - - - - - -+-------+ vSphere cluster N |
 ||  (loginN/passN)  ||       |                  |       |                   |
 ||                  ||       |                  |       +-------------------+
 |+------------------+|       +------------------+
 +--------------------+

Add an opportunity for user to specify different credentials for different
vSphere clusters.  It is not possible to allow different nova-compute instances
use same login and password to connect to one vCenter, due to internal vCenter
server limitations that do not allow connect to same vCenter from different
places.

It seems that a separate tab would be needed for entering vSphere cluster names
and credentials for each vSphere cluster.  UI must allow a user to add more
vSphere clusters after the deployment is done.  But it would be not possible to
remove existing vSphere clusters.

In order to simplify Puppet manifests execution and to support the 'granular
deployment' feature in some way it will be good to add a new role
'vmware-compute'. It will allow us to add a support of heterogeneous clouds
(cloud that runs on top of multiple hypervisors simultaneously) in future.


Alternatives
------------

We can leave things as they work right now: single nova-compute instance
utilizes multiple vSphere clusters that are specified in
*/etc/nova/nova-compute.conf*.

Alternative solution to the problem would be rewriting
*/etc/nova/nova-compute.conf* with additional vSphere cluster names and
restarting nova-compute service.

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

vCenter settings block on Settings tab should be moved to separate tab (e.g.
'vCenter').  On this tab operator will be able to configure and specify vSphere
clusters.

Performance Impact
------------------

Controller node will be running number of nova-compute processes as number of
specified vSphere clusters.  Maximum number of hosts that are supported by
vCenter is 1000, it means that each host can form a cluster of itself, so
maximum number of nova-compute instances might raise to 1000.
(http://www.vmware.com/pdf/vsphere5/r55/vsphere-55-configuration-maximums.pdf).
So controller must be able to run additional 1000 processes.

There is a limit on number of concurrent vSphere connections to vCenter (100
and 180 for vSphere Web Client).  Some nova-computes connections must scheduled
across timeline.

Other deployer impact
---------------------

Separate role will be introduce (e.g. 'vmware-controller').


Developer impact
----------------

None.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Andrey Danin <adanin@mirantis.com>
  Igor Zinovik <izinovik@mirantis.com>

Work Items
----------

- Modify web UI that way so it would allow user to add multiple vSphere
  clusters with different credentials.
- Modify puppet manifests that will create multiple nova-compute instances in
  simple deployment mode.  Create appropriate configuration file for each
  nova-compute instance with different credentials for vCenter.
- Modify puppet manifests that will creates multiple pacemaker nova-compute
  resources in HA deployment mode.  Create one nova-compute resource and
  corresponding configuration file per one vSphere cluster.
- Move vCenter settings block from Settings tab to separate 'vCenter' tab for
  environment that uses vCenter as hypervisor option.
- Add UI control on the vCenter tab that would allow user to dynamically add
  new vSphere clusters (you may consider IP ranges implementation on the
  Networks tab).
- Reference architecture in our documentation must be updated and reflect
  implementation of this specification.


Dependencies
============

None.


Testing
=======

New system tests will be provided for proposed functionality.


Documentation Impact
====================

Proposed change modifies Reference Architecture. All vCenter related sections
must be reviewed and updated.  Screenshots must be updated to reflect changes
on web UI.  Section that describes how to add vSphere clusters to running
Mirantis OpenStack environment must be added.



References
==========

