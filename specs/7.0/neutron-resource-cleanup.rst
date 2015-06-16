..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================
Neutron Resource Cleanup
========================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/neutron-resource-cleanup

Resource created by Neutron agents are managed not only by agents, but also
by external `q-agent-cleanup` script. The goal is to move all responsibility
to a single point - Neutron.


Problem description
===================

Right now resource cleanup is performed by external script provided by Fuel
(q-agent-cleanup). That leads to unstable resource management especially
under the load because the script is started under pacemaker which
has tight time constraints for such tasks.

We need to move this mechanism into particular agents which should cleanup
resources (namespaces, ns-metadata-proxies, dnsmasqs) that don't correspond
to active resources hosted by L3 or DHCP agents.

The proposal in inspired by issues:

* Restart of a particular agent is performed via banning and clearing the
  associated pacemaker resource. As result all network namespaces are dropped
  and then created again causing traffic interruptions
  (https://bugs.launchpad.net/fuel/+bug/1464817).

* Clearing up the large number of network namespaces is very time consuming.
  Pacemaker has very strict timeout management and if the operation doesn't
  fit the whole resource may turn into unmanaged state
  (https://bugs.launchpad.net/fuel/+bug/1436414).


Proposed change
===============

Neutron Kilo release already supports resource cleanup within corresponding
agents. E.g. L3-agent when restarted is able to find and remove orphan
network namespaces.

The change includes:
 * Enabling cleanup feature in Neutron conf
 * Remove cleanup logic from OCF scripts

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

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

Restart of agents will be faster since there's no need to clear resources and
re-create them

Plugin impact
-------------

None

Other deployer impact
---------------------

None


Developer impact
----------------

Only positive - all resources are managed in a single place, no magic anymore.

Infrastructure impact
---------------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  shakhat

Other contributors:
  skolekonov
  kkuznetsova

Work Items
----------

* Test first

    * Revisit and add more destructive tests

* Implementation

    * Enable cleaning logic in Neutron and related puppet scripts
    * Remove q-agent-cleanup and clean OCF scripts out of resource management
      stuff

Dependencies
============

None

Testing
=======

Add automation tests that verify functionality during different types of
failures: death of agent, restart of agent, stop/start of agent.

Documentation Impact
====================

None

References
==========

None