..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Agent Local Reports
==========================================

https://blueprints.launchpad.net/fuel/+spec/neutron-agents-local-reports

Provide additional hints to local monitoring


Problem description
===================

Currently Pacemaker OCF scripts make desicion about liveleness of neutron
agents based on the agents processes status.
In some cases it makes sense to detect other cases like an agent's inability to
communicate with neutron server over message queue. In this case current OCF
scripts can't detect the failure and restart an agent.

So in order to provide additional hints to monitoring scripts 'local reports'
are introduced. Local report is a piece of information written to a local file
by neutron agent about status of certain kind of operations.


Proposed change
===============

Proposed change affects L3 and DHCP agents.
Agents will write status of certain operations to a local file.
The list of operations include:
* startup
* state reports status
* network (for DHCP agent) or router (for L3 agent) synchronization with
neutron server

File will reside in the path, configured in neutron.conf as 'state path'

The format of those report will include:
* pid of the agent
* time stamp of the status report
* name of operation
* status itself

Example (dhcp agent local report, note that formatting is for ease
of spec readers):

..
 {
  SYNC_STATE':
  {
   'Pid': '12345',
   'Timestamp': '1231342352345',
   'Date': '2014-12-18 12:03:05',
   'Status': 'failure',
   'Since': '123123123123123'
  },
  'RPC_STATE_REPORT':
  {
   'Status': 'success'
   'Pid': '12345',
   'Timestamp': '1231342352345',
   'Date': '2014-12-18 12:03:05',
   'Since': '123123123123123'
  }
  'STARTUP':
  {
   'Status': 'success',
   'Pid': '12345',
   'Timestamp': '1231342352345',
   'Date': '2014-12-18 12:03:05',
  }
 }

Currently preferred format is json. The reason for it is that json
simplifies updating local reports file by reading-updating-writing its
contents. This is needed so contents is not flushed/rewritten after
agent restart.

Main goal of local reports is to help with detecting different issues that
are not "visible" to methods like pid monitoring.

For instance, 'since' field is used to estimate time which agent was in
inconsistent state (out of sync with neutron-server) and restart the agent.

The fuel-library part of this feature consists of changes to the OCF scripts
which will parse the local state reports files and make decision whether to
restart Neutron agents or not according to timeout settings (if agent seems to
be dead for a short period of time it isn't considered as dead) and reported
statuses.

This feature will be disabled by default, because currently in most cases,
Neutron can handle the explained problems itself, whilst unnecessary restarts
initiated by Pacemaker will slow down work of Neutron agents under high load.

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

None

Other deployer impact
---------------------

None

Developer impact
----------------

The change is not going to be submitted to upstream, so it must be kept in
a local repository for each release.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  enikanorov

Other contributors:
  Sergey Kolekonov
  Sergey Vasilenko

Work Items
----------

 * state reports for L3 and DHCP agents
 * additional code for ocf monitoring that analyses local reports


Dependencies
============

None


Testing
=======

Testing should involve artificial interruption of rpc communication
between agents and neutron server to test that ocf scripts can detect that
through local reports file.


Documentation Impact
====================

None


References
==========

1. https://review.fuel-infra.org/#/c/1450/
2. https://review.openstack.org/#/c/155752/
