..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Add UI item on VMware tab from Fuel plugin
==========================================

https://blueprints.launchpad.net/fuel/+spec/ui-item-on-vmware-tab-from-plugin

Presently, in Fuel plugins you can create environment_config.yaml file. This
file describes additional attributes that will appear on the Settings tab or
Networks tab of the Fuel web UI after plugin is installed. When the environment
is deployed, these attributes are passed to the task executor so that the data
is available in the /etc/astute.yaml file on each target node and can be
accessed from your bash or puppet scripts. But you can not extend a
VMware tab [2]_ in the same way.


--------------------
Problem description
--------------------

For example, in case with Fuel VMware DVS plugin [1]_ (default network backend
for VMware environment), the user must specify the vCenter Cluster to VDS
mapping. For consistency Fuel Web UI interface, we need add the ability to add
fields in VMware tab [2]_ from plugin and display plugin checkbox on the
VMware tab [2]_. Currently plugin checkbox placed into the Settings tab or
Networks tab of the Fuel web UI. After implement this blueprint user can
specify VMware data in one place.


----------------
Proposed changes
----------------

The following changes need to be done to implement this feature:

* [Nailgun] Introduced new `vmware_config.yaml` as optional metadata file in
  plugin for VMware tab [2]_.
* [Nailgun] Describe desired structure for it. For example Fuel VMware DVS
  plugin [1]_:

.. code-block:: yaml

    vmware_config.yaml
    ...
    metadata:
      - name: "availability_zones"
        fields:
          - name: "nova_computes"
            fields:
               - name: "vmware_dvs_fw_driver"
                 type: "checkbox"
                 label: "Use the VMware DVS firewall driver."
               - name: "vmware_dvs_net_maps"
                 type: "text"
                 label: "Enter the dvSwitch name for mapping."
                 description: "dvSwitch name"
    value:
      availability_zones:
        -
          nova_computes:
            -
              vmware_dvs_fw_driver: false
              vmware_dvs_net_maps: ""

* [Nailgun] Merge structures from all plugins which have `vmware_config.yaml`
  into vmware_attributes.
* [Web UI] Parse vmware_attributes with custom attributes on UI.
* [Nailgun] Serialize data from plugins as is into astute.yaml.
* [Fuel Library] Check and rework vmware parsers and manifests if something
  wrong.

Web UI
======

Add support parse changed vmware_attributes with custom attributes on
VMware tab [2]_.

Nailgun
=======

Data model
----------

Nailgun should be able to serialize plugin data and pass it into astute.yaml
file, for example, in case with Fuel VMware DVS plugin [1]_:

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
        vmware_dvs_fw_driver: true
        vmware_dvs_net_maps: VDS1
      - availability_zone_name: vcenter
        datastore_regex: .*
        service_name: vmcluster2
        target_node: controllers
        vc_cluster: Cluster2
        vc_host: 172.16.0.254
        vc_password: Qwer!1234
        vc_user: administrator@vsphere.local
        vmware_dvs_fw_driver: true
        vmware_dvs_net_maps: VDS2
      ...


REST API
--------

VMware plugins will be in `/api/cluster/<cluster_id>/vmware_attributes`.


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

These changes will affect the plugins:

* Fuel VMware DVS plugin [1]_

* Fuel VMware NSXv plugin [0]_

In each of the above plugins need to change the `vmware_config.yaml`, puppet
manifests and plugins documentation.


Fuel Library
============

Check and rework vmware parsers and manifests if something wrong.


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

User can specify all VMware specific data in one place - VMware tab [2]_.


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

The Fuel plugins documentation should describe:

* how to use new `vmware_config.yaml`


--------------
Implementation
--------------

Assignee(s)
===========

======================= =============================================
Primary assignee        - Alexander Arzhanov <aarzhanov@mirantis.com>
Developers              - Alexander Arzhanov <aarzhanov@mirantis.com>
                        - Anton Zemlyanov <azemlyanov@mirantis.com>
                        - Andriy Popovych <apopovych@mirantis.com>
QA engineers            - Ilya Bumarskov <ibumarskov@mirantis.com>
Mandatory design review - Iuliia Aranovich <jkirnosova@mirantis.com>
                        - Bulat Gaifullin <bgaifullin@mirantis.com>
                        - Aleksandr Didenko <adidenko@mirantis.com>
======================= =============================================


Work Items
==========

* [Nailgun] Introduced new `vmware_config.yaml` as optional metadata file in
  plugin for VMware tab [2]_.
* [Nailgun] Describe desired structure for it. For example Fuel VMware DVS
  plugin [1]_:

.. code-block:: yaml

    vmware_config.yaml
    ...
    metadata:
      - name: "availability_zones"
        fields:
          - name: "nova_computes"
            fields:
               - name: "vmware_dvs_fw_driver"
                 type: "checkbox"
                 label: "Use the VMware DVS firewall driver."
               - name: "vmware_dvs_net_maps"
                 type: "text"
                 label: "Enter the dvSwitch name for mapping."
                 description: "dvSwitch name"
    value:
      availability_zones:
        -
          nova_computes:
            -
              vmware_dvs_fw_driver: false
              vmware_dvs_net_maps: ""

* [Nailgun] Merge structures from all plugins which have `vmware_config.yaml`
  into vmware_attributes.
* [Web UI] Parse vmware_attributes with custom attributes on UI.
* [Nailgun] Serialize data from plugins as is into astute.yaml.
* [Fuel Library] Check and rework vmware parsers and manifests if something
  wrong.


Dependencies
============

None


------------
Testing, QA
------------

* UI functional tests for appropriate versions of Fuel VMware DVS plugin [1]_
  and Fuel VMware NSXv plugin [0]_ should cover the changes.

Acceptance criteria
===================

User can describes additional attributes in plugin that will appear on the
VMware tab [2]_ of the Fuel web UI. When the environment is deployed,
these attributes are passed to the task executor so that the data is available
in the /etc/astute.yaml file on each target node and can be accessed from bash
or puppet scripts.


----------
References
----------

.. [0] https://github.com/openstack/fuel-plugin-nsxv
.. [1] https://github.com/openstack/fuel-plugin-vmware-dvs
.. [2] https://blueprints.launchpad.net/fuel/+spec/vmware-ui-settings
