..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
VmWare UI Settings Tab for FuelWeb
==========================================

https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings

VmWare vCenter settings are currently available on Settings Tab and are only 
available before the deploy is done. It is very desirable to have the settings 
available after deploy. It is also required to support multiple vCenters for 
Compute service. The settings will be always available in VmWare tab of 
Cluster page, the functionality will be moved to a plugin when plugins 
are available.


Problem description
===================

VmWare settings have following problems in the current FuelWeb UI:

* It is impossible to edit VmWare settings after deploy is done. All the 
  settings are now "predeploy" only.

* It is impossible to have different vCenter clusters for Compute 
  and Cinder/Glance services

* There is no way of adding multiple vCenter clusters for Compute or 
  other services. 


Proposed change
===============

Add the VmWare Tab on the Cluster page with all the related settings. The 
settings are separated into Compute, Glance and Cinder Groups [1]. 

Compute Service Group. Zero or more repetions of the following block:
--------------------------------------------------------------------------

::

  Name of service: ______________  (description)
  vCenter IP:      ______________  (description)
  Username:        ______________  (description)
  Password:        ______________  (description)
  Cluster name:    ______________  (description)
  Openstack node:  [dropdown list] (description)
  Datastore regex: _______________ (description) OPTIONAL

Glance Service Group. Single entry of the following block:
----------------------------------------------------------

::

  vCenter IP:      ______________  (description)
  Username:        ______________  (description)
  Password:        ______________  (description)
  Datacenter name: ______________  (description)
  Datastore name:  ______________  (description)
  Directory for images: _________  (description) OPTIONAL

Cinder Service Group. Zero or more repetions of the following block:
--------------------------------------------------------------------

::

  Name of service: ________________  (description)
  vCenter IP:      ________________  (description)
  Username:        ________________  (description)
  Password:        ________________  (description)
  Availability zone: [dropdown list] (description) OPTIONAL
  Directory for volumes: __________  (description) OPTIONAL
  Directory for temp names: _______  (description) OPTIONAL

Alternatives
------------

Alternatively, VmWare settings can be added to Settings Tab. Settings Tab 
will require refactoring allowing settings to stay editable after Cluster 
deployment.

Data model impact
-----------------

Data model is out of scope of this document

REST API impact
---------------

There is a new REST API URL added: **/api/plugins/vmware/cluster/:id**

======  ===============================  =======
method  URL                              action
======  ===============================  =======
GET     /api/plugins/vmware/cluster/:id  Get all cluster settings
POST    /api/plugins/vmware/cluster/:id  Write updated clusted settings
DELETE  /api/plugins/vmware/cluster/:id  Remove all plugin settings
======  ===============================  =======

GET returns JSON with the following structure

.. code-block:: json

    {
        "Compute": {
            "meta": {
                "name": "name",
                "restrictions": []
            },
            "instances": [
                {
                    "id": 12345678,
                    "vCenterIp": {
                        "value": "...",
                        "restrictions": [],
                        "bind": "..."
                    },
                    "username": {
                        "value": "...",
                        "restrictions": [],
                        "bind": "..."
                    },
                    "password": {
                        "value": "...",
                        "restrictions": [],
                        "bind": "..."
                    },
                    ...
                }
            ]
        },
        "Glance": {
            "meta": {
                "name": "name",
                "restrictions": []
            },
            "instances": [
            ]
        },
        "Cinder": {
            "meta": {
                "name": "name",
                "restrictions": []
            },
            "instances": [
            ]
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
  azemlyanov@mirantis.com

Work Items
----------

- Implement interface of the VmWare tab without server interaction
- Make HTTP mock methods to test GET/POST/DELETE
- Integrate UI with real Nailgun API when it's done


Dependencies
============

* Nailgun API support

Testing
=======

Manual functional testing will be performed in recent versions of four major browsers

* Chrome
* Firefox
* Safary
* IE 9 and above

Documentation Impact
====================

The blueprint impacts Fuel User Guide [x]


References
==========

[1] UI Scketch https://etherpad.openstack.org/p/vmware-tab-predesign

