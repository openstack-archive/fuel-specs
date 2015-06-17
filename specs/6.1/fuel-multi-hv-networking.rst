..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Fuel Multiple Hypervisor Networking
==========================================

https://blueprints.launchpad.net/fuel/+spec/TBD

Allow a user to choose in the Fuel UI wizard multiple hypervisors and a
suitable Neutron plugin for them. Also allow Fuel plugins to extend HV and
Neutron plugins options in the wizard.

Problem description
===================

We are going to get rid of supporting Nova-Network in Fuel 7.0 making Neutron
the only option.

Also the developing of the Contrail plugin for Fuel 6.1 reveals that our plugin
framework doesn't support a clear notification of which Neutron plugin or ML2
driver will be used in a cloud. In 6.1 it looks like "create a cluster with
strictly Neutron VLAN, then enable our Fuel plugin, it will deploy the cluster
with Contrail enabled but everywhere in Fuel the cluster will be mentioned as
OpenVSwitch + VLANs."

The situation with different hypervisors looks the same way. The Fuel wizard
allows a user to switch a libvirt operation mode between KVM or Qemu and
enable/disable VMware vCenter support. It looks quite complicated and unclear
and forces people make mistakes. Also a plugin is not allowed to add other HV
types into the wizard or the Settings tab.

Proposed change
===============

#. Move the Qemu/KVM switch to the Settings tab because it's not the HV from
   the OSt stand point. It's just a libvirt setting.
#. Redesign the Compute wizard pane to support multiple selections of HVs.
#. Allow Fuel plugins to mix their options into the Compute pane like it's done
   now for the Setting tab.
#. Redesign the Network wizard pane to support radio buttons for monolithic
   Neutron plugins and multiple selections for ML2 drivers.
#. Fuel Plugins should be also allowed to add monolithic options or ML2
   drivers.
#. Each HV option provides its HV type, like "libvirt" or "vmware". Each
   Neutron monolithic plugin or ML2 driver reports HV types it's able to
   support. A user choose one or more HVs first and then select a suitable
   network backend. The wizard may hide/disable inappropriate Neutron
   options based on selected HVs.
#. A user is allowed to select one of the monolithic Neutron plugins or, in
   case he chose ML2 plugin, he is able to select one or more ML2 drivers. The
   "Next" button will be blocked until a set of chosen ML2 dirvers may cover
   all HVs selected on the previous step.
#. Fuel Puppet manifests should respect new fields with a list of HVs enabled
   and a chosen Neutron backend. To do this best we need to make deploy tasks
   more isolated and independent. But this isolation improvement may wait till
   the next release.

Since we will have "roles from plugins" and a single graph for all tasks
with task override [0] a Fuel plugin may fairly easy alternate Neutron
and Nova-compute configurations to add a new HV or network backend.

This is how the new wizard may look like:

  +---------------------------------------------+
  |                                             |
  |     Hypervisor list                         |
  |     ===============                         |
  |                                             |
  |                                             |
  |          [x]  Libvirt                       |
  |                                             |
  |          [ ]  VMware vCenter                |
  |                                             |
  |          [ ]  Xen                           |
  |                                             |
  |                                             |
  |                                             |
  +---------------------------------------------+
                                                 
  +---------------------------------------------+
  |                                             |
  |      Neutron plugins                        |
  |      ===============                        |
  |                                             |
  |           ( )  Contrail plugin              |
  |                                             |
  |           ( )  VMware NSX plugin            |
  |                                             |
  |           (*)  ML2 plugin                   |
  |                                             |
  |               [x]  OVS driver               |
  |                                             |
  |               [x]  VMware DVS driver        |
  |                                             |
  |               [ ]  Mellanox driver          |
  |                                             |
  |                                             |
  +---------------------------------------------+


Alternatives
------------

??????

Data model impact
-----------------

#. A new JSON field 'hypervisor_list' should be added into the Cluster model.
   It will be a JSONized list of strings of HV types enabled for cluster.
