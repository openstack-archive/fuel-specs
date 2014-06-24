==========================================
Support SSL for OpenStack endpoints
==========================================

https://blueprints.launchpad.net/fuel/+spec/ssl-endpoints

OpenStack public endpoints that provide APIs on public networks need to
operate over SSL.

Problem description
===================

OpenStack services receive requests from public networks. It is a good
practice to secure data over public networks. One way to achieve this is to
use mechanism such Secure Sockets Layer. Into the OpenStack security guide,
it is recommended to secure all domains with SSL/TLS including the management
services.

If a tenant escapes its VM isolation we must prevent it from easily injecting
or capturing messages or affect the management capabilities of the cloud.
SSL/TLS provides mechanisms to ensure this kind of troubles.

Proposed change
===============

OpenStack services can be configured to use SSL/TLS libraries. We propose to
modify the puppet manifests to be able to use SSL/TLS and HTTP services.

This blueprint will focus on HTTP services that provides API endpoints on
public networks. Endpoints used for management and other services like
messaging will not be done in this blueprint.

We will use the HAProxy and its support of SSL. The endpoints of public URLs
will be configured with the IP of the HAproxy. It will handle incoming SSL
connections, decrypting the SSL and passing the unencrypted request to the
corresponding service. That means that the communication between the proxy
and the endpoints will not be encrypted.

Here is a schema of the encryption of the traffic paths:

  1. Between client and OpenStack services:
      Client --{ HTTPS }--> public API endpoint --{ HTTP }--> OSt services

  2. Between OpenStack services:
      OSt service --{ HTTP }--> internal API endpoint
                                           \--{ HTTP }--> OSt service

Even if it is recommended that an OpenStack service communicate to another
OpenStack service by using the internal API endpoint, it can occurs that
it is not the case and it uses the public endpoint. For these reason we need
to explicitly configured all OpenStack services to use the internal API
endpoint when communicating with other services. If a project doesn't
offer this possibility we will then configure the service with the correct CA
for authentication.

Here are the different steps needed to implement SSL with public API
endpoints:

- We need to install at least the version 1.5.0 of the HAProxy because the
  support of SSL is available since this version. As it is not available in
  Ubuntu we will need to rebuild it.

- We need to configure HAProxy to manage SSL connections and to forward the
  request to the corresponding service.

- We need to ensure that an internal OpenStack service is using the internal
  API endpoint and if it is not possible to explicitly configured the access
  we need to configure the certificate for authentication.

- We will use a self-signed certificate. We will use openssl to manage them
  so that means that we will add a dependence to openssl. We also need to
  provide the ability to upload an alternative CA from the user. This will be
  done if it is supported by the UI.

- We need to ensure that each client gets the appropriate configuration
  for SSL certificates, keys and CAs.


Alternatives
------------

#. Enable SSL for all OpenStack services.

   Cons:
      - API services need to respond quickly and SSL handshake can add a
        significant overhead. Python services do not work well with direct SSL
        integration.
      - You need to manage as many certificates as there are services.

   Pros:
      - It enables SSL on both, public and internal APIs. That means that we
        don't need to care about OpenStack service that uses public endpoint.

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
system with authentication, confidentiality and integrity.

Notifications impact
--------------------

None

Other end user impact
---------------------

We generate certificate that ends ten years later. Is it fair to think that
we don't need to take care of the expiration of a certificate? If it is not
fair we will need to add some sort of monitoring to identify when a
certificate is near to expire.

Performance Impact
------------------

The SSL-overhead is generally small. The major cost of HTTPS is the SSL
handshaking so depending the typical session length and the caching behavior
of clients the overhead may be different. For very short sessions you can see
performance issue.

The internal communications between services involved many API calls for
small tasks and this is why we will not implement SSL endpoints for the
management network. OpenStack services need to be configure properly.

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

- We need to generate a self-signed CA that will be used for authentication.

  **Note**: There is a discussion about downloading a certificate from the
  WebUI. This feature seems to be needed to implement SSL for Horizon. If
  there is progress in this direction we will follow the path.

- We need to install HAProxy and configure it to handle SSL connections and
  forward requests to the corresponding service.

- We see at least 7 services for which we want to enable SSL. Those services
  are:

    - nova
    - glance
    - neutron
    - cinder
    - keystone
    - heat
    - ceilometer

  Puppet's manifests of most of them are supporting the possibility of
  specifying SSL certificate. If it is not the case we will need to add it.

  Horizon is not part of this blueprint because it doesn't expose any APIs.
  The work to enable SSL is done in another blueprint.

Dependencies
============

- openssl
- haproxy 1.5 for Ubuntu

Testing
=======

Build a new fuel ISO and test if the deployment corresponds to what is
expected. The existing deployment tests seems adequate.

Documentation Impact
====================

None

References
==========

- http://docs.openstack.org/security-guide/content/ch020_ssl-everywhere.html
- https://help.ubuntu.com/community/OpenSSL
