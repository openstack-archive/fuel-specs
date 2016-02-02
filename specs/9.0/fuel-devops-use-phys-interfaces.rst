..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================
Use physical network interfaces in fuel-devops
==============================================

https://blueprints.launchpad.net/fuel/+spec/fuel-devops-use-phys-interfaces

Allow to use physical interfaces from a host where fuel-devops is running
as a slave interfaces of libvirt bridges. Untag specified VLANs to allow
access to these tagged networks from the host with fuel-devops.

--------------------
Problem description
--------------------

fuel-devops operates with libvirt networks that support different forward
modes, but there is no possibility to configure access from these networks
to L2 networks of baremetal labs.
Another issue that there is no possibility to test a cluster with tagged
public network without manual host configuration.

----------------
Proposed changes
----------------

To allow running baremetal and hybrid environments, libvirt virtual networks
should be able to use already created network interfaces on the host server,
that was configured to provide connectivity to baremetal nodes or VMs from
the other host that available thru these network interfaces.

Tagged environment networks also should be accessible from the host with
fuel-devops.

In case if the baremetal environment has already configured gateways for admin
and/or public networks, then appropriate libvirt virtual networks should be
configured with a specific IP address instead of the first address
in the network and without 'nat' forwarding.


The baremetal lab configuration like this:

.. code-block:: text

                    WAN
                     ^
                     |
              +------+------+
              |    eth0     |
              |             |
              | fuel+devops |
              |   CI host   |
              |             |
              |    eth1     |
              +------+------+
                     |
  +------------------+------------------+
  |     admin(pxe) isolated network     |
  +--+-------+-------+-------+-------+--+
     |       |       |       |       |
  +--+--+ +--+--+ +--+--+ +--+--+ +--+--+
  |slave| |slave| |slave| |slave| |slave|
  |  1  | |  2  | |  3  | |  4  | |  5  |
  +-----+ +-----+ +-----+ +-----+ +-----+
             Baremetal servers


, where 'admin(PXE)' network is untagged and
'public', 'management', 'storage' and 'private' networks are tagged,
could be configured like this:

.. code-block:: text

  l2_network_device:  host's bridge name:   child interfaces
                                            added to the bridge:

  admin               fuelbr1               eth1
                      # tagged interfaces
                        fuelbr1.100
                        fuelbr1.101
                        fuelbr1.102
                        fuelbr1.103

  public              fuelbr2               fuelbr1.100

  management          fuelbr3               fuelbr1.101

  storage             fuelbr4               fuelbr1.102

  private             fuelbr5               fuelbr1.103


Here, 'fuelbr1' is connected to the baremetal network via eth1, while other
libvirt briges are configured as endpoints to provide access into the tagged
networks and perform 'nat' forwarding from untagged public network to the
Internet.

In fuel-devops YAML templates new fields can be used for l2_network_devices:

- vlan_ifaces: list of tags for creating tagged interfaces on the libvirt
               network's bridge;
- child_ifaces: list of physical interfaces that should be added to the
                libvirt network's bridge;
- child_vlan_ifaces: list of pairs l2_network_device names and tag numbers,
                     to find tagged interfaces that was created for
                     'vlan_ifaces' tags list on a specified l2_network_device
                     and add them as child interfaces to the libvirt
                     network's bridge.

.. code-block:: yaml

       l2_network_devices:
         admin:
           address_pool: fuelweb_admin-pool01
           forward:
             mode: nat
           vlan_ifaces:
            - 100
            - 101
            - 102
            - 103
           child_ifaces:
            - eth1

         public:
           address_pool: public-pool01
           forward:
             mode: nat
           child_vlan_ifaces:
            - admin: 100

         management:
           address_pool: management-pool01
           child_vlan_ifaces:
            - admin: 101

         storage:
           address_pool: storage-pool01
           child_vlan_ifaces:
            - admin: 102

         private:
           address_pool: private-pool01
           child_vlan_ifaces:
            - admin: 103