#. The field 'net_l23_provider' in the NeutronConfig model should mean a
   Neutron monolithic plugin used for a cluster.
#. A new 
#. New bind operators should be added into the openstack.yaml DSL. They are
   ".!add" and "!remove". They work with a list and add or delete a value
   to/from the list. So it acts more like a set rather than a list.
#. The Network and Compute wizard panes' descriptions should be reworked.
   This is an example how they may look like:

   .. code:: yaml

      Compute:
        libvirt:
          type: "checkbox"
          weight: 5
          bind: 
            - "cluster:hypervisor_list.!add": "libvirt"
            - "wizard:Storage.ceph": "disable"
	      label: "dialog.create_cluster_wizard.compute.kvm"
          description: "dialog.create_cluster_wizard.compute.kvm_description"
        vcenter:
          type: "checkbox"
          weight: 10
          label: "dialog.create_cluster_wizard.compute.vcenter"
          description: "dialog.create_cluster_wizard.compute.vcenter_description"
          bind:
            - "cluster:hypervisor_list.!add": "libvirt"
            - "wizard:Storage.ceph": "disable"
      Network:
        neutron_plugin:
          type: "radio"
          values:
            - data: "neutron-vlan"
              label: "dialog.create_cluster_wizard.network.neutr_vlan"
              description: "dialog.create_cluster_wizard.network.neutr_vlan_description"
              restrictions:
                - "Compute.vcenter == true": "dialog.create_cluster_wizard.network.hypervisor_alert"
              bind:
                - "cluster:net_provider": "neutron"
                - "cluster:net_segment_type": "vlan"
            - data: "neutron-gre"
              label: "dialog.create_cluster_wizard.network.neutr_gre"
              description: "dialog.create_cluster_wizard.network.neutr_gre_description"
              restrictions:
                - "Compute.vcenter == true": "dialog.create_cluster_wizard.network.hypervisor_alert"
              bind:
                - "cluster:net_provider": "neutron"
                - "cluster:net_segment_type": "gre"
            - data: "nova-network"
              label: "dialog.create_cluster_wizard.network.nova_network"
              description: "dialog.create_cluster_wizard.network.nova_network_description"
              bind:
                - "cluster:net_provider": "nova_network"


REST API impact
---------------

/api/releases Nailgun API is affected, will return a wizard metadata with mixed
parts from plugins.

Upgrade impact
--------------

No extrnal dependencies added

Security impact
---------------

No impact

Notifications impact
--------------------

No impact

Other end user impact
---------------------

End user will see the new wizard's Compute and Network panes in Fuel UI.
CLI should support a listing of available HVs and network backends and
relationships netween them.

Performance Impact
------------------

Not applicable

Plugin impact
-------------

Plugins can add new network backends and hypervisors. This information will be
taken from environment_config.yaml. A new section "wizard" should be added for
this.

Other deployer impact
---------------------

No impact

Developer impact
----------------

No impact

Infrastructure impact
---------------------

No impact

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  
  Anton Zemlyanov - azemlyanov

Other contributors:

  Andrei Danin - adanin

Work Items
----------

- update wizard's Compute Pane to use checkboxes
- update wizard's Network Pane to use Neutron and ML2 drivers
- introduce a merge mechanism in Naigun /api/releases handler
- Add necessary actions into Fuel CLI


Dependencies
============

* https://blueprints.launchpad.net/fuel/+spec/role-as-a-plugin

Testing
=======

- manual testing
- UI wizard functional tests update

Documentation Impact
====================

Fuel Users Guide should be updated, Create cluster wizard section

References
==========

[0] https://blueprints.launchpad.net/fuel/+spec/role-as-a-plugin

http://storage4.static.itmages.com/i/15/0617/h_1434550933_8693687_954fa15ccf.png
http://storage4.static.itmages.com/i/15/0617/h_1434551033_4332075_8e85a8fe7d.png

