===========================================
Remove classic provisioning in favor of IBP
===========================================

https://blueprints.launchpad.net/fuel/+spec/remove-classic-provisioning

In case of classic provisioning fuel engineering team spends a lot of time
and effort to support or/and add new features by maintaining simultaneously at
least 2 linux distros (Ubuntu and Centos) with quite different native
installion mechanisms with their own quirks and limitations.

An alternative way of provisioning - image-based provisioning (IBP, for short)
was included in 6.0 under experimental status [1]. Being faster, more reliable
and easier to support it has become the default choice for 6.1/7.0

Problem description
===================

Classic provisioning should be removed in favor of IBP,
so fuel devs can reduce the overhead and cost of maintaining the
additional functionality.

Proposed change
===============

The actual change mainly disables classic provisioning, it doesn't substitute
cobbler. The rest of related code will be kept.
It's a very first step of a removal, not just a disabling when something
could be enabled back.
It means that user won't be to provision a node by classic way.
Ability to perform classic provisioning will be completely removed from UI.

Alternatives
------------

Spend a lot of time on obsolete and rarely used piece of code which is
getting more hard and painful to support if speaking in terms of amount of
related 'won't fixed' bugs.

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
re-create env and re-provision it with IBP. Provisioned slave node is acting
like a cattle, not a pet. [2]

There're two ways of getting OS images:
1) to build them on a master node against hosted on master node mirror with
   old packages.
2) to ship prebuild images as a part of upgrade.

On the one hand, in order to build images for centos and ubuntu precise,
fuel-agent should be improved to be able to perform that.
But on the other hand, having images to be prebuild is not a silver bullet,
since users couldn't be happy with only one set of generic images.
We can't provide a set of images which will work on every kind of h/w as
customizations during build process required somethimes.

Security impact
---------------

None

Notifications impact
--------------------

Users should be informed that after upgrade classic provisioning has been
removed.

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

fuel-library: cobbler stuff like kickstart [3], preseed [4], snippets [5] and
scripts [6] will become unsupported and will be removed soon.

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
   will not be touched for 7.0
4. All leftovers will be completely removed in 7.1

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

.. [1] https://blueprints.launchpad.net/fuel/+spec/image-based-provisioning
.. [2] http://www.theregister.co.uk/2013/03/18/servers_pets_or_cattle_cern/
.. [3] https://github.com/stackforge/fuel-library/tree/master/deployment/puppet/cobbler/templates/kickstart
.. [4] https://github.com/stackforge/fuel-library/tree/master/deployment/puppet/cobbler/templates/preseed
.. [5] https://github.com/stackforge/fuel-library/tree/master/deployment/puppet/cobbler/templates/snippets
.. [6] https://github.com/stackforge/fuel-library/tree/master/deployment/puppet/cobbler/templates/scripts
