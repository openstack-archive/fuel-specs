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

Currently single nova-compute service instance utilizes all vSphere clusters
(clusters that are formed by ESXi hosts) managed by a single vCenter server
which is specified by a user. This behaviour prevents user to specify a
vSphere's cluster on which user may launch a VM instance at. Now that decision
happens automatically and is controlled by nova-scheduler logic and vCenter
DRS logic.

::

  +--------------------+       +------------------+       +-------------------+
  |                    |       |                  |       |                   |
  |  OSt controller    |       |  vCenter server  |       |  Sphere cluster 1 |
  |                    |       |        +- - - - -+-------+                   |
  |                    |       |                  |       +-------------------+
  |                    |       |        |         |
  ++------------------++       |                  |       +-------------------+
  ||                  ||       |        |         |       |                   |
  ||   nova-compute   |--------+ - - - -+- - - - -+-------+  Sphere cluster 2 |
  ||                  ||       |        |         |       |                   |
  ||                  ||       |                  |       +-------------------+
  ++------------------++       |        |         |
  |                    |       |                  |       +-------------------+
  |                    |       |        |         |       |                   |
  |                    |       |        +- - - - -+-------+  Sphere cluster N |
  |                    |       |                  |       |                   |
  +--------------------+       +------------------+       +-------------------+


Also, Fuel cannot add vSphere clusters to an already deployed environment on
the fly, but there are customers, who want it. 1 nova-compute-many clusters is
a part of the other problem when it comes to addition of a new cluster. Another
part of the problem is the fact that nova-compute runs on Controller nodes,
when vCenter is used as hypervisor. And Fuel allows to extend the working
cluster only by adding new nodes, not roles.

A single nova-compute service instance also acts as a single point of failure,
even if we defend it with Pacemaker. If the service fails for some reason a
whole cloud loses access to compute resources.

Also, VMware itself recommends to avoid 1-M mapping between a nova-compute
service and vSphere clusters.

Proposed change
===============

Launch multiple instances of nova-compute service and map each nova-compute to
a single vSphere cluster.  Nova-compute services will be running on OpenStack
controller nodes like it does now. We are not proposing creation of a separate
compute node for each nova-compute, because it requires us to configure
additional pacemaker group that will backup nova-compute services on those
compute nodes. It also requires customer procure additional hardware to run
additional nova-compute process which might be unacceptable.

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

A separate tab would be needed for entering vSphere cluster names and
credentials for each vSphere cluster.  UI must allow a user to add more vSphere
clusters after deployment is done, e.g. user deployed Mirantis OpenStack
integrated with vCenter, after some time additional hardware was purchased and
new vSphere clusters were formed.  User should be able to add these new
clusters to existing OpenStack installation without environment redeployment.
Right now our web UI does not allow leave some parts of tab unlocked, it locks
all tab elements after successful deployment, that is why we need separate tab.

This specification does not cover removal of clusters from existing
environment.

In order to simplify Puppet manifests execution and to support the 'granular
deployment' feature[0] in some way it will be good to add a new role
'vmware-compute'. It will allow us to add a support of heterogeneous
environments (cloud that runs on top of multiple hypervisors simultaneously) in
future.  Heterogeneous environment will allow user to use KVM/QEMU and vCenter
simultaneously in single environment.

[0] https://blueprints.launchpad.net/fuel/+spec/granular-deployment-based-on-tasks

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

End users workflow may be affected as interface of system will be changed so
adequate documentation must be provided for them.

Performance Impact
------------------

Controller node will be running number of nova-compute processes as number of
specified vSphere clusters.  Maximum number of hosts that are supported by
vCenter is 1000, it means that each host can form a cluster of itself, so
in worst case maximum number of nova-compute instances might raise to 1000.
(http://www.vmware.com/pdf/vsphere5/r55/vsphere-55-configuration-maximums.pdf).
So controller must be able to run additional 1000 processes.

There is a limit on number of concurrent vSphere connections to vCenter (100
and 180 for vSphere Web Client).  Some nova-computes connections must scheduled
across timeline.

Other deployer impact
---------------------

Separate role will be introduce (e.g. 'vmware-compute').


Developer impact
----------------

Fuel web UI team help is needed in aspects of implementing separate tab.


Implementation
==============

Assignee(s)
-----------

Drafter:
  Igor Zinovik (izinovik)

Primary assignee:
  Andrey Danin (gcon-monolake)
  Igor Zinovik (izinovik)

Reviewer:
  Andrey Danin (gcon-monolake)
  Evgeniya Shumakher (eshumakher)

QA:
  Tatiana Dubyk (tdubyk)

Work Items
----------

#. Modify web UI that way so it will allow user to add multiple vSphere
   clusters with different credentials.

#. Modify puppet manifests that will create multiple nova-compute instances in
   simple deployment mode.  Create appropriate configuration file for each
   nova-compute instance with different credentials for vCenter.

#. Modify puppet manifests that will creates multiple pacemaker's nova-compute
   resources in HA deployment mode.  Create one nova-compute resource and
   corresponding configuration file per one vSphere cluster.

#. Move vCenter settings block from the Settings tab to separate 'vCenter' tab
   for environment that uses vCenter as hypervisor option.  On this tab
   operator will be able to configure and specify vSphere clusters.

#. Add UI control on the vCenter tab that would allow user to dynamically add
   new vSphere clusters (you may consider IP ranges implementation on the
   Networks tab).

#. Reference architecture in our documentation must be updated and reflects
   implementation of this specification.


Dependencies
============

None.


Testing
=======

Manual testing using checklists according to acceptance criteria below.

Acceptance Criteria:

Stage I:

- User should be able to add multiple vSphere's clusters with different
  credentials through Fuel UI;
- User should be able to add vSphere's clusters on already deployed
  environment;
- Check that using Fuel UI user has ability to add more vSphere's clusters
  after the deployment is done, but it wouldn't be possible for him to remove
  existing vSphere's clusters.

Stage II:

- Verify that in Fuel UI added separate tab for vCenter's settings and that
  they work correctly;
- Verify that "vmware-compute" role will work correctly with another roles and
  according to specification of this feature.

Stage III:

- Verify recommendations, which have been described in 'Performance impact'
  section
- Verify that puppet's manifests have been updated according to features'
  descriptions in this document.


Documentation Impact
====================

Proposed change modifies Reference Architecture. All vCenter related sections
must be reviewed and updated.  Screenshots must be updated to reflect changes
on web UI.  Section that describes how to add vSphere clusters to running
Mirantis OpenStack environment must be added.


References
==========

