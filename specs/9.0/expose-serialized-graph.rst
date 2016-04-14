..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Provide api to download serialized graph
==========================================

API for downloading serialized graph, that is used for task-based deployment,
can be usefull in next scenarios:

- Manual pre-deployment verification
- Consumption of fuel composition layer in 3rd party applications

This specification is concerned with latter usage scenario.

--------------------
Problem description
--------------------

In solar we want to regenerate fuel resource composition, and take into
account - role allocation, conditions based on fuel settings, and other misc
logic that are used to build deployment composition. And all of those actions
are executed during graph compilation procedure.

Instead of fetching deployment graph we could fetch other configuration
options exposed by fuel API, like role allocation and settings. And write
conditional allocator ourselves, but it will lead to duplication of logic
in nailgun, and introduce potential desynchronization between newly introduced
component and nailgun.

----------------
Proposed changes
----------------

Web UI
======

None


Nailgun
=======

New handler that will expose already existing logic.


Data model
----------

None

REST API
--------

===== =====================================================================
HTTP  URL
===== =====================================================================
GET   /api/v1/clusters/<:cluster_id>/serialized_tasks/?nodes=<:nodes>&
      tasks=<:tasks>
===== =====================================================================

On request it will use task_based_deployment.TaskSerializer.serialize method
with all provided by user parameters.

Additional validations provided by handler:

- If node is not present in cluster request will be invalidated with
  400 Bad Request
- Cluster or node is not found in database - 404 Not Found
- If task based deployment is not allowed - 400 Bad Request


Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

Exposing handler data with fuel client is out of scope for this
specification.

Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

Build more complicated policy engine based on raw fuel configuration.
Taking into account date of the release this is not even feaasible alternative.

--------------
Upgrade impact
--------------

No impact

---------------
Security impact
---------------

No impact

--------------------
Notifications impact
--------------------

No impact

---------------
End user impact
---------------

No impact

------------------
Performance impact
------------------

No impact

-----------------
Deployment impact
-----------------

No impact

----------------
Developer impact
----------------

No impact

---------------------
Infrastructure impact
---------------------

No impact

--------------------
Documentation impact
--------------------

Documentation will added in code

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  dshulyak

Mandatory design review:
  bgaifulin
  evgeniyl
  ikalnitsky


Work Items
==========

- Handler that will implement part of exsisting produre
- Proper validation
- Tests coverage

Dependencies
============

For LCM improvements some changes will be done in TasksSerializer API,
after they will be introduced - REST API will adjusted to those changes.

------------
Testing, QA
------------

Change is not complex, unit testsing and manual verification that it works
on ISO should be enough

Acceptance criteria
===================

Serialized deployment graph, that is sent to astute for deployment procedure,
can be downloaded using fuel REST API.
API should provide interface to take into account all variables
exposed by TasksSerializer, including:
- choose cluster
- select subset of nodes in cluster
- select list of tasks that will be included in tasks serialization


----------
References
----------

None
