..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Puppet noop run for Fuel puppet deployment tasks
================================================

https://blueprints.launchpad.net/fuel/+spec/puppet-noop-run

--------------------
Problem description
--------------------

Currently, Fuel Environment re-deployment re-runs all Fuel tasks without any
check of customizations which could be applied for different OpenStack and
Fuel components aka files and config values changes, running and stopped
services and etc. If such changes weren't applied to Fuel deployment tasks
(manifests, scripts) as well (that the most frequent case for the users)
new tasks run (in case of re-deloyment or update) could lead to losing of
applied customization.

----------------
Proposed changes
----------------

Before re-deployment or update run of successfully deployed cluster it should
be possible to get a report about those customizations which were applied to
the Fuel cluster or particular node which differs from performed previously
deployment and which could be possible overridden by new Fuel tasks run. Those
customizations should be stored in the report file or database in readable
(or parsable format) and it should be possible to get it using REST API.

Noop run for Fuel tasks could be used as a mechanism for detecting of any set
of customizations applied to the services, configuration files and etc in the
cluster. Tasks noop run is able to show changes in the metaparameters for
files (e.g. owner, mode, content), services (e.g. status, service provider),
OpenStack configs (e.g. missed options, incorrect values for options) and
other (even custom) resources. This approach could be easily implemented
for all types of tasks: Puppet tasks could be executed with '--noop' option,
other types could be just skipped.

Exactly Puppet Noop run will help to detect required types of customization
in Fuel environment. Puppet store report of each run (even noop run) in
/var/lib/puppet/reports/<node-fqdn>/ folder in YAML format. Each puppet
operation is tracked here and it has detailed description. The most important
information is: was resource changed or not? This is shown by 'changed'
parameter. So every puppet operation could be easily checked by status. Another
aprroach here is to generate Puppet report in JSON format. For enabling of
this feature is required to add '--logdest /path/to/file.json' to the end of
puppet apply command. In that case it's possible to store a report for all
Fuel puppet tasks in one file or separate a report per running task.

The implementation of this approach requires changes in the Fuel:

  * Puppet tasks: all Fuel puppet tasks should support noop action. Some tasks
    may error with '--noop' option. Such failures will be stored in report but
    they won't stop Tasks noop run. They also won't affect cluster/node status.

  * Astute: Astute tasks executor should support noop option for all type of
    tasks: in case of puppet tasks executor should be able to set '--noop' and
    --logdest options for puppet (for JSON format of output); in case of other
    tasks types executor does nothing. The logging output will be also reduced:
    '--debug' and '--verbose' options for Puppet Noop run are useless. We need
    to see only resources which are going to be changed. Additional information
    will make a report really huge and difficult to parse, that's why these
    options won't be used.

  * Task history: Noop run report should be stored in deployment tasks history.

  * Nailgun: Noop run report should be available through nailgun API for each
    particular node in environment.

  * Fuel CLI: it should be possible to run any custom graph for particular
    environment or node with Noop option.

This Noop run for the any cluster or set of nodes shouldn't change their
statuses. Noop run is not a part of deployment. It should work similar
to addional checks (like OSTF is working).

Web UI
======

None

Nailgun
=======

* Nailgun API functionality should be expanded to support required
  functionality for Puppet noop run. Puppet noop run can be started
  using Fuel CLI command or API request to Nailgun.

* Nailgun shouldn't change cluster state (e.g. deployed -> deploying) during
  and after/during Noop run even if it has failed.

Data model
----------

None

REST API
--------

Described in Nailgun section.

Orchestration
=============

RPC Protocol
------------

None

Fuel Client
===========

Fuel client should support following Noop actions:

  * Run any graph with a 'noop' option which would ask nailgun to format
    a message to Astute properly, so that Astute runs only 'noop' tasks.

  * Start Noop run for particular environment, node, task or
    set of tasks (custom graph).

  * Get report from each Noop run.

Plugins
=======

Fuel Puppet tasks in plugins should also support Puppet noop run with new
log destination.

Fuel Library
============

None

------------
Alternatives
------------

Manual detect of customizations applied to the clusrer.

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

None

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

End users will be able to check their environment for customizations before
cluster re-deployment, update or upgrade. They will be notified about the
differences between current cluster/nodes state and original (after last
deployment). It will help to reduce the risk of missing important
customizations applied to cluster/nodes.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Documentation will have to be updated to reflect changes.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Denis Egorenko

Other contributors:
  Ivan Berezovskiy

Mandatory design review:
  Vladimir Kuklin
  Vladimir Sharshov

QA engineer:
  Timur Nurlygayanov

Work Items
==========

* Update Fuel Astute to support Noop run for all type of tasks.

* Add support for keeping Puppet Noop run report in parsable format
  (YAML or JSON) and make it available to download through API call or using
  Fuel client.

* Update Fuel client to be able to apply custom graph on particular environment
  or set of nodes with Noop option.

* Update Nailgun to ignore Noop run errors. They shouldn't affect cluster or node
  state/status.


Dependencies
============

None

------------
Testing, QA
------------

* Nailgun's unit and integration tests will be extended to test new feature.

* Astute's unit and integration tests will be extended to test new feature.

* Fuel Client's unit and integration tests will be extended to test new feature.

Acceptance criteria
===================

* Noop run should be possible to execute on only successfully deployed
  environment.

* It should be possible check custom changes in services, files, OpenStack
  components configuration and other puppet resources applied to cluster or
  particular node using simple command of Fuel client.

* It should be possible to get report of Noop run using REST API.

* Noop run shouldn't affect cluster deployment status.

----------
References
----------

1. LP Blueprint https://blueprints.launchpad.net/fuel/+spec/puppet-noop-run
