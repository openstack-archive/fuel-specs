..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Package upgrade test
==========================================

https://blueprints.launchpad.net/fuel/+spec/package-upgrade-test

We shall implement aditional test of upgrade for DEB and RPM packages.


Problem description
===================

A detailed description of the problem:

* To facilitate patching story, we must be sure that new packages built
  on our infrastructure can be used to safely update corresponding
  packages in existing repositories


Proposed change
===============

We shall create and implement additional upgrade test for DEB and RPM
packages in our current packaging workflow.

It shall be a Jenkins job similar to package installation job or
part of package installation job.

Currently, after DEB or RPM package has been created we have
2 created package mirrors:

* One of them is 'main mirror', where changeset will be merged
* Another one is 'changeset mirror', created after package
  build was finished

We shall use both of following mirrors in upgrade process for
making sure that upgrade of packages will be safe.

Proposed logic of the upgrade job:

* Find previous version of the package on 'main mirror'.
  If not exist - quit the job.
* Install previous version of the package from 'main mirror'
  with dependencies.
* Update package from the 'changeset mirror'.
* If all goes without errors and update successfully,
  then in gerrit bot will put an assessment "+1".
  Otherwise bot will put an assessment "-1".

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

By implementing following feature we can avoid upgrade issues.

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

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Infrastructure impact
---------------------

* Following feature may be runned in case if previous version of
  pakage exists on mirror, so it may require resources for VM.

* Workflow will be the same in general, upgrade test will be
  added before or after install test.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  dkaiharodsev

Work Items
----------

* Create Jenkins job or modify package Installation script.
* Write and put JJB yaml for the job.

Dependencies
============

None


Testing
=======

The feature may be tested on new code of packages which
is already exists in infra repositories according to proposed
logic of the upgrade job on existing 'infra' resources.


Documentation Impact
====================

OSCI workflow will be increased on 1 Jenkins job inside internal documentation.


References
==========

* https://mirantis.jira.com/browse/PROD-474

* https://blueprints.launchpad.net/fuel/+spec/package-upgrade-test
