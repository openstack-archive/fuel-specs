..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================================
Use vSphere Datastore backend for Glance with vCenter
=====================================================

https://blueprints.launchpad.net/fuel/+spec/vsphere-glance-backend

Fuel will be able to deploy OpenStack with vSphere Datastore support as glance
backend.

Problem description
===================

Fuel doesn't support deployment with vSphere Datastore as glance backend, but
OpenStack already supports this feature. [0]
For users using vmware vCenter/ESX, it would be great and comfortably(for
simplicity of administration) to store openstack data(images, disks, etc.)
in vCenter/ESX storages.

Proposed change
===============

Add this case in puppet manifetst and add "vsphere" option for Glance backend
and disable Swift installation in HA mode.
Add options to connect to this backend in UI:
* In wizard in Storage Backends add vCenter/ESX button for Glance.

* In Setting tab in Storage section add vCenter/ESX connetion options fields.

  * You can also use ESX host as Glance backend by setting "ha-datacenter" in
    the "Datacenter name" field.

Alternatives
------------

None

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

None

Notifications impact
--------------------

None

Other end user impact
---------------------

User must choose in wizard vCenter/ESX type backend for Glance.
And to fill the connection settings in Setting tab in Storage section.

Performance Impact
------------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  srogov (Stepan Rogov)

Other contributors:
  None

Work Items
----------

* Set up the dev environment with one vCenter.
* Writing puppet modules.
* Writing UI enhancements.
* Testing.

Dependencies
============

https://blueprints.launchpad.net/glance/+spec/vmware-datastore-storage-backend

Testing
=======

Perform manual acceptance testing according to acceptance criteria below:
Acceptance criteria:
1. To verify that user can create environment with CentOS or Ubuntu in simple
or HA mode with different roles and to use as image storage - Glance with
VMDK backend. For this in Fuel UI must be in Storages section 2 new options:

   - vmware vcenter/esxi datastore for images(Glance)
   - esxi datastore for images (Glance)

2. User should have ability to upload OS image on VM in vmdk format or in
iso format.

3. User can ensure that generated snapshot from VM with different size can be
successfully copied into glance that in our case placed inside
vCenter's Datastore.

4. OSTF tests according this feature must be passed.

Documentation Impact
====================

The documentation should describe how to set up vCenter data stores for the
Image Service backend.

References
==========

[0] http://docs.openstack.org/trunk/config-reference/content/vmware-glance-backend.html

https://blueprints.launchpad.net/glance/+spec/vmware-datastore-storage-backend

http://docs.openstack.org/trunk/config-reference/content/vmware-glance-backend.html
