..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Fuel Multiple Hypervisor Networking
==========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-multi-hv-networking

Allow a user to choose in the Fuel UI wizard multiple hypervisors and a
suitable Neutron plugin for them. Also allow Fuel plugins to extend HV and
Neutron plugins options in the wizard.

Problem description
===================

We are going to get rid of supporting Nova-Network in Fuel 7.0 making Neutron
the only option [0]_.

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

- Move the Qemu/KVM switch to the Settings tab because it's not the HV from
  the OSt stand point. It's just a libvirt setting.
- Redesign the Compute wizard pane to support multiple selections of HVs.
- Allow Fuel plugins to mix their options into the Compute pane like it's done
  now for the Setting tab.
- Redesign the Network wizard pane to support radio buttons for monolithic
  Neutron plugins [1]_ and multiple selections for ML2 drivers [2]_.
- Fuel Plugins should be also allowed to add monolithic options or ML2
  drivers.
- Each HV option provides its HV type, like "libvirt" or "vmware". Each
  Neutron monolithic plugin or ML2 driver reports HV types it's able to
  support. A user choose one or more HVs first and then select a suitable
  network backend. The wizard may hide/disable inappropriate Neutron
  options based on selected HVs.
- A user is allowed to select one of the monolithic Neutron plugins or, in
  case he chose ML2 plugin, he is able to select one or more ML2 drivers. The
  "Next" button will be blocked until a set of chosen ML2 dirvers may cover
  all HVs selected on the previous step.
- Fuel Puppet manifests should respect new fields with a list of HVs enabled
  and a chosen Neutron backend. To do this best we need to make deploy tasks
  more isolated and independent. But this isolation improvement may wait till
  the next release.

Since we will have "roles from plugins" and a single graph for all tasks
with task override [3]_ a Fuel plugin may fairly easy alternate Neutron
and Nova-compute configurations to add a new HV or network backend.

This is how the new wizard may look like:

.. image:: ../../images/6.1/fuel-multi-hv-networking/new-compute-pane.jpg

.. image:: ../../images/6.1/fuel-multi-hv-networking/new-network-pane.jpg

Alternatives
------------

TBD

Data model impact
-----------------

- A new JSON field 'hypervisor_list' should be added into the Cluster model.
  It will be a JSONized list of strings of HV types enabled for cluster.
- The field 'net_l23_provider' in the NeutronConfig model should mean a
  Neutron monolithic plugin used for a cluster.
- A new JSON field 'ml2_drivers' should be added into the NeutronConfig model.
  It will be a JSONized list of strings of ML2 drivers enabled for a cluster.
- A New bind operator ".!add" should be added into the UI DSL. For instance:

  ::

    mycheckbox:
      type: checkbox
      bind:
        - "cluster:hypervisor_list.!add": "libvirt"

  When a checkbox is selected it adds a string "libvirt" into the list
  "cluster:hypervisor_list" if there is no such string in it.
  When a checkbox is unselected it removes all strings "libvirt" from the
  list. So it acts more like a set rather than a list.
- New condition operators "[list1] all in [list2]" and "[list1] any in [list2]"
  should be added into the UI DSL. They check if all/any item from the list1
  are/is in the list2.
- The Network and Compute wizard panes' descriptions should be reworked.
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
        value: ml2
        bind: "cluster:net_l23_provider"
        values:
          - data: ml2
            label: "Neutron ML2 plugin"
            description: "Lorem ipsum dolor sit amet"
      ml2_drivers:
          openvswitch:
            type: checkbox
            weight: 5
            value: true
            label: "OpenVSwitch driver"
            description: "Required for controllers and must be always enabled"
            restrictions:
              - "1 == 0"
            bind:
              - "cluster:ml2_drivers.!add": "openvswitch"
          vmware_dvs:
            type: checkbox
            weight: 10
            label: "VMware vCenter Distributed vSwitch driver"
            description: "Required for VMware vCenter"
            bind:
              - "cluster:ml2_drivers.!add": "vmware_dvs"
            restrictions:
              - "not (cluster:hypervisor_list any in ['vmware'])"


REST API impact
---------------

/api/releases Nailgun API is affected, will return a wizard metadata with mixed
parts from plugins.

Upgrade impact
--------------

No external dependencies added

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

.. code:: yaml

  wizard:
    Compute:
      xen:
        type: "checkbox"
        weight: 15
        bind: 
          - "cluster:hypervisor_list.!add": "xen"
        label: "XEN server"
        description: "lorem ipsum dolor sit amet"
    Network:
      neutron_plugin:
        values:
          - data: contrail
            label: "Contrail neutron plugin"
            description: "Supports libvirt only"
            restrictions:
              - "not (cluster:hypervisor_list all in ['libvirt'])"
      ml2_drivers:
        baremetal:
          type: checkbox
          label: "Baremetal driver"
          description: "Required for Ironic"
          bind:
            - "cluster:ml2_drivers.!add": "baremetal"
          restrictions:
            - "not (cluster:hypervisor_list any in ['ironic'])"  

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
  
  Anton Zemlyanov - azemlyanov@mirantis.com

Other contributors:

  Andrei Danin - adanin@miranits.com

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

Fuel Users Guide should be updated. Create the environment creation wizard
section.

References
==========

.. [0] https://bugs.launchpad.net/fuel/+bug/1446322
.. [1] https://wiki.openstack.org/wiki/Neutron_Plugins_and_Drivers
.. [2] https://wiki.openstack.org/wiki/Neutron/ML2
.. [3] https://blueprints.launchpad.net/fuel/+spec/role-as-a-plugin