* Resulting bridges configuration on the host with fuel-devops:

.. code-block:: text

  $ brctl show
  bridge name  bridge id               STP enabled  interfaces
  fuelbr1       8000.525400288ed7       yes         eth1
                                                    fuelbr1-nic

  fuelbr2       8000.525400288ed7       yes         fuelbr1.100
                                                    fuelbr2-nic

  fuelbr3       8000.525400288ed7       yes         fuelbr1.101
                                                    fuelbr3-nic

  fuelbr4       8000.525400288ed7       yes         fuelbr1.102
                                                    fuelbr4-nic

  fuelbr5       8000.525400288ed7       yes         fuelbr1.103
                                                    fuelbr5-nic

Web UI
======

None

Nailgun
=======

None

Data model
----------

New fields will be added to the 'params' field of the table
'devops_l2_network_device'. The field 'params' is serialized into JSONField
so there is no need to do a database migration.
See 'ParamModel' django data type extension in [1] for details.

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

---------------------
Infrastructure impact
---------------------

- Necessary physical interface names should be provided for system tests on CI
  to access networks that are connected to baremetal labs (optional)
- Necessary VLAN tags should be provided for system tests on CI in case if
  there is required access to a tagged network from the tests (optional, can be
  used for system tests on qemu-kvm, where public and other networks are tagged)

--------------------
Documentation impact
--------------------

- YAML template changes should be documented
- YAML examples and usage should be updated

--------------
Implementation
--------------

Assignee(s)
===========

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  Denys Dmytriiev (ddmitriev): ddmitriev@mirantis.com

Other contributors:
  Anton Studenov (astudenov): astudenov@mirantis.com
  Dmitry Tyzhnenko (dtyzhnenko): dtyzhnenko@mirantis.com

Mandatory design review:
  Anastasiia Urlapova (aurlapova): aurlapova@mirantis.com
  Dmitry Tyzhnenko (dtyzhnenko): dtyzhnenko@mirantis.com


Work Items
==========

- Add new fields to L2NetworkDevice class for libvirt driver;
- Add XML builder for tagged interfaces
- Add method for inserting host's network interfaces to libvirt bridges
- Add support for specifying an IP address that should be assigned to the
  libvirt network from an address pool in additional to the gateway address
  (may be the same)
- Add support of new data fields to the template validator
- Perform testing on a baremetal lab.

Dependencies
============

This feature depends on fuel-devops 3.0.0 implementation [2] with templates
support.

------------
Testing, QA
------------

- Create a template for a virtual environment, where all nodes have a single
  network interface and are connected to the 'admin' network.
  Configure 'admin' L2 network device with necessary tagged interfaces, and
  connect these tagged interfaces to other necessary L2 network devices.

- Create a template for a baremetal environment, where all nodes have a single
  network interface and are connected to the 'admin' network.
  Configure 'admin' L2 network device with necessary tagged interfaces, and
  connect these tagged interfaces to other necessary L2 network devices.

- Create a template for a baremetal environment where 'admin' and 'public'
  networks are connected to different physical interfaces on the host with
  fuel-devops. All other networks should be tagged and assigned on 'public'
  network later.

- Create environments using these templates.
  Create a VM on the host with fuel-devops, with a single network interface
  connected to the 'admin' network of required environmetn.
  Perform manual setup of Fuel master node, create a cluster with network
  assignements and tags like in the template that was used for creating
  the environment.
  Deploy cluster.

* Note: fuel-qa system tests are not ready for such testing because
  it doesn't support fuel-devops 3.0.0 yet.

Acceptance criteria
===================

Using devops templates, can be created the following:

- tagged interfaces are created for libvirt l2 network devices;
- specified tagged interfaces are added to the libvirt l2 network devices;
- specified physical interfaces are added to the libvirt l2 network devices.

----------
References
----------

[1] https://review.openstack.org/#/c/274578/
[2] https://blueprints.launchpad.net/fuel/+spec/template-based-virtual-devops-environments
