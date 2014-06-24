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

This blueprint will focus on HTTP services that provides API endpoints on
public networks. Endpoints used for management and other services like
messaging will not be done in this blueprint.

We will use the HAProxy and its support of SSL. The endpoints of public URLs
will be configured with the IP of the HAproxy. It will handle incoming SSL
connections, decrypting the SSL and passing the unencrypted request to the
corresponding service. That means that the communication between the proxy and
the endpoints will not be encrypted.

- We need to install at least the version 1.5.0 of the HAProxy because the
  support of SSL is available since this version. As it is not available in
  Ubuntu we will use the PPA repository.

- We need to configure HAProxy to manage SSL connections and to forward the
  request to the corresponding service.

- We will use our own CA. We will use openssl to manage them so that means
  that we will add a dependence to openssl.

- We need to ensure that each components gets the appropriate configuration
  for SSL certificates, keys and CAs.


Alternatives
------------

#. Enable SSL for all OpenStack services. The problem with this solution is
   that API services need to respond quickly and SSL handshake can add a
   significant oberhead. Python services are not good for SSL management.

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

The internal communications between services involved many API calls for
small tasks and this is why we will not implement SSL endpoints for the
management network.

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

- We need to generate a CA that will be used for authentification.

- We need to install HAProxy and configure it to handle SSL connections and
  forward requets to the corresponding service.

- We see at least 7 services for which we want to enable SSL. Those services
  are:

    - nova
    - glance
    - neutron
    - cinder
    - keystone
    - heat
    - ceilometer

  Puppet's manifests of most of them are supporting the possiblity of specifying
  SSL certificate. If it is not the case we will need to add it.

Dependencies
============

- openssl

Testing
=======

Build a new fuel ISO and test if the deployement corresponds to what is
expected. The existing deployement tests seems adequate.

Documentation Impact
====================

None

References
==========

- http://docs.openstack.org/security-guide/content/ch020_ssl-everywhere.html
- https://help.ubuntu.com/community/OpenSSL
