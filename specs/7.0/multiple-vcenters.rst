..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Support multiple vCenters in one environment
============================================

https://blueprints.launchpad.net/fuel/+spec/multiple-vcenters

An environment deployed by Fuel should be able to operate with multiple
vCenters as hypervisors.


Problem description
===================

Currently Fuel only supports single vCenter in one environment. Support for
multiple vCenter in one environment to avoid the effect of bottleneck when
heavy API use is required and solve the problem of scalability. Starting
from here and below mentioning of 'nova-compute' term we implicitly consider
that service is configured with VCDriver.


Proposed change
===============


In the current version of the Fuel (with support for one vCenter) integration
with vSphere is as follows:

 .. image:: ../../images/7.0/multiple-vcenters/with-single-vcenter.png
    :width: 100 %

Some explanation of the scheme (Multi-node HA Deployment with single vCenter):

* nova-compute and nova-network run under HA (Pacemaker).
* for each cluster vCenter runs nova-compute [3]_.
* cinder-vmware (volume) [2]_ is run on each node (not on HA), which is
  assigned the role of cinder-vmware [2]_.
* Of all the clusters vCenter we form an availability zone. 

After the implementation of this blueprint, vCenter integration scheme would
be:

 .. image:: ../../images/7.0/multiple-vcenters/with-multiple-vcenters.png
    :width: 100 %

Some explanation of the scheme (Multi-node HA Deployment with multiple
vCenters):

* in Fuel 7.0 nova-network will not be supported. For the vCenter will be used
  Neutron.
* nova-compute and neutron networking run under HA (Pacemaker).
* for each cluster vCenter runs nova-compute [3]_.
* for each vCenter runs (not on HA) cinder-vmware (volume) [2]_ on each node,
  which is assigned the role of cinder-vmware [2]_. So that for each vCenter
  using a separate cinder-volume (VMDK backend).
* Each vCenter with all its clusters forms separate availability zones.

Because Glance currently supports a single store per scheme [1]_, user must
decide which vCenter (only one) it will be used as a Glance backend [5]_.

To accomplish this blueprint it is necessary to make the following changes:

* It is necessary to make changes to the Fuel Web UI (VMware tab). The
  settings for each vCenters will be in subtabs [0]_.
* Glance (vSphere backend) [5]_ settings will also be moved in subtab
  (VMware tab). It is worth noting that the user will still be able to
  configure only one vCenter, as a backend Glance, due to limitations
  Glance [1]_.
* Testing and writting (if needed) puppet manifest for support multiple
  vCenters:

  * nova-compute [3]_
  * availability zones
  * cinder-vmware [2]_
* Testing and writting (if needed) puppet manifest for support multiple
  vCenters:

  * neutron networking
* Amend OSTF for testing each availability zone.

Alternatives
------------

Leave it as-is. We will be limited to using a single vCenter, this will limit
our ability to deploy large-scale environments.

Data model impact
-----------------

Nailgun should be able to serialize multiple vCenters and pass it into
astute.yaml file:

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
      - datastore_regex: "openstack-.*"
        service_name: cluster2
        availability_zone_name: vcenter
        vc_cluster: Cluster2
        vc_host: 172.16.0.254
        vc_password: Qwer!1234
        vc_user: administrator@vsphere.local
      - datastore_regex: "openstack-.*"
        service_name: cluster1
        availability_zone_name: vcenter2
        vc_cluster: Cluster1
        vc_host: 172.16.0.253
        vc_password: Qwer!12345
        vc_user: administrator@vsphere.local
      - datastore_regex: "openstack-.*"
        service_name: cluster2
        availability_zone_name: vcenter2
        vc_cluster: Cluster2
        vc_host: 172.16.0.253
        vc_password: Qwer!12345
        vc_user: administrator@vsphere.local
   cinder:
     instances:
     - availability_zone_name: vcenter
       vc_password: Qwer!1234
       vc_host: 172.16.0.254
       vc_user: administrator@vsphere.local
     - availability_zone_name: vcenter2
       vc_password: Qwer!12345
       vc_host: 172.16.0.253
       vc_user: administrator@vsphere.local

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

