======================
Virtual IP reservation
======================

https://blueprints.launchpad.net/fuel/+spec/vip-reservation

This document is about additional virtual IP (VIP)
reservation during deployment.

Problem description
===================

Some plugins require additional VIP to proper configuration.
For example Zabbix could be configured in way that it expect SNMP traffic
on dedicated VIP.

In current version VIPs reservation is done based on information from
release field in the database.

So the plugin developer should have a better way to create extra VIPs
as puppet resource in pre-deployment or post-deployment plugin stage.

Proposed change
===============

Give user a possibility to reserve additional VIPs during deployment process.
This should be possible by providing additional plugin configuration.

Add support of new configuration file to the plugin.
Configuration file should be named `network_roles.yaml`.

Plugin developers will provide new network roles configuration.
Network roles description is placed in `network_roles.yaml`.
Network role description includes information on VIPs reservation.

At the deployment stage Nailgun will reserve VIPs and they
will be accessible in the Puppet manifests via Hiera.

Deployment flow: None

Migration script flow: None

Alternatives
------------

Provide REST API to reserve VIPs. This allows 3rd party software to
reserve additional VIPs.

  Cons:
   - Authentication from plugin is difficult
   - Requires installation of Fuel client or direct access
     to the REST API server

  Pros:
   - Allows VIP management outside of the plugin

Data model impact
-----------------

Network roles data format:

* Proposed network roles configuration file format:

  .. code-block:: yaml

    - id: "name_of_network_role"
      default_mapping: "public"
      properties:
        subnet: true
        gateway: false
        vip:
          - name: "my_vip_a"
            shared: false


Nailgun DB tables changes:

**Plugin**

`network_roles_metadata`
plugin network roles data taken from `network_roles.yaml` file.


REST API impact
---------------

None

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Other deployer impact
---------------------

Performance Impact
------------------

None

Plugin impact
-------------

* New network roles with VIPs reservation can be described
  in `network_roles.yaml` file which is loaded into Nailgun DB
  when plugin gets installed or on plugin sync API call.

* `network_roles.yaml` file format is described in `Data model impact`_.

Developer impact
----------------

Developer that works on Fuel plugins can use new `network_roles.yaml`
to reserve VIPs for the plugin.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  * Alexander Saprykin <asaprykin@mirantis.com>

Mandatory design review:
  * Igor Kalnitsky <ikalnitsky@mirantis.com>
  * Aleksey Kasatkin <akasatkin@mirantis.com>

QA engineers:
  * Egor Kotko <ykotko@mirantis.com>

Work Items
----------

  - Implement configuration file data loading to the database.
  - Implement VIP reservation from plugin network roles metadata.

Dependencies
============

- https://blueprints.launchpad.net/fuel/+spec/templates-for-networking

Testing
=======

- Additional unit/integration tests for Nailgun.
- Additional System tests for test environment with plugin installed
  and VIPs set using configuration file.
- Regression testing is required.

Acceptance criteria:

   - Configuration data from `network_roles.yaml` is stored to the database.
   - VIPs defined in `network_roles.yaml` are accessible via Hiera.

Documentation Impact
====================

We need to update documentation about VIPs in networks. Plugin documentation
should be updated as well.

References
==========

- https://blueprints.launchpad.net/fuel/+spec/vip-reservation

