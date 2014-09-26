..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================================
Use FUEL to Deploy OpenLDAP across all Controller Nodes
=======================================================

https://blueprints.launchpad.net/fuel/+spec/deploy-ha-openldap

LDAP integration is a frequently asked feature. At the same time,
Keystone's LDAP integration is not very sophisticated. OpenLDAP is a
much better fit to provide an interface for integration with existing
IAM systems such as Active Directory. It also provides saner ways to
store and manage users, passwords and has mature mechanisms for
password policies as well as HA capability.

Problem description
===================

Storing Users, Passwords, Roles and Tenants inside MySQL may be an
obvious solution to the problem, but it is flawed in at least two ways:

#. it does not integrate with existing user database
#. it does not support sophisticated password policies
#. it does not allow for compliance auditing

OpenLDAP is an open source project that comes with a mature code base,
is carrier-grade, and serves as the de-facto LDAP server
implementation. OpenLDAP supports Multi-Master-Replication (MMR) and
advanced proxying mechanisms, access lists and security rules
concerning required encryption, implements the (delta-)syncrepl
protocol and has a proven track record in carrier-grade stability
throughout the years of its existence. OpenLDAP has multiple ways to
integrate with existing directory infrastructures containing
authentication (AuthN) and authorization (AuthZ) information
pertaining to the organizational users, groups and roles.

Use Cases:

* A directory solution already exists but is administered by a
  different team which is not willing to accommodate or slow to react
  to change requests from the cloud operations team.

* Integration with existing IAM solutions are not supported by
  Keystone (sophisticated group membership resolutions, role
  occupancy, or others), or existing code base is functionally not
  performant enough to provide useful integration options.

* User Life-Cycle mechanisms do typically not include
  (de-)provisioning of users in MySQL databases as they are usually
  application specific. Organizations intending to create a
  comprehensive and best practice IAM solution build their lifecycle
  management around a single directory database containing all users,
  groups and roles. OpenStack as deployed by FUEL does not integrate
  with that.

* Cloud Operators want to enforce password policies and other advanced
  AuthN or AuthZ options which are not available in MySQL or which
  Keystone/LDAP does not support out of the box, however OpenLDAP
  would provide.

* There is an auditing need by the Cloud Operator requiring all
  authentication, changes to tenants, roles, passwords, etc. to be
  tracked in an audit log file for compliance or other security
  purposes.

Proposed change
===============

Deploy OpenLDAP in a standard, known fashion using FUEL. Implement and
deploy all required schema files to provide Keystone with a well known
and supported database layout. Use this backend for both reads and
writes. After deployment the de-facto OpenLDAP management tool is
already provided through the Identity section in Horizon. Further
integration work can do be done to tie the OpenLDAP master servers
into the existing IAM infrastructure if necessary, rather than relying
on Keystone to provide that functionality which is severely lacking as
of this point.

Each Controller node should have two OpenLDAP processes running.

#. Master Server (in MMR fashion)
#. Proxy Server (using LDAP backend)

The Master server daemon only listens on ``ldap://localhost:10389``,
and on the service-facing interface ``ldaps://<mgmt-ip>:636/`` using
self-signed SSL certificates.

The Proxy server listens on all interfaces: ``ldap://*:389``.

Access rules restrict connections to master servers to allow only
those connections made by the proxy; and further allow only syncrepl
replication connections between master servers.

The LDAP proxy is client facing and accepting connections from
Keystone. At the operators preference, this connection can be TLS
secured (strongly recommended) or unencrypted.

The integration with the local IAM infrastructure is performed by
adjusting the configuration on the master servers. Multiple options exist:

* SASL pass-through authentication (requires sasl2-bin package to be installed)
* LDAP Backend in conjunction with suffix-massaging (rwm overlay)
* possibly others depending on the existing infrastructure

The Keystone, OpenLDAP Proxy and the OpenLDAP Server interface are
well-defined and basically static; they provide by default a simple
backend with no functional change to the MySQL backend equivalent.

