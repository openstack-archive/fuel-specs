..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
VMware UI Settings Tab for FuelWeb
==========================================

https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings

VMware vCenter settings are currently available on Settings tab, it
does not allow dynamic addition/removal of settings and is already big
enough. The vCenter functionality will be moved to a separate Cluster tab
of the Fuel web UI to provide better user experience.

Problem description
===================

VMware settings have the following problems in the FuelWeb UI implementation:

* It is impossible to have different vCenter clusters for nova-compute
  and Cinder/Glance services

* There is no way of adding multiple vCenter clusters for nova-compute or
  other services.


Proposed change
===============

Add the VMware tab on the Cluster page with all the related settings. The
settings are separated into vCenter, Network, and Glance Groups [1].

User Interface
--------------------------------------------------------------------------

::

  vCenter:
  --------
  Availability zone:  ______________  (description)
  vCenter Host:       ______________  (description)
  vCenter Username:   ______________  (description)
  vCenter Password:   ______________  (description)
    Nova Computes: (multiple instances allowed)
    --------------
    Name of service:    ______________  (description)
    vCenter Cluster:    ______________  (description)
    Datastore regex:    _______________ (description) OPTIONAL
    Cinder:
    -------
    [x] Enable Cinder VMDK
    Data Center:     ________________  (description)

  Glance:
  -------
  [x] Enable Glance
  vCenter Host:    ______________  (description)
  vCenter Username:______________  (description)
  vCenter Password:______________  (description)
  Datacenter name: ______________  (description)
  Datastore name:  ______________  (description)
  Directory for images: _________  (description) OPTIONAL

  Network:
  --------
  ESXi VLAN Inerface: _____________ (description)

Alternatives
------------

Alternatively, the VMware settings can be added to Settings tab.
Adding more and more options to the Settings tab will make it
bloated. It will require a lot of scrolling to find something.

Data model impact
-----------------

Data model is out of scope of this document

REST API impact
---------------

There is a new REST API URL added:

======  ===================================  =======
method  URL                                  action
======  ===================================  =======
GET     /api/v1/vmware/:cluster_id/settings  Get all cluster settings
PUT     /api/v1/vmware/:cluster_id/settings  Write updated clusted settings
======  ===================================  =======

GET returns JSON with the following structure

.. code-block:: json

	{
	    "availability_zones": {
		"meta": [
		    {
			"name": "name",
			"label": "Name",
			"description": "Name",
			"type": "text"
		    },
                    {
                        "name": "vCenterHost",
                        "label": "VCenter Host",
                        "description": "vCenter Host",
                        "type": text
                    },
                    ...
		],
		"instances": [
		    {
			"name": "Compute 1",
			"vcenter_host": "1.1.1.1",
			"vcenter_user": "user",
			"vcenter_password": "123",
			"computes": {
			    "meta": [
				{
				    "name": "vSphereCluster",
				    "label": "vSphere Cluster",
				    "description": "Oppa vSphere Cluster",
				    "type": "text"
				},
                                ...
			    ],
			    "instances": [
				{
				    "vsphere_cluster": "123",
				    "name": "name1",
				    "data_store_regex": ".*"
				}
			    ]
			},
			"cinder": {
			    "meta": [
				{
				    "name": "enableCinderVMDK",
				    "label": "Enable Cinder",
				    "description": "Enable Cinder",
				    "type": "bool"
				}
			    ],
			    "instance": {
				"enable_Cinder_vmdk": true,
				"data_center": "azsx",
				"data_store_regex": ".*",
				"clusterRegex": ".*"
			    }
			}
		    }
		]
	    },
	    "network": {
		"meta": [
		    {
			"name": "esxi_host_interface",
			"label": "Name",
			"description": "Name",
			"type": "select"
		    },
                    ...
		],
		"instance": {
		    "esxi_host_interface": ""
		}
	    },
	    "glance": {
		"meta": [
		    {
			"name": "vcenter_host",
			"label": "Name",
			"description": "Name",
			"type": "select"
		    }
		],
		"instance": {
		    "vcenter_host": "1.1.1.1",
		    "vcenter_user": "user",
		    "vcenter_password": "123",
		    "dc": "123",
		    "directory": "123"
		}
	    }
	}

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

None

Performance Impact
------------------

No tangible performance impact expected.

Other deployer impact
---------------------

Configuration of plugins is not yet finalized

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  Anton Zemlyanov (azemlyanov)

Design reviewers:
  Andrey Danin (gcon-monolake)

Mandatory reviewers:
  Vitaly Kramskikh (vkramskikh)
  Nikolay Markov (meow-nofer)

QA:
  Tetiana Dubyk (tdubyk),
  Oleksandr Kosse (okosse)

Developers:
  Anton Zemlyanov (azemlyanov),
  Andriy Popovich (popovych-andrey)

Work Items
----------

- Implement interface of the VMware tab without server interaction
- Make HTTP mock methods to test GET/POST/DELETE
- Integrate UI with real Nailgun API when it is done


Dependencies
============

bp/vmware-dual-hypervisor

Testing
=======

Manual functional testing will be performed in recent versions of four
major browsers

* Chrome
* Firefox
* Safari
* IE 9 and above

Documentation Impact
====================

The blueprint impacts Fuel User Guide.
Fuel User Guide should be updated to incorporate interface changes

References
==========

[1] UI Scketch https://etherpad.openstack.org/p/vmware-tab-predesign

