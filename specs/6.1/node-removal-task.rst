..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================
Node removal task
=================

https://blueprints.launchpad.net/fuel/+spec/node-removal-task

There is a need to remove a node from Fuel inventory completely, without
touching its contents. This has been partially solved in Fuel CLI in bug [1]_.
However, node is still not removed from Cobbler. It is the purpose of this
blueprint to implement this change.

Problem description
===================

Current node is removed from Fuel DB only, we have to send also a task to
Astute so that it will be removed from Cobbler. This was implemented in CLI
in [1]_ only by displaying a warning to the user about required manual
intervention.


Proposed change
===============

Upon a ``DELETE`` request for a node in the API, we first create a new task that
sends ``remove_nodes`` task to Astute with the data of the node that is being
deleted. There is no need to wait for this task to complete in the API. We then
delete the node from DB.

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

The internals of the ``DELETE`` method of ``/api/v1/nodes/<node_id>/`` handler
will be changed.

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

Remove warning in the CLI about a required manual intervention in Cobbler.

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

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  pkaminski

Other contributors:
  fuel-python

Work Items
----------

None

Dependencies
============

Related to [1]_.

Testing
=======

It is assumed that Astute's ``remove_nodes`` method works correctly. Tests
will be added that assert that task is created with proper node data.


Documentation Impact
====================

None


References
==========

.. [1] https://bugs.launchpad.net/fuel/+bug/1326116