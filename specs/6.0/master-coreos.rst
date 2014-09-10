..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Fuel Master on CoreOS
==========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/coreos-fuel-master

Replacing Fuel Master with CoreOS is a building block to moving toward
containers for our end-to-end architecture of Fuel. Making a smaller
base OS lets us make more granular and modular changes to Fuel without
having so much dependence on a complex host OS.


Problem description
===================

Deploying CentOS and managing it as a host OS for Docker is a burden.

* For CentOS 6.5, using an old kernel hinders Docker/LXC performance.


Proposed change
===============

By leveraging CoreOS and its etcd and Docker capability, we could improve
the workflow of deploying Fuel Master. CoreOS relies on a read-only base
filesystem.

This is a stepping stone change toward containerized deployment of
OpenStack itself. Since Fuel Master already runs Docker containers,
the limit of this change is reasonably small.

Alternatives
------------

There are other projects, such as Project Atomic, that aim to achieve
the same results. CoreOS is a leader in this sphere, with many success
stories already.

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

None

* What database migrations will accompany this change.

None

* How will the initial set of new data objects be generated, for example if you
  need to take into account existing instances, or modify other existing data
  describe how that will work.

None

REST API impact
---------------

None

Upgrade impact
--------------

This will impact upgrades from Fuel 5.x which are still based on CentOS. An
upgrade strategy should be proposed that can convert a Fuel 5.x deployment
to a CoreOS deployment. This may include a backup/restore process.

Security impact
---------------

Describe any potential security impact on the system.  Some of the items to
consider include:

* Does this change touch sensitive data such as tokens, keys, or user data?

Yes, authentication data for deployment (that goes in astute.yaml) will be
affected.

* Does this change alter the API in a way that may impact security, such as
  a new way to access sensitive information or a new way to login?

No

* Does this change involve cryptography or hashing?

No

* Does this change require the use of sudo or any elevated privileges?

No

* Does this change involve using or parsing user-provided data? This could
  be directly at the API level or indirectly such as changes to a cache layer.

No

* Can this change enable a resource exhaustion attack, such as allowing a
  single API interaction to consume significant server resources? Some examples
  of this include launching subprocesses for each connection, or entity
  expansion attacks in XML.

No

For more detailed guidance, please see the OpenStack Security Guidelines as
a reference (https://wiki.openstack.org/wiki/Security/Guidelines).  These
guidelines are a work in progress and are designed to help you identify
security best practices.  For further information, feel free to reach out
to the OpenStack Security Group at openstack-security@lists.openstack.org.

Notifications impact
--------------------

Please specify any changes to notifications. Be that an extra notification,
changes to an existing notification, or removing a notification.
None

Other end user impact
---------------------

Aside from the API, are there other ways a user will interact with this
feature?

* Does this change have an impact on python-fuelclient? What does the user
  interface there look like?

No

Performance Impact
------------------

Describe any potential performance impact on the system, for example
how often will new code be called, and is there a major change to the calling
pattern of existing code.

None. Performance should be improved by the use of a newer kernel.

Other deployer impact
---------------------

Discuss things that will affect how you deploy and configure Fuel
that have not already been mentioned, such as:

* What config options are being added? Should they be more generic than
  proposed? Are the default values ones which will work well in
  real deployments?

Configuration for network/hostname/dns will still have the same defaults, but
parameters for predefining network configuration will need to be determined in
the design. 
CoreOS config is all defined via something called "butt-config". 
Fuelmenu will work as before and apply the necessary configuration.


* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

Yes.

* If this change is a new binary, how would it be deployed?

Fuel Master on CoreOS would be deployed via ISO as we use it currently.

* Please state anything that those doing continuous deployment, or those
  upgrading from the previous release, need to be aware of. Also describe
  any plans to deprecate configuration values or features.  For example, if we
  change the directory name that instances are stored in, how do we handle
  instance directories created before the change landed?  Do we move them?  Do
  we have a special case in the code? Do we assume that the operator will
  recreate all the instances in their cloud?

CentOS as a host OS for Fuel Master will be deprecated. A process to upgrade
will be required for those upgrading. Deployed environments will not be
affected.

Developer impact
----------------

Discuss things that will affect other developers working on Fuel,
such as:

* This changes limits what commands can be run directly on the master because
  it will only contain tools to manage Docker containers.
* A utility container based on CentOS may be implemented for a "developer
  playground" as needed.

Implementation
==============

Assignee(s)
-----------

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  raytrac3r

Other contributors:
  None

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.

Research viability of bare metal install of CoreOS
Implement changes needed for the following components:
* Containerization of ntpd
* Adapt fuelmenu for etcd/butt-config
* Adapt dockerctl and fuel_upgrade for CoreOS
Upgrade path for Fuel 5.x on CentOS to CoreOS

Nice to have:
* Add Fuel splash to installer for CoreOS
* Fully automated upgrade


Dependencies
============

None

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


Testing
=======

fuelweb_test needs to be modified to support this deployment mode.

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly,
but discussion of why you think unit tests are sufficient and we don't need
to add more functional tests would need to be included.

Is this untestable in gate given current limitations (specific hardware /
software configurations available)? If so, are there mitigation plans (3rd
party testing, gate enhancements, etc).


Documentation Impact
====================

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.

The Fuel Master installation guide and dev docs should be updated to reflect
CoreOS differences.

References
==========

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
