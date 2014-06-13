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

nailgun currently provides

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

and

.. code-block:: yaml

  quantum_settings:
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


Puppet modules

Items to discuss:

* sanitize_network_config: should be removed, we should be doing any of this
  testing in NeutronDeploymentSerlializer.
* waistline: appears to be un-necessary and should be removed.
* create_predefined_networks_and_routers: there are now separate handlers for
  these, we should use them instead.

Follow-up actions (what to do after this bp):

* possibly clean up q-agent-cleanup.py, there is open bug about time it
  takes to run
* Its not necessary to run DHCP agent in HA, we can run more than one per
  network as HA solution.
* need to support linuxbridge, this should be simply allowing network_scheme
  in astute.yaml to have less data, and passing slightly different data to
  quantum_settings.
* ml2-plugin supports multiple type_drivers at a time, nailgun and UI should
  be updated to allow for this as well.



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

Possible change in layout of astute.yaml

Performance Impact
------------------

New code should reduce dependancy complexity and hopefully improve deployment
performance.

Other deployer impact
---------------------

quantum_settings should be further re-factored to more closely resemble the
 data structure consumed by the neutron model, however it's not a priority at
 this time.

Developer impact
----------------

this will change the astute.yaml layout which would case it to become
incompatible with older versions.

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

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


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