==========================================
Support SSL for OpenStack endpoints
==========================================

https://blueprints.launchpad.net/fuel/+spec/ssl-endpoints

SSL needs to be configured between OpenStack services when deployed.

Problem description
===================

OpenStack services receive requests from public networks. It is a good
practice to secure data over public networks. One way to achieve this is to
use mechanism like Secure Sockets Layer. Into the OpenStack security guide,
they recommend securing all domains with SSL/TLS including the management
services.

If a tenant escape their VM isolation we must prevent him to easly inject or
capture messages or affect the management capabilites of the cloud. SSL/TLS
provides mechanisms to ensure this kind of troubles.

Proposed change
===============

As OpenStack services can be configured to use SSL/TLS libraries. We propose
to modify the puppet manifests to be able to use SSL/TLS and HTTP services.

We need to ensure that each components gets the appropriate configuration for
SSL certificates, keys and CAs.

This blueprint will focus on API endpoints. Other services like messaging will
not be done in this blueprint.

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

None

Security impact
---------------

By using SSL/TLS over HTTP services, we will be able to provide a secure
system with authentification, confidentiality and integrity.

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

The SSL-overhead is generally small. The major cost of HTTPS is the SSL
handshaking so depending the typical session length and the caching behavior
of clients the overhead may be different. For very short sessions you can see
performance issue.

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
  guillaume-thouvenin

Work Items
----------

We see at least 7 services for which we want to enable SSL. Those services
are:

* nova
* glance
* neutron
* cinder
* keystone
* heat
* ceilometer

Puppet's manifests of most of them are supporting the possiblity of enabling
SSL endpoints but this option is generally only available upstream and not in
the version that we are using with fuel. So we will need to backport the part
of the manifest that allows SSL endpoints.

Dependencies
============

None

Testing
=======

Build a new fuel ISO and test if the deployement is OK.

Documentation Impact
====================

None

References
==========

http://docs.openstack.org/security-guide/content/ch020_ssl-everywhere.html
