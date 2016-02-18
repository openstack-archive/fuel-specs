..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================
Testing external and core extensions with Nailgun
=================================================

https://blueprints.launchpad.net/fuel/+spec/testing-extensions

--------------------
Problem description
--------------------

Since extensions for Nailgun can be installed from separate repositories
[#stevedore_discovery]_ we need to provide a way to test these extensions
with Nailgun.

We must be able to use different versions of Nailgun and extensions so it could
be used by Fuel developers who want to test the core with extensions and it
also could be used by external extensions developers to test their extensions
against various versions of Nailgun.

----------------
Proposed changes
----------------

The proposed solution is to create a script which will be used to set up
environment for integration testing of extensions and Nailgun combined.

The script will be able to use predefined config with repository URLs for
fuel-web and python-fuelclient with the possibility to customize them and with
choice to select specific branch/tag/commit (branch master by default) which
will be cloned to temporary directory. It will be also possible to set fuel-web
root directory which will allow to use locally edited version of Nailgun.

The script will be able to receive list of additional packages (extensions) -
literally a list of repos URLs (or root directory paths) with branch/tag/commit
specified. They also will be cloned and installed locally.

The source code will be placed in `nailgun/bin` directory and could be used
as a standalone script without nailgun requirements. It's a a right place
because all extensions will have Nailgun in their requirements anyway.

The main consumer of the script is CI. The script will be executed on events:

#. Patch in fuel-web has been submitted. Test are run for all core extensions
#. Patch in external Extension has been submitted. Test for Nailgun, core
   extensions and external extensions are executed with different versions of
   each project (depending on specified values).


Web UI
======

None

Nailgun
=======

Data model
----------

None

REST API
--------

None

Orchestration
=============


RPC Protocol
------------

None

Fuel Client
===========

None


Plugins
=======

None

Fuel Library
============

None

------------
Alternatives
------------

* We could enable Nailgun to be run on devstack [#devstack]_ but:

  * It seems to be over-engineered approach since devstack is prepared to run
    whole OpenStack, while all we need is Nailgun and PostgreSQL.

* We could adapt fuel-dev-tools to use different versions of Nailgun
  and be able to install extensions in user friendly and automated way.
  But:

  * It requires vagrant to run

  * Seems to be over-engineering also since Nailgun doesn't even have to be
    running.


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

None

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

Extensions developers will be able to run integration tests against various
versions of Nailgun and its extensions which are placed in different
repositories.


---------------------
Infrastructure impact
---------------------

(NEEDS DISCUSSION)
The change requires additional `nailgun-extensions` job which will test
extensions. The job should be skipped for previous releases of Fuel.

--------------------
Documentation impact
--------------------

* We should describe how to run the script

* What are the required env variables

* What are the script requirements (PostgreSQL, python version etc.)


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee: Sylwester Brzeczkowski <sbrzeczkowski@mirantis.com>

Other contributors:

  * Evgeny Li <eli@mirantis.com>

Mandatory design review:

  * Evgeny Li <eli@mirantis.com>
  * Igor Kalnitsky <igor@kalnitsky.org>


Work Items
==========

* Write the script

* Change Nailgun documentation

* Change CI to run the script.

Dependencies
============

None

------------
Testing, QA
------------

Manual testing only:

* run the script with various versions of fuel-web, python-fuelclient and
  some extension and check if it works

* run the script with root directories set for above projects

Acceptance criteria
===================

Script must be able to install Nailgun along with specified extensions,
so the develops can run integration tests on prepared environment.

----------
References
----------

.. [#stevedore_discovery] https://blueprints.launchpad.net/fuel/+spec/stevedore-extensions-discovery
.. [#devstack] https://github.com/openstack-dev/devstack
