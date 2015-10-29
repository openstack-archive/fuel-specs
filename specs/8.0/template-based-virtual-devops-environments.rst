..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================================
Use YAML templates for creating new virtual devops environments
===============================================================

https://blueprints.launchpad.net/fuel/+spec/template-based-virtual-devops-environments

Describing virtual devops environments in YAML templates for #fuel-devops gives
much more flexible configuration options for creating environments and allows
to implement some additional functionality that weren't possible before.

--------------------
Problem description
--------------------

fuel-devops project has a certain amount of limitations and hardcode:

* All settings are provided through the fixed amount of environment variables
  that should set some configuration options or enable some features.
  It is difficult to consider them all for inexperienced users.
  For some settings it is difficult to understand how the setting will affect
  the environment.

* There are a lot of environment variables, and there are a lot of code that
  process each of the provided settings (or defaults) and resolve possible
  conflicts between certain settings.

* It is impossible to reproduce the existing environment configuration without
  setting a lot of environment variables that must be given exactly as in the
  original environment. But there is no way to find which of the environment
  variables were changed for making the original environment.
  This complicates run system tests on CI or locally, requiring to
  configure a lot of different settings manually, or hardcode a single set
  of settings for all system tests in the run.

* However, a lot of settings remained hardcoded, for example:

  * the same amount of vcpus for all slaves. It is impossible to set increased
    amount of vcpus for certain nodes;
  * the same amount of memory for all slaves. It is impossible to set different
    memory size for different nodes (for example, for further 'compute' and
    'storage' nodes)
  * the same amount of network interfaces and networks attached to them on all
    slaves. It is impossible to get flexible network topologies, and any
    additional topology requires a lot of additional hardcode.
  * the same amount and sizes of disk devices for all slaves. It is impossible
    to set several volumes only for nodes that will become a storage; it is
    impossible to use an external image as a volume for a node where it should
    be used.

* It is difficult to extend the settings for each node: custom hostnames,
  custom network interfaces names, custom settings for baremetal nodes, etc.

* It is difficult to describe and manage multi-rack environments, hybrid
  environments with mixed hypervisors, some nodes with dedicated roles that
  should not be used directly from tests but should be managed as a part of the
  environment.

----------------
Proposed changes
----------------

Settings for #fuel-devops are separated into host-related settings (django,
qemu, vnc password, and other static settings) and environment-related
settings.

* Settings related to the virtual devops environment should be moved to
  templates with such structure that allows to describe each necessary detail
  for each part of the environment.
* Template should be easily scalable for additional settings if necessary.
* Hypervisor driver model should be node-related instead of environment-related
  to get environments with nodes on mixed hypervisor or baremetal drivers.
* Node 'role' should be used for extending the 'Node' model via external
  modules to get some additional steps for node creation or extend the node
  methods for any custom role that defined in template.
* Various network topologies should be easily described for reflecting any
  possible configuration.


YAML template
-------------

There is a main section 'template' that can contain several sub-sections for
different proposes. One of these sub-sections is 'devops_settings' where
located all necessary settings for #fuel-devops. In the other sub-sections
can be settings for a test case for the environment. Thus, one template can
contain settings for a virtual devops environment and for test case that
might be performed on this environment.

The tag '!os_env' is used for get various settings to template directly from
environment variables if it is necessary:  !os_env SOME_VAR[, <devaful_value>]
For example:

- !os_env ISO_PATH                # ISO_PATH is the required variable
- !os_env SLAVE_NODE_MEMORY, 3072    # SLAVE_NODE_MEMORY is optional,
                                      # default is 3072

The tag '!include' is used for inserting YAML objects from an another
YAML file.

Base structure of the YAML template:

::
    ---
    template:
      devops_template:
        ...
        network_pools:
        ...
        groups:
          ...
          driver:
            ...
          l2_network_devices:
            ...
          nodes:
            ...

* template: The main section where are located different sub-sections such as
  'devops_template' and 'cluster-template' (see [1] for additional details).

* devops_template: This section contains all data that describes configuration
  of nodes and networks for an existing hardware or virtual environment, or for
  the virtual/hybrid environment which is created by this configuration.

* network_pools: Reserve address pools and VLAN tags for networks in the
  current group. In different groups can be reserved a different pool for the
  same L3 network.
  -  baremetal pool: if 'net' is specified as x.x.x.x/YY , then the network is
     stored 'as is', 'gateway' and at least one element in 'ip_ranges' is
     required.

  -  virtual pool: if 'net' is specified as x.x.x.x/YY:ZZ , where YY > ZZ, then
     the network x.x.x.x/ZZ will be dynamically allocated from the network
     range x.x.x.x/YY. In this case 'gateway' and 'ip_ranges' will be set
     automatically.

* groups: Each group can use a different driver for accessing network and node
  devices, use different network devices for each group.
  -  There can be a group for 'libvirt' driver and a group for 'ipmi' driver in
     the hybrid environment.
  -  Two groups with 'libvirt' driver and different lists of network devices
     can describe 'multirack' configuration

