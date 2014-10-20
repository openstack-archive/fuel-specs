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

New entity VmwareAttributes will be added to current functionality. It
will be similar to existing Attributes. New model, object, serializer
and DB table will be created. Relation with Cluster will be one-to-one.
Also release table and model should changed to support metadata for it.

**VmwareAttributes**

* `id` - unique identificator
* `cluster_id` - relation key for cluster
* `editable` - vmware attributes in json format
* `generated` - vmware attributes with generated attributes in json
    format (existing of this field should be discussed)

**Release**

* `vmware_attributes_metadata` - new field to store vmware metadata

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
        "meta": [
        {
            "name": "availability_zones",
            "type": "array",
            "fields": [
            {
                "name": "az_name",
                "type": "text",
                "label": "AZ Name",
                "description": "..."
            },
            {
                "name": "vcenter_host",
                "type": "text",
                "label": "vCenter Host",
                "description": "..."
            },
            "...",
            {
                "name": "nova_computes",
                "type": "array",
                "fields": [
                {
                    "name": "vsphere_cluster",
                    "type": "text",
                    "label": "VSphere Cluster",
                    "description": "..."
                },
                {
                    "name": "service_name",
                    "type": "text",
                    "label": "Service Name",
                    "description": "..."
                },
                "..."
                ]
            },
            {
                "name": "cinder",
                "type": "object",
                "fields": [
                {
                    "name": "enable",
                    "type": "checkbox",
                    "label": "Enable Cinder",
                    "description": "..."
                },
                {
                    "name": "datacenter",
                    "type": "text",
                    "label": "Datacenter",
                    "description": "..."
                },
                "..."
                ]
            }
            ]
        },
        {
            "name": "glance",
            "type": "object",
            "fields": [
            {
                "name": "vcenter_host",
                "type": "text",
                "label": "VCenter Host",
                "description": "..."
            },
            "..."
            ]
        },
        {
            "name": "network",
            "type": "object",
            "fields": [
            {
                "name": "esxi_vlan_interface",
                "type": "text",
                "label": "VLAN interface",
                "description": "..."
            }
            ]
        }
        ],
        "value": {
        "availability_zones": [
            {
            "az_name": "Zone 1",
            "vcenter_host": "1.2.3.4",
            "...": "...",
            "nova_computes": [
                {
                "vsphere_cluster": "cluster1",
                "service_name": "Compute 1"
                },
                {
                "vsphere_cluster": "cluster2",
                "service_name": "Compute 3"
                }
            ],
            "cinder": {
                "enable": true,
                "datacenter": "some_name",
                "...": "..."
            }
            },
            "..."
        ],
        "glance": {
            "vcenter_host": "1.2.3.4",
            "...": "..."
        },
        "network": {
            "esxi_vlan_interface": "eth0"
        }
        }
    }

Upgrade impact
--------------

deployment_serializers should be changed to support processing VMware
attributes. It can be some mixin classes to handle vmware data for old
and new releases.

Security impact
---------------

None

Notifications impact
--------------------

Notifications partially covered by bp/cinder-vmdk-role.
Other notifications can be:

#. Warn a user before deployment if Glance VMDK is used but not all vCenter
   credentials provided.
#. Warn a user before deployment if there are vCenter compute services selected
   but not all vCenter credentials provided.
#. (optional) Warn a user if "ESXi host interface" is not provided. It can be
   useful to force a user to fill this information to avoid network
   misconfigurations.

Other end user impact
---------------------

As a basic solution we decided to block the vCenter tab after deployment.
It means that after deployment a user can only add more KVM Compute nodes
but no new vSphere clusters or change their settings
(like username/password/cluster_name).

If we ensure that Controller nodes can be safely redeployed in a live env,
we can keep the vCenter tab enabled after deployment to be able to add more
vSphere clusters and to modify parameters. For instance, it will allow a user
to deploy a part of KVM infrastructure and then add a part of vCenter
infrastructure.

The decision of keeping the vCenter tab enabled or blocking the tab depends
of implementation of bp/vmware-dual-hypervisor.

Fuel client impact
~~~~~~~~~~~~~~~~~~

Support for VMware attributes in fuel client should be added. It can be
implemented in a similar way as network_settings and cluster_settings actions.

Performance Impact
------------------

No tangible performance impact expected.

Other deployer impact
---------------------

None

Developer impact
----------------

This is how an astute.yaml part will look like:

.. code-block:: yaml

    use_vcenter: true
    vcenter:
        esxi_vlan_interface: lalala
        computes:
              - availability_zone_name: aaaa
                vc_host: XXX
                vc_user: XXX
                vc_password: XXX
                service_name: XXX
                cluster: XXX
                datastore_regex: XXX
              - ailability_zone_name: aaaa
                vc_host: XXX
                vc_user: XXX
                vc_password: XXX
                service_name: YYYY
                cluster: YYYY
                datastore_regex: YYYY
    cinder_vmware:
        instances:
              - availability_zone_name: aaaa
                vc_host: XXX
                vc_user: XXX
                vc_password: XXX
    glance:
        vc_host: XXX
        vc_user: XXX
        vc_password: XXX
        dc: XXX
        ds: XXX
        directory: XXX

The 'glance' part remains unchanged. The 'vcenter' part will be refactored to
support multiple compute instances. The new 'cinder-vmware' part will be
introduced to keep all cinder-vmdk settings in it.

The 'use_vcenter' flag will be added to be sure that this environment will be
deployed with vCenter support.

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
- Implement new handler and validator for VMware attributes
- DB integration: new table, model. Implement CRUD operations in Cluster
  object for working with VMmware attributes data
- Add new deployment serializer for working with VMware data


Dependencies
============

* Corresponded modifications of Puppet manifests would be done by the
  blueprint https://blueprints.launchpad.net/fuel/+spec/vmware-dual-hypervisor

Testing
=======

* Manual functional testing will be performed in recent versions of four
  major browsers

  * Chrome
  * Firefox
  * Safari
  * IE 9 and above

* Automated UI tests will be added.
* Unit and integration tests for REST API and a deployment serializer
  will be added.

Acceptance criteria
-------------------

* UI part

  * The VMware tab should appear only if 'use_vcenter' attribute is true.
  * It is possible to modify data at the VMware tab and regexes are
    applied to it.
  * It is not poassible to save an invalid data (which is not fit to regex).
  * A modified data can be saved and obtained back properly.

* Nailgun part

  * The new handler should answer with a data structure described in a
    release metadata.
  * If no vmware-specific metadata provided in a release the handler should
    answer with 204 (No Content) HTTP code.
  * The handler should accept a valid data structure and drop an invalid.
  * The handler should save a modified data in DB and return it with GET
    request.
  * The output of deployment_serializer for older releases (6.0, 5.1) shouldn't
    be changed.
  * For 6.1 release deployment_serializer should provide a new structure of
    data described in the 'Developer impact' section.
  * We should be sure that the data with multiple compute instances is accepted
    by the handler and properly serialized by deployment_serializer.

* Fuel-CLI part

  * Fuel-cli is able to get VMware settings for cluster.
  * Fuel-cli handles an answer with 204 HTTP code properly (i.e. it can show a
    message "This cluster doesn't support separate VMware settings.").
  * Fuel-cli can upload modified VMware settings back to Nailgun.

Documentation Impact
====================

The blueprint impacts Fuel User Guide.
Fuel User Guide should be updated to incorporate interface changes

References
==========

[1] UI Scketch https://etherpad.openstack.org/p/vmware-tab-predesign

https://blueprints.launchpad.net/fuel/+spec/cinder-vmdk-role
