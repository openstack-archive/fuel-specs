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
be used for attacks, should anyone compromise one of the nodes of the cluster
and get shell access to it.


----------------
Proposed changes
----------------

The proposed change is to enable `SASL based authentication`_ for TCP
connections to the libvirtd daemon on compute nodes and create a SASL account
to be used by remote libvirt clients (username / password pair).

SASL credentials for the libvirt account can be shared among all compute nodes
of a Fuel cluster similarly to how cold migration in Nova is currently
configured (SSH public key authentication is used, the private / public keypair
is the same for every compute node).

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

 * create a SASL account for user ``libvirt`` by the means of ``saslpasswd2``
   command passing the password value generated before

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

The ``opestack.yaml`` fixture will be modified, so that:

 * the cluster settings page contains a new checkbox, that allows to enable /
   disable libvirtd authentication for remote connections

 * a random password is generated for libvirt SASL account when a cluster is
   created. The username / password pair will be used to configure both
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


Fuel Library
============

If authentication for remote connections to libvirtd is enabled in the cluster
settings, Puppet manifests must configure `SASL based authentication`_ and
use the generated credentials from ``openstack.yaml``.


------------
Alternatives
------------

The alternative would be to use `TLS (authentication and encryption)`_ for TCP
connections to libvirtd. At the same, TLS setup requires considerably more work
(particularly, dealing with creation of TLS certificates for clients / servers)
and does not seem to provide any real benefits, as the primary focus is to
have authentication for remote connections, not to enable strong network traffic
encryption, as the latter is only for libvirt management data, not tenant VM
data in case of `Managed peer to peer migration`_.


--------------
Upgrade impact
--------------

Fuel cluster upgrades, which involve live migration of tenant VMs between
"old" and "new" compute nodes (e.g. done by `fuel-octane`_) might be affected,
if libvirtd remote connections authentication is enabled for the "new" Fuel
cluster - in this case a libvirtd daemon running on the source compute host will
fail to connect to the one running on the destination host, unless the former
is reconfigured to use SASL based authentication first.

The solution is to either disable libvirtd authentication for the "new" cluster
and enable it after all the compute nodes have been successfully upgraded or
run the corresponding Puppet manifests on the "old" compute nodes before the
upgrade procedure in order to enable auth in advance.


---------------
Security impact
---------------

# TODO(rpodolyaka): describe SASL vs TLS vs no-auth


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

# TODO(rpodolyaka): ...


-----------------
Deployment impact
-----------------

Discuss things that will affect how you deploy and configure Fuel
that have not already been mentioned, such as:

* What configuration options are being added? Should they be more generic than
  proposed? Are the default values ones which will work well in
  real deployments?

* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

* If this change is a new binary, how would it be deployed?

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

Discuss things that will affect other developers working on Fuel,
such as:

* If the blueprint proposes a change to the driver API, discussion of how
  drivers would implement the feature is required.


---------------------
Infrastructure impact
---------------------

Explain what changes in project infrastructure will be required to support the
proposed change. Consider the following:

* Will it increase the load on CI infrastructure by making build or test jobs
  consume more CPU, network, or storage capacity? Will it increase the number
  of scheduled jobs?

* Will it require new workflows or changes in existing workflows implemented in
  CI, packaging, source code management, code review, or software artifact
  publishing tools?

  * Will it require new or upgraded tools or services to be deployed on project
    infrastructure?

  * Will it require new types of Jenkins jobs?

  * Will it affect git branch management strategies?

  * Will it introduce new release artifacts?

  * Will it require changes to package dependencies: new packages, updated
    package versions?

  * Will it require changes to the structure of any package repositories?

* Will it require changes in build environments of any existing CI jobs? Would
  such changes be backwards compatible with previous Fuel releases currently
  supported by project infrastructure?


--------------------
Documentation impact
--------------------

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.


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
  TBD

Other contributors:
  TBD

Mandatory design review:
  aheczko-mirantis
  amogylchenko
  gelbuhos
  tdurakov


Work Items
==========

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


------------
Testing, QA
------------

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly.

This should include changes / enhancements to any of the integration
testing. Most often you need to indicate how you will test so that you can
prove that you did not adversely effect any of impacts sections above.

If there are firm reasons not to add any other tests, please indicate them.

After reading this section, it should be clear how you intend to confirm that
you change was implemented successfully and meets it's acceptance criteria
with minimal regressions.

Acceptance criteria
===================

Please specify clearly defined acceptance criteria for proposed changes.


----------
References
----------

.. _`Managed peer to peer migration`: https://libvirt.org/migration.html#flowpeer2peer
.. _`SASL based authentication`: https://libvirt.org/auth.html#ACL_server_username
.. _`TLS (authentication and encryption)`: http://wiki.libvirt.org/page/TLSSetup
.. _`fuel-octane`: https://github.com/openstack/fuel-octane
