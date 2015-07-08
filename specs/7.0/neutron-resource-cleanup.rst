..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================
Neutron Resource Cleanup
========================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/neutron-resource-cleanup

On controllers Neutron network resources such as namespaces, interfaces,
OVS ports and processes are managed in two unrelated parts of code:
Neutron agents and OCF scripts including `q-agent-cleanup` script.
The goal is to move all responsibility to a single point - Neutron.


Problem description
===================

Right now resource cleanup is performed by external script provided by Fuel
(`q-agent-cleanup`). The script lives in `fuel-library` repo and it may be
changed to re-use code from Neutron. Ideally all cleanup code should belong to
Neutron agents as they currently able to manage namespaces, network interfaces,
OVS ports and processes.

The proposal in inspired by issues:

* Clearing up the large number of network namespaces is very time consuming.
  Pacemaker has very strict timeout management and if the operation doesn't
  fit the whole resource may turn into unmanaged state
  (https://bugs.launchpad.net/fuel/+bug/1436414).

* Restart of a particular agent is performed via banning and clearing the
  associated pacemaker resource. As result all network namespaces are dropped
  and then created again causing traffic interruptions
  (https://bugs.launchpad.net/fuel/+bug/1464817).

* Code defects in `q-agent-cleanup`
  (https://bugs.launchpad.net/fuel/+bug/1434196)


Proposed change
===============

The proposed change is mostly related to code refactoring and optimization. It
doesn't suggest changes in the architecture. OCF scripts will remain the
entry-point for resource clean-up, however the code will move to Neutron.

Step-by-step changes:
 1. Move `q-agent-cleanup` and the corresponding test into Neutron tree.
    Add shell entry point into Neutron package.
 2. Refactor the code by re-using existing parts from Neutron. The CLI should
    stay the same.
 3. Apply optimizations with replacing shell calls by iproute2 (native ovsdb if
    applicable)


Alternatives
------------

Initially we discussed the proposal to move the whole clean-up from OCF to
Neutron agents. However there are cases where resources need to be cleared
by external stuff.

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

Restart of agents should become faster when using native APIs instead of
shell commands.

Plugin impact
-------------

None

Other deployer impact
---------------------

None


Developer impact
----------------

Patches into `q-agent-cleanup` will be tested with Neutron infra, thus making
changes less risky.

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

* Implementation

    * Move `q-agent-cleanup` into Neutron tree
    * Update Neutron package to install `q-agent-cleanup` shell utility
    * Remove the old script from fuel-library tree
    * Optimize resource cleanup to satisfy scale tests

Dependencies
============

None

Testing
=======

Revisit disaster tests, add new if needed. The following cases should be
covered: restart of agent, death of agent, banning agent on a particular node.
The same scenarios should be ran manually at scale on large numbers (thousands)
of networks and routers.

Documentation Impact
====================

None

References
==========

None
