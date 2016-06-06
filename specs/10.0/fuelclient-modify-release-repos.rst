..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Example Spec - The title of your blueprint
==========================================

https://blueprints.launchpad.net/fuel/+spec/fuelclient-modify-release-repos

--------------------
Problem description
--------------------

Currently we use fuel-mirror tool both to build partial mirrors
and to modify default release/cluster repos. We'd better use
packetary for building partial repos and fuelclient for
modifying repos.

----------------
Proposed changes
----------------

The proposal is to implement an option in fuelclient that
could be used to modify repos in releases/clusters.
Then we could get rid of fuel-mirror totally.

Web UI
======

None

Nailgun
=======

None

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

There will be a command

.. code-block:: bash

    fuel2 rel update --repos-file repos_file.yaml 1
    fuel2 env update --repos-file repos_file.yaml 1

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

It will be easy to modify default release/cluster repos.

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
and fuelclient docs. Fuelclint section should be modified
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

* Implement release/cluster update subcommand in fuelclient.


Dependencies
============

None

------------
Testing, QA
------------

There should be a functional test that checks this new feature.

Acceptance criteria
===================

It must be possible to update release/cluster repos using fuel2
command. It is to receive yaml file with the list of repositories.

----------
References
----------

None
