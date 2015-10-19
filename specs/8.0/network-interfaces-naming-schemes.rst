..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================================
Use the predictable network interfaces' names
=============================================

The URL of the launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/network-interfaces-naming-schemes

Allow arbitrary names for network interfaces in Fuel.
The practical reason is to fix known issues for classical naming policy by
using the predictable interface naming policy.


-------------------
Problem description
-------------------

Currently Fuel relies on an old-fashioned (classical) ethX network interfaces
naming. Such a naming is known to be unstable in the following ways::
  1) two machines with the same hardware can have different interface naming.
     Consider two machines having an on board NIC and the one installed into
     PCI-E slot. Depending on luck the name of the interface corresponding to
     the on-board NIC can be eth0 on machine 1, and eth1 on machine 2.
  2) the interfaces' names are not preserved across the reboots.

The 2nd problem can be solved by udev rule which pins the interface name to
the MAC address of the NIC. Solving the 1st problem requires a different
naming convention, such as the predictable network interfaces' names (as
implemented in udev >= 197). Modern Linux distributions (Ubuntu >= 15.04,
CentOS >= 7) use this scheme by default, and it can be enabled in Ubuntu
14.04 (and Debian Jessie).

Switching to predictable interface naming policy doesn't require pinning
interface name to the MAC address. The udev rules do that, if any, can be
preserved for backward compatibility with the classical naming policy.

Hard-coded interface names ethX in Fuel code should be changed to support
arbitrary interface naming schemes. Fighting the naming convention used by
all major Linux distributions takes too much effort, it's simpler to adapt
Fuel instead.

By default, systemd will name Ethernet interfaces using different from the
conventional policy and can apply one of supported naming schemes. See the
link for details about naming schemes:
http://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames/

Example of classical interface naming, the interfaces are named as "eth0" ,
"eth1"::

  $ ip -4 link
  2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP
        mode DEFAULT qlen 1000 link/ether 00:50:56:9c:74:4d brd ff:ff:ff:ff:ff:ff
  3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP
        mode DEFAULT qlen 1000 link/ether 00:50:56:9c:03:0a brd ff:ff:ff:ff:ff:ff

Example of interface naming based on physical location of the hardware
(PCI bus). The interfaces are named as "enp0s3" , "enp0s8"::

  $ ip -o -4 link
  2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast
        state UP mode DEFAULT qlen 1000
        link/ether 08:00:27:4b:f0:40 brd ff:ff:ff:ff:ff:ff
  3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast
        state UP mode DEFAULT qlen 1000
        link/ether 08:00:27:bc:4d:85 brd ff:ff:ff:ff:ff:ff

Example of interface naming based on MAC addresses. The interfaces are named
as "enx0800274bf040" and "enx080027bc4d85"::

  $ ip -o -4 link
  2: enx0800274bf040: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
        qdisc pfifo_fast state UP mode DEFAULT qlen 1000
        link/ether 08:00:27:4b:f0:40 brd ff:ff:ff:ff:ff:ff
  3: enx080027bc4d85: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
        qdisc pfifo_fast state UP mode DEFAULT qlen 1000
        link/ether 08:00:27:bc:4d:85 brd ff:ff:ff:ff:ff:ff

Ethernet interfaces could also have names incorporating Firmware/BIOS provided
index numbers for on-board devices (example: eno1), names incorporating
Firmware/BIOS provided PCI Express hotplug slot index numbers (example: ens1).

----------------
Proposed changes
----------------

Fuel should support the predictable interfaces' names and use it by default.
Hard-coded interface names and regular expressions bounded to a particular
naming policy should be avoided in the code.

Here are examples from the code (written in bash), which should be re-worked.
The "eth0", "eth1" and "eth." should be changed in the code below ::

  # THIS CODE IS BROKEN
  ADMIN=eth0
  PUBLIC=eth1
  ALL_ETH_IP=$(ip -o -4 addr | grep "eth." | awk '{print \$4 }' | cut -d/ -f1)

There are default settings (expectations) in Fuel. For example, the interface
eth0 is expected to be an admin interface by default now.

Since Ethernet interfaces could have any names (we can't predict which one it
would be), and to preserve backward compatibility with the current classical
naming schema (ethX), the following approach is proposed for changes in code:

