============================================
Disable classic provisioning in favor of IBP
============================================

https://blueprints.launchpad.net/fuel/+spec/disable-classic-provisioning

In case of classic provisioning fuel engineering team spends a lot of time
and effort to support or/and add new features by maintaining simultaneously at
least 2 linux distros (Ubuntu and Centos) with quite different native
installation mechanisms with their own quirks and limitations.

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

The actual change disables classic provisioning, it doesn't substitute
cobbler. The rest of related code will be kept.
It means that user won't be to provision a node by classic way.
An error will returned if user tries to perform that.

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

Cluster update method and its handler will be improved in order to disallow
classic provisioning to be used for 7.0 or newer environments.
If classic provisioning is disallowed, PUT will throw HTTP 405 error.

Upgrade impact
--------------

After upgrade end user will be able to provision a new node to existent
environment using the way of provisioning which was chosen on the environment
creation.

Otherwise, no impact.

Security impact
---------------

None

Notifications impact
--------------------

Users should be informed that after upgrade classic provisioning has been
disabled.

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

fuel-library: cobbler stuff like kickstart [2], preseed [3], snippets [4] and
scripts [5] will become unsupported.

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

1. Remove provisioning related radio button from UI
2. All classic provisioning related code in nailgun, astute, and fuel-library
   will not be touched for 7.0
3. Improve cluster's update handler from REST API side

Dependencies
============

None

Testing
=======

Test case to ensure that a new node could be provisioned via IBP only in 7.0
should be added.

Acceptance criteria
-------------------

User must not be able to provision a node via classic provisioning.

Documentation Impact
====================

Documentation should notify the fact of classic provisioning has been disabled.

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/image-based-provisioning
.. [2] https://github.com/stackforge/fuel-library/tree/master/deployment/puppet/cobbler/templates/kickstart
.. [3] https://github.com/stackforge/fuel-library/tree/master/deployment/puppet/cobbler/templates/preseed
.. [4] https://github.com/stackforge/fuel-library/tree/master/deployment/puppet/cobbler/templates/snippets
.. [5] https://github.com/stackforge/fuel-library/tree/master/deployment/puppet/cobbler/templates/scripts
