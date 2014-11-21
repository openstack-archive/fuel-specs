==============================================
Support for Zabbix server in HA on controllers
==============================================

https://blueprints.launchpad.net/fuel/+spec/zabbix-ha

Zabbix server should be running in HA mode.

Problem description
===================

Fuel supports monitoring solution only in non-HA mode. Administrator can
assing zabbix-server role only to single, dedicated machine.

Proposed change
===============

Zabbix server can be configured on all OpenStack controllers.

We will abandon 'zabbix-server' role. Instead we will introduce zabbix as an
additional component. When enabled, zabbix will be installed on all
controllers.

We will also introduce 'zabbix-monitoring' role, which will be assigned to all
servers in environment after enabling zabbix. This role will have lowest
priority in nailgun serializer. In that way we can ensure that zabbix can
monitor every service in env.

Here are the different steps needed to implement zabbix with HA:

- Add new 'zabbix-monitoring' role.

- Add new additional component in UI.

- Modify nailgun serializers to automatically assign zabbix-monitoring role
  to all servers, when zabbix enabled.

- Modify puppet manifests to configure and run zabbix-server on controllers
  when zabbix enabled.

- Modify puppet manifets to configure and run zabbix-agent on servers with
  assigned role zabbix-monitoring.

Alternatives
------------

Install zabbix-server on machines with role 'zabbix-server' in HA mode.

   Cons:
      - In case where 'zabbix-server', can not be assigned to controller
        we need 3 additional psychical servers.

   Pros:
      - Better performance in scale

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Current zabbix implementation is experimental. We do not have to provide
any detailed procedure how to migrate from non-HA to HA zabbix.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Zabbix instalation in active-backup mode.

Performance Impact
------------------

In scale zabbix-server can consume lot of resources. When we will have
running zabbix-server on controllers this can lead to performance problems.

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
  Bartosz Kupidura (zynzel)

Work Items
----------

Implement puppet manifests for zabbix server on controllers.
Add additional role 'zabbix-monitoring' in nailgun.
Implement puppet manifests for zabbix-monitoring role.

Dependencies
============

None

Testing
=======

Build a new fuel ISO and test if the deployment corresponds to what is
expected.

Documentation Impact
====================

We need to prepare architecute diagram for zabbix-server.

References
==========

- https://blueprints.launchpad.net/fuel/+spec/zabbix-ha
- https://gerrit.mirantis.com/#/c/30698/9
- https://gerrit.mirantis.com/#/c/30700/
