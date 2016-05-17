..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================================
Support custom CA bundle file to use in verifying the vCenter server certificate
================================================================================

https://blueprints.launchpad.net/fuel/+spec/custom-ca-bundle-verify-vcenter-cert

After implementation this blueprint, user can specify CA bundle file to use in
verifying the vCenter server certificate for nova-compute [4]_ and cinder-volume
[3]_. Also we improve use cases for Glance vSphere backend and CA bundle file.


--------------------
Problem description
--------------------

The VMware driver for cinder-volume and nova-compute establishes connections to
vCenter over HTTPS, and VMware driver support the vCenter server certificate
verification as part of the connection process.
Currently, for cinder-volume [3]_ we use ``vmware_insecure = True`` [1]_ and for
nova-compute [4]_ we set ``insecure = True`` [2]_ options therefore the vCenter
server certificate is not verified.
In Fuel Web UI is not possible to select a certificate for cinder-volume [3]_
and nova-compute [4]_.
For Glance vSphere backend we can specify custom CA bundle file and it covers
the case where the vCenter is using a Self-Signed certificate. But if vCenter
server certificate was emitted by know CA (e.g. GeoTrust) and we don't specify
custom CA bundle file, certificate verification turn off, because by default we
set ``vmware_insecure = True`` [5]_.
Use cases which cover this blueprint for cinder-volume [3]_, nova-compute [4]_
and Glance vSphere backend:

1. ``Case 1.`` Bypass vCenter certificate verification (default). Certificate
verification turn off. This case is useful for faster deployment and for testing
environment.

2. ``Case 2.`` vCenter is using a Self-Signed certificate. In this case the user
must upload custom CA bundle file certificate.

3. ``Case 3.`` vCenter server certificate was emitted by know CA
(e.g. GeoTrust). In this case user have to leave CA certificate bundle upload
field empty.


----------------
Proposed changes
----------------

The following changes need to be done to implement this feature:

* [Web UI] Add file upload support that allows certificate upload on the
  VMware tab [0]_.
* [Web UI] Implement restrictions [6]_ support on VMware tab [0]_.
* [Nailgun] Add field that allows user to upload CA certificate that emitted
  vCenters TLS/SSL certificate.
* [Nailgun] Add checkbox "Bypass vCenter certificate verification".
* [Fuel Library] Fetch CA certificate bundle and deploy services with using
  certificate.

Web UI
======

On VMware tab [0]_ in the availability zone section need to add the ability to
certificate upload and restrictions [6]_ support.

Availability zone section on VMware tab [0]_:

 .. image:: ../../images/10.0/custom-ca-bundle-verify-vcenter-cert/fuel_web_ui_vmware_tab.png
    :width: 100 %

For the ``case 1`` availability zone section on VMware tab [0]_ will look like:

 .. image:: ../../images/10.0/custom-ca-bundle-verify-vcenter-cert/fuel_web_ui_vmware_tab_case1.png
    :width: 100 %

For the ``case 2`` availability zone section on VMware tab [0]_ will look like:

 .. image:: ../../images/10.0/custom-ca-bundle-verify-vcenter-cert/fuel_web_ui_vmware_tab_case2.png
    :width: 100 %

For the ``case 3`` availability zone section on VMware tab [0]_ will look like:

 .. image:: ../../images/10.0/custom-ca-bundle-verify-vcenter-cert/fuel_web_ui_vmware_tab_case3.png
    :width: 100 %

Description of the above cases can be found in section ``Problem description``.

It will use the same logic for the Glance vSphere backend (Glance section on
VMware tab [0]_).


Nailgun
=======

Data model
----------

Nailgun should be able to serialize CA certificate data and pass it into
astute.yaml file, astute.yaml for ``case 2``:

.. code-block:: yaml

    /etc/astute.yaml
    ...
    vcenter:
      computes:
      - availability_zone_name: vcenter
        datastore_regex: .*
        service_name: vmcluster1
        target_node: controllers
        vc_cluster: Cluster1
        vc_host: 172.16.0.254
        vc_password: Qwer!1234
        vc_user: administrator@vsphere.local
        vc_insecure : false
        vc_ca_file:
          content: RSA
          name: vcenter-ca.pem
      - availability_zone_name: vcenter
        datastore_regex: .*
        service_name: vmcluster2
        target_node: controllers
        vc_cluster: Cluster2
        vc_host: 172.16.0.254
        vc_password: Qwer!1234
        vc_user: administrator@vsphere.local
        vc_insecure: false
        vc_ca_file:
          content: RSA
          name: vcenter-ca.pem
      ...
    cinder:
      ...
      instances:
      - availability_zone_name: vcenter
        vc_host: 172.16.0.254
        vc_password: Qwer!1234
        vc_user: administrator@vsphere.local
        vc_insecure: false
        vc_ca_file:
          content: RSA
          name: vcenter-ca.pem
      ...
    glance:
      ...
      vc_insecure: false
      vc_ca_file:
        content: RSA
        name: vcenter-ca.pem
      vc_datacenter: Datacenter
      vc_datastore: nfs
      vc_host: 172.16.0.254
      vc_password: Qwer!1234
      vc_user: administrator@vsphere.local
    ...