* The user can add vCenters in subtabs [0]_ (VMware tab).
* The user can specify the Glance (vSphere backend) [5]_ settings in
  subtab [0]_ (VMware tab). The user must decide which vCenter it will
  be used as a Glance backend [5]_ , due to limitations Glance [1]_.

Performance Impact
------------------

None.

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

Fuel web UI impact
~~~~~~~~~~~~~~~~~~

Specification requires changes in Fuel Web UI interface in order to provide
desired user experience.

Nailgun impact
~~~~~~~~~~~~~~

Deployment serializer must pass multiple vCenters attributes to orchestrator.

Infrastructure impact
---------------------

* These changes increase the number of scheduled CI jobs. The exact number of
  CI jobs will determine QA team.
* Need to create a multiple vCenters lab.


Implementation
==============

Assignee(s)
-----------

======================= =============================================
Primary assignee        Alexander Arzhanov <aarzhanov@mirantis.com>
Developers              Alexander Arzhanov <aarzhanov@mirantis.com>
                        Anton Zemlyanov <azemlyanov@mirantis.com>
QA engineers            Olesia Tsvigun <otsvigun@mirantis.com>
Mandatory design review Andrey Danin <adanin@mirantis.com>
                        Igor Zinovik <izinovik@mirantis.com>
======================= =============================================

Work Items
----------

* Implement subtabs [0]_ in Fuel Web UI for vCenters and Glance [5]_ on the
  VMware tab.
* Testing and writting (if needed) puppet manifest for support multiple
  vCenters:

  * nova-compute [3]_
  * availability zones
  * cinder-vmware [2]_
* Testing and writting (if needed) puppet manifest for support multiple
  vCenters:

  * neutron networking
* Amend OSTF for testing each availability zone.


Dependencies
============

* Fuel plugin for Neutron ML2 Driver For VMWare vCenter DVS [7]_.
* Deploy nova-compute (VCDriver) as standalone role [6]_.
* Fuel Plugin for NSX-V support [8]_, if it declared support multiple
  vCenters.


Testing
=======

Minimum testing is to test the deploy Dual hypervisor mode [9]_ and check
network connection between VM's from different availability zones. This
testing should be performed for each network backend:

* Neutron ML2 Driver For VMWare vCenter DVS [7]_.
* NSX-V support [8]_ (if it declared support multiple vCenters).

Minimal testing might look like this:

* Create cluster with vCenter support.
* Add 3 nodes with Controller roles.
* Add 2 nodes with compute role.
* Deploy the cluster.
* Run network verification.
* Run OSTF.
* Create 2 VMs on each availability zones.
* Verify that VMs on different availability zones should communicate between
  each other.

Acceptance criteria
-------------------

User is able to deploy cluster with support multiple vCenters.
After deploy user must use availability zone for each vCenters for create VMs.


Documentation Impact
====================

The documentation should describe:

* VMware vSphere integration (multiple vCenters architecture).
* how to setup multiple vCenters (VMware tab), move Glance settings in subtab
  (VMware tab).
* network topology for multiple vCenters.


References
==========

.. [0] https://blueprints.launchpad.net/fuel/+spec/fuel-ui-settings-subtabs
.. [1] https://blueprints.launchpad.net/glance/+spec/multi-store
.. [2] https://blueprints.launchpad.net/fuel/+spec/cinder-vmdk-role
.. [3] https://blueprints.launchpad.net/fuel/+spec/1-1-nova-compute-vsphere-cluster-mapping
.. [4] https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings
.. [5] https://blueprints.launchpad.net/fuel/+spec/vsphere-glance-backend
.. [6] https://blueprints.launchpad.net/fuel/+spec/compute-vmware-role
.. [7] https://github.com/stackforge/fuel-plugin-vmware-dvs/blob/master/specs/spec.rst
.. [8] https://github.com/openstack/vmware-nsx
.. [9] https://blueprints.launchpad.net/fuel/+spec/vmware-dual-hypervisor
