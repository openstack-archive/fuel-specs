..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================================================================
Plugin developer can specify major version in release dependencies
==================================================================

https://blueprints.launchpad.net/fuel/+spec/plugin-major-version-for-releases

Plugin developer should be able to specify only major version
in plugin release dependencies.

Problem description
===================

Currently there is a field in plugin's metadata which looks like:

.. code-block:: yaml

    releases:
      - os: ubuntu
        version: 2014.2-6.0
        mode: ['ha', 'multinode']
        deployment_scripts_path: deployment_scripts/
        repository_path: repositories/ubuntu

Where "version" is a version of Fuel OpenStack release which
the plugin is compatibele with.

The problem is the plugin will not work for releases with
versions 2014.2-6.0.1 and 2014.2.1-6.0. Also user should be
able to specify specific minor veresion, because his plugin
can have some minor specific hacks.

Proposed change
===============

OpenStack release in Fuel consists of two parts,
"<openstack version>-<fuel version>", we will split this version
by "-" symbol and then get all releases with prefix <openstack version>,
and all releases with prefix <fuel version>.

For example we have the releases with the next versions

* 2014.2-6.0

* 2014.2-6.0.1

* 2014.2.1-6.0

* 2014.2.1-6.0.1

* 2014.2.1-6.0.2

When user specifies **2014.2-6.0** as dependencies, all releases
from the list are compatibele with the plugin.

When user specifies **2014.2.1-6.0** as dependencies, only next
releases are compatibele:

* 2014.2.1-6.0.1

* 2014.2.1-6.0.2

When user specifies **2014.2-6.0.1** as dependencies, only next
releases are compatibele:

* 2014.2-6.0.1

* 2014.2.1-6.0.1

Also user can specify exact version of release which is
compatibele with the plugin **2014.2.1-6.0.1**

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Plugin impact
-------------

Described above.

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

  eli@mirantis.com

Work Items
----------

* Fix compatibility parsing on Nailgun side

Dependencies
============

None

Testing
=======

Cases are described in **Proposed changes** section.

Documentation Impact
====================

Parsing logic should be described in plugins documentation.

References
==========

None