1. List of physical Ethernet interfaces should be collected from the system.
2. This list is sorted in alphabetic order.
3. The very first interface from the sorted list is assigned to the role of
   eth0, the second interface is assigned to the role of eth1 , etc ...

The function gathering Ethernet network interface names is required to
implement the feature. The function should collect information about only
physical Ethernet interfaces in the system (avoid virtual, e.g. loopback,
tunnel, VLAN, bound interfaces ... etc and wireless ).

Web UI
======

The feature doesn't require changing the web UI, the possible impact is
a variable size for an interface names placeholder.

Alexey Shtokolov: "Read the spec and don't see how it affects UI. If it's
just change of network interface names which are shown in UI - no changes on
UI side are needed".


Nailgun
=======

None.
No changes to the architecture, tasks and encapsulated business logic.
Possible changes (if any) are connected to the implementation of network
interface filtering templates 'eth*', which should be avoided to use in the
code.


Data model
----------

None.


REST API
--------

None.


Orchestration
=============

None.


RPC Protocol
------------

None.


Fuel Client
===========

TODO:

Fuel Client is a tiny but important part of the ecosystem. The most important
is that it is used by other people as a CLI tool and as a library.

This section should describe whether there are any changes to:

* HTTP client and library

* CLI parser, commands and renderer

* Environment

It's important to describe the above-mentioned in details so it can be fit
into both user's and developer's manuals.


Plugins
=======

TODO:

Plugins are ofter made by third-party teams. Please describe how these changes
will affect the plugin framework. Every new feature should determine how it
interacts with the plugin framework and if it should be exposed to plugins and
how that will work:

* Should plugins be able to interact with the feature?

* How will plugins be able to interact with this feature?

* There is something that should be changed in existing plugins to be
  compatible with the proposed changes

* The proposed changes enable or disable something for new plugins

This section should be also described in details and then be put into the
developer's manual.


Fuel Library
============

(V Kuklin): "Fuel Library is abstract enough to be interface name agnostic.
We use bridges with names like 'br-mgmt' and this is matter of Nailgun to
decide which port to put into which bridge. The only problem here is to
retain interface mapping on-bootstrap/installation/post-installation phases
which is a matter of fuel-agent and Nailgun teams."

In the case when interface names are passed correctly to the fuel-library,
no issues are expected.

The Puppet manifests contains default (hard-coded) interface names like eth0,
which names and IP address are taken if nothing is specified. This might be
an issue. It's suggested to gather a least of the real interfaces (presented
in the system) and modify the manifests correspondingly.

------------
Alternatives
------------

None.
We can stick to the classicall interface naming schema, but it does not allow
us to work with contemporary Linux distributives using another network
interface naming policies and prevent from including already deployed hosts
(like RHEL) to Fuel environment.

--------------
Upgrade impact
--------------

Upgrading from CentOS 6.x to CentOS 7.0 lead to change network interface
naming policy and can break a network configuration used before the upgrade.

The simplest solution is do not do upgrade at all.

In case of upgrade, the plausible solution is to stick to hardware (MAC)
addresses during the upgrade, when the naming of network interfaces are
changed. The (upgrade) scripts should collect information about current
network configuration and modify the configs in way preserving current
interfaces' roles.


---------------
Security impact
---------------

None.

--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

TODO:

Aside from the API, are there other ways a user will interact with this
feature?

* Does this change have an impact on python-fuelclient? What does the user
  interface there look like?


------------------
Performance impact
------------------

None.


-----------------
Deployment impact
-----------------

TODO:

Discuss things that will affect how you deploy and configure Fuel
that have not already been mentioned, such as:

* What configuration options are being added? Should they be more generic than
  proposed? Are the default values ones which will work well in
  real deployments?

* Is this a change that takes immediate effect after it is merged, or is it
  something that has to be explicitly enabled?

* If this change is a new binary, how can it be deployed?

* Please state anything that those doing continuous deployment, or those
  upgrading from the previous release, need to be aware of. Also describe
  any plans to deprecate configuration values or features.  For example, if a
  directory with instances changes its name, how are instance directories
  created before the change handled?  Are they get moved them? Is there
  a special case in the code? Is it assumed that operators will
  recreate all the instances in their cloud?


