==========================================
VLAN manager support for vCenter
==========================================

https://blueprints.launchpad.net/fuel/+spec/vcenter-vlan-manager

Now, in a 5.0 and 5.1 releases Fuel doesn't support Nova-Network in VLANmanager
mode for vCenter as a hypervisor. We want to add this feature in Fuel 6.0.


Problem description
===================

Nova-network can run in several modes,  but only FlatDHCPManager works properly
with vCenter now. In this case all virtual machines (even used by different
tenants) are contained in one L2 broadcast domain. Also only one pool of ip
addresses is used for all tenants. It is a problem for security and
scalability.


Proposed change
===============

We can avoid problems which were described in the previous point by using vlan
technology. Thereafter fuel-clouds will meet the needs of huge enterprise
deployment.

To fully support VlanManager the following changes must be implemented:

* Unlock 'VLAN Manager' --- element of UI on the Networks tab for choosing this
  variant of networking mode.

* Provide correct configuration to nova-network service for managing
  portgroups, vlans and networks as described in [1].

This is the principle scheme of deployment configuration:

::
 		     	                                                          
		     	                      +---------------------+             
     		     	                      |    ESXi1            |             
       	       	     	                      | +-----+             |             
               	     	                      | | VM1 +--+          |             
       	       	     	                      | +-----+  | +------+ |vlan 100
       	       	     	                      |          +-+-br100+-+---------|
       	       	     	                      | +-----+  | +------+ |	      |
       	       	     	                      | | VM2 +--+          |	      |
       	       	     	                      | +-----+             |	      |
       	       	     	                      |                     |	      |
       	       	     	                      | +-----+             |	      |
                     	                      | | VM5 +--+          |	      |
                       	                      | +-----+  | +------+ |vlan 103 |
  +---------------------+  +---------+        |          +-+-br103+-+-------+ |
  | Controller node 	|  | VMware  |        | +-----+  | +------+ |	    | |
  |   	             	|  | vCenter | +------+ | VM6 +--+          |	    | |
  |  +----------------+ |  |         | |      | +-----+             |	    | |
  |  |nova-compute    |	|  |         | |      +---------------------+	    | |
  |  |services        +----+         +-+				    | |
  |  |+-------------+ |	|  |         | |  +---------------------------------| |
  |  ||nova-network + |	|  |         | |  |   +---------------------+	    | |
  |  ||             + |	|  |         | +--o---+    ESXi2            |	    | |
  |  |+----+----+---+ |	|  |         |    |   | +-----+             |	    | |
  |  +-----|----|-----+	|  +---------+    |   | | VM7 +--+          |	    | |
  +--------|----|-------+                 |   | +-----+  | +------+ |	    | |
	   |	|      	       	       	  |   |          +-+-br103+-+-------| |
       	   |    +-------------------------+   | +-----+  | +------+ |	      |
	   |	     	                      | | VM8 +--+          |	      |
	   |	     	                      | +-----+             |	      |
	   |	     	                      |                     |	      |
	   |	     	                      | +-----+             |	      |
	   |	     	                      | | VM3 +--+          |	      |
	   |	     	                      | +-----+  | +------+ |	      |
	   |	     	                      |          +-+-br100+-+---------+
	   |	     	                      | +-----+  | +------+ |	      |
	   |	     	                      | | VM4 +--+          |	      |
	   |	     	                      | +-----+             |	      |
	   |	     	                      +---------------------+	      |
	   |								      |
	   +------------------------------------------------------------------+

   
Alternatives
------------

Using FlatDHCPManager mode of nova-network or neutron networking.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

None

Security impact
---------------

Because in this mode virtual machines from different tenants work in different
L2 segments, security of environment will be increased by this changes.

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

Some network performance improvement is awaited due to segregating virtual
machines into different broadcast domains. This effect will be increased with
growth of cloud and amount of virtual machines.

Other deployer impact
---------------------

Because this technology is based on vlan tagging before deploy you need to make
sure, that your switch supports 802.1q standard.

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee: igajsin (Igor Gajsin)

Feature Lead: gcon-monolake (Andrey Danin)

QA: tdubyk (Tatyana Dubyk)

Documentations: ipovolotskaya (Irina Povolotskaya)

Work Items
----------

* Unlock UI element to enable 'VLAN Manager' option.

* Understand how it works.

* Make changes manually.

* Write puppet manifests.


Dependencies
============

None


Testing
=======

* Perform manual acceptance testing of this feature to verify that with Vlan
  Manager we can create environment that will pass network connectivity.

* Check that all ostf tests, which are linked with network connectivity will
  be passed.

Documentation Impact
====================

Fuel documentation which describes networking in vCenter based deployment must
be rewritten with taking into account new features:

* New work mode of nova-network.

* New UI with unlocked element.

* How to configure network interfaces on controller node according to
  configuration of vCenter and ESXi-hosts must have a detailed description.

References
==========

[1] http://docs.openstack.org/grizzly/openstack-compute/admin/content/vmware.html#VMWare_networkin
