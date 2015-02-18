..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Cover 'Critical' and 'High' bugs via the set of tests and checks
================================================================

https://blueprints.launchpad.net/fuel/+spec/implement-regressive-tests-and-checks

When a bug is fixed, it should be covered by apropriate system test to avoid
regressions in the future.

Problem description
===================

Many bugs was already fixed in different components of Fuel and MOS, but not
all of them were covered by system tests.

As the Fuel and MOS are constantly developing, there can be regressions that
was fixed before new components with the same issues were implemented.

Proposed change
===============

Add tests and checks for the following items:

* Fuel admin node: tests should cover issues with installing Fuel admin
node, issues with docker containers, Fuel services that run in the containers,
etc.;

* Static configuration data: check that the configuration data prepared by
nailgun is correctly delivered on the slaves during provisioning
(for example, partitions sizes);
OS system settings and configuration files on slaves took into account
changes that were proposed during bug fixes.;

* Functional tests for individual components of deployed cluster: test for each
component should cover individual cases for that component where were faced and
fixed the issues in bugs. Most of these tests will be covered by the [1].

* Simple check for list of key phrases in specified log files in case if there
is not possible to get actual status regarding the issue from a component.
Many bugs that fixed internal behaviour of components, can be found only in
this way, including some 'false positive' functional behaviours.


Alternatives
------------

The only alternative is the manual debug of every failed environment to
find out the root of the issue.

Some results may be obtained by using OSTF, but in any case it needs the live
environment for get the detailed information 

The tool that automatically inspects logs for key phrases on OpenStack project:
https://github.com/openstack-infra/elastic-recheck
, but it is mainly for integration with OpenStack infrastructure.

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

Additional notifications about check results will be added to the output
of system tests.

Other end user impact
---------------------

None

Performance Impact
------------------

Additional checks will slightly increase overall time of system tests.

Plugin impact
-------------

None

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

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  Denis Dmitriev <ddmitriev@mirantis.com>
  Maksym Strukov <mstrukov@mirantis.com>

Work Items
----------

* Review all bugs with 'Critical' and 'High' status to collect the scope of
issues that should be covered by system tests; separate the collected scope
into the groups for further implementing tests and checks;

* Add tests for Fuel admin node

* Add checks for configuration data and system settings on slaves;

* Add necessary functional tests for individual components or re-use already
created tests (in OSTF, or for blueprint 'fuel-library-modular-testing') to
get the actual status of the cluster components in addition to the status
of deployment taken from nailgun.

* Add a dictionary of key phrases with common errors from logs and implement
simple check for these phrases in specified log files.

Dependencies
============

* Partically depends on [1].

Testing
=======

* Will be covered under the system tests.

Documentation Impact
====================

* [2] should be updated regarding additional information that will be added
to the output of system tests.

References
==========

[1] https://blueprints.launchpad.net/fuel/+spec/fuel-library-modular-testing
[2] https://mirantis.jira.com/wiki/display/PRD/System+tests
