..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Neutron ML2 plugin support for Fuel
===================================


https://blueprints.launchpad.net/fuel/+spec/ml2-neutron

Fuel needs to support this:

* Much of the newer functionality in plugins is only supported when using the
ML2 plugin.
* Using the ML2 Plugin format forces more common configuration allowing for
plugins to more easily be interchanged.
* Many of the vendor or NFV plugs only work inside ML2 plugin format.
* ML2 format allows for multiple concurrent plugins.


Problem description
===================

Monolithic Neutron plugins are deprecated in Ice-house and will be removed in
Juno. Fuel needs to be able to support this as it is the assumed entry point
for all 3rd party modules.


Proposed change
===============

Some simple changes to the data structure sent by nailgun should allow for us
to take advantage of the upstream puppet-neutron
https://github.com/stackforge/puppet-neutron module. Some work will need to
be taken in order to add back in our HA support into the module, however upon
review this action may also help to simplify the neutron module and increase
its effectiveness.

nailgun provided network scheme (consumed by l23network)

from: NeutronNetworkDeploymentSerializer.generate_network_scheme(node)
(https://github.com/stackforge/fuel-web/blob/master/nailgun/nailgun/orchestrator/deployment_serializers.py#L709)

(un-modified for reference)

.. code-block:: yaml

  network_scheme:
    provider: ovs
    interfaces:
      eth0:
        L2:
          vlan_splinters: "off"
      eth1:
        L2:
          vlan_splinters: "off"
      eth2:
        L2:
          vlan_splinters: "off"
      eth3:
        L2:
          vlan_splinters: "off"
      eth4:
        L2:
          vlan_splinters: "off"
    endpoints:
      br-mgmt:
        IP:
        - 192.168.0.4/24
      br-ex:
        gateway: 10.108.43.1
        IP:
        - 10.108.43.4/24
      br-fw-admin:
        IP:
        - 10.108.42.4/24
      br-prv:
        IP: none
      br-storage:
        IP:
        - 192.168.1.3/24
    transformations:
    - name: br-eth0
      action: add-br
    - bridge: br-eth0
      name: eth0
      action: add-port
    - name: br-eth1
      action: add-br
    - bridge: br-eth1
      name: eth1
      action: add-port
    - name: br-eth2
      action: add-br
    - bridge: br-eth2
      name: eth2
      action: add-port
    - name: br-eth3
      action: add-br
    - bridge: br-eth3
      name: eth3
      action: add-port
    - name: br-eth4
      action: add-br
    - bridge: br-eth4
      name: eth4
      action: add-port
    - name: br-ex
      action: add-br
    - name: br-mgmt
      action: add-br
    - name: br-storage
      action: add-br
    - name: br-fw-admin
      action: add-br
    - bridges:
      - br-eth4
      - br-storage
      tags:
      - 102
      - 0
      action: add-patch
    - bridges:
      - br-eth1
      - br-ex
      trunks:
      - 0
      action: add-patch
    - bridges:
      - br-eth2
      - br-mgmt
      tags:
      - 101
      - 0
      action: add-patch
    - bridges:
      - br-eth0
      - br-fw-admin
      trunks:
      - 0
      action: add-patch
    - name: br-prv
      action: add-br
    - bridges:
      - br-eth3
      - br-prv
      action: add-patch
    roles:
      ex: br-ex
      management: br-mgmt
      fw-admin: br-fw-admin
      private: br-prv
      storage: br-storage
    version: "1.0"

nailgun provided neutron configuration

from: NeutronNetworkDeploymentSerializer.neutron_attrs
(https://github.com/stackforge/fuel-web/blob/master/nailgun/nailgun/orchestrator/deployment_serializers.py#L657)

(modifications shown diff style)

.. code-block:: yaml

-  quantum_settings:
+  neutron_settings:
+   - mechanisms:
+     - ovs
+   - type_drivers:
+     - vlan
+    l2_population: true
+    arp_responder: true
    database:
      passwd: lVnpS5Qd
    metadata:
      metadata_proxy_shared_secret: VBqWVGHn
    keystone:
      admin_password: qRr8TVr8
    predefined_networks:
      net04_ext:
        shared: false
        L3:
          gateway: 10.108.43.1
          floating: 10.108.43.21:10.108.43.40
          subnet: 10.108.43.0/24
          nameservers: []

          enable_dhcp: false
        L2:
          network_type: flat
          segment_id:
          physnet: physnet1
          router_ext: true
        tenant: admin
      net04:
        shared: false
        L3:
          gateway: 192.168.111.1
          floating:
          subnet: 192.168.111.0/24
          nameservers:
          - 8.8.4.4
          - 8.8.8.8
          enable_dhcp: true
        L2:
          network_type: vlan
          segment_id:
          physnet: physnet2
          router_ext: false
        tenant: admin
    L2:
      phys_nets:
        physnet1:
          bridge: br-ex
          vlan_range:
        physnet2:
          bridge: br-prv
          vlan_range: 1000:1030
      base_mac: fa:16:3e:00:00:00
      segmentation_type: vlan
    L3:
      use_namespaces: true


Generated data from sanitize_network_config:

(un-modified for reference)

.. code-block::

  debug: importing '/etc/puppet/modules/osnailyfacter/manifests/cluster_ha.pp' in environment production
  debug: Automatically imported osnailyfacter::cluster_ha from osnailyfacter/cluster_ha into production
  debug: get_network_role_property(...): Undefined network_role 'mesh'.
  debug: -*- Actual Neutron config is: ---
    metadata:
      metadata_port: 8775
      metadata_proxy_shared_secret: G6xZ6PnO
      nova_metadata_ip: "192.168.0.2"
      metadata_ip: "169.254.169.254"
      nova_metadata_port: 8775
    polling_interval: 2
    database:
      host: "192.168.0.2"
      reconnect_interval: 2
      charset:
      database: neutron
      url: "mysql://neutron:QpHEllN9@192.168.0.2:3306/neutron?read_timeout=60"
      reconnects: -1
      username: neutron
      provider: mysql
      read_timeout: 60
      passwd: QpHEllN9
      port: 3306
    L2:
      integration_bridge: br-int
      mac_generation_retries: 32
      phys_bridges:
        - br-ex
        - br-prv
      tun_peer_patch_port: patch-int
      bridge_mappings: "physnet1:br-ex,physnet2:br-prv"
      tunnel_id_ranges:
      tunnel_bridge: br-tun
      segmentation_type: vlan
      network_vlan_ranges: "physnet1,physnet2:1000:1030"
      local_ip: "192.168.0.3"
      base_mac: "fa:16:3e:00:00:00"
      phys_nets:
        physnet2:
          bridge: br-prv
          vlan_range: "1000:1030"
        physnet1:
          bridge: br-ex
          vlan_range:
      enable_tunneling: false
      int_peer_patch_port: patch-tun
    L3:
      resync_fuzzy_delay: 5
      router_id:
      gateway_external_network_id:
      resync_interval: 40
      use_namespaces: true
      network_auto_schedule: true
      dhcp_agent:
        lease_duration: 120
        enable_isolated_metadata: false
        enable_metadata_network: false
      send_arp_for_ha: 8
      allow_overlapping_ips: true
      public_bridge: br-ex
      router_auto_schedule: true
    predefined_routers:
      router04:
        external_network: net04_ext
        tenant: admin
        internal_networks:
          - net04
        virtual: false
    amqp:
      rabbit_virtual_host: /
      protocol: tcp
      hosts: "192.168.0.3:5673,192.168.0.4:5673,192.168.0.6:5673"
      control_exchange: neutron
      heartbeat: 60
      ha_mode: true
      username: nova
      provider: rabbitmq
      passwd: JcwwbHcm
      port: "5673"
    root_helper: "sudo neutron-rootwrap /etc/neutron/rootwrap.conf"
    keystone:
      admin_password: CqQtUd0I
      admin_user: neutron
      auth_region: RegionOne
      auth_protocol: http
      auth_api_version: v2.0
      admin_email: "neutron@localhost"
      auth_host: "192.168.0.2"
      signing_dir: /var/lib/neutron/keystone-signing
      auth_url: "http://192.168.0.2:35357/v2.0"
      auth_port: 35357
      admin_tenant_name: services
    server:
      allow_bulk: true
      bind_port: 9696
      api_protocol: http
      bind_host: "192.168.0.3"
      control_exchange: neutron
      report_interval: 5
      agent_down_time: 15
      api_url: "http://192.168.0.2:9696"
    predefined_networks:
      net04_ext:
        L2:
          network_type: flat
          physnet: physnet1
          segment_id:
          router_ext: true
        L3:
          gateway: "10.108.48.1"
          enable_dhcp: false
          floating: "10.108.48.11:10.108.48.20"
          nameservers: []
          subnet: "10.108.48.0/24"
        shared: false
        tenant: admin
      net04:
        L2:
          network_type: vlan
          physnet: physnet2
          segment_id:
          router_ext: false
        L3:
          gateway: "192.168.111.1"
          enable_dhcp: true
          floating:
          nameservers:
            - "8.8.4.4"
            - "8.8.8.8"
          subnet: "192.168.111.0/24"
        shared: false
        tenant: admin

Puppet modules

Items to discuss:

* sanitize_network_config: should be removed, we should be doing all of this
  in NeutronNetworkDeploymentSerializer or rely on the defaults in the puppet
  manifests and neutron.
* waistline: appears to be un-necessary and should be removed.
* create_predefined_networks_and_routers: This will need to be abstracted into
  a method that can be consumed by the manifests or carried forward in the
  interim.

HA issues:

the neutron services are hard-coded into pacemaker in their respective
classes. These will need to be abstracted into a composition layer that can
then hook back into the upstream module without mangling with upstream module
code.

See https://github.com/xarses/fuel-library/commit/8278087d97e4e6c0c5793ff0f20801f9c5447b7c#diff-6

the services with pacemaker/corosync are:

* neutron-l3-agent
* neutron-dhcp-agent
* neutron-openvswitch-agent
* neutron-metadata-agent


Alternatives
------------

We can back port relevant portions of the ml2 plugin code from upstream,
however this will further separate us from upstream which we want to work on
regardless.

Data model impact
-----------------

Some changes to the astute.yaml:

* rename quantum_settings to neutron_settings
* add setting to track mechanisms
* add setting to track type_drivers
* add setting to track if using l2_population
* add setting to track if using arp_responder


REST API impact
---------------

None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Changes in layout of astute.yaml

Performance Impact
------------------

New code should reduce dependency complexity and hopefully improve deployment
performance.

Other deployer impact
---------------------

quantum_settings should be further re-factored to more closely resemble the
 data structure consumed by the neutron model, however its not a priority at
 this time.

Developer impact
----------------

this will change the astute.yaml layout which would case it to become
incompatible with older versions.

Beyond this implementation
--------------------------

(Things out of scope for this blueprint but should be kept in mind)

Follow-up actions:

* possibly clean up q-agent-cleanup.py, there is open bug about time it
  takes to run
* Its not necessary to run DHCP agent in HA, we can run more than one per
  network as HA solution.
* need to support linuxbridge, this should be simply allowing network_scheme
  in astute.yaml to have less data, and passing slightly different data to
  quantum_settings.
* ml2-plugin supports multiple type_drivers at a time, nailgun and UI should
  be updated to allow for this as well.



Implementation
==============

Assignee(s)
-----------

Primary assignee:
  xarses (Andrew Woodward)

Other contributors:
  xenolog (Sergey Vasilenko)

Work Items
----------

:

* Research ml2-plugin usage and config 1d
* Compare current neutron plugin with upstream 1d
* Model changes to pull down upstream 2d
* Produce working prototype 2d
* Submit for review and testing 2d


Dependencies
============

* This work is inclusive of pulling upstream puppet modules


Children of this are:

* https://blueprints.launchpad.net/fuel/+spec/mellanox-features-support
* https://blueprints.launchpad.net/fuel/+spec/neutron-nsx-plugin-integration
* https://blueprints.launchpad.net/fuel/+spec/neutron-vxlan-support

Testing
=======

Current CI should provide sufficient coverage as we are not adding new
 features at this time

Upstream module contains significantly more rspec testing than current module.


Documentation Impact
====================

Docs can be updated to reflect that ml2 plugin is used, and that other options
 might be supplied.


References
==========

Branch showing current diff between two modules
https://github.com/xarses/puppet-neutron/compare/fuel-neutron?expand=1

*WIP* Branch on GitHub
https://github.com/xarses/fuel-library/compare/bp;ml2-neutron?expand=1