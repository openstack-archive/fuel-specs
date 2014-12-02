..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Substitution Cobbler with OpenStack Ironic
==========================================

https://blueprints.launchpad.net/fuel/+spec/cobbler-ironic-substitute [2]_

Problem description
===================

Currently we have working image based provisioning scheme which uses Fuel
Agent on a node side to do advanced partitioning, download images and put
them on a hard drive. The next logical step is to get rid of provisioning
scheme based on native installers like Anaconda and Debian-installer and
stop wasting resources for maintaining them. Cobbler seems to be an
unnecessary component in the case because it has many features which we
don't need if we use image based scheme only.

However, Cobbler manages DHCP, DNS, TFTP services on a master node and
those services are needed for image based scheme as well. Fortunately,
OpenStack has Ironic in its core which is capable to do the same. Ironic
has PXE boot support, IPMI/ILO based power management. Ironic can manage
DHCP and DNS (maybe via Neutron). Besides, Ironic is an implementation of
server side of image based provisioning for bare metal in OpenStack.
That is exactly what we need instead of Cobbler.


Proposed change
===============

::

    Nailgun   Astute   Ironic   Fuel Agent
    +         +        +        +
    |         |      Default    |
    |         |       TFTP      |
    |         |        |  PXE   |
    |         |        +------> |
    |     DISCOVERY    |        |
    | <-------+-----------------+
    |         |        |        |
    | PROVISION        |        |
    +-------> |        |        |
    |         |        |        |
    |         | ADD NODE        |
    |         +------> |        |
    |         |        |        |
    |         | DEPLOY |        |
    |         +------> |        |
    |         |        |        |
    |         |        |PROVISION DATA
    |         |        +------> |
    |         |        |        |
    |         |        |RUN FUEL AGENT
    |         |        +------> |
    |         |        |        |
    |         | DONE   |        |
    |         | <------+        |
    |   DONE  |        |        |
    | <-------+        |        |
    +         +        +        +

To make Ironic able to interact with Fuel Agent (put provision.json and
run /usr/bin/provision) we need to implement corresponding Fuel Agent driver.
It should be able to create default TFTP configuration so as to boot all
new unknown nodes with bootstrap ramdisk where Fuel Agent (provisioning) and
Nailgun Agent (discovery) are installed. That is exactly like current default
system in Cobbler.

When a node boots with this bootstrap ramdisk, Nailgun Agent sends
hardware info to Nailgun REST API. Then Nailgun is able to append
this node to a cluster.

Nailgun sends provisioning info to Astute via AMQP and waits for
provisioning is done. It is not supposed to change current provisioning
data format. Astute is going to convert those data into Ironic
format if necessary.

Astute adds node info into Ironic via its REST API, chooses FuelAgentDriver and
sets driver_info according to provisioning data gotten from Nailgun.
It then calls deploy Ironic REST method to start actual provisioning.

Ironic then needs to put provisioning data (driver_info)
into /tmp/provision.json file on a node. The format is supposed to differ
from Nailgun format, so we need to implement a corresponding Ironic driver
for Fuel Agent (part of Fuel Agent). Currently Fuel Agent
can parse Nailgun format only. Ironic then runs /usr/bin/provision
entry point and waits for it to finish and return exit code.

TODO: describe how to manage DHCP and DNS

As far as we are going to get rid of native OS installers we need to
remove the radio button on Fuel web UI which currently allows user to choose
between two ways of OS installing.


Alternatives
------------

Cobbler has plenty of features and we don't need most of them if we get rid of
native OS installers. However, we need some service to manage DHCP, DNS and
TFTP services. An alternative to using Ironic is to implement standalone
service or add corresponding capabilities into Astute.

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

We also need to disable radio button which allows one to choose between
two ways of provisioning.

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

- *Fuel Agent driver for Ironic.* [1]_
  The majority of Ironic functionality is implemented as drivers. Currently it
  has PXE, IPMI, IPA (Ironic Python Agent) drivers and we need to have the same
  for Fuel Agent.
- *Ironic Ruby binding (Fog) for using it in Astute.*
- *Ironic driver for Astute.*
  Currently we have Cobbler driver which allows us to use Cobbler for
  OS provisioning. This change supposes having Ironic driver.
- *Ironic data driver for Fuel Agent.*
  Currently Fuel Agent is able to parse provisioning data in Nailgun format.
  If Ironic is going to use another format, we need to implement a
  corresponding data driver for Fuel Agent. (apart from nailgun data driver)
- *Ironic Puppet module.*
  We need to be able to deploy Ironic on a master node, so we need to have a
  corresponding Puppet module.
- *Ironic Docker container.*
  We have all major master node components packed into Docker containers.
  So we need to have Ironic one.
- *Ironic related stuff in upgrade script.*


Dependencies
============

- https://blueprints.launchpad.net/ironic/+spec/fuel-agent-driver [1]_
- https://github.com/fog/fog [3]_ (OpenStack Ruby binding)


Testing
=======

Testing approach

- Deploy master node with Ironic (Fuel Agent driver).
- Start slave VM and boot it via PXE with bootstrap ramdisk (Fuel Agent).
- Wait for slave node is discovered.
- Create new cluster and append slave node to it.
- Start deployment.

Testing is supposed to be implemented according to this document [4]_

Acceptance criteria
-------------------

- Ironic must be able to put provisioning data (maybe specific format) into
  /tmp/provision.json on a slave node.
- Ironic must be able to run Fuel Agent provision entry point
  (a.k.a. /usr/bin/provision).
- Ironic must be able to get Fuel Agent exit code and report error if it is
  not 0.
- Astute must be able to use Ironic REST API for provisioning.

Documentation Impact
====================

It is necessary to re-write those parts of Fuel documentation which are
about provisioning and about Fuel architecture.

References
==========

.. [1] https://blueprints.launchpad.net/ironic/+spec/fuel-agent-driver
.. [2] https://blueprints.launchpad.net/fuel/+spec/cobbler-ironic-substitute
.. [3] https://github.com/fog/fog
.. [4] http://docs.mirantis.com/fuel-dev/devops.html