REST API
--------

GET ``/api/clusters/%cluster_id%/vmware_attributes/`` method should return data
with the following structure:

.. code-block:: json

   [{
       "pk": 1,
       "editable": {
           "metadata": [
               {
                   "fields": [
                       {
                           "type": "text",
                           "description": "Availability zone name",
                           "name": "az_name",
                           "label": "AZ name"
                       },
                       {
                           "type": "text",
                           "description": "vCenter host or IP",
                           "name": "vcenter_host",
                           "label": "vCenter host"
                       },
                       {
                           "type": "text",
                           "description": "vCenter username",
                           "name": "vcenter_username",
                           "label": "vCenter username"
                       },
                       {
                           "type": "password",
                           "description": "vCenter password",
                           "name": "vcenter_password",
                           "label": "vCenter password"
                       },
                       {
                           "type": "checkbox",
                           "name": "vcenter_insecure",
                           "label": "Bypass vCenter certificate verification"
                       },
                       {
                           "type": "file",
                           "description": "vCenter CA file",
                           "name": "vcenter_ca_file",
                           "label": "CA file",
                           "restrictions": [
                               {
                                   "message": "Bypass vCenter certificate verification should be disabled.",
                                   "condition": "currentVCenter:vcenter_insecure == true"
                               }
                           ]
                       },
                       {
                           "fields": [
                               {
                                   "type": "text",
                                   "description": "vSphere Cluster",
                                   "name": "vsphere_cluster",
                                   "label": "vSphere Cluster",
                                   "regex": {
                                       "source": "\\S",
                                       "error": "Empty cluster"
                                   }
                               },
                               {
                                   "type": "text",
                                   "description": "Service name",
                                   "name": "service_name",
                                   "label": "Service name"
                               },
                               {
                                   "type": "text",
                                   "description": "Datastore regex",
                                   "name": "datastore_regex",
                                   "label": "Datastore regex"
                               },
                               {
                                   "type": "select",
                                   "description": "Target node for nova-compute service",
                                   "name": "target_node",
                                   "label": "Target node"
                               }
                           ],
                           "type": "array",
                           "name": "nova_computes"
                       }
                    ],
                    "type": "array",
                    "name": "availability_zones"
               },
               {
                   "fields": [
                    {
                           "type": "text",
                           "description": "VLAN interface",
                           "name": "esxi_vlan_interface",
                           "label": "VLAN interface"
                       }
                   ],
                    "type": "object",
                    "name": "network"
               },
               {
                   "fields": [
                       {
                           "type": "text",
                           "description": "VCenter host or IP",
                           "name": "vcenter_host",
                           "label": "VCenter Host",
                           "regex": {
                               "source": "\\S",
                               "error": "Empty host"
                           }
                       },
                       {
                           "type": "text",
                           "description": "vCenter username",
                           "name": "vcenter_username",
                           "label": "vCenter username",
                           "regex": {
                               "source": "\\S",
                               "error": "Empty username"
                           }
                       },
                       {
                           "type": "password",
                           "description": "vCenter password",
                           "name": "vcenter_password",
                           "label": "vCenter password",
                           "regex": {
                               "source": "\\S",
                               "error": "Empty password"
                           }
                       },
                       {
                           "type": "text",
                           "description": "Datacenter",
                           "name": "datacenter",
                           "label": "Datacenter",
                           "regex": {
                               "source": "\\S",
                               "error": "Empty datacenter"
                           }
                       },
                       {
                           "type": "text",
                           "description": "Datastore",
                           "name": "datastore",
                           "label": "Datastore",
                           "regex": {
                               "source": "\\S",
                               "error": "Empty datastore"
                           }
                       },
                       {
                           "type": "checkbox",
                           "name": "vcenter_insecure",
                           "label": "Bypass vCenter certificate verification"
                       },
                       {
                           "type": "file",
                           "description": "File containing the trusted CA bundle that emitted vCenter server certificate. If empty vCenters certificate is not verified.",
                           "name": "ca_file",
                           "label": "CA file",
                            "restrictions": [
                               {
                                   "message": "Bypass vCenter certificate verification should be disabled.",
                                   "condition": "Glance:vcenter_insecure == true"
                               }
                           ]
                       }
                   ],
                   "type": "object",
                   "name": "glance",
                   "restrictions": [
                       {
                           "action": "hide",
                           "condition": "settings:storage.images_vcenter.value == false or settings:common.use_vcenter.value == false"
                       }
                   ]
               }
           ],
           "value": {
               "availability_zones": [
                   {
                       "az_name": "Zone 1",
                       "vcenter_host": "1.2.3.4",
                       "vcenter_username": "admin",
                       "vcenter_password": "secret",
                       "vcenter_insecure": "true",
                       "vcenter_ca_file": "file_blob",
                       "nova_computes": [
                           {
                               "vsphere_cluster": "cluster1",
                               "service_name": "Compute 1",
                               "datastore_regex": "",
                               "target_node": {
                                   "current": {
                                       "id": "test_target_node"
                                   }
                               }
                           },
                           {
                               "vsphere_cluster": "cluster2",
                               "service_name": "Compute 3",
                               "datastore_regex": "",
                               "target_node": {
                                   "current": {
                                       "id": "test_target_node"
                                   }
                               }
                           }
                       ]
                   },
                   {
                       "az_name": "Zone 2",
                       "vcenter_host": "1.2.3.6",
                       "vcenter_username": "user$",
                       "vcenter_password": "pass$word",
                       "vcenter_insecure": "true",
                       "vcenter_ca_file": "file_blob",
                       "nova_computes": [
                           {
                               "vsphere_cluster": "cluster1",
                               "service_name": "Compute 4",
                               "datastore_regex": "^openstack-[0-9]$"
                           },
                           {
                               "vsphere_cluster": "",
                               "service_name": "Compute 7",
                               "datastore_regex": ""
                           }
                       ]
                   }
               ],
               "glance": {
                   "vcenter_host": "1.2.3.4",
                   "vcenter_username": "admin",
                   "vcenter_password": "secret",
                   "datacenter": "test_datacenter",
                   "datastore": "test_datastore",
                   "vcenter_insecure": "true",
                   "ca_file": "file_blob",
               },
               "network": {
                   "esxi_vlan_interface": "eth0"
               }
            }
        }
    }]


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

