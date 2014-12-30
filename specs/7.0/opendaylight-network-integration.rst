..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Integration of ODL mechnisim driver and OpenDaylight with Neutron
===============================

https://blueprints.launchpad.net/fuel/+spec/opendaylight-network-integration

Fuel will be able to deploy Openstack with OpenDayligh SDN Controller and
Neutron configured to use the ML2 plugin with the ODL mechinism driver.

Problem description
===================

For teleco customers, Neutron networking alone is not sufficent, and many
operators are considering deploying a dedicated SDN solution such as OpenContrial
or OpenDaylight.  The OPNFV group are specifically focusing on creating a reference 
implmentation based on Openstack and OpenDaylight (ODL).
 
Since the icehouse release of Openstack the ODL driver has been included in
the Openstack distribution.

The problem is that when Fuel provisions the networks it sets up the admin, public, management, storage networks all on OpenvSwitch (using bridges and ports).  ODL works by managing the OpenvSwitches, but as the management interface is on the Openvswitch communication breaks down when setting the ovs manager on compute nodes.

Compare this to RDO, RHOS or devstack, where Openvswitch is only used for the data (private) networks.

Proposed change
===============

After the blueprints [0] and [1] mentioned above would be implemented, there
will be a possibility to enable both features deployed simultaneously. It's
mostly an administrative work needed because all the manifests will be ready,
and we need just to allow a simultaneous use of the features somewhere in
Release description.

Include OpenDaylight in the packages to be installed on the controller.  By default ODL uses some ports that conflict with swift (8080).  These would need updated if swift was used.

The modules that take care of setting up networking would have to configure the management interface outside of openvswitch, so that the controller node can manage remote vswitches.

Alternatives
------------

N/A

Data model impact
-----------------

No data models modifications needed.

REST API impact
---------------

No REST API modifications needed.

Upgrade impact
--------------

The ODL controller is a seperate release from Openstack.  One option maybe to have a seperate ODL controller deployed, prior to setting up Openstack, although many people are deploying the SDN controller on the Openstack controller nodes.

Security impact
---------------

No additional security modifications needed.

Notifications impact
--------------------

None.

Other end user impact
---------------------

None.

Performance Impact
------------------

None.

Other deployer impact
---------------------

Changes to puppet modules, to setup networking as reuired.
Additional modules required for the installation of Open Daylight.


Developer impact
----------------


Implementation
==============

Assignee(s)
-----------

Primary assignee:

Other contributors:

Work Items
----------


Dependencies
============

Testing
=======

Acceptance Criteria:
* No noticable impact to the deployment after provisioning.  User should be able to
    create networks, without interacting with ODL
* ODL DLUX dashboard should be available and show the deployment.

Documentation Impact
====================

A reference architecture of the feature should also be described.


References
==========

http://www.opendaylight.org/
