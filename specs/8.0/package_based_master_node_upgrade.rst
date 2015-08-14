..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
Package based master node upgrade
=================================

https://blueprints.launchpad.net/fuel/+spec/package-master-node-upgrade

Problem description
===================

Currently, we use tarball based approach for the master node upgrade. It
assumes we package everything we need for upgrade into the tarball including
Centos and Ubuntu mirrors, pip packages for virtual environment, docker
containers, some build related files and upgrade script itself.
However, this tarball approach contradicts with our package
based approach to deliver updates.

Proposed change
===============

We should get rid of upgrade tarball in favor of upgrade rpm package. It is
enough to package upgrade script itself into rpm and then a user is to install
this package and run the script to upgrade the master node.

User experience is to be like the following:

#. User downloads rpm package fuel-release-X.Y.Z.rpm and installs it using
   ``rpm -i fuel-release-X.Y.Z.rpm`` command. This package configures X.Y.Z
   yum repositories.
#. User installs fuel-X.Y.Z.rpm package (meta package) which requires other
   fuel packages like fuel-docker-images-X.Y.Z, fuel-upgrade-X.Y.Z etc.
#. User runs upgrade script ``/usr/bin/fuel-upgrade`` which is executable
   entry point for upgrade script written in python.
#. This script does everything else including stopping old containers and
   starting new ones, moving some files and creating some links,
   uploading some fixtures, etc.

In order to make this happen we need to change upgrade script itself as well
as the upgrade delivery approach.

#. We don't need to copy package repositories from upgrade tarball to the
   master node any more. We assume all necessary repositories are either
   available online or mirrored locally using fuel-createmirror.
#. Installing fuel-release package will configure new repositories on the
   master node as well as install necessary keys.
#. We don't need version.yaml file any more as it assumes master node is
   installed from ISO and all packages installed on the master node came
   from rpm repository provided by ISO. The majority of parameters set in
   version.yaml can be either packaged into rpm or deprecated/substituted.

version.yaml
------------

Below is an example of the file:

::

  VERSION:
    feature_groups:
      - mirantis
    production: "docker"
    release: "7.0"
    openstack_version: "2015.1.0-7.0"
    api: "1.0"
    build_number: "82"
    build_id: "2015-07-23_10-59-34"
    nailgun_sha: "d1087923e45b0e6d946ce48cb05a71733e1ac113"
    python-fuelclient_sha: "471948c26a8c45c091c5593e54e6727405136eca"
    fuel-agent_sha: "bc25d3b728e823e6154bac0442f6b88747ac48e1"
    astute_sha: "b1f37a988e097175cbbd14338286017b46b584c3"
    fuel-library_sha: "58d94955479aee4b09c2b658d90f57083e668ce4"
    fuel-ostf_sha: "94a483c8aba639be3b96616c1396ef290dcc00cd"
    fuelmain_sha: "68871248453b432ecca0cca5a43ef0aad6079c39"

Let's go through this file step by step.

#. feature_groups - It is, in fact, runtime parameter and it should be moved
   into nailgun config.
#. production - It is always equal to "docker" when we build ISO and deploy
   the Fuel master node, but it can be set to other values when we deploy
   fake UI or when we run functional tests for UI and python-fuelclient. So,
   it is seems to be runtime parameter rather than buildtime and it also
   should be moved into nailgun config file.
#. release - It is like /etc/issue and it, in fact, reflects which
   repositories are currently configured. For example in Fedora this
   file /etc/issue is provided by fedora-release package. So, we probably
   can put this value into /etc/fuel-issue and put this file into fuel-release
   package. This value is shown on UI.
#. openstack_version - It is just an extraction from openstack.yaml. There is
   no need to have this value somewhere else.
#. api -  It is 1.0 currently. And we still don't have other versions of API.
   Even more, it contradicts to the common practice to make several different
   versions available at the same time. And a user should be able to ask API
   which versions are currently available. It should be deprecated.
#. build_number - I don't even know if it makes any sense to have this
   information on the master node. Probably, it is only makes it a little bit
   more convenient to troubleshoot issues during development. It is related
   to a particular ISO and can be moved to, say, /etc/fuel-buildstamp.
#. build_id - Same as above.
#. *_sha - These are just SHA sums and this list can be easlily substituted by
   rpm -qa output. One can easlily find out SHA from the package version.
   (Perestroika is going to increase the package version every time when
   it re-builds a package.)

Therefore, this file version.yaml should be deprecated and the information
from this file should be partly available from other sources mentioned above.

openstack.yaml
--------------

Upgrade script needs some information from openstack.yaml file [1]_. This
file is available in nailgun package, and it seems that it is rational to
put this file into a separate package. Nailgun and fuel-upgrade packages are
to depend on this package.


Alternatives
------------

Upgrade tarball does not match our recent efforts to move to package based
approach.

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

Each API method which is either added or changed should have the following

* Specification for the method

  * A description of what the method does suitable for use in
    user documentation

  * Method type (POST/PUT/GET/DELETE)

  * Normal http response code(s)

  * Expected error http response code(s)

    * A description for each possible error code should be included
      describing semantic errors which can cause it such as
      inconsistent parameters supplied to the method, or when an
      instance is not in an appropriate state for the request to
      succeed. Errors caused by syntactic problems covered by the JSON
      schema defintion do not need to be included.

  * URL for the resource

  * Parameters which can be passed via the url

  * JSON schema definition for the body data if allowed

  * JSON schema definition for the response data if any

