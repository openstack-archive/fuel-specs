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
specified by operator.

This behaviour prevents us to add useful things like fine-grained resource
allocation for virtual machines and makes our way harder to implement complex
and demanded things like heterogeneous cloud and support for multiple vCenter
servers managed by single Mirantis OpenStack environment.

Single nova-compute instance also acts as single point of failure.  If service
fails for some reason whole cloud loses its compute resources.  If we are
running multiple nova-compute instances, in case of failure of single instance
cloud still has place where to run virtual machines.

It is good to mention that now user does not have an opportunity to select in
which vSphere cluster virtual machine will be running, currently it happens
automatically and is controlled by nova-scheduler logic.  Implementation of 1-1
mapping might allow us to implement more manageable way of starting virtual
machines.

This change will allow us implement addition of vSphere clusters to deployed
Mirantis OpenStack environment.

Proposed change
===============

We need to map one nova-compute to one vSphere cluster.

We must implement following functionality in our web UI: add an opportunity for
operator to specify different credentials for different vSphere clusters.  It
is not possible to allow different nova-compute instances use same login and
password to connect to one vCenter, due to internal vCenter server limitations
that do not allow connect to same vCenter from different places.


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


Alternatives
------------

We can leave things as they work right now: single nova-compute instance
utilizes multiple vSphere clusters that are specified in */etc/nova/nova.conf*.

Alternative solution to the problem would be rewriting */etc/nova/nova.conf*
with additional vSphere cluster names and restarting nova-compute service.

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

None.


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


Dependencies
============

None.


Testing
=======

New system tests will be provided for proposed functionality.


Documentation Impact
====================

Screenshots must be updated to reflect changes on web UI.
Section that describes how add vSphere clusters to running Mirantis OpenStack
environment.

Changes to Reference architecture must be reflected in documentation.


References
==========

