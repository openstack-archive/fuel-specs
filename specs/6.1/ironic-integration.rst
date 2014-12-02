..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Substitution Cobbler with OpenStack Ironic
==========================================

TODO: actual link to a blueprint
https://blueprints.launchpad.net/fuel/+spec/example

Problem description
===================

Currently we have working image based provisioning scheme which uses Fuel Agent
on a node side to do advanced partitioning, download images and put them on a hard drive.
The next logical step is to get rid of provisioning scheme based on native installers
like anaconda and debian-installer and stop wasting resources for maintaining them.
Cobbler seems to be an extra component in the case because it has many features which we
don't need if we use image based scheme only.

However, Cobbler manages DHCP, DNS, TFTP services on a master node and those services are
needed for image based scheme as well. Fortunately, OpenStack has Ironic in its core which
is capable to do the same. Ironic has PXE booting support, IPMI/ILO based power management.
Ironic can manage DHCP and DNS (maybe via Neutron). Besides, Ironic is an implementation of
server side of image based provisioning for bare metal in OpenStack. That is exactly what we
need instead of Cobbler.


Proposed change
===============

TODO: sequence diagram

1) Ironic -> Default TFTP configuration (all unknown nodes boot with bootstrap ramdisk)
2) TFTP -> PXE boot with Fuel Agent + Nailgun Agent
3) Nailgun Agent -> Nailgun (discovery data)
4) Nailgun -> Astute (provisioning data)
5) Astute -> Ironic (add node)
6) Astute -> Ironic (deploy node)
7) Ironic -> Fuel Agent (put /tmp/provision.json and run /usr/bin/provision)
8) Ironic -> Astute (provisioning done, GET request)

To make Ironic able to interact with Fuel Agent (put provision.json and
run /usr/bin/provision) we need to implement corresponding Ironic driver. It should
be able to create default TFTP configuration so as to make all new unknown
nodes booting with bootstrap ramdisk where Fuel Agent (provisioning) and
Nailgun Agent (discovery) are installed. That is exactly like current default
system in Cobbler.

Then a node boots with this bootstrap ramdisk and Nailgun Agent sends
hardware info to Nailgun REST API. Nailgun is able to append this node to a cluster.

Nailgun sends provisioning info to Astute via AMQP and waits for provisioning is done.
It is not supposed to change current provisioning data format. Astute is going to
convert those data into Ironic format if necessary.

Astute adds node info into Ironic via its REST API, chooses FuelAgentDriver and
sets driver_info according to provisioning data gotten from Nailgun. It then calls
deploy Ironic REST method to start actual provisioning. We need to implement ruby Ironic
binding and then use this binding in Astute for interacting with Ironic.

Ironic then needs to put provisioning data (driver_info) into /tmp/provision.json file
on a node. The format is supposed to differ from Nailgun format, so we need to implement
corresponding Fuel Agent data driver (part of Fuel Agent). Currently Fuel Agent
can parse Nailgun format only. Ironic then runs /usr/bin/provision
entry point and waits for it to finish and return exit code.

TODO: describe how to manage DHCP and DNS

As far as we are going to get rid of native OS installers we need to remove radio button
on Fuel web UI which currently allows user to choose between two ways of installing OS.

* Implement Ironic driver for Fuel Agent
  The majority of Ironic functionality is implemented as drivers. Currently it
  has PXE, IPMI, IPA (Ironic Python Agent) drivers and we need to have the same
  for Fuel Agent.

* Implement Puppet module for Ironic deployment.
  We need to be able to deploy Ironic on a master node, so we need to have a
  corresponding Puppet module.

* Implement Docker container for Ironic.
  We have all major master node components packed into Docker containers.
  So we need to do


Alternatives
------------

Cobbler has plenty of features and we don't need most of them if we get rid of
native OS installers. However, we need some service to manage DHCP, DNS and TFTP services.
Alternative to using Ironic is to implement our own standalone service or add corresponding
capabilities info Astute.

Data model impact
-----------------

* It is not supposed to change data models neither in Nailgun nor in Ironic.

REST API impact
---------------

* It is not supposed to change REST API neither in Nailgun nor in Ironic.

Upgrade impact
--------------

It is planned to substitude cobbler docker container with ironic one and
save TFTP configuration (cobbler default system, systems for particular nodes).
It is also supposed to save DHCP and DNS configurations.

We also need to disable radio button which allows one to choose between two ways of
provisioning.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Provisioning way radio button is going to be removed.

Performance Impact
------------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <vkozhukalov@mirantis.com>
  <agordeev@mirantis.com>

Work Items
----------

- Fuel Agent driver for Ironic. [1]_
- Ironic Ruby binding (Fog) for using it in Astute.
- Ironic driver for Astute.
- Ironic data driver for Fuel Agent. (apart from Nailgun driver)
- Ironic Puppet module.
- Ironic Docker container.
- Ironic related stuff in upgrade script.


Dependencies
============

TODO: include Ironic spec
TODO: openstack ruby binding
TODO: ironic as a project

Testing
=======

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly,
but discussion of why you think unit tests are sufficient and we don't need
to add more functional tests would need to be included.

Is this untestable in gate given current limitations (specific hardware /
software configurations available)? If so, are there mitigation plans (3rd
party testing, gate enhancements, etc).

Acceptance criteria
-------------------


Documentation Impact
====================

It is necessary to re-write those parts of Fuel documentation which are
about provisioning and about Fuel architecture.

References
==========

.. [1] https://blueprints.launchpad.net/ironic/+spec/fuel-agent-driver
