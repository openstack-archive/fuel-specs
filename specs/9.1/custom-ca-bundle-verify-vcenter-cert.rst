..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================================
Support custom CA bundle file to use in verifying the vCenter server certificate
================================================================================

https://blueprints.launchpad.net/fuel/+spec/custom-ca-bundle-verify-vcenter-cert

After implementation this blueprint, user can specify CA bundle file to use in
verifying the vCenter server certificate for compute-vmware and cinder-vmware.


--------------------
Problem description
--------------------

The VMware driver for cinder and compute establishes connections to vCenter
over HTTPS, and VMware driver support the vCenter server certificate
verification as part of the connection process.
Currently, for cinder-vmware and compute-vmware we use "insecure = True" option
and the vCenter server certificate is not verified.
In Fuel Web UI is not possible to select a certificate for cinder-vmware and
compute-vmware.


----------------
Proposed changes
----------------

The following changes need to be done to implement this feature:

* [Web UI] Add file upload support that allows certificate upload on the
  VMware tab [0]_.
* [Nailgun] Add field that allows user to upload CA certificate that emitted
  vCenters TLS/SSL certificate.
* [Fuel Library] Fetch CA certificate bundle and deploy services with using
  certificate.

Web UI
======

On VMware tab [0]_ in the availability zone section need to add the ability
to certificate upload.
Availability zone section on VMware tab [0]_:

 .. image:: ../../images/9.1/custom-ca-bundle-verify-vcenter-cert/fuel_web_ui_vmware_tab.png
    :width: 100 %

It is necessary to add a field, as is done for the section "Glance",
"CA file" field:

 .. image:: ../../images/9.1/custom-ca-bundle-verify-vcenter-cert/fuel_web_ui_vmware_tab_glance_section.png
    :width: 100 %


Nailgun
=======

Data model
----------

Nailgun should be able to serialize CA certificate data and pass it into
astute.yaml file:

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
        vc_ca_file:
          content: RSA
          name: vcenter-ca.pem
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
                           "label": "vCenter password"
                       },
                       {
                           "type": "file",
                           "description": "vCenter CA file",
                           "name": "ca_file",
                           "label": "CA file"
                       }
                   ],
                   "type": "array",
                   "name": "availability_zones"
               },
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

None


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


------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

None


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

Document how to use 'CA file' field on VMware tab in the availability zone
section.


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

* [Nailgun] Add field that allows user to upload CA certificate that emitted
  vCenters TLS/SSL certificate. Need to make changes:

  * openstack.yaml
  * vmware_attributes.json
  * base_serializers.py

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

Necessary to check both scenarios:

* insecure connections for cinder-vmware and compute-vmware
* secure connections for cinder-vmware and compute-vmware
  (with CA bundle file for vCenter)

Acceptance criteria
===================

User can upload the CA certificate for vCenter and after deploy compute and
cinder service works. If the user does not upload the CA certificate for
vCenter, everything works too.


----------
References
----------

.. [0] https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings
