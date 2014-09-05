..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Enable SSL for Fuel API endpoints
==========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-ssl-endpoints

All traffic from/to Fuel is unsecured.

Problem description
===================

After introduction of access control to Fuel security has been improved
but all credentials and data are transferred using HTTP protocol and
are not protected.

As solution to this problem is to secure all requests by using HTTPS
connection and enable verification of certificate in all components
of Fuel.


Proposed change
===============

Changes will be implemented in several stages.

Stage I
-------

Fuel use Nginx as a proxy for services that expose API endpoints. We will
enable SSL connection in Nginx to secure traffic from/to Fuel.

For the first phase of this feature we will use self-signed certificate
that will be generated for the purpose of changes described in blueprint
https://blueprints.launchpad.net/fuel/+spec/ssl-endpoints. We will also try
to reuse as much as possible from the feature created in that blueprint.

We will need also to adjust fuelclient to work with secure API. The most
important change is to validate certificate. On master node it will not
be a problem since that certificate will be available in the system.
If fuelclient will be used outside of the master node we need to add option
to specify path to the certificate so user could download certificate from
master node and use it to verify connection.

It should be also possible to skip certificate check in fuelclient.

In this stage also OSTF will be configured to check certificate.


Stage II
--------

Fuel agent should also verify that certificate is valid. This mean that
the certificate must be delivered to nodes together with agent.


Alternatives
------------

None


Data model impact
-----------------

None


REST API impact
---------------

All API requests will be encrypted using HTTPS.


Upgrade impact
--------------

Upgrade script will be responsible to generate new self-signed certificate
that will be later used in Fuel.


Security impact
---------------

Using HTTPS for API requests will improve master node security.


Notifications impact
--------------------

None


Other end user impact
---------------------

As we are using a self-signed certificate by default, if a user is using a
web browser to query Fuel there will be a popup to warn than the certificate
can not be trusted.

Certificate that will be used will be expired after some time so user need to
monitor expiration of the certificate.


Performance Impact
------------------

Usage of HTTPS may add some latency to the APIs.


Other deployer impact
---------------------

None


Developer impact
----------------

Every component of Fuel that is calling any of the APIs will need to be able
to handle self-signed certificates.

Using a self-signed certificate will affect Selenium tests for UI since
browsers will display a warning about problems with certificate.

API client in system test should skip certificate validation.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>


Work Items
----------

Stage I
^^^^^^^

* Configure Nginx to handle SSL connection.

* Add certificate validation in OSTF.

* Add certificate validation in fuelclient with option to ignore it.


Stage II
^^^^^^^^

* Distribute certificate together with the Fuel agent.

* Enable certificate validation in Fuel agent.


Dependencies
============

* https://blueprints.launchpad.net/fuel/+spec/ssl-endpoints

* https://blueprints.launchpad.net/fuel/+spec/refactoring-for-fuelclient


Testing
=======

Since we are using self-signed certificate by default.


Documentation Impact
====================

It should be described how to work with self-signed certificate.


References
==========

None
