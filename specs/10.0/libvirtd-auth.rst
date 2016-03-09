..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================================
Enable client authentication for TCP connections to libvirtd
============================================================

https://blueprints.launchpad.net/fuel/+spec/libvirtd-auth

Currently Fuel configures libvirtd daemon on compute nodes to listen on a TCP
port in the management network, so that libvirtd's can communicate with each
other during live migration of a tenant VM. At the same time user
authentication is not enabled for TCP connections, which means anyone who has
access to the management network can connect to a libvirtd daemon and control
it.


-------------------
Problem description
-------------------

In terms of libvirt this is `Managed peer to peer migration`_, where
nova-compute only talks to the libvirtd daemon running on the source compute
host, and the latter controls the entire migration process by directly
connecting to the libvirtd daemon on the destination host.

Fuel does not currently enable authentication in libvirtd: neither for local
connections (via a unix domain socket), nor for remote ones (via a TCP socket).
While the former is ok (as only users of ``libvirtd`` group are allowed to
connect to the libvirtd socket), the latter means that anyone who has access
to the management network can connect to a libvirtd daemon and control it.

The management network is internal and only accessible from within a Fuel
cluster, still no authentication in libvirtd is a security flaw, which can
be used for attacks, should anyone get access to the management network.


----------------
Proposed changes
----------------

The proposed change is to enable `SASL based authentication`_ for TCP
connections to the libvirtd daemon on compute nodes and create a SASL account
to be used by remote libvirt clients (username / password pair).

SASL credentials for the libvirt account can be shared among all compute nodes
of a Fuel cluster similarly to how cold migration in Nova is currently
configured (SSH public key authentication is used, the private / public keypair
is the same for every compute node of a cluster).

Additionally, SASL provides encryption of TCP connections. Please note, that in
`Managed peer to peer migration`_ QEMU processes communicate directly with
each other bypassing libvirt, which effectively means only libvirt management
network traffic will be encrypted, not the VM data passed over a network.

Specifically, the following actions must be performed in order to enable SASL
based authentication.

When a new cluster is created in Fuel:

 * make it possible to enable / disable libvirt authentication for TCP
   connections in Fuel Web UI cluster settings. The default must be ``enabled``

 * generate a random password to be used by the SASL libvirt account later

During deployment of each compute node of a cluster (by the means of Puppet
manifests):

 * create a SASL account for user ``libvirt`` using ``saslpasswd2`` command
   (passing the password value generated before)

 * set the value of ``auth_tcp`` option to ``"sasl"`` in the libvirtd daemon
   configuration file

 * put the credentials for ``libvirt`` user to the libvirt client configuration
   file


Web UI
======

When a new cluster is created it must be possible to enable / disable SASL
authentication for TCP connections to libvirtd on the cluster settings page,
similarly to how it's currently possible to enable / disable using of quotas
in Nova.

The default value of the checkbox must be ``enabled``. The tooltip should say,
that disabling authentication for remote connections to libvirtd is strongly
undesirable due to the security implications.


Nailgun
=======

Minimal changes to the data model are needed to add the checkbox to Web UI
and generate a random password for libvirt SASL account on creation of a
cluster.


Data model
----------

The ``openstack.yaml`` fixture will be modified, so that:

 * the cluster settings page contains a new checkbox, that allows to enable /
   disable libvirtd authentication for remote connections

 * a random password is generated for libvirt SASL account when a cluster is
   created. The username / password pair will be used for configuring both
   libvirt daemon and client on each compute node of the cluster


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

None.


Plugins
=======

Plugins which use / configure libvirtd on the compute nodes must be aware that
authentication will be enabled by default for remote connections to libvirtd.
This might affect plugins which directly talk to libvirt, e.g. to gather some
stats.


Fuel Library
============

If authentication for remote connections to libvirtd is enabled in the cluster
settings, Puppet manifests must configure `SASL based authentication`_ and
use the generated credentials from ``openstack.yaml`` as described above.


------------
Alternatives
------------

The alternative would be to use `TLS (authentication and encryption)`_ for TCP
connections to libvirtd. At the same, TLS setup requires considerably more work
(particularly, dealing with creation of TLS certificates for clients / servers)
and does not seem to provide any real benefits, as the primary focus is to
have authentication for remote connections, not to enable strong network
traffic encryption, as the latter is only for libvirt management data, not
tenant VM data in case of `Managed peer to peer migration`_.


--------------
Upgrade impact
--------------

