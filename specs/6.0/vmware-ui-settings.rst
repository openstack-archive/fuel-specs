..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
VMware UI Settings Tab for FuelWeb
==========================================

https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings

VMware vCenter settings are currently available on Settings Tab, it
does not allow dynamic addition/removal of settings and is already big
enough. vCenter functionality will be moved to a separate Cluster Tab
to provide better user experience.

Problem description
===================

VMware settings have the following problems in FuelWeb UI implementation:

* It is impossible to have different vCenter clusters for nova-compute
  and Cinder/Glance services

* There is no way of adding multiple vCenter clusters for nova-compute or
  other services.


Proposed change
===============

Add the VMware Tab on the Cluster page with all the related settings. The
settings are separated into vCenter, Network, and Glance Groups [1].

User Interface
--------------------------------------------------------------------------

::

  vCenter:
  --------
  Availability group: ______________  (description)
  vCenter Host:       ______________  (description)
  vCenter Username:   ______________  (description)
  vCenter Password:   ______________  (description)
    Nova Computes:
    --------------
    Name of service:    ______________  (description)
    vCenter Cluster:    ______________  (description)
    Datastore regex:    _______________ (description) OPTIONAL
    Cinder:
    -------
    vCenter IP:      ________________  (description)
    Username:        ________________  (description)
    Password:        ________________  (description)
    Directory for volumes: __________  (description) OPTIONAL
    Directory for temp names: _______  (description) OPTIONAL

  Glance:
  -------
  [x] Enabled Vinder VMDK
  vCenter Host:    ______________  (description)
  vCenter Username:______________  (description)
  vCenter Password:______________  (description)
  Datacenter name: ______________  (description)
  Datastore name:  ______________  (description)
  Directory for images: _________  (description) OPTIONAL

  Network:
  --------
  iESXI VLAN Inerface: _____________ (description)

Alternatives
------------

Alternatively, VMware settings can be added to Settings Tab.
Adding more and more options to the Settings tab will make it
bloated. It will require a lot of scrolling to find something.

Data model impact
-----------------

Data model is out of scope of this document

REST API impact
---------------

There is a new REST API URL added: **/api/plugins/vmware/cluster/:id**

======  ===================================  =======
method  URL                                  action
======  ===================================  =======
GET     /api/v1/vmware/:cluster_id/settings  Get all cluster settings
POST    /api/v1/vmware/:cluster_id/settings  Write updated clusted settings
======  ===================================  =======

GET returns JSON with the following structure

.. code-block:: json

	{
	    "availabilityZones": {
		"meta": [
		    {
			"name": "name",
			"label": "Name",
			"description": "Name",
			"type": "text"
		    }
		],
		"instances": [
		    {
			"name": "Compute 1",
			"vcenterHost": "1.1.1.1",
			"vcenterUser": "user",
			"vcenterPassword": "123",
			"computes": {
			    "meta": [
				{
				    "name": "vSphereCluster",
				    "label": "vSphere Cluster",
				    "description": "Oppa vSphere Cluster",
				    "type": "text"
				}
			    ],
			    "instances": [
				{
				    "vSphereCluster": "123",
				    "name": "name1",
				    "DataStoreRegex": ".*"
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
				"enableCinderVMDK": true,
				"dataCenter": "azsx",
				"dataStoreRegex": ".*",
				"clusterRegex": ".*"
			    }
			}
		    }
		]
	    },
	    "network": {
		"meta": [
		    {
			"name": "name",
			"label": "Name",
			"description": "Name",
			"type": "select"
		    }
		],
		"instance": {
		    "esxiHostInterface": ""
		}
	    },
	    "glance": {
		"meta": [
		    {
			"name": "name",
			"label": "Name",
			"description": "Name",
			"type": "select"
		    }
		],
		"instance": {
		    "vcenterHost": "1.1.1.1",
		    "vcenterUser": "user",
		    "vcenterPassword": "123",
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

Fuel User Guide should be updated to incorporate interface changes

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
  Nickolay Markov (meow-nofer)

QA:
  Tetiana Dubyk (tdubyk),
  Oleksandr Kosse (okosse)

Developers:
  Anton Zemlyanov (azemlyanov),
  Andrii Popovich (popovych-andrey)

Work Items
----------

- Implement interface of the VMware tab without server interaction
- Make HTTP mock methods to test GET/POST/DELETE
- Integrate UI with real Nailgun API when it is done


Dependencies
============

* Nailgun API support

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

The blueprint impacts Fuel User Guide [x]


References
==========

[1] UI Scketch https://etherpad.openstack.org/p/vmware-tab-predesign

