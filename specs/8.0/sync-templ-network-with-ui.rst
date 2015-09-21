..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================
Sync templated netwroking representation and UI
===============================================

https://blueprints.launchpad.net/fuel/+spec/sync-ui-and-templated-networking

--------------------
Problem description
--------------------

Currently the full networking setup in Fuel is possible in two mutually
exclusive ways - with Fuel UI or with Templated Networking.
When Templated Networking is in action, the UI page for configuring the
network interfaces on nodes is completely disabled.

Ironic integration into MOS requires creating a new network role and a new
network for baremetal instances.
As Ironic is optional component, ideally these should be created only
in case Ironic was chosen for deployment from UI,
and removed when it is not chosen.
Currently for integrated components adding an optional network/role
is supported in "templated networking" configuration mode only,
which has no sync with UI, does not accept changes from UI, and blocks
further usage of UI.
Also usage of Templated Networking feature requires careful building
of the whole networking representation as a template,
limiting it to power-users only.


----------------
Proposed changes
----------------

Have a two-way sync between the UI for networking settings and
Templated Networking.

Web UI
======

TBD

Nailgun
=======

TBD

Data model
----------

TBD

REST API
--------

TBD

Orchestration
=============

TBD

RPC Protocol
------------

None?

Fuel Client
===========

None

Plugins
=======

TBD

Fuel Library
============

TBD

------------
Alternatives
------------

Alternative 1
=============

Pre-create the internal representation of baremetal network(-role) for
all environments, but hide it from UI when Ironic is not chosen.
This is the approach our currently proposed changes to Nailgun [1]_
are following.

Alternative 2
=============

Allow creating network roles via Fuel API.
Ironic team might consider a UX trade-off in this case, requiring user
to first execute some commands in CLI (creating a network role and network
itself) *before* activating Ironic from UI.

--------------
Upgrade impact
--------------

TBD

---------------
Security impact
---------------

TBD

--------------------
Notifications impact
--------------------

TBD

---------------
End user impact
---------------

TBD

------------------
Performance impact
------------------

TBD

-----------------
Deployment impact
-----------------

TBD

----------------
Developer impact
----------------

TBD

--------------------------------
Infrastructure/operations impact
--------------------------------

TBD

--------------------
Documentation impact
--------------------

TBD

--------------------
Expected OSCI impact
--------------------

TBD

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  ashestakov
  TBD

Other contributors:
  pshchelo
  TBD

Mandatory design review:
  alekseyk-ru
  xenolog
  vkramskikh
  ikalnistky


Work Items
==========

TBD

Dependencies
============

TBD

------------
Testing, QA
------------

TBD

Acceptance criteria
===================

TBD

----------
References
----------

.. [1] https://review.openstack.org/#/c/223626
