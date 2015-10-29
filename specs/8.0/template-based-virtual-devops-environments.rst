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

Here is where you cover the change you propose to make in detail. How do you
propose to solve this problem?

If this is one part of a larger effort make it clear where this piece ends. In
other words, what's the scope of this effort?


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

The tag '!get_env' is used for get various settings to template directly from
environment variables if it is necessary:  !get_env SOME_VAR[, <devaful_value>]
For example:

- !os_env_get ISO_PATH                # ISO_PATH is required
- !get_env SLAVE_NODE_MEMORY, 3072    # SLAVE_NODE_MEMORY is optional,
                                      # default is 3072

Example of the YAML template format:
------------------------------------

::

    # Main section
    template:
      ...

      # Sub-section for fuel-devops settings
      devops_settings:

        # Required option: env_name
        env_name: !os_env ENV_NAME

        # Dict of virtual or/and physical networks for the current group
        devops_nets:  # type: dict of dicts
          ...
          bond0:            # A name for a devops network device
            # Various network-specific options here such as address pool,
            # or/and forwarding type and dhcp for virtual networks.
            ...
            networks:       # List of openstack networks that should be
             - management   # assigned to the devops network 'bond0' from
             - storage      # the tests. It is just a reference information.
             - private

        # Groups are used for describing multi-rack or multi-host environments.
        # Each group has it's own hypervisor or baremetal driver.
        groups:  # type: list of dicts
         - name: rack-01

           driver:  # type: dict
             # Various driver-specific options here
             name: devops.driver.libvirt.libvirt_driver
             connection_string: !os_env CONNECTION_STRING, qemu:///system
             storage_pool_name: !os_env STORAGE_POOL_NAME, default
             ...


           # List of settings for nodes in the current group
           nodes:  # type: list of dicts
            ...
            - name: admin       # Custom name of VM
              role: fuel_admin  # This role is used for Fuel admin node

              # Here can be located settings for IPMI credentials of baremetal
              # driver or SSH credentials (is it necessary here?) to access
              # some already deployed nodes.

              # Following settings are used for creating a virtual node instead
              # of baremetal node:

              # amount of virtual CPUs
              vcpu: !os_env ADMIN_NODE_CPU, 2

              # amount of node memory in MB
              memory: !os_env ADMIN_NODE_MEMORY, 3072

              # Boot order
              boot:
               - hd
               - cdrom  # for boot from usb - without 'cdrom'

              # Volumes that should be created and attached to the node.
              volumes:  # type: list of dicts
               ...
                 # Empty volume with specified size in GB
               - name: admin_system
                 capacity: !os_env ADMIN_NODE_VOLUME_SIZE, 75
                 format: qcow2

                 # Volume that will be filled from the specified source image
               - name: admin_iso
                 # If 'source_image' set, then volume capacity is calculated
                 # from the image size.
                 # ISO_PATH doens't have a default value so it is required here
                 source_image: !os_env ISO_PATH
                 format: raw
                 device: cdrom   # for boot from usb - 'disk'
                 bus: ide        # for boot from usb - 'usb'
               ...

              # List of node interfaces and attached networks to them
              interfaces:     # type: list of dicts
               - name: eth0   # Name is just a symbolic label which can be
                              # used from test cases
                 net: bond0   # Net is one of devops_nets
               - name: eth2
                 net: bond0
               - name: eth3
                 net: bond0
               - name: eth4
                 net: bond0
               - name: eth5
                 net: admin0
               - name: enp2s0
                 net:         # interface that is not accosiated to any network
               - name: enp2s1
                 net:


* Node 'role' is also the name of a model extension with the name 'fuel_admin'
  in the example above. This extension can be empty for some roles, or contain
  pre- and post-create methods to make some preparations for some specific
  node roles. It will allow to automatically prepare environment with
  installed Fuel admin node (several different roles could be added for several
  Fuel versions to support version-specific deployment processes); to prepare
  nodes with installed and configured OVS for multi-rack and multi-host
  features; or for any other preparations for various roles and cases.

* Each node 'group' has it's own driver, so can be used (local or remote)
  libvirt for one node group and IPMI driver for other node group.

* 'devops_nets' are the logical devices (libvirt bridges, (group of) hardware
  switches) that provide access to some OpenStack networks for the nodes.
  The same logical device (with the same network address pools for OpenStack
  networks) can be used in different node groups, or a separated logical
  devices can be assigned to nodes in various order.

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
Infrastructure/operations impact
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

--------------------
Expected OSCI impact
--------------------

None

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
- Extend django data model to support different node groups with each own
  driver settings inside a single environment, updated node model, node roles
  extensions, and updated network model.

Dependencies
============

None

------------
Testing, QA
------------

None

Acceptance criteria
===================

- Environment can be created from a specified template
- API remains back-compatible to previous versions

----------
References
----------

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
