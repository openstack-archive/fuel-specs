.. -- coding: utf-8 --

..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================
Calamari: a CEPH UI
===================

Include the URL of your launchpad blueprint:

TODO: https://blueprints.launchpad.net/fuel/+spec/example


We would like to install Calamari in the next release of Fuel (7.0). Calamari
is a management and monitoring service for Ceph. Calamari is composed by a
server-side and by a client-side components.

In more depth Calamari consists of three major components:

- Data-collection agents running on each Ceph Storage Cluster host.
- The  ceph-rest-api running on one Ceph Monitor host.
- The Calamari web application running on a remote monitoring/control host,
  which is named calamari by default.

Problem description
===================

In this section we describe the main steps that a user should perform for
installing Calamari. We suppose that:

- Calamari server is installed on the controller node Storage
- Ceph OSD is selected by User

Calamari installation
---------------------

- Actor: User
- Pre-Conditions: the User has already created a new environment and he has
  configured a CEPH cluster.
- Post-Conditions: Calamari is correctly installed on the controller node.

Flow:
 
  - The User assigns the ceph role to unallocated nodes.
  - The User configures in Settings tab the CEPH section.
  - The User deploys the environment.

Proposed change
===============

We would like a new “Operation” Fuel plugin in order to install Calamari. We
suggest two changements:

- Install Calamari server on a Controller node. In a HA deployment, we may
  install it only on the primary-controller.

- Install Calamari server on a new “Monitoring” node. That implies that a
  redesign of the Zabbix node is required. A draft proposal about this is
  available at http://goo.gl/mU1gpT

In this proposal we analyze the first solution.

The plugin installs also the required agents on each Ceph OSD node. The
collected information will be pushed to Calamari server.

The communication among agents and server will use the OpenStack management
network. Obviously, the Calamari UI has a public interface.


Alternatives
------------
None

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

The new feature does not affect the master node upgrading process but it
impacts, if it is necessary, only on updating the required packages list
(e.g. update to a newest version of Calamari).


Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Plugin impact
-------------

TBD

Other deployer impact
---------------------

Officially, the Calamari agents are compatible with the following operating
system versions:

- Ubuntu 12.04
- CentOS 6.3 and higher
- RHEL 6.3 and higher
- Debian Wheezy

The Calamari web application is compatible with:

- CentOS 6.4 and higher
- RHEL 6.4 and higher

On the RedHat installation guide there is a procedure that installs Calamari
server on an Ubuntu 12.04

Developer impact
----------------

None

Infrastructure impact
---------------------

Installing the server on the controller node, it will increase the consume of
CPU and RAM resources. Probably, restructuring the current Zabbix node, and
transforming it in a more generic “monitoring node”, we could install Calamari
on that.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Alessandro Martellone <alessandro.martellone@create-net.org>

Other contributors:
  Daniele Pizzolli <daniele.pizzolli@create-net.org>

Work Items
----------

Task name: Calamari installation recipe
  Task description: write a puppet module in order to install Calamari server
  and configure properly all nodes to monitor.

  Assignee(s): Alessandro Martellone, Daniele Pizzolli.

Task name: include the latest version of Calamari package
  Task description: include in the Fuel’s repositories the Calamari packages.

  Assignee(s): someone of Mirantis’ team, Alessandro Martellone,
  Daniele Pizzolli.

Dependencies
============

This feature has no dependencies from other projects or functionalities, but it
requires including in fuel repository the latest version of Calamari for
debian/centOS.

Testing
=======

We are going to define a number of unit tests which will cover all aspects of
the change. Furthermore, we plan to test the make iso scripts so that all
required external packages are included into Fuel master node (ISO).

Documentation Impact
====================

We should update the User Guide
http://docs.mirantis.com/openstack/fuel/fuel-7.0/user-guide.html#user-guide

References
==========

Calamari installation guide:
https://download.inktank.com/docs/Calamari%201.1%20Installation%20Guide.pdf
