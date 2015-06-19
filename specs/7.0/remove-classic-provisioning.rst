===========================================
Remove classic provisioning in favor of IBP
===========================================

https://blueprints.launchpad.net/fuel/+spec/remove-classic-provisioning

In case of classic provisioning fuel engineering team spends a lot of time
and effort to support or/and add new features by maintaining simultaneously at
least 2 linux distros (Ubuntu and Centos) with quiet different native
installion mechanisms with their own quirks and limitations.

An alternative way of provisioning - image-based provisioning (IBP, for short)
was included in 6.0 under experimental status. Being faster, more reliable and
easier to support it has become the default choice for 6.1/7.0


Problem description
===================

Classic provisioning should be remove native provisioning in favor of IBP,
so that fuel devs can reduce the overhead and cost of maintaining the
additional functionality.

Proposed change
===============

The actual change mainly disables classic provisioning.
It doesn't substitute cobbler.

Alternatives
------------

Spend a lot of time time on obsoleted and rarely used piece of code which is
getting more harder and painful to support.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

After upgrade to 7.0 user will loose ability to provision a new node for
already existent old envs if them were created with fuel older than 6.1

Since users mostly cares about upgrading OpenStack, it's not a big deal to
re-create env and re-provision it with IBP.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

End user will be able to provision a node only with IBP.

Performance Impact
------------------

None

Plugin impact
-------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

fuel-library: cobbler stuff like kickstart/preseed snippets and pmanager.py
will become unsupported and will be removed soon.

Infrastructure impact
---------------------

CI jobs for testing classic provisioning is not needed for 7.0

Implementation
==============

Assignee(s)
-----------

:Primary assignee: Alexandr Gordeev

:QA:

:Documentation:

:Mandatory design review: Vladimir Kozhukalov

Work Items
----------

1. Remove cobbler profiles needed for classic provisioning
2. Remove provisioning related radio button from UI

Dependencies
============

None

Testing
=======

No need of additional functional tests as IBP already covered by them.

Acceptance criteria
-------------------

User must not be able to provision a node thought classic provisioning.


Documentation Impact
====================

Documentation should notify the fact of classic provisioning to be removed.

References
==========

None