----------------
Developer impact
----------------

TODO:

Discuss things that will affect other developers working on Fuel,
such as:

* If the blueprint proposes a change to the driver API, discussion of how
  drivers would implement the feature is required.


--------------------------------
Infrastructure/operations impact
--------------------------------

None.


--------------------
Documentation impact
--------------------

None.

--------------------
Expected OSCI impact
--------------------

None.

--------------
Implementation
--------------

Assignee(s)
===========

TODO:

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  asyriy

Other contributors:
  isuzdal

Mandatory design review:
  aadamov
  agordeev
  aheczko
  aurlapova
  dpyzhov
  ikalnitsky
  msemenov
  sgolovatiuk
  svasilenko
  vkozhukalov
  vkuklin


Work Items
==========

TODO:

Work items or tasks -- break the feature up into the things that need to be
done. Those parts might end up being done by different people, but we're
mostly trying to understand the timeline for implementation.


Dependencies
============

None.

-----------
Testing, QA
-----------

We are having impact on two subsystems: fuel-devops and fuel-qa.
Jenkins jobs are not affected.

Impact on fuel-devops
=====================
The main impact is to create interfaces in predictable way.
Currently we create interfaces based on infomation from
fuel-devops/devops/settings.py, lines are like:
DEFAULT_INTERFACE_ORDER = 'admin,public,management,private,storage'
'admin': ['eth0', 'eth1']
There is a work in fuel-qa/fuel-devops
https://blueprints.launchpad.net/fuel/+spec/template-based-testcases
to move that to yaml files with settings, so it is going to be fixed anyway.
Later changes will require simple rename in yaml files.

Interface order is used  to correctly create interfaces in virtual domains.
Currently INTERFACE_ORDER is primary source of truth. Based on
that ordering we map networks to interfaces.
fuel-devops/devops/models/environment.py
def create_interfaces(self, networks, node,
                      model=settings.INTERFACE_MODEL):
interfaces = settings.INTERFACE_ORDER
    if settings.MULTIPLE_NETWORKS:
        logger.info('Multiple cluster networks feature is enabled!')
    if settings.BONDING:
        interfaces = settings.BONDING_INTERFACES.keys()

Also, IPMI driver is slightly affected:
fuel-devops/devops/driver/ipmi/ipmi_driver.py
class DevopsDriver(object):
interface_install_server='eth0',
def _create_boot_menu(self, interface='eth0',

And node model. It is enough to rename eth0 to correctly mapped
first interface.
fuel-devops/devops/models/node.py
def pxe_boot_interface_is_eth0(self):
@property
def interfaces(self):
    return self.interface_set.order_by('id')

Impact on fuel-qa
=================
The main impact in fuel-qa is a communication with the nailgun.
With current nailgun scheme we need just to change
interface information updates in fuel-qa/fuelweb_test/models/fuel_web_client.py
There are 14 lines to send to nailgun interfaces.
Need to carefully update them with information from yaml files and devops.
For now we need to update info based on INTERFACE_ORDER and test logic.

Simple fix in tests of fuel contrail plugin.
fuel-qa/fuelweb_test/tests/plugins/plugin_contrail/test_fuel_plugin_contrail.py
raw_data = [{
            'mac': None,
            'mode': 'active-backup',
            'name': 'bond0',
            'slaves': [
                {'name': 'eth4'},
                {'name': 'eth2'},
            ],

Also, simple fix in dhcrelay_check
fuel-qa/fuelweb_test/models/environment.py
def dhcrelay_check(self):
    with self.d_env.get_admin_remote() as admin_remote:
        out = admin_remote.execute("dhcpcheck discover "
                                   "--ifaces eth0 "

Simple replace of 'eth*' in currently used network templates.
fuel-qa/fuelweb_test/network_templates/\*.yaml

This is a folder with yaml files which are going to be
base for tests. Same as above - replace 'eth*' is enough.
fuel-qa/system_test/tests_templates/

Acceptance criteria
===================

Fuel should work well with different Ethernet interface naming policy.
In general Ethernet interface can have an arbitrary name.

----------
References
----------

http://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames/
https://bugs.launchpad.net/fuel/+bug/1494223
https://bugs.launchpad.net/mos/+bug/1487044
https://review.openstack.org/#/c/223939