* driver: Describes a driver that should be used to manage networks and nodes.
  Can be 'libvirt' driver for virtual environments, 'ipmi' driver for baremetal
  nodes, or any additional custom driver.
  - the driver name should be a path to a python module with the driver:
    name: devops.driver.libvirt.libvirt_driver
  - other driver-specific options are placed in this section.

* l2_network_devices: List of network devices used in the current group.
  It is used for connecting node interfaces to the specified network devices.
  In case of 'libvirt' driver, there is a list of libvirt networks with
  additional properties such as forwarding mode, dhcp, network_pool used for
  the network, etc. In case of another driver there can be another list of
  parameters used by the driver, or the section can be omitted if not used.
  - network_pool specifies which address pool should be used, in the following
    format:

    network_pool: public

    , or:

    network_pool: public:0

    , where 'public' is the name of the OpenStack network, and ':0' is the
    number of the pool configured to 'public'.

    It allows to get several dynamic address pools for a network, but for
    different groups use only specific pools from the network: the same pool
    for all groups or different pools for some groups.

* nodes: List of nodes, where is described configuration of virtual or
  baremetal nodes: memory size, number of CPU cores, disks, network interfaces
  and some additional parameters, if it is necessary.

  - Node 'role' is also the name of a model extension with the name, for
    example, 'fuel_admin' in the example below. This extension can be empty
    for some roles, or contain pre- and post-create methods to make some
    preparations for some specific node roles.
    It will allow to automatically prepare environment with installed Fuel
    admin node (several different roles could be added for several Fuel
    versions to support version-specific deployment processes); to
    prepare nodes with installed and configured OVS for multi-rack and
    multi-host features; or for any other preparations for various roles and
    cases.


Example of the YAML template format:
------------------------------------

