..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Fuel release bundle for Puppet Application Orchestration install
================================================================

https://blueprints.launchpad.net/fuel/+spec/fuel-release-pao

Fuel uses puppet in a very odd way, and this results in difficulties in
managing environments after initial deployment. Given the recent movement
to allow for alternative release bundles, we should establish a release
and working team to explore installation with the puppet application
orchestrator.


--------------------
Problem description
--------------------

Fuel is a common kit of tools to deploy openstack, the default way of
installing openstack, using the default release and fuel-library has stood
for sometime. We've grown to the point where we should allow for other
teams to develop their own release bundles, to this end I propose that we
establish a release to produce a release bundle based on puppet server,
its application orchestration language extensions, and the puppet agent.

This should allow for an increased focus on working through solutions
in a way that is more in-line with the larger Puppet community, improves
post-deployment maintenance, or Day 2 management functions.

----------------
Proposed changes
----------------

We should establish a puppet-application delivery team who would be
responsible for development of the release bundle. Changes to components
outside of the release bundle would continue to work through the regular
teams and process.

Web UI
======

None

Nailgun
=======

Changes needed in nailgun are already annotated and in progress as part
of previously described specs. [1]

Data model
----------

None

REST API
--------

None

Orchestration
=============

Fuel task orchestration will be retained, but instead used to set up components
of the puppet server, after this, puppet’s internal orchestration will
be it's primary driver.

RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

This will provide a vastly different data profile and puppet module usage
than is traditional to fuel plugins. As such it will likely require
plugins to be explicitly built as compatible to this release. It is not
yet clear what all this will entail and will only become so after further
development of this release.

The Puppet Application Orchestrator (pao) team will be responsible for
working with some of the active plugin teams to identify, and help them
to modify their plugins in whichever way is appropriate so that there
may be some quality examples for others to draw upon.

Fuel Library
============

Since we are building our own release bundle, fuel-library is not impacted
by this.

------------
Alternatives
------------

We can continue to work with and enhance the default fuel release, however
that limits fuel to just one form of implementation, and implies that it
isn't flexible enough to do things such as this.

--------------
Upgrade impact
--------------

Because this is release bundle, it reuses all of the other fuel components
as they are. This means that we can't break the fuel node upgrade.

From release to release, it may be difficult to upgrade from a different
release type, however since we will use the same data input from fuel,
the same puppet-openstack modules, it's highly probable that we will be able to
work out migration between the default release and this one.

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

User will interact with this the same as a regular release, however there
will be additional roles to assign.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

The deployment model will change. The expectation is that we will use
the fuel task engine to set up components needed to run puppet application
orchestration, from there these components will deploy openstack on the node.

These tools can then be exercised to alter the deployment, either by
updating options in fuel, or directly with them.

Components will at least include:

* Puppet Server
* R10k
* A Git server
* Parts of the ConfigDB component
* A PAO deployer

----------------
Developer impact
----------------

None

---------------------
Infrastructure impact
---------------------

We will need to create a repos for:

* the fuel release bundle `fuel-release-pao`

* the puppet-openstack application `fuel-puppet-application`

* the puppet server installation module `fuel-puppet-server`

We should create a gerrit group to enable additional cores besides
fuel-library (which we should include)

We will need to set up infra jobs for the different repos, which will
increase the load some on the CI system due to changes landing in the
repos.

We will need to set up an infra job to build the fuel-pao install rpm

Deployed nodes will require Puppet 4, which we can configure with the repo
in the release data.

--------------------
Documentation impact
--------------------

New deployment workflow, components, and how to interact with them
will require new documentation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  xarses

Other contributors:
  grimlock
  rberwald

Mandatory design review:
  None


Work Items
==========

* Creation of repos and initial population
* Creation of CI jobs
* Implementation of new modules

Dependencies
============

* Would benefit from the implementation of release-as-a-plugin spec [2],
  but this isn't a hard requirement (we can add a new release to
  openstack.yaml in nailgun in the meantime.)

* role-decomposition spec [1]

* requires new components described in the deployment section

------------
Testing, QA
------------

Testing will be performed
* against the puppet modules
* fuel deployment

Acceptance criteria
===================

* Operator can install the new pao release and deploy openstack
  successfully

----------
References
----------

[1] https://review.openstack.org/#/c/346248/ role-decomposition
[2] https://review.openstack.org/#/c/351569/ release-as-a-plugin