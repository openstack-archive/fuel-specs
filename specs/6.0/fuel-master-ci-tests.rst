..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================
Fuel Master CI Tests
====================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/fuel-master-ci-tests

This spec enables the CI testing of Fuel Library changes on deployment
of Fuel Master node.

Problem description
===================

Puppet deployment on OpenStack nodes and Fuel Master nodes use a common
collection of Puppet modules, but there is no automated testing of Puppet
on Fuel Master. This leads to regressions when patches are made against
OpenStack deployment, but break Fuel Master deployment. One noteworthy
example was nova-specific code added to a custom RabbitMQ init script.

The reason this has not been implemented yet is because there is no place
during deployment where system tests could pause deployment and change
the Puppet manifests.

Proposed change
===============

The change requires a modification to fuelmenu, which will allow the deployment
to be paused for some time while system tests can copy new puppet manifests
onto the Fuel Master node. To enable resumption of deployment, fuelmenu
will save and quit when it is sent a SIGUSR1 kill signal. 

The second modification required is mapping /etc/puppet to the Puppet manifests
that are stored on the base Fuel Master host, rather than storing several
independent copies. 

Lastly, a new system test is required that is capable of creating a snapshot
of Fuel Master at this pre-deploy stage for syncing new manifests and
deploying Fuel Master and a single node. This test should be added as CI
for fuel-library commits.


Alternatives
------------

We could build an entire ISO and remove the need for this test, but it
would slow down CI significantly. If ISO build was reduced down to ~5 minutes,

Data model impact
-----------------

Changes which require modifications to the data model often have a wider impact
on the system.  The community often has strong opinions on how the data model
should be evolved, from both a functional and performance perspective. It is
therefore important to capture and gain agreement as early as possible on any
proposed changes to the data model.

Questions which need to be addressed by this section include:

* What new data objects and/or database schema changes is this going to
  require?

* What database migrations will accompany this change.

* How will the initial set of new data objects be generated, for example if you
  need to take into account existing instances, or modify other existing data
  describe how that will work.

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
  raytrac3r

Other contributors:
  ekotko

Work Items
----------

Fuelmenu work (Matthew Mosesohn)
System test (Egor Kotko)


Dependencies
============

None


Testing
=======

This change is in effect a new test. It has already been described above
and it will cover puppet deployment the same way OpenStack nodes are
deployed, as well as the extent of Puppet testing we do for full system
tests with ISO installation.


Documentation Impact
====================

None


References
==========

https://etherpad.openstack.org/p/fuel-library-sustaining-september-2014-meetup