::
    ##############
    # Main section
    ##############
    template:

      ######################################
      # Sub-section for fuel-devops settings
      ######################################
      devops_template:

        # Required option: env_name
        env_name: !os_env ENV_NAME

        ######################################
        # Address pools for OpenStack networks
        ######################################
        network_pools:  # type: dict of lists

          # Actual names of OpenStack networks could be useful here as the
          # keys, so the external components like #fuel-qa could get
          # the necessary pool by the common name of the network.

          fuelweb_admin:
           - net: !os_env POOL_DEFAULT, 10.109.0.0/16:24
             tag: 0

          public:  # multiple network pools can be set for further purposes

           - net: !os_env POOL_DEFAULT, 10.109.0.0/16:24
             tag: 100
             ip_ranges:
              -          # If several empty elements are specified, then
              -          # several equal sized ranges will be generated.

           - net: 209.30.42.64/26  # An external network pool example
             gateway: 209.30.42.65
             # ip_ranges should be inside the net. for fuel-qa tests, first
             # range can be used for 'public range', and the rest ranges -
             # for 'floating ranges'.
             ip_ranges:
              - [209.30.42.66, 209.30.42.94]
              - [209.30.42.98, 209.30.42.121]
             tag: 200

          storage:
           - net: !os_env POOL_DEFAULT, 10.109.0.0/16:24
             tag: 101
          management:
           - net: !os_env POOL_DEFAULT, 10.109.0.0/16:24
             tag: 102
          private:
           - net: !os_env POOL_DEFAULT, 10.109.0.0/16:24
             tag: 103

        ######################################################################
        # Groups are used for describing multi-rack or multi-host environments
        # Each group has it's own hypervisor or baremetal driver
        ######################################################################
        groups:  # type: list of dicts
         - name: rack-01

           #######################################################
           # Settings for libvirt driver used in the current group
           #######################################################
           driver:  # type: dict
             # Various driver-specific options here
             name: devops.driver.libvirt.libvirt_driver

             # For different groups, different hosts with libvirt can be used
             connection_string: !os_env CONNECTION_STRING, qemu:///system
             storage_pool_name: !os_env STORAGE_POOL_NAME, default
             stp: True
             hpet: False
             use_host_cpu: !os_env DRIVER_USE_HOST_CPU, true


           ################################################################
           # List of network devices (libvirt bridges / baremetal switches)
           ################################################################
           l2_network_devices:
             admin01:
               # Name of the network pool that will be used for creating the
               # virtual network
               network_pool: fuelweb_admin:0
               # Other parameters for the libvirt network
               dhcp: false
               forward:
                 mode: nat

             public01:
               network_pool: public:0
               dhcp: false
               forward:
                 mode: nat

             bond01:
               dhcp: false
               forward:
                 mode: hostonly


           #################################################
           # List of settings for nodes in the current group
           #################################################
           nodes:  # type: list of dicts

            - name: admin       # Custom name of VM
              role: fuel_admin  # This role is used for Fuel admin node

              # Here can be located settings for IPMI credentials of baremetal
              # driver or SSH credentials (if it is necessary here) to access
              # some already deployed nodes.

              # Following settings are used for creating a virtual node instead
              # of baremetal node:

              # Amount of virtual CPUs
              # ----------------------
              vcpu: !os_env ADMIN_NODE_CPU, 2

              # Amount of node memory in MB
              # ---------------------------
              memory: !os_env ADMIN_NODE_MEMORY, 3072

              # Boot order
              # ----------
              boot:
               - hd
               - cdrom           # for boot from usb - without 'cdrom'

              # Volumes that should be created and attached to the node.
              # --------------------------------------------------------
              volumes:  # type: list of dicts
                 # Empty volume with the specified size in GB
               - name: system
                 capacity: !os_env ADMIN_NODE_VOLUME_SIZE, 75
                 format: qcow2

                 # Volume that will be filled from the specified source image
               - name: iso
                 # If 'source_image' set, then the capacity of the volume
                 # is calculated from the image size.
                 source_image: !os_env ISO_PATH
                 format: raw
                 device: cdrom   # for boot from usb - 'disk'
                 bus: ide        # for boot from usb - 'usb'

              # Interfaces are described how many network interfaces has the
              # node and how they are connected to l2_network_devices
              # ------------------------------------------------------------
              interfaces:
               - label: enp2s0              # First interface is not connected
               - label: enp2s1              # Second interface is not connected
               - label: enp3s0              # Third interface is connected
                 l2_network_device: admin01  # to the l2 network device admin01

              # Here is described which OpenStack networks are assigned to
              # which network interfaces on the node.
              # This information is useful for external frameworks such as
              # fuel-qa, to get networks assigned correctly for nodes with
              # different configurations.
              # ----------------------------------------------------------
              network_config:
                enp3s0:
                  networks:
                   - fuelweb_admin


              # Typical slave node with bonded interfaces
              # -----------------------------------------
            - name: slave-01
              role: fuel_slave
              vcpu: !os_env SLAVE_NODE_CPU, 2
              memory: !os_env SLAVE_NODE_MEMORY, 3072
              boot:
                - network
                - hd
              volumes:
               - name: system
                 capacity: !os_env NODE_VOLUME_SIZE, 50
                 format: qcow2
               - name: cinder
                 capacity: !os_env NODE_VOLUME_SIZE, 50
                 format: qcow2
               - name: swift
                 capacity: !os_env NODE_VOLUME_SIZE, 50
                 format: qcow2
              interfaces:
               - label: eth0
                 l2_network_device: admin01
               - label: eth1
                 l2_network_device: public01
               - label: eth2
                 l2_network_device: bond01
               - label: eth3
                 l2_network_device: bond01
               - label: eth4
                 l2_network_device: bond01
               - label: eth5
                 l2_network_device: bond01
              network_config:
                eth0:
                  networks:
                   - fuelweb_admin
                eth1:
                  networks:
                   - public
                bond0:  # In case of 'aggregation', interface bond0 should be
                        # used by an external framework such as fuel-qa for
                        # customize node settings before deploy.
                  networks:
                   - management
                   - storage
                   - private
                  aggregation: active-backup
                  parents:
                   - eth2
                   - eth3
                   - eth4
                   - eth5

Web UI
======

None

Nailgun
=======

None

Data model
----------

None

REST API
--------

None

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

None

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

None

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

--------------------------------
Infrastructure impact
--------------------------------

Some shell commands for dos.py will be changed (that create and scale the
devops environment).
There should be no impact to CI because remains back-compatibility to fuel-qa
tests and 'dos.py start/stop/destroy/erase'

--------------------
Documentation impact
--------------------

Documentation for using updated #fuel-devops should be created, it is in
work items.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Dennis Dmitriev (ddmitriev): ddmitriev@mirantis.com

Other contributors:
  Dmitry Tyzhnenko (dtyzhnenko): dtyzhnenko@mirantis.com
  Kirill Rozin: krozin@mirantis.com
  Anton Studenov: astudenov@mirantis.com

Mandatory design review:
  None

Work Items
==========

- Rewrite environment creation methods in common way to get parameters from
  a template.
- Add API compatibility layer to make a template on-the-fly from old-style
  environment creation with environment variables.
- Switch #fuel-devops to use sqlite3 for easier installation.
- Extend the data model to support different node groups with each own
  driver settings inside a single environment, updated node model, node roles
  extensions, and updated network model.
- Documentation in [] should be updated.

Dependencies
============

None

------------
Testing, QA
------------

None

Acceptance criteria
===================

- Environment can be created from a specified template.
  Example templates in YAML format can be found in [2].
- API remains back-compatible to previous versions.

----------
References
----------

[1] - https://review.openstack.org/#/c/239895/4/specs/8.0/template-based-testcases.rst
[2] - https://review.openstack.org/#/c/238105/
[3] - https://docs.fuel-infra.org/fuel-dev/devops.html
