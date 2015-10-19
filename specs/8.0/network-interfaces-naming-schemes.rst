..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================================================
Use the predictable network interfaces' names
==================================================

The URL of the launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/network-interfaces-naming-schemes

Allow arbitrary names for network interfaces in Fuel.


Problem description
===================

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

Proposed changes
================

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

TODO:

If the proposed changes require changing the web UI please describe in details:

* How existing controls or representation is going to be changed

* What changes are required for underlying engines


Nailgun
=======

TODO:

General changes to the architecture, tasks and encapsulated business logic
should be described here.

Data model
----------

TODO:

Changes which require modifications to the data model often have a wider impact
on the system.  The community often has a strong opinion on how the data model
should be evolved, from both a functional and performance perspective. It is
therefore important to capture and gain agreement as early as possible on any
proposed changes to the data model.

Questions which need to be addressed by this section include:

* What new data objects and/or database schema changes are require?

* What database migrations will accompany this change.

* How will the initial set of new data objects be generated, for example if you
  need to take into account existing instances, or modify other existing data
  describe how that will work.


REST API
--------

TODO:

Each API method which is either added or changed should have the following

* Specification for the method

  * A description of what the method is suitable for user documentation

  * Method type (POST/PUT/GET/DELETE)

  * Normal HTTP response code(s)

  * Expected error HTTP response code(s)

    * A description for each possible error code should be included
      describing semantic errors which can cause it such as
      inconsistent parameters supplied to the method, or when an
      instance is not in an appropriate state for the request to
      succeed. Errors caused by syntactic problems covered by the JSON
      schema definition do not need to be included.

  * URL for the resource

  * Parameters which can be passed via the URL

  * JSON schema definition for the body data if allowed

  * JSON schema definition for the response data if any

* Example use case including typical API samples for both data supplied
  by the caller and the response

* Discuss any policy changes, and discuss what things a deploy engineer needs
  to think about when defining their policy.


Orchestration
=============

TODO:

General changes to the logic of orchestration should be described in details
in this section.


RPC Protocol
------------

TODO:

RPC protocol is another crucial part of inter-component communication in Fuel.
Thus it is very important to describe in details at least the following:

* How messaging between Nailgun and Astute will be changed in order to
  implement this specification.

* What input data is required and what the result format is expected

* If changes assume performing operations of nodes, a description of messaging
  protocol, input and output data should be also described.


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


Changes to Puppet manifests and supporting scripts are required.
The changes connected to avoiding hard-coded interface names and gathering
real interface names using in the system.


Alternatives
============

None.
We can stick to the classicall interface naming schema, but it does not allow
us to work with contemporary Linux distributives using another network
interface naming policies and prevent from including already deployed hosts
(like RHEL) to Fuel environment.


Upgrade impact
==============

Upgrading from CentOS 6.x to CentOS 7.0 lead to change network interface
naming policy and can break a network configuration used before the upgrade.

The simplest solution is do not do upgrade at all.

In case of upgrade, the plausible solution is to stick to hardware (MAC) 
addresses during the upgrade, when the naming of network interfaces are
changed. The (upgrade) scripts should collect information about current
network configuration and modify the configs in way preserving current 
interfaces' roles.


Security impact
===============

TODO:

None

Notifications impact
====================

Please specify any changes to notifications. It can be an extra notification,
changes to an existing notification, or removing a notification.


End user impact
===============

TODO:

Aside from the API, are there other ways a user will interact with this
feature?

* Does this change have an impact on python-fuelclient? What does the user
  interface there look like?


Performance impact
==================

None


Deployment impact
=================

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


Developer impact
================

TODO:

Discuss things that will affect other developers working on Fuel,
such as:

* If the blueprint proposes a change to the driver API, discussion of how
  drivers would implement the feature is required.


Infrastructure/operations impact
================================

None


Documentation impact
====================

None


Expected OSCI impact
====================

None

Implementation
==============

Assignee(s)
-----------

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
----------

TODO:

Work items or tasks -- break the feature up into the things that need to be
done. Those parts might end up being done by different people, but we're
mostly trying to understand the timeline for implementation.


Dependencies
------------

None

Testing, QA
============

TODO:

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly.

If there are firm reasons not to add any other tests, please indicate them.


Acceptance criteria
-------------------

Fuel should work well with different Ethernet interface naming policy.
In general Ethernet interface can have an arbitrary name.


References
==========

http://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames/
https://bugs.launchpad.net/fuel/+bug/1494223
https://bugs.launchpad.net/mos/+bug/1487044
https://review.openstack.org/#/c/223939