Functional Diagram::

 +--------------+ MMR +--------------+ MMR +---------------+
 |  Master #1   |_____|  Master #2   |_____|  Master #3    |
 |              |     |              |	   |               |
 +--------------+     +--------------+	   +---------------+
         |            /                ------/    
         | __________/                /           
         |/---------------------------            
 +--------------+    +---------------+    +----------------+
 |  Proxy #1    |    |   Proxy #2    |	  |   Proxy #3     |
 |              |    |               |	  |                |
 +--------------+    +---------------+	  +----------------+

The proxies are connected to all three masters (in above drawing, only
the connections from proxy #1 are drawn for clarity).

The OpenLDAP Proxy server is configured using the back_ldap
overlay. It supports passing a list of backend servers to which the
proxy connects to. Should the first server on the list be unreachable,
the next one in the list is being contacted, transparently, and the
list is re-ordered. There is no outage in functionality. Data
integrity is being guaranteed by the syncrepl protocol (RFC
4533). High-Volume changes can be addressed by configuring
delta-syncrepl.

Alternatives
------------

None.


Data model impact
-----------------

None.

REST API impact
---------------

None.

Upgrade impact
--------------

Existing OpenLDAP-enabled Deployments (using this mechanism) are not
affected in a meaningful way when upgrading; OpenLDAP supports
upgrading the server version without affecting the underlying
database. Existing SSL certificates would remain in place unless the
name or IP address of the controller changes.

Security impact
---------------

Using OpenLDAP in conjunction with SSL encrypted syncrepl connections
and TLS-enabled (or TLS-required) client facing daemons increases the
security of the IAM model currently employed by default FUEL
(MySQL). It enables advanced auditing and compliance mechanisms not
available with other backends.


Notifications impact
--------------------

None.


Other end user impact
---------------------

It is out of scope to configure the IAM integration piece through
FUEL. There are too many different options and deployed IAM solutions
at any given site, and it is not feasible to expect such integration
work to be done through FUEL. However, clean user management could be
part of the FUEL admin page, interacting with the OpenLDAP server
through an application-specific account. Other information could also
be stored in the OpenLDAP database, such as DHCP pools, DNS host name
assignments, and other info regarding the nodes themselves (MAC/IP
address pairs, etc.).


Performance Impact
------------------

While largely due to the current LDAP backend implementation in
Keystone, Horizon performance will typically be slower using an LDAP
enabled backend; performance enhancements would have to be addressed
in order to provide meaningful progress. As it stands today, the read
performance for OpenLDAP exceeds MySQL.


Other deployer impact
---------------------

None.


Developer impact
----------------

None.

Implementation
==============

Assignee(s)
-----------

As I do not have significant FUEL developer experience, this blueprint
is in need of a developer resource to implement this. I would be happy
to provide default configurations, and run tests.

Primary assignee:
  None

Other contributors:
  sfabel

Work Items
----------

* include latest OpenLDAP (NOT from distribution repository) in the
  FUEL repository. Likely requires re-packaging.

* create puppet templates to provide the configuration files for the
  OpenLDAP master servers.

* create puppet templates to provide the configuration files for th
  OpenLDAP proxy servers.


Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


Testing
=======

* create user, tenant, role
* assign user to tenant as role
* failover/HA tests


Documentation Impact
====================

The configuration and default functionality needs to be
documented. Different integration options should be outlined and
examples given.


References
==========

* Syncrepl Protocol
  http://tools.ietf.org/html/rfc4533

* OpenLDAP n-way Multimaster Replication Options:
  http://www.openldap.org/doc/admin24/replication.html

* OpenLDAP/LMDB Performance:
  http://symas.com/mdb/

* OpenLDAP meta backend for multiple upstream directories:
  http://www.openldap.org/doc/admin24/backends.html#Metadirectory

* OpenLDAP meta backend for single upstream directory:
  http://www.openldap.org/doc/admin24/backends.html#LDAP