Fuel cluster upgrades, which involve live migration of tenant VMs between
"old" and "new" compute nodes (e.g. done by `fuel-octane`_) might be affected,
if libvirtd remote connections authentication is enabled for the "new" Fuel
cluster - in this case the libvirtd daemon running on the source compute host
will fail to connect to the one running on the destination host, unless the
former is reconfigured to use SASL based authentication first.

The solution is to either disable libvirtd authentication for the "new" cluster
and enable it after all the compute nodes have been successfully upgraded.


---------------
Security impact
---------------

Enabling authentication for remote connections to libvirtd will close the
existing potential security issue of controlling libvirtd, should an attacker
get access to the management network.

The proposed solution is to create a SASL account for libvirt on every compute
node of a Fuel cluster using a shared username / password pair of credentials
(similar to how cold migration of VMs is currently configured by sharing the
same SSH key among all compute nodes).

Storing SASL credentials in libvirt client config file is not optimial, but
it's no different from storing credentials for MySQL / RabbitMQ in config files
of OpenStack services.

SASL also provides encryption of libvirt management traffic. Please note, that
this does not include actual data of tenant VMs - QEMU processes communicate
directly bypassing libvirtd's in case of `Managed peer to peer migration`_.
Encryption of tenant VM data during the process of live migration should be
addressed separately (if needed).


--------------------
Notifications impact
--------------------

None.


---------------
End user impact
---------------

None.


------------------
Performance impact
------------------

Performance impact from enabling SASL based authentication / encryption for
remote connections to libvirtd is negligible, as libvirt uses highly optimized
system libraries under the hood.

Another point is that only libvirt management traffic is encrypted, not the
actual data of tenant VMs being live migrated.


-----------------
Deployment impact
-----------------

* one new configuration option is added to Fuel Web UI, which allows to enable
  or disable authentication for remote connections to libvirtd on compute nodes

* the default value will be `enabled` due to security implications of libvirtd
  daemon listening on a TCP socket

* libvirt authentication can be enabled at any time: before and after deployment
  of a Fuel cluster (thanks to `Unlocked Settings Tab`_ spec implementation)

* upgrade impact has already been described above


----------------
Developer impact
----------------

None.


---------------------
Infrastructure impact
---------------------

None.


--------------------
Documentation impact
--------------------

Documenting the new checkbox in the Fuel Web UI and its security implications
must be sufficient.

It's worth to also provide a guide how to enable libvirtd authentication
manually for already deployed cluster, as well as for previous releases of
Fuel.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  TBD

Other contributors:
  rpodolyaka

Mandatory design review:
  aheczko-mirantis
  amogylchenko
  gelbuhos
  tdurakov


Work Items
==========

* update ``openstack.yaml`` in fuel-web to make enabling of libvirtd
  authentication configurable

* update ``openstack.yaml`` in fuel-web to generate a random password for
  libvirt SASL account

* update fuel-library Puppet manifests to configure SASL authentication for
  libvirt, if it's enabled in a cluster settings

* add a test to fuel-ostf to ensure authentication is required for remote
  connections to libvirtd, if it was enabled in the cluster settings


Dependencies
============

The following BP would be very useful to have in order to provide a smooth
upgrade path (a new Fuel cluster is deployed with libvirtd authentication
disabled, all tenant VMs are live migrated from "old" compute nodes,
authentication is enabled after all compute nodes have been upgraded):

https://blueprints.launchpad.net/fuel/+spec/unlock-settings-tab


------------
Testing, QA
------------

fuel-ostf already contains tests for live migration of VMs, which are run as a
part of BVT. If they pass, that will mean enabling of authentication in
libvirtd does not break anything.

An additional test is needed to make sure connecting to a libvirtd daemon on a
compute node requires authentication.


Acceptance criteria
===================

* Fuel allows to enable authentication for remote connections to libvirt on
  compute nodes and enables it by default

* it's not possible to connect to a libvirtd daemon on a compute node via TCP
  without authentication

* live migration of VMs between compute nodes succeeds

* libvirt authentication can be enabled on all compute nodes after upgrade of
  a Fuel cluster


----------
References
----------

.. _`Managed peer to peer migration`: https://libvirt.org/migration.html#flowpeer2peer
.. _`SASL based authentication`: https://libvirt.org/auth.html#ACL_server_username
.. _`TLS (authentication and encryption)`: http://wiki.libvirt.org/page/TLSSetup
.. _`fuel-octane`: https://github.com/openstack/fuel-octane
.. _`Unlocked Settings Tab`: https://blueprints.launchpad.net/fuel/+spec/unlock-settings-tab
