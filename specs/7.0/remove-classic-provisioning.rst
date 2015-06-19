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

Classic provisioning should be removed in favor of IBP,
so fuel devs can reduce the overhead and cost of maintaining the
additional functionality.

Proposed change
===============

The actual change mainly disables classic provisioning.
It doesn't substitute cobbler.

Alternatives
------------

Spend a lot of time on obsolete and rarely used piece of code which is
getting more hard and painful to support.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Users will not be able to deploy new nodes for their existent envs older than
6.0 using classic way. And in order to make them able to use IBP for their old
envs, we need to give them the corresponding OS image.

Since users mostly care about upgrading OpenStack, it's not a big deal to
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
3. All classic provisioning related code in nailgun, astute, and fuel-library
   will not be touched for 7.0 and will be completely removed in 7.1. 

Dependencies
============

None

Testing
=======

No need of additional functional tests as IBP already covered by them.

Acceptance criteria
-------------------

User must not be able to provision a node via classic provisioning.

Documentation Impact
====================

Documentation should notify the fact of classic provisioning to be removed.

References
==========

None