Specification might affect plugins that connect to vCenter server:

* Fuel VMware DVS plugin [8]_.

* Fuel VMware NSXv plugin [7]_.


Fuel Library
============

Changes to Puppet manifests:

* vmware::cinder::vmdk
* vmware::compute_vmware
* vmware::ceilometer::compute_vmware
* vmware::controller
* vmware::ceilometer
* parse_vcenter_settings function


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

None


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

* The user can upload in VMware tab [0]_ CA certificate that emitted
  vCenters TLS/SSL certificate.
* The user can check or uncheck ``Bypass vCenter certificate verification`` in
  VMware tab [0]_.


------------------
Performance impact
------------------

None


-----------------

----------------
Developer impact
----------------

None


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

Document how to use ``CA file`` field and ``Bypass vCenter certificate
verification`` checkbox on VMware tab in the availability zone section and in
Glance section.


--------------
Implementation
--------------

Assignee(s)
===========

======================= ==============================================
Primary assignee        - Alexander Arzhanov <aarzhanov@mirantis.com>
Developers              - Alexander Arzhanov <aarzhanov@mirantis.com>
                        - Anton Zemlyanov <azemlyanov@mirantis.com>
                        - Andriy Popovych <apopovych@mirantis.com>
QA engineers            - Ilya Bumarskov <ibumarskov@mirantis.com>
Mandatory design review - Igor Zinovik <izinovik@mirantis.com>
                        - Sergii Golovatiuk <sgolovatiuk@mirantis.com>
======================= ==============================================


Work Items
==========

* [Web UI] Add file upload support that allows certificate upload on the
  VMware tab [0]_.

* [Web UI] Implement restrictions [6]_ support on VMware tab [0]_.

* [Nailgun] Add field that allows user to upload CA certificate that emitted
  vCenters TLS/SSL certificate. Need to make changes:

  * openstack.yaml
  * vmware_attributes.json
  * base_serializers.py

* [Nailgun] Add checkbox ``Bypass vCenter certificate verification``.

* [Fuel Library] Fetch CA certificate bundle and deploy services with using
  certificate. Need to make changes:

  * vmware::cinder::vmdk
  * vmware::compute_vmware
  * vmware::ceilometer::compute_vmware
  * vmware::controller
  * vmware::ceilometer
  * parse_vcenter_settings function


Dependencies
============

None


------------
Testing, QA
------------

Necessary to check scenarios:

* insecure connections for nova-compute [4]_, cinder-volume [3]_ and Glance
  vSphere backend.
* secure connections for nova-compute [4]_ and cinder-volume [3]_. and Glance
  vSphere backend (with CA bundle file for vCenter).

Acceptance criteria
===================

User can upload the CA certificate for vCenter and after deploy nova-compute
[4]_, cinder-volume [3]_ and Glance vSphere backend service works. If the user
does not upload the CA certificate for vCenter and enable ``Bypass vCenter
certificate verification`` checkbox everything works too.


----------
References
----------

.. [0] https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings
.. [1] https://github.com/openstack/fuel-library/blob/master/deployment/puppet/vmware/templates/cinder-volume.conf.erb#L81
.. [2] https://github.com/openstack/fuel-library/blob/master/deployment/puppet/vmware/templates/nova-compute.conf.erb#L17
.. [3] configured with VMwareVcVmdkDriver
.. [4] configured with VMwareVCDriver
.. [5] https://github.com/openstack/puppet-glance/blob/master/manifests/backend/vsphere.pp#L112
.. [6] https://wiki.openstack.org/wiki/Fuel/Plugins#What_are_restrictions.3F
.. [7] https://github.com/openstack/fuel-plugin-nsxv
.. [8] https://github.com/openstack/fuel-plugin-vmware-dvs
