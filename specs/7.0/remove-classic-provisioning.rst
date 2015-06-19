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

To support provisioning a new node for old env after upgrade to 7.0:
1. Prebuild centos images will be shipped in RPM packages as a part of upgrade
2. fuel-agent will be improved to be capable to build ubuntu 12.04 images on a
fuel-master node from existing repos.
Those steps let IBP to be used to provision a new node for existing env for
5.0, 5.1, 6.0, 6.1 after fuel-master node upgrade to 7.0 will be performed.

Alternatives
------------

Spend a lot of time on obsolete and rarely used piece of code which is
getting more hard and painful to support if speaking in terms of amount of
related won't be fixed bugs.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

After upgrade to 7.0 end users won't be able to provision a new node using
classic way.

To mitigate that limitation, IBP will be used in order to provision a new
node for existent old envs.

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

:QA: Yegor Kotko

:Documentation:

:Mandatory design review: Vladimir Kozhukalov

Work Items
----------

1. Remove cobbler profiles needed for classic provisioning
2. Remove provisioning related radio button from UI
3. All classic provisioning related code in nailgun, astute, and fuel-library
   will not be touched for 7.0
4. All leftovers will be completely removed in 7.1
5. Build centos images for 5.0, 5.1
6. Improve fuel-agent for letting it be able to build ubuntu precise images

Dependencies
============

None

Testing
=======

Test cases to ensure that a new node could be provisioned via IBP for existent
old envs after upgare to 7.0 should be added. Eg.:

1. Create env on XX, classic provisioning
2. Upgrade master to 7.0
3. Add&Deploy node to current env
4. Check that node was provisioned via IBP && 
   check that it is inaccessible to provision node via Classical method

where XX is stands for 5.0, 5.1, 6.0, 6.1

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