* Example use case including typical API samples for both data supplied
  by the caller and the response

* Discuss any policy changes, and discuss what things a deployer needs to
  think about when defining their policy.

Upgrade impact
--------------

If this change set concerns any kind of upgrade process, describe how it is
supposed to deal with that stuff. For example, Fuel currently supports
upgrading of master node, so it is necessary to describe whether this patch
set contradicts upgrade process itself or any working feature that we need
to support.

Security impact
---------------

Describe any potential security impact on the system.  Some of the items to
consider include:

* Does this change touch sensitive data such as tokens, keys, or user data?

* Does this change alter the API in a way that may impact security, such as
  a new way to access sensitive information or a new way to login?

* Does this change involve cryptography or hashing?

* Does this change require the use of sudo or any elevated privileges?

* Does this change involve using or parsing user-provided data? This could
  be directly at the API level or indirectly such as changes to a cache layer.

* Can this change enable a resource exhaustion attack, such as allowing a
  single API interaction to consume significant server resources? Some examples
  of this include launching subprocesses for each connection, or entity
  expansion attacks in XML.

For more detailed guidance, please see the OpenStack Security Guidelines as
a reference (https://wiki.openstack.org/wiki/Security/Guidelines).  These
guidelines are a work in progress and are designed to help you identify
security best practices.  For further information, feel free to reach out
to the OpenStack Security Group at openstack-security@lists.openstack.org.

Notifications impact
--------------------

Please specify any changes to notifications. Be that an extra notification,
changes to an existing notification, or removing a notification.

Other end user impact
---------------------

Aside from the API, are there other ways a user will interact with this
feature?

* Does this change have an impact on python-fuelclient? What does the user
  interface there look like?

Performance Impact
------------------

Describe any potential performance impact on the system, for example
how often will new code be called, and is there a major change to the calling
pattern of existing code.

Examples of things to consider here include:

* A periodic task might look like a small addition but if it calls conductor or
  another service the load is multiplied by the number of nodes in the system.

* Scheduler filters get called once per host for every instance being created,
  so any latency they introduce is linear with the size of the system.

* A small change in a utility function or a commonly used decorator can have a
  large impacts on performance.

* Calls which result in a database queries (whether direct or via conductor)
  can have a profound impact on performance when called in critical sections of
  the code.

* Will the change include any locking, and if so what considerations are there
  on holding the lock?

Plugin impact
-------------

Discuss how this will affect the plugin framework. Every new feature should
determine how it intearcts with the plugin framework and if it should be
exposed to plugins and how that will work. Some areas to cover:

* Should plugins be able to interact with the feature?

* How will plugins be able to interact with this feature?

* How might this change the current plugin framwork?

  * How will existing plugins interact with the feature?

Other deployer impact
---------------------

Discuss things that will affect how you deploy and configure Fuel
that have not already been mentioned, such as:

* What config options are being added? Should they be more generic than
  proposed? Are the default values ones which will work well in
  real deployments?

* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

* If this change is a new binary, how would it be deployed?

* Please state anything that those doing continuous deployment, or those
  upgrading from the previous release, need to be aware of. Also describe
  any plans to deprecate configuration values or features.  For example, if we
  change the directory name that instances are stored in, how do we handle
  instance directories created before the change landed?  Do we move them?  Do
  we have a special case in the code? Do we assume that the operator will
  recreate all the instances in their cloud?

Developer impact
----------------

Discuss things that will affect other developers working on Fuel,
such as:

* If the blueprint proposes a change to the driver API, discussion of how
  drivers would implement the feature is required.

Infrastructure impact
---------------------

Explain what changes in project infrastructure will be required to support the
proposed change. Consider the following:

* Will it increase the load on CI infrastructure by making build or test jobs
  consume more CPU, network, or storage capacity? Will it increase the number
  of scheduled jobs?

* Will it require new workflows or changes in existing workflows implemented in
  CI, packaging, source code management, code review, or software artefact
  publishing tools?

  * Will it require new or upgraded tools or services to be deployed on project
    infrastructure?

  * Will it require new types of Jenkins jobs?

  * Will it affect git branch management strategies?

  * Will it introduce new release artefacts?

* Will it require changes in build environments of any existing CI jobs? Would
  such changes be backwards compatible with previous Fuel releases currently
  supported by project infrastructure?


Implementation
==============

Assignee(s)
-----------

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>

Mandatory design review:
  <launchpad-id or None>

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


Testing
=======

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly,
but discussion of why you think unit tests are sufficient and we don't need
to add more functional tests would need to be included.

Is this untestable in gate given current limitations (specific hardware /
software configurations available)? If so, are there mitigation plans (3rd
party testing, gate enhancements, etc).

Acceptance criteria
-------------------

Please specify clearly defined acceptance criteria for proposed changes.


Documentation Impact
====================

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.


References
==========

.. [1] https://github.com/stackforge/fuel-web/blob/master/nailgun/nailgun/fixtures/openstack.yaml

