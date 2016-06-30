..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================================
Modify release repositories using Fuel client
=============================================

https://blueprints.launchpad.net/fuel/+spec/fuelclient-modify-release-repos

--------------------
Problem description
--------------------

Currently we use fuel-mirror tool both to build partial mirrors
and to modify default release repos. We'd better use
packetary for building partial repos and fuelclient for
modifying repos.

----------------
Proposed changes
----------------

The proposal is to implement an option in fuelclient that
could be used to modify repos in Fuel releases.
Then we could get rid of fuel-mirror totally.

Web UI
======

None

Nailgun
=======

Get and put handlers for release attributes metadata
must be implemented.

Data model
----------

None

REST API
--------

None

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

There will be commands

.. code-block:: bash

    fuel2 release list
    fuel2 release repos list <release_id>
    fuel2 release repos update <release_id> <-f repos.yaml>


Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

Continue to use fuel-mirror.

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

It will be easy to modify default release repos using Fuel client.

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

Sections in the documentation that mention fuel-mirror should
be removed. Instead there should be references to packetary
and fuelclient docs. Fuelclient section should be modified
in order to reflect this additional repository manipulation
functionality.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>

Mandatory design review:
  Bulat Gaifullin <bgaifullin@mirantis.com>
  Roman Prikhodchenko <rprikhodchenko@mirantis.com>


Work Items
==========

* Implement release repos get and put handlers in nailgun.
* Implement release repos update subcommand in fuelclient.


Dependencies
============

None

------------
Testing, QA
------------

There should be a functional test that checks this new feature.

Acceptance criteria
===================

It must be possible to update release repos using fuel2
command. It is to receive yaml file with the list of repositories.

----------
References
----------

None
