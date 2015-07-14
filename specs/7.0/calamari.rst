.. -*- coding: utf-8 -*-

..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================
Calamari: a Ceph UI
===================

Include the URL of your launchpad blueprint:

TODO: https://blueprints.launchpad.net/fuel/+spec/example

We would like to develop a plugin to install Calamari in the next release of
Fuel (7.0).  Calamari is a management and monitoring service for Ceph.
Calamari is composed by monitoring agents, a server-side and a client-side
components.

In more depth Calamari consists of three major components:

- Data collection agents running on each Ceph Storage Cluster host.
- The REST API running on one host (also called calamari server).
- The Calamari web application running on one host (also called calamari
  client).


Problem description
===================

In this section we describe the main steps that a user should perform for
installing Calamari. We suppose that:

- Ceph OSD is selected by User.
- Calamari agent will be installed on the Ceph OSD nodes.
- Calamari server and Calamari web application (GUI) will be installed on a
  new base-os node.


Calamari installation
---------------------

- Actor: User
- Pre-Conditions: the User has already created a new environment and he has
  configured a Ceph cluster.
- Post-Conditions: Calamari is correctly working.

Flow:

- The User assigns base-os role to an unallocated node.
- The User renames this node as Calamari
- The User configures in Settings tab the Ceph section.
- The User configures in Settings tab the Calamari section.
- The User deploys the environment.


Proposed change
===============

We would like develop a new Fuel plugin in order to install Calamari [1]_.
Our proposal considers the following aspects:

- Install Calamari server (REST API) and client (web application) on a new node
  with the base-os role.

- The plugin installs also the required agents on each Ceph OSD node.  The
  collected information will be pushed to Calamari server.

- The communication among agents and server will use the OpenStack management
  network.

- There will be a configuration switch to make the REST API and web application
  of Calamari available on the public interface (if the base-os support this
  already).

- No load balance for HA in the first implementation.  This topic will be
  explored in the future.


Planned improvements
--------------------

- Possibility to install Calamari on a controller node.

- Configure Calamari to use Keystone as the authentication backend.

- User session sharing between Calamari and the OpenStack dashboard.


Alternatives
------------

None.  The aim is to provide monitoring and management for Ceph.  There are
more general monitoring solution like Zabbix [2]_, LMA collector [3]_ and
Elasticsearch-Kibana [4]_ plugins.


Data model impact
-----------------

None


REST API impact
---------------

None


Upgrade impact
--------------

None.


Security impact
---------------

The default admin user name and password for the web interface will be
configured in the setting tab of the Fuel UI.

In the Fuel UI will be possible to allow the deploy of the REST API and web
application on the public network.


Notifications impact
--------------------

There will be a deployment successful message displaying the text pointing to
the URL of the web application.

We can also add some info to the `Post Deployment Dashboard
<https://review.openstack.org/#/c/180181/>`_ once it is implemented.


Other end user impact
---------------------

None

Performance Impact
------------------

None


Other deployer impact
---------------------

In the source tree of calamari there are Vagrantfile and scripts to build the
packages for Ubuntu 14.04, Centos and RHEL.

There is a `guide on building packages
<http://calamari.readthedocs.org/en/latest/development/building_packages.html>`_.



Developer impact
----------------

None


Infrastructure impact
---------------------

The agent impact on Ceph servers and on the network should be negligible.


Implementation
==============


Assignee(s)
-----------

Primary assignee:
  Alessandro Martellone <amartellone@create-net.org>

Other contributors:
  Daniele Pizzolli <dpizzolli@create-net.org>


Work Items
----------

Task name: Calamari installation recipe
  Task description: write a puppet module in order to install Calamari server
  and configure properly all nodes to monitor.

  Assignees: Alessandro Martellone, Daniele Pizzolli.

Task name: include the latest version of Calamari package
  Task description: include in the plugin repositories the required packages.

  Assignees: Dmytro Iurchenko, Alessandro Martellone,
  Daniele Pizzolli.


Dependencies
============

- Fuel 6.1 or higher.
- Base-os node role.

Nice to have, but not essential:

- `Post Deployment Dashboard <https://review.openstack.org/#/c/180181/>`_
- `Role as a plugin <https://review.openstack.org/#/c/143690/>`_


Testing
=======

- Prepare a test plan.
- Test the plugin by deploying environments with all Fuel deployment nodes.
- Create integration tests.


Documentation Impact
====================

None.  It will be a Fuel plugin with its own documentation.


References
==========

.. [1] http://calamari.readthedocs.org/en/latest/operations/server_install.html
.. [2] https://docs.mirantis.com/fuel-dev/develop/addition_examples.html
.. [3] https://github.com/stackforge/fuel-plugin-lma-collector
.. [4] https://github.com/stackforge/fuel-plugin-elasticsearch-kibana
