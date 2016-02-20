..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================================
Make Deployment Tasks Fields Computable as YAQL Expressions
===========================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/computable-task-fields-yaql

This blueprint proposes to add an ability for deployment engineers
that are using Fuel Library deployment tasks to be able to introduce
expressions that can be computed within the context of cluster configuration,
so that user can actually control how tasks are assigned and executed
depending on the configuration or depending on the changes
in the configuration.

--------------------
Problem description
--------------------

Currently we have hardcoded, non-obvious, non-flexible and sub-optimal way
of calculating deployment process parameters, such as which particular nodes
should be scheduled for the deployment, which tasks should be executed and 
in which order.

For example, in current Fuel Nailgun component we re-run the whole
redeployment of all the OpenStack nodes in case when controllers amount
changes. This actually leads to redundant execution of the tasks and makes
things go slower and introduce potential risks of things being broken.

We could tackle this by, for example, making 'condition' field of tasks
computable with a yaql expression of something like:

"len($.nodes.where($.status = 'ready' and 'controller' in $.roles)) > 0
        and len($.nodes.where($.status = 'discover' and 'controller' in
        $.roles and $.pending_addition = true)) >"

This will make only selected tasks being executed on the nodes and controller
addition will take much lesser time.

Another example of how it can be used is a task of MySQL configuration change.
For example, for the default deployment it is ok to run secondary database
nodes deployment in parallel as there is actually no risk of data corruption
or service degradation for the newly created cluster. But during the cluster
operation it is not ok to restart all the secondary MySQL cluster on config
change as this will lead to quorum loss and service degradation. As en example
, we could create an expression for task policy to be 'parallel' for new
deployment and 'one-by-one' when operating with the existing cluster.

Another benefit of this approach is that these expressions can be overriden
with Fuel Pluggable Framework within plugins **.yaml** files bringing Fuel
onto new level of flexibility.

Additionally, it will allow users to extract all the hardcoded logic such 
as 'update_required|update_once' fields from business logic of Nailgun node
resolver, thus making it data-driven and also pluggable.

This will open the door for transforming Fuel into purely data-driven
deployment engine allowing users to perform Life-Cycle Management tasks based
on the history of the cluster states.


----------------
Proposed changes
----------------

We propose to use YAQL language as it is developed by OpenStack community,
provides all the necessary functionality, been already used for Murano project
is easily extendable and can be used to work with any arbitrary
structured data format such as JSON or YAML.

We are going to change several pieces of Nailgun where actual calculation
of deployment candidates and deployment graph is done.

We are also going to add a set of helper methods that should get registered
within YAQL context of YAQL parser that should allow a deployment enginner
to easily construct YAQL expressions for the majority of cases.

It should also be possible for a user to develop his own set of such helpers
and install them deliberately onto the Master node, so that Nailgun could
import them and register them within YAQL parser context. This would differ
from plugins as these are actual extensions and while python does not allow
for incapsulation, this would mean that 99% of the code of that helpers
should be maintained within Nailgun core, but with a possibility for a
3rd party user to extend Nailgun behaviour when he really needs it.

Web UI
======

None

Nailgun
=======

Majority of changes will happen within TaskHelper class, node_resolver method
in tasks serializers and within ExpressionBasedTask class of deployment tasks
serializers.

The other important part of modifications in Nailgun would be a set of helpers
that should introduce methods that will be executed within YAQL Parser context
and allow a deployment engineer to easily express what he wants.

The amount of use cases supported by those helpers out of the box should be 
equivalent to the list of cases resolved in Task Helper module, thus these
YAQL helpers should completely eliminate need for hardcoded business logic 
in TaskHelper.

Changes for TaskHelper should allow for a user to:
 
  * Identify cluster status change 

  * Identify node amount changes

  * Identify cluster settings changes

  * Identify node settings changes

  * Identify changes of nodes with particular labels or roles

  * Other things implemented in TaskHelper

Data model
----------

The only change to data model (if needed at all) should allow tasks metadata
to be not only lists of tasks, but also an arbitrary multiline string
comprising YAQL expression, which, when being evaluated, should return
corresponding 

REST API
--------

None

Orchestration
=============

This will require to make node_resolver and nailgun task serializers methods
to actually detect yaql fields and evaluate them. It will also require to
create YAQL engine only once.

RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

These are the changes to pluggable framework

* Simple validation changes of deployment_tasks yaml files to
  allow yaql expressions to be placed into task fields.

Fuel Library
============

Fuel Library impact will produce a need for changing
tasks condition. E.g. controller addition should be detected
by yaql condition and should trigger particular tasks that 
are actually required to be re-run, e.g. cluster,database,rabbitmq
for controller nodes and roles/compute.pp only for compute nodes.

------------
Alternatives
------------

We could use existing Nailgun Expressions, but they are actually the same
but lack myriads of features of YAQL

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

YAQL is designed with respect to isolation and containing of possible 
malicious code, so there will be no additional efforts required so far.

--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

Performance and flexibility boost. Ability to run more sophisticated
plugins and implement day-2 operations with the cluster.

------------------
Performance impact
------------------

Being carefully implemented, this feature should reuse either one YAQL engine
per cluster or even have the only YAQL engine. While YAQL context creation
is a relatively cheap operation, performance impact should be nothing compared
to the boost of flexibility and benefits for end users.

-----------------
Deployment impact
-----------------

From now on deployment workflow and sequence will be programmable according
to what is changed in the cluster

----------------
Developer impact
----------------

Plugin and Fuel Library developers will be able to introduce YAQL expressions
and script much more sophisticated actions with cluster while retaining
sustainability.

---------------------
Infrastructure impact
---------------------

Possible increase of memory and CPU consumption during YAQL expression
evaluation

--------------------
Documentation impact
--------------------

Documentation on tasks fields format should be updated.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  ashtokolov

Other contributors:
  vkuklin 
  bgaifullin
  ikutukov

Mandatory design review:
  rustyrobot


Work Items
==========

* Change TaskHelper

* Change Node_resolver methode

* Change plugin validation

* Change tasks classes

* Introduce YAQL Helper functions

Dependencies
============

None

===========
Testing, QA
===========

It should be enough to have simple unit and integration tests in Nailgun
to verify sanity of the feature as the main deployment scenarios output
will remain intact.

===================
Acceptance criteria
===================

User should be able to specify a YAQL expression in any task field except for
id (or it subfields) and get this YAQL expression evaluated correctly with
respect to its context.

----------
References
----------

https://github.com/openstack/yaql
